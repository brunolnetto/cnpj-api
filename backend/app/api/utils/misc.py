from time import perf_counter
import re
from functools import wraps
from inspect import iscoroutinefunction
from typing import Dict, List, Any, Union

from backend.app.utils.misc import is_positive, is_non_negative
from backend.app.api.constants import UNIT_MULTIPLIER, MAX_LIMIT


def build_condition(
    column: str,
    value: Union[str, int, float, list, None],
    condition_type: str = "eq",
    array_condition: bool = False
) -> str:
    """
    Builds a SQL condition snippet based on column, value and condition type.

    Args:
        column: Column name in SQL.
        value: Value to compare. Can be string, number or list.
        condition_type: Type of condition ("eq", "gt", "ge", "lt", "le", "contains").
        array_condition: Whether to treat the value as an array (for Postgres array operations).

    Returns:
        A string with the SQL condition (e.g., "column='value'").
    """

    if value in [None, "", [], {}]:
        return "1=1"

    def quote(v: Any) -> str:
        return f"'{v}'" if isinstance(v, str) else str(v)

    condition_map = {
        "eq": lambda: f"{column} = {quote(value)}",
        "gt": lambda: f"{column} > {quote(value)}",
        "ge": lambda: f"{column} >= {quote(value)}",
        "lt": lambda: f"{column} < {quote(value)}",
        "le": lambda: f"{column} <= {quote(value)}",
        "contains": lambda: (
            f"{column} @> ARRAY[{', '.join(map(quote, value))}]"
            if array_condition and isinstance(value, (list, tuple))
            else f"{column} LIKE '%{value}%'"
        )
    }

    return condition_map.get(condition_type, lambda: "1=1")()


def print_execution_time(label: str):
    def wrapper(func):
        @wraps(func)
        async def async_inner(*args, **kwargs):
            t0 = perf_counter()
            result = await func(*args, **kwargs)
            print(f"[{label}] took {perf_counter() - t0:.2f}s")
            return result

        @wraps(func)
        def sync_inner(*args, **kwargs):
            t0 = perf_counter()
            result = func(*args, **kwargs)
            print(f"[{label}] took {perf_counter() - t0:.2f}s")
            return result

        return async_inner if iscoroutinefunction(func) else sync_inner
    return wrapper


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
        raise ValueError(f"Limit must be positive. Provided limit value: {limit}")

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
