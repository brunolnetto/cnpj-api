from datetime import datetime, timezone

from backend.app.utils.misc import is_positive, is_non_negative
from backend.app.api.constants import UNIT_MULTIPLIER

# The maximum limit value that can be provided.
MAX_LIMIT = 100

def check_limit_and_offset(limit: int, offset: int) -> None:
    """
    Checks if the limit and offset are non-negative.

    Args:
        limit: The limit value.
        offset: The offset value.

    Raises:
        ValueError: If the limit or offset are negative.
    """
    if not is_non_negative(offset):
        explanation = f"Offset must be non-negative. Provided offset value: {offset}"
        raise ValueError(explanation)

    if not is_positive(limit):
        explanation = f"Limit must be positive. Provided limit value: {limit}"
        raise ValueError(explanation)

    return min(limit, MAX_LIMIT), offset


def convert_to_bytes(size_str):
    """
    This function converts a size string (e.g., "22K", "321M") into bytes.

    Args:
        size_str (str): The size string to convert.

    Returns:
        int: The size in bytes, or None if the format is invalid.
    """
    try:
        size_value = float(size_str[:-1])  # Extract numerical value
        size_unit = size_str[-1].upper()  # Get the unit (K, M, G, ...)

        if size_unit in UNIT_MULTIPLIER:
            multiplier=UNIT_MULTIPLIER[size_unit]
            return int(size_value * multiplier)
        else:
            return None  # Handle invalid units
    except ValueError:
        return None 

