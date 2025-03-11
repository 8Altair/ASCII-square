import time
from functools import lru_cache, wraps


def timer(function):    # Function for time measurement called with the decorator @timer
    @wraps(function)
    def wrapper(*args, **kwargs):   # Wrapper function to automatically calculate the execution time of ASCII square construction
        start_time = time.time()
        result = function(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time of {function.__name__}: {end_time - start_time} seconds\n")
        return result

    return wrapper


@lru_cache(maxsize=None)
@timer
def ascii_square_construction(n):
    reference = ord("A")    # Starting character ASCII
    last_index = n - 1      # Last possible index (any direction) of a square

    row_distances = [min(i, last_index - i) for i in range(n)]    # Precompute row distances
    column_distances = [min(j, last_index - j) for j in range(n)]    # Precompute column distances

    rows = (" ".join(chr(reference + min(row_distances[i], column_distances[j])) for j in range(n)) for i in range(n))
    return "\n".join(rows)

print(ascii_square_construction(13))    # Call the function to draw ASCII square for a designated dimension
