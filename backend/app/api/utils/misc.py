import time
import re
from functools import wraps
from inspect import iscoroutinefunction
from typing import Dict, List, Any

from backend.app.utils.misc import is_positive, is_non_negative
from backend.app.api.constants import UNIT_MULTIPLIER, MAX_LIMIT


def build_condition(column: str, value, condition_type="eq", array_condition=False):
    """
    Helper function to build SQL conditions.
    """
    if not value:
        return "1=1"

    if condition_type == "eq":
        return f"{column}='{value}'"
    elif condition_type == "gt":
        return f"{column}>'{value}'"
    elif condition_type == "ge":
        return f"{column}>='{value}'"
    elif condition_type == "lt":
        return f"{column}<'{value}'"
    elif condition_type == "le":
        return f"{column}<='{value}'"
    elif condition_type == "contains" and array_condition:
        return f"{column} @> Array[{value}]"
    
    return "1=1"  # Default fallback, though rarely used with the above checks.

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
        # If the value contains a decimal point, split it and pad only the digits part
        if '.' in value:
            int_part, dec_part = value.split('.', 1)
            return f"{int_part.zfill(num - len(dec_part) - 1)}.{dec_part}"
        return value.zfill(num)

    def zfill_n(value: Any):
        return zfill_map(str(value), n)

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
    return ",".join(str(item) for item in lst)


def paginate_dict(data_dict: Dict, page_size: int, page_number: int, sort_by: str = None):
    """
    Paginate a dictionary with an optional sorting key.
    
    Args:
    - data_dict (dict): The dictionary to paginate.
    - page_size (int): The number of items per page.
    - page_number (int): The page number to retrieve (0-based index).
    - sort_by (str, optional): The key to sort the dictionary by. Defaults to None, meaning no sorting.

    Returns:
    - dict: A dictionary containing the key-value pairs for the specified page.
    """
    
    # If sorting is required, sort by the specified key or by keys alphabetically
    if sort_by:
        # Use a default value (-float('inf')) for missing keys to avoid TypeError
        sorted_items = sorted(
            data_dict.items(), 
            key=lambda x: x[1].get(sort_by, float('-inf')) if isinstance(x[1], dict) else x[1]
        )
    else:
        sorted_items = list(data_dict.items())
    
    # Flatten the sorted items back to a dictionary after sorting
    sorted_dict = dict(sorted_items)

    # Calculate start and end indices for pagination
    start_index = page_number * page_size  # Adjusted for 0-based index
    end_index = start_index + page_size

    # Check if the page_number exceeds available data, return empty dict if so
    if start_index >= len(sorted_items):
        return {}

    # Get the slice of items for the current page
    page_items = sorted_items[start_index:end_index]

    # Return a dictionary containing the items on the current page
    return dict(page_items)