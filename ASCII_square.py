from functools import lru_cache
from timer_wrapper import timer


@timer
@lru_cache(maxsize=128)
def ascii_square_construction(square_size, starting_character="A") -> str:
    # Define the allowed characters: A-Z then a-z.
    allowed_chars = [chr(i) for i in range(ord("A"), ord("Z") + 1)] + \
                    [chr(i) for i in range(ord("a"), ord("z") + 1)]
    total_letters = len(allowed_chars)  # 52

    # Ensure starting_character is one of the allowed ones; fallback to "A" if not
    try:
        start_index = allowed_chars.index(starting_character)
    except ValueError:
        start_index = 0

    last_index = square_size - 1  # Last possible index (any direction) of a square

    offsets = [min(i, last_index - i) for i in range(square_size)]  # Precompute offsets for rows and columns
    maximum_offset = max(offsets)  # Maximum offset possible (will be <= last_index // 2)
    ascii_map = [allowed_chars[(start_index + offset) % total_letters] for offset in range(maximum_offset + 1)]  # Precompute the mapping from offset to character

    # Build the square rows using the precomputed mapping
    rows = (" ".join(ascii_map[min(row_offset, column_offset)] for column_offset in offsets)
            for row_offset in offsets)

    return "\n".join(rows)  # Return a constructed square
