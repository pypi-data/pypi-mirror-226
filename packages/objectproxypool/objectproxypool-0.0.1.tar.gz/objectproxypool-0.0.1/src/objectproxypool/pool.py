from copy import deepcopy
from functools import partial, cached_property
from collections import deque
from itertools import repeat, starmap, count as itercount
from multiprocessing import util
from multiprocessing.pool import (
    ThreadPool,
    Pool,
    ExceptionWithTraceback,
    _helper_reraises_exception,
    MaybeEncodingError,
)
from threading import Lock
import os
import sys
import threading

import more_itertools
import numpy as np


MAX_WIN32_WORKERS = 61

INIT_COUNTER = itercount()


class lenzip:
    def __init__(self, *args) -> None:
        if not args:
            raise ValueError("lenzip takes at least one argument")
        self._args = args

    def __iter__(self):
        return zip(*self._args)

    def _classify_args(self):
        self._noLenArgs_ = []
        self._minLen_ = np.inf
        for arg in self._args:
            if isinstance(arg, lenzip):
                self._minLen_ = min(self._minLen_, arg._minLen)
                self._noLenArgs_ += arg._noLenArgs
            elif hasattr(arg, "__len__"):
                self._minLen_ = min(self._minLen_, len(arg))
            else:
                self._noLenArgs_.append(arg)

    @cached_property
    def _minLen(self):
        self._classify_args()
        return self._minLen_

    @cached_property
    def _noLenArgs(self):
        _ = self._minLen  # invoke argument classification if necessary
        return self._noLenArgs_

    @cached_property
    def _len(self):
        if self._noLenArgs:
            if np.isfinite(self._minLen):
                iterable = zip(range(self._minLen), *self._noLenArgs)
            else:
                iterable = zip(*self._noLenArgs)

            try:
                return more_itertools.ilen(deepcopy(iterable))
            except TypeError:
                raise TypeError(
                    "Cannot determine the length of an unpickable object such as "
                    "a generator. Convert the argument to a list first."
                )
        else:
            return self._minLen

    def __len__(self):
        return self._len


class lenrepeat:
    def __init__(self, value, number):
        self._number = number
        self._value = value

    def __len__(self):
        return self._number

    def __iter__(self):
        return iter(repeat(self._value, self._number))


def get_chunks_iter(iterator, chunksizes, manager):
    iterator = iter(iterator)
    return (ManagedIterator(iterator, manager, limit) for limit in chunksizes)


class ResultManager:
    def __init__(self) -> None:
        self._resultIndices = deque()
        self._iteratorNumber = 0
        self._resultIterators = []
        self.lock = Lock()

    def register_input(self, *iterators):
        for iterator in iterators:
            iterator._id = self._iteratorNumber
            self._iteratorNumber += 1

    def add_result_id(self, resultID):
        self._resultIndices.append(resultID)

    def register_output(self, *iterators):
        for iterator in iterators:
            self._resultIterators.append(iter(iterator))

    def __next__(self):
        if not self._resultIndices:
            raise StopIteration()
        return next(self._resultIterators[self._resultIndices.popleft()])

    def __iter__(self):
        assert len(self._resultIterators) == self._iteratorNumber
        return self


class ManagedIterator:
    def __init__(self, iterator, manager, limit):
        self._index = 0
        self._iterator = iterator
        self._limit = limit
        self._id = None
        self._manager = manager
        manager.register_input(self)

    def __len__(self):
        return self._limit - self._index

    def __next__(self):
        with self._manager.lock:
            if not len(self):
                raise StopIteration()
            self._manager.add_result_id(self._id)
            self._index += 1
            return next(self._iterator)

    def __iter__(self):
        return self


