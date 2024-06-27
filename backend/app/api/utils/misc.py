from backend.app.utils.misc import is_positive, is_non_negative

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