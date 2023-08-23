# ObjectProxyPool - simple object-based multiprocessing

This package provides the implementation of an ObjectProxyPool, a 
multiprocessing pool of instances of a specified class. The pool
object features all methods that the original class provides.
Whenever a methods is called, this call is applied to all remote copies;
the results are computed in parallel, collected, and returned as an
array. This makes it very easy to implement object-based parallelism. 

## Motivation

Object-based parallelism is useful if an object-based workflow 
should be repeated several times, e.g. to assess the impact
of stochasticity. In modelling, for example, we may want to 
repeat a simulation with multiple instances of the model and
compare the results.

The approach has significant advantages if the object used for
the computations is expensive to initialize. As the instances
can be reused for multiple tasks, initialization needs
to happen only once for each process.


## Example usage

```python
from objectproxypool import ProxyPool
import numpy as np
import os
import time


# Define some class providing the
# the functionality we are interested in
class MyClass:
    def __init__(self) -> None:
        np.random.seed(os.getpid())
        self.property = None
    
    def get_normal_sample(self, mean, std):
        return mean + np.random.randn(10) * std
    
    def set_property(self, value):
        self.property = value
        
        # we add some delay to prevent that one worker 
        # does this task twice whereas another worker has 
        # an unspecified property.
        time.sleep(0.1)
    
    def add_and_get_property(self, *args):
        return self.property, sum(args)

    def fill_and_compute_sum(self, arr, i, value):
        
        # add some delay for dempnstration purposes only
        time.sleep(0.2)
        
        # The with statment is needed to access and close
        # a version of the shared memory in this process.
        with Unpacker(arr) as arr:
            
            # Here we can use `arr` as any other numpy array. 
            arr[i] = value
            return arr.sum()


if __name__ == "__main__":
    # Create a pool of 4 instances of MyClass, each running
    # in a separate process. Set `separateProcesses=False`
    # to work with threads instead of processes.
    # (Caution: if numWorkers is larger than the number of
    # available CPUs, the performance can be bad!)
    with ProxyPool(MyClass, numWorkers=4, separateProcesses=True) as pool:
        # We can easily parallelize a task by letting
        # each remote instance do the same. For example,
        # we obtain a sample of normally distributed random
        # numbers in parallel.
        print(pool.get_normal_sample(10, 1))

        # We can change the state of the remote instances.
        # `map_args=True` makes that each worker receives
        # one particular number of the range 1:4.
        # Without this argument, each worker would receive the
        # argument `range(4)`, i.e., all four numbers
        pool.set_property(range(4), map_args=True)

        # Add numbers to the property
        # Even though we have only four workers, we can reuse
        # the workers to do multiple tasks until all the
        # work is done.
        print(pool.add_and_get_property(range(20), range(20), map_args=True))


        # We can also exchange data via shared arrays.
        # To that end, wrap an array that we want to share with a SharedArrayWrapper.
        # Note: this only works properly if we use separate processes.
        # If not, we do not need shared memory anyway!
        arr = SharedArrayWrapper(np.zeros(10))

        # Passing the shared memory is as easy as passing the array as argument. 
        # However, we need to use the `remoteArray` property of the array wrapper.
        sums = pool.fill_and_compute_sum(repeat(arr.remoteArray), range(10), range(10), map_args=True)
        
        # We see that the array has been filled as desired
        print(arr.array)
        
        # When the entries were filled, the array was not completely full yet. 
        # Here, we see that the method was indeed processes in parallel,
        # since the input array is similar in several instances, as 
        # indicated by equal sums of the entries.
        print(sums)
```