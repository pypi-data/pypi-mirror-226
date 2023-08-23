"""
Created on 08.02.2021

@author: fischsam

This module fixes a bug in Python's shared memory module
causing a memory leak. It can be safely removed once the bug is fixed. 

Issue: https://bugs.python.org/issue40882
Merge request: https://github.com/python/cpython/pull/20684

The patch in this file was created based on the instructions on 
https://stackoverflow.com/questions/65968882/unlink-does-not-work-in-pythons-shared-memory-on-windows
"""

import ctypes, ctypes.wintypes
import errno
import mmap
import multiprocessing, multiprocessing.shared_memory
from multiprocessing.shared_memory import _make_filename, _O_CREX
import os


if os.name == "nt":
    import _winapi

    _USE_POSIX = False
    UnmapViewOfFile = ctypes.windll.kernel32.UnmapViewOfFile
    UnmapViewOfFile.argtypes = (ctypes.wintypes.LPCVOID,)
    UnmapViewOfFile.restype = ctypes.wintypes.BOOL
else:
    import _posixshmem

    _USE_POSIX = True


def _SharedMemory_init(self, name=None, create=False, size=0):
    if not size >= 0:
        raise ValueError("'size' must be a positive integer")
    if create:
        self._flags = _O_CREX | os.O_RDWR
    if name is None and not self._flags & os.O_EXCL:
        raise ValueError("'name' can only be None if create=True")

    if _USE_POSIX:
        # POSIX Shared Memory

        if name is None:
            while True:
                name = _make_filename()
                try:
                    self._fd = _posixshmem.shm_open(name, self._flags, mode=self._mode)
                except FileExistsError:
                    continue
                self._name = name
                break
        else:
            name = "/" + name if self._prepend_leading_slash else name
            self._fd = _posixshmem.shm_open(name, self._flags, mode=self._mode)
            self._name = name
        try:
            if create and size:
                os.ftruncate(self._fd, size)
            stats = os.fstat(self._fd)
            size = stats.st_size
            self._mmap = mmap.mmap(self._fd, size)
        except OSError:
            self.unlink()
            raise

        from multiprocessing.resource_tracker import register

        register(self._name, "shared_memory")

    else:
        # Windows Named Shared Memory

        if create:
            while True:
                temp_name = _make_filename() if name is None else name
                # Create and reserve shared memory block with this name
                # until it can be attached to by mmap.
                h_map = _winapi.CreateFileMapping(
                    _winapi.INVALID_HANDLE_VALUE,
                    _winapi.NULL,
                    _winapi.PAGE_READWRITE,
                    (size >> 32) & 0xFFFFFFFF,
                    size & 0xFFFFFFFF,
                    temp_name,
                )
                try:
                    last_error_code = _winapi.GetLastError()
                    if last_error_code == _winapi.ERROR_ALREADY_EXISTS:
                        if name is not None:
                            raise FileExistsError(
                                errno.EEXIST,
                                os.strerror(errno.EEXIST),
                                name,
                                _winapi.ERROR_ALREADY_EXISTS,
                            )
                        else:
                            continue
                    self._mmap = mmap.mmap(-1, size, tagname=temp_name)
                finally:
                    _winapi.CloseHandle(h_map)
                self._name = temp_name
                break

        else:
            self._name = name
            # Dynamically determine the existing named shared memory
            # block's size which is likely a multiple of mmap.PAGESIZE.
            h_map = _winapi.OpenFileMapping(_winapi.FILE_MAP_READ, False, name)
            try:
                p_buf = _winapi.MapViewOfFile(h_map, _winapi.FILE_MAP_READ, 0, 0, 0)
            finally:
                _winapi.CloseHandle(h_map)
            try:
                size = _winapi.VirtualQuerySize(p_buf)
                self._mmap = mmap.mmap(-1, size, tagname=name)
            finally:
                UnmapViewOfFile(p_buf)
    self._size = size
    self._buf = memoryview(self._mmap)


def remove_shm_from_resource_tracker():
    """Monkey-patch multiprocessing.resource_tracker so SharedMemory won't be tracked

    More details at: https://bugs.python.org/issue38119
    """
    from multiprocessing import resource_tracker

    def fix_register(name, rtype):
        if rtype == "shared_memory":
            return
        return resource_tracker._resource_tracker.register(self, name, rtype)

    resource_tracker.register = fix_register

    def fix_unregister(name, rtype):
        if rtype == "shared_memory":
            return
        return resource_tracker._resource_tracker.unregister(self, name, rtype)

    resource_tracker.unregister = fix_unregister

    if "shared_memory" in resource_tracker._CLEANUP_FUNCS:
        del resource_tracker._CLEANUP_FUNCS["shared_memory"]


if os.name == "nt":
    remove_shm_from_resource_tracker()

multiprocessing.shared_memory.SharedMemory.__init__ = _SharedMemory_init
