from functools import lru_cache
from timer_wrapper import timer


@timer
@lru_cache(maxsize=None)
def ascii_square_construction(square_size, starting_character = "A") -> str:
    reference = ord(starting_character)    # First ASCII character
    last_index = square_size - 1      # Last possible index (any direction) of a square

    offsets = [min(i, last_index - i) for i in range(square_size)]    # Precompute offsets for rows and columns
    maximum_offset = max(offsets)    # Maximum offset possible (will be <= last_index // 2)
    ascii_map = [chr(reference + offset) for offset in range(maximum_offset + 1)]    # Precompute the mapping from offset to character.

    # Build the square rows using the precomputed maping
    rows = (" ".join(ascii_map[min(row_offset, column_offset)] for column_offset in offsets)
             for row_offset in offsets)

    return "\n".join(rows)  # Return a constructed square