def get_chunksizes(num, chunksize):
    result = np.zeros(num // chunksize + 1, dtype=int)
    result[:] = num // result.size
    result[: num % result.size] += 1
    return result


def get_chunksize_per_worker(num, workers):
    if hasattr(workers, "__iter__"):
        workers = list(workers)
        for i, w in enumerate(workers):
            if hasattr(w, "_processes"):
                workers[i] = w._processes
        workerNumber = sum(workers)
        if len(workers) <= 1:
            workers = workerNumber
    else:
        workerNumber = workers

    result = np.full(workerNumber, num // workerNumber, dtype=int)
    result[: num % workerNumber] += 1

    if hasattr(workers, "__iter__"):
        splits = np.cumsum([0] + workers)
        result = [
            sum(result[start:stop]) for start, stop in zip(splits[:-1], splits[1:])
        ]

    return result


def iterlen(iterable):
    """
    Returns the length of an iterable.
    WARNING! The iterator needs to be copied and evaluated,
             which may fail for generator objects. In these
             cases, convert the generator to a list first!
    """
    if hasattr(iterable, "__len__"):
        return len(iterable)
    else:
        try:
            return more_itertools.ilen(deepcopy(iterable))
        except TypeError:
            raise TypeError(
                "Cannot determine the length of an unpickable object such as "
                "a generator. Convert the argument to a list first."
            )


def sampler_mapstar(sampler, args):
    return list(map(partial(args[0], sampler), args[1]))


def sampler_starmapstar(sampler, args):
    return list(starmap(partial(args[0], sampler), *args[1:]))


def sampler_kwstarmapstar(sampler, args):
    fun = args[0]
    return [fun(sampler, *row[0][0], **dict(zip(row[1], row[0][1]))) for row in args[1]]


class _InitCounter(object):
    def __init__(self, pool, count, jobID=-1):
        self._pool = pool
        self._event = threading.Event()
        self._jobID = jobID
        self._cache = pool._cache
        self._cache[self._jobID] = self
        self.count = count

    def ready(self):
        return self._event.is_set()

    def wait(self, timeout=None):
        self._event.wait(timeout)

    def _set(self, i, obj):
        self._success, self._value = obj
        self.count -= 1
        if self.count <= 0:
            self._event.set()
            del self._cache[self._jobID]
            self._pool = None

    def get(self, timeout=None):
        self.wait(timeout)
        if self._success:
            return self._value
        else:
            raise self._value


def worker(inqueue, outqueue, cls, initargs=(), maxtasks=None, wrap_exception=False):
    if (maxtasks is not None) and not (isinstance(maxtasks, int) and maxtasks >= 1):
        raise AssertionError("Maxtasks {!r} is not valid".format(maxtasks))
    put = outqueue.put
    get = inqueue.get
    if hasattr(inqueue, "_writer"):
        inqueue._writer.close()
        outqueue._reader.close()

    try:
        sampler = cls(*initargs)
        result = (True, None)
    except Exception as e:
        if wrap_exception:
            e = ExceptionWithTraceback(e, e.__traceback__)
        result = (False, e)
        return
    finally:
        put((-1, 0, result))

    completed = 0
    while maxtasks is None or (maxtasks and completed < maxtasks):
        try:
            task = get()
        except (EOFError, OSError):
            util.debug("worker got EOFError or OSError -- exiting")
            break

        if task is None:
            util.debug("worker got sentinel -- exiting")
            break

        job, i, func, args, kwds = task
        try:
            result = (True, func(sampler, *args, **kwds))
        except Exception as e:
            if wrap_exception and func is not _helper_reraises_exception:
                e = ExceptionWithTraceback(e, e.__traceback__)
            result = (False, e)
        try:
            put((job, i, result))
        except Exception as e:
            wrapped = MaybeEncodingError(e, result[1])
            util.debug("Possible encoding error while sending result: %s" % (wrapped))
            put((job, i, (False, wrapped)))

        task = job = result = func = args = kwds = None
        completed += 1
    util.debug("worker exiting after %d tasks" % completed)


# def distributedRemoteTask(task, *args, **kwargs):
#     threadID = threading.get_native_id()
#     return task(*(arg[threadID] for arg in args), **{kwarg[threadID] for kwarg in kwargs})


class _ObjectPoolExt:
    def _repopulate_pool(self):
        if hasattr(self, "initCounter"):
            self.initCounter.count += self._processes - len(self._pool)
        else:
            self.initCounter = _InitCounter(self, self._processes - len(self._pool))
        return self._repopulate_pool_static(
            self._ctx,
            self.Process,
            self._processes,
            self._pool,
            self._inqueue,
            self._outqueue,
            self._initializer,
            self._initargs,
            self._maxtasksperchild,
            self._wrap_exception,
        )

    """
    Applies all calls to the pool to a number of object instances of given type
    """

    @staticmethod
    def _repopulate_pool_static(
        ctx,
        Process,
        processes,
        pool,
        inqueue,
        outqueue,
        initializer,
        initargs,
        maxtasksperchild,
        wrap_exception,
    ):
        """Bring the number of pool processes up to the specified number,
        for use after reaping workers which have exited.
        """
        for i in range(processes - len(pool)):
            w = Process(
                ctx,
                target=worker,
                args=(
                    inqueue,
                    outqueue,
                    initializer,
                    initargs,
                    maxtasksperchild,
                    wrap_exception,
                ),
            )
            w.name = w.name.replace("Process", "PoolWorker")
            w.daemon = True
            w.start()
            pool.append(w)
            util.debug("added worker")

    def map(self, func, iterable, chunksize=None):
        """
        Apply `func` to each element in `iterable`, collecting the results
        in a list that is returned.
        """
        return self.map_async(func, iterable, chunksize).get()

    def map_async(self, func, iterable, chunksize=None):
        """
        Apply `func` to each element in `iterable`, collecting the results
        in a list that is returned.
        """
        return self._map_async(func, iterable, sampler_mapstar, chunksize)

    def starmap(self, func, iterable, chunksize=None):
        """
        Like `map()` method but the elements of the `iterable` are expected to
        be iterables as well and will be unpacked as arguments. Hence
        `func` and (a, b) becomes func(a, b).
        """
        return self.starmap_async(func, iterable, chunksize).get()

    def starmap_async(self, func, iterable, chunksize=None):
        """
        Like `map()` method but the elements of the `iterable` are expected to
        be iterables as well and will be unpacked as arguments. Hence
        `func` and (a, b) becomes func(a, b).
        """
        return self._map_async(func, iterable, sampler_starmapstar, chunksize)

    def kwstarmap(self, func, args, kwargs, chunksize=None):
        """
        Apply `func` to each element in `iterable`, collecting the results
        in a list that is returned.
        """
        return self.kwstarmap_async(func, args, kwargs, chunksize).get()

    def kwstarmap_async(self, func, args, kwargs, chunksize=None):
        """
        Apply `func` to each element in `iterable`
        """
        return self._kwstarmap_async(
            func,
            lenzip(args, lenzip(*kwargs.values())),
            tuple(kwargs.keys()),
            chunksize,
        )

    def _kwstarmap_async(self, func, args, keys, chunksize=None):
        """
        Apply `func` to each element in `iterable`
        """
        return self._map_async(
            func,
            lenzip(args, lenrepeat(keys, iterlen(args))),
            sampler_kwstarmapstar,
            chunksize,
        )


class ObjectPool(_ObjectPoolExt, Pool):
    pass


class ObjectThreadPool(_ObjectPoolExt, ThreadPool):
    pass


class DistributedPool:
    """
    Extension of Pool to circumvent the bug
    limiting the process count to 61 on Windows.
    """

    def __init__(self, numWorkers=None):
        if numWorkers is None:
            numWorkers = os.cpu_count()

        self.distributedPools = (
            numWorkers > MAX_WIN32_WORKERS and sys.platform == "win32"
        )

        if not self.distributedPools:
            self.pool = Pool(numWorkers)
        else:
            self.pool = [
                Pool(num) for num in get_chunksizes(numWorkers, MAX_WIN32_WORKERS)
            ]

        self.numWorkers = numWorkers

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def join(self):
        if self.distributedPools:
            for pool in self.pool:
                pool.join()
        else:
            self.pool.join()

    def close(self):
        if self.distributedPools:
            pools = self.pool
        else:
            pools = (self.pool,)

        for pool in pools:
            pool.close()
            pool.join()
            pool.terminate()

    def starmap(self, fun, args, **kwargs):
        if self.distributedPools:
            resultManager = ResultManager()
            workerChunks = get_chunksize_per_worker(iterlen(args), self.pool)
            results = [
                pool.starmap_async(fun, arg, **kwargs)
                for pool, arg in zip(
                    self.pool,
                    get_chunks_iter(args, workerChunks, manager=resultManager),
                )
            ]
            resultManager.register_output(*(result.get() for result in results))
            return resultManager
        else:
            return self.pool.starmap(fun, args, **kwargs)

    def map(self, fun, args, **kwargs):
        if self.distributedPools:
            workerChunks = get_chunksize_per_worker(iterlen(args), self.pool)
            resultManager = ResultManager()
            results = [
                pool.map_async(fun, arg, **kwargs)
                for pool, arg in zip(
                    self.pool,
                    get_chunks_iter(args, workerChunks, manager=resultManager),
                )
            ]
            resultManager.register_output(*(result.get() for result in results))
            return resultManager
        else:
            return self.pool.map(fun, args, **kwargs)


class ProxyPool:
    def __init__(self, cls, numWorkers=None, initargs=(), separateProcesses=False):
        self._cls = cls

        if numWorkers is None:
            numWorkers = os.cpu_count()

        self.distributedPools = (
            separateProcesses
            and numWorkers > MAX_WIN32_WORKERS
            and sys.platform == "win32"
        )

        if separateProcesses:
            poolCls = ObjectPool
        else:
            poolCls = ObjectThreadPool

        if not self.distributedPools:
            self.pool = poolCls(numWorkers, cls, initargs)
            pools = [self.pool]
        else:
            self.pool = [
                poolCls(num, cls, initargs)
                for num in get_chunksizes(numWorkers, MAX_WIN32_WORKERS)
            ]
            pools = self.pool

        for pool in pools:
            pool.initCounter.get()

        self.numWorkers = numWorkers

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def join(self):
        if self.distributedPools:
            for pool in self.pool:
                pool.join()
        else:
            self.pool.join()

    def close(self):
        if self.distributedPools:
            pools = self.pool
        else:
            pools = (self.pool,)

        for pool in pools:
            pool.close()
            pool.join()
            pool.terminate()

    def _starmap(self, fun, args, **kwargs):
        if self.distributedPools:
            workerChunks = get_chunksize_per_worker(iterlen(args), self.pool)
            resultManager = ResultManager()
            results = [
                pool.starmap_async(fun, arg, **kwargs)
                for pool, arg in zip(
                    self.pool,
                    get_chunks_iter(args, workerChunks, manager=resultManager),
                )
            ]
            resultManager.register_output(*(result.get() for result in results))
            return resultManager
        else:
            return self.pool.starmap(fun, args, **kwargs)

    def _kwstarmap(self, fun, args, kwargs, **poolkwargs):
        if not kwargs:
            return self._starmap(fun, args, **poolkwargs)

        if self.distributedPools:
            keys = tuple(kwargs.keys())
            kwargs = lenzip(*kwargs.values())

            if not args:
                taskLength = len(kwargs)
                iterArgs = lenzip(lenrepeat((), taskLength), kwargs)
            else:
                iterArgs = lenzip(args, kwargs)
                taskLength = len(iterArgs)

            workerChunks = get_chunksize_per_worker(taskLength, self.pool)

            resultManager = ResultManager()
            results = [
                pool._kwstarmap_async(fun, arg, keys, **poolkwargs)
                for pool, arg in zip(
                    self.pool,
                    get_chunks_iter(iterArgs, workerChunks, manager=resultManager),
                )
            ]
            resultManager.register_output(*(result.get() for result in results))
            return resultManager
        else:
            return self.pool.kwstarmap(fun, args, kwargs, **poolkwargs)

    def __getattr__(self, key):
        try:
            if isinstance(getattr(self._cls, key), staticmethod):
                return self._cls.key
        except AttributeError:
            pass

        def function_wrapper(*args, map_args=False, chunksize=None, **kwargs):
            fun = getattr(self._cls, key)
            if map_args:
                result = list(
                    self._kwstarmap(fun, lenzip(*args), kwargs, chunksize=chunksize)
                )
            else:
                if kwargs:
                    fun = partial(fun, **kwargs)
                result = list(
                    self._starmap(
                        fun, lenrepeat(args, self.numWorkers), chunksize=chunksize
                    )
                )
            if result and isinstance(result[0], np.ndarray):
                return np.vstack(result)
            else:
                return result

        return function_wrapper
