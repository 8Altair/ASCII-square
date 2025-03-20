import time
from functools import wraps


def timer(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        info_before = function.cache_info().misses
        start_time = time.time()
        result = function(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        info_after = function.cache_info().misses

        if info_after == info_before:        # If misses did not change, this was a cache hit.
            wrapper.last_execution_time = None
        else:
            wrapper.last_execution_time = elapsed_time
        print(f"Execution time of {function.__name__}: {elapsed_time} seconds")
        return result

    wrapper.last_execution_time = None
    return wrapper

