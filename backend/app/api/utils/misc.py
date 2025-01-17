import time
import re
from functools import wraps
from inspect import iscoroutinefunction
from typing import Dict, List, Any

from backend.app.utils.misc import is_positive, is_non_negative
from backend.app.api.constants import UNIT_MULTIPLIER, MAX_LIMIT


def print_execution_time(func):
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(
            f"Execution time of {func.__name__}: {execution_time:.4f} seconds")
        return result

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(
            f"Execution time of {func.__name__}: {execution_time:.4f} seconds")
        return result

    return async_wrapper if iscoroutinefunction(func) else sync_wrapper


def zfill_factory(n: int):
    # Normalize data
    def zfill_map(value: str, num: int):
        return value.zfill(num)

    def zfill_n(value: Any):
        return zfill_map(value, n)

    return zfill_n


def remove_quotes(text: str) -> str:
    return text.replace("'", "").replace('"', "")


def normalize_json(json_str: str):
    return re.sub(r"(?<!\\)'", '"', json_str)


def check_limit_and_offset(limit: int, offset: int) -> tuple[int, int]:
    """Checks if limit and offset are valid."""
    if not is_non_negative(offset):
        raise ValueError(
            f"Offset must be non-negative. Provided offset value: {offset}"
        )
    if not is_positive(limit):
        raise ValueError(
            f"Limit must be positive. Provided limit value: {limit}")

    return min(limit, MAX_LIMIT), offset


def convert_to_bytes(size_str: str) -> int:
    """Converts a size string (e.g., '22K', '321M') into bytes."""
    try:
        size_value = float(size_str[:-1])  # Extract numerical value
        size_unit = size_str[-1].upper()  # Get the unit (K, M, G, ...)

        if size_unit in UNIT_MULTIPLIER:
            return int(size_value * UNIT_MULTIPLIER[size_unit])

    except ValueError:
        pass  # Invalid format

    return 0  # Default value for invalid format


def comma_stringify_list(lst: List[Any]) -> str:
    return ",".join(f"'{str(item)}'" for item in lst)


def commify_list(lst: List[Any]) -> str:
    return ",".join(item for item in lst)


def paginate_dict(data_dict: Dict, page_size: int, page_number: int):
    """
    Paginate a dictionary.

    Args:
    - data_dict (dict): The dictionary to paginate.
    - page_size (int): The number of items per page.
    - page_number (int): The page number to retrieve (1-based index).

    Returns:
    - dict: A dictionary containing the key-value pairs for the specified page.
    """

    # Convert dictionary keys to a list for easy slicing
    keys_list = list(data_dict.keys())

    # Calculate start and end indices
    start_index = (page_number + 1) * page_size
    end_index = start_index + page_size

    # Get the slice of keys for the current page
    page_keys = keys_list[start_index:end_index]

    # Build the paginated dictionary
    paginated_dict = {key: data_dict[key] for key in page_keys}

    return paginated_dict
