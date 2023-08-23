"""
Created on 21.12.2020

@author: fischsam
"""
from multiprocessing import shared_memory
import numpy as np

# monkey-patch an issue with shared_memory
# DO NOT REMOVE this import. It is used for the actions executed
# during the import process.
try:
    from . import shared_memory_fix
except ImportError:
    import shared_memory_fix


def unpack(array):
    if isinstance(array, RemoteSharedArrayWrapper):
        return array.array
    else:
        return array


class Unpacker:
    def __init__(self, array):
        self.isRemoteSharedArrayWrapper = isinstance(array, RemoteSharedArrayWrapper)
        self.array = array

    def __enter__(self):
        if self.isRemoteSharedArrayWrapper:
            return self.array.array

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.isRemoteSharedArrayWrapper:
            self.array.close()


class SharedArrayWrapper:
    def __init__(self, array):
        if not type(array) == np.ndarray:
            array = np.asarray(array, dtype=float)

        self.data = shared_memory.SharedMemory(create=True, size=array.nbytes)
        self.array = np.ndarray(array.shape, dtype=array.dtype, buffer=self.data.buf)
        self.array[:] = array[:]

        self.name = self.data.name
        self.shape = array.shape
        self.dtype = array.dtype
        self.remoteArray = RemoteSharedArrayWrapper(self.name, self.dtype, self.shape)

    def __del__(self):
        self.data.close()
        self.data.unlink()
        

class RemoteSharedArrayWrapper:
    def __init__(self, name, dtype, shape):
        self.name = name
        self.dtype = dtype
        self.shape = shape
        self.data = None

    @property
    def array(self):
        if self.data is None:
            self.data = shared_memory.SharedMemory(name=self.name)
        return np.ndarray(self.shape, dtype=self.dtype, buffer=self.data.buf)

    def __del__(self):
        self.close()

    def close(self):
        if self.data is not None:
            self.data.close()


