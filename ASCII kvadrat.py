import time
from functools import lru_cache, wraps


def timer(function):    # Function for time measurement called with the decorator @timer
    @wraps(function)
    def wrapper(*args, **kwargs):   # Wrapper function to automatically calculate the execution time of ASCII square construction
        start_time = time.time()
        result = function(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time of {function.__name__}: {end_time - start_time} seconds")
        return result

    return wrapper

@lru_cache(maxsize=None)    # Least-recently-used caching technique (with maximum size unlimited)
@timer      # Decorator for time measurement
def ascii_square_construction(n):
    reference = ord("A")    # Starting character ASCII
    last_index = n - 1      # Last possible index (any direction) of a square

    # Constructing a generator of square rows, then adding them from the top to the bottom
    ascii_square = "\n".join(" ".join(chr(reference + min(i, j, last_index - i, last_index - j))
                                      for j in range(n)) for i in range(n))
    return ascii_square

print(ascii_square_construction(13))    # Call the function to draw ASCII square for a designated dimension
