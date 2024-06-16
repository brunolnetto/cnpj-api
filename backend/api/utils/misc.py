from backend.utils.misc import is_positive, is_non_negative


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
        explanation = "Offset must be non-negative. Offset value: {offset}"
        raise ValueError(explanation)

    if not is_positive(limit):
        explanation = "Limit must be positive. Limit value: {limit}"
        raise ValueError(explanation)
