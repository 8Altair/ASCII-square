def validate_square_size(value):
    """
        Validates that the given value can be converted to a positive integer.
        Returns a tuple: (is_valid, error_message).
    """
    try:
        size = int(value)
        if size <= 0:
            return False, "Size must be a positive integer."
        return True, ""
    except ValueError:
        return False, "Size must be a valid integer."


def validate_size_length(new_value):
    # Allow only up to 5 characters in the square size entry.
    return len(new_value) <= 5


def validate_starting_character(value):
    """
        Validates that the starting character is a single alphabetical character.
        Returns a tuple: (is_valid, error_message).
    """
    if len(value) != 1 or not value.isalpha():
        return False, "Starting character must be a single alphabetic character."
    return True, ""
