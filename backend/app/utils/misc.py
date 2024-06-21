from typing import Union, List, Tuple, Dict, Any
from os import makedirs, path
from datetime import datetime
import json
import re

from backend.app.setup.logging import logger

NumberList = List[Union[int, float]]


def are(args: List[Any], validation_map: callable) -> bool:
    """
    Checks if a field is equal to any of the given values.

    Args:
        field (str): The field to check.
        *args (str): The values to compare with.

    Returns:
        bool: Whether the field is equal to any of the values.
    """
    return all(map(validation_map, args))


def is_positive(x: NumberList) -> bool:
    return x > 0


def is_non_negative(x: NumberList) -> bool:
    return x >= 0


def is_negative(x: NumberList) -> bool:
    return x < 0


def is_non_positive(x: NumberList) -> bool:
    return x <= 0


def are_positive(lst: NumberList) -> bool:
    return are(lst, is_positive)


def are_non_negative(lst: NumberList) -> bool:
    return are(lst, is_non_negative)


def are_negative(lst: List[Union[int, float]]) -> bool:
    return are(lst, is_negative)


def are_non_positive(lst: NumberList) -> bool:
    return are(lst, is_non_positive)


def date_str():
    """
    Returns the current date as a string in the format 'YYYY-MM-DD'.

    Returns:
        str: The current date as a string.
    """
    return datetime.now().strftime("%Y-%m-%d")


def number_string_to_number(number_string: str) -> int:
    """
    Converts a float string to an integer.

    Args:
        float_string (str): The float string to convert.

    Returns:
        int: The integer value.
    """
    int_value = int(float(number_string))
    float_value = float(number_string)
    remainder = float_value - int_value

    return int_value if remainder == 0 else float_value


def time_str():
    """
    Returns the current time as a string in the format 'HH_MM'.

    Returns:
        str: The current time as a string.
    """
    return datetime.now().strftime("%H_%M")


def humanize_string(s):
    # Step 1: Separate letters and special characters from numbers
    s = re.sub(r"(\W+)(\d+)", r"\1 \2", s)
    s = re.sub(r"([A-Za-z]+)(\d+)", r"\1 \2", s)

    # Step 2: Remove leading zeros from numbers
    s = re.sub(r"\b0+(\d+)", r"\1", s)

    # Step 3: Replace multiple spaces with a single space
    s = re.sub(r"\s+", " ", s).strip()

    # Step 4: Capitalize the first letter of each word
    s = s.title()

    return s


def string_to_json(string: str) -> dict:
    string = string.replace("'", '"')
    string = re.sub(r"\bNone\b", "null", string)

    return json.loads(string)


def is_number(text: str) -> bool:
    """
    Checks if a string is a number.

    Args:
        text (str): The string to check.

    Returns:
        bool: Whether the string is a number.
    """

    # Matches digits with an optional decimal part
    pattern = r"^\d+(\.\d+)?$"
    return bool(re.match(pattern, text))


def are_numbers(lst: List[Union[str, int, float]], is_strict: bool = False) -> bool:
    """
    Checks if all elements in a list are numbers.

    Args:
        lst (List): The list to check.
        is_strict (bool, optional): Whether to check for strict numbers. Defaults to False.

    Returns:
        bool: Whether all elements in the list are numbers.
    """
    if is_strict:
        return all(map(lambda x: is_number(str(x)), lst))
    else:
        return all(map(lambda x: is_number(str(x).replace(".", "")), lst))


def format_decimal(float_string: str, num_decimal_places: int = 2) -> str:
    """
    Formats a decimal number to a string with a fixed number of decimal places.

    Args:
        float_string (str): The decimal number to format.
        num_decimal_places (int): The number of decimal places to use.

    Returns:
        str: The formatted decimal number.
    """
    return f"{float(float_string):.{num_decimal_places}f}"


def is_field_valid(field: str) -> bool:
    """
    Checks if a field is valid.

    Args:
        field (str): The field to check.

    Returns:
        bool: Whether the field is valid.
    """
    is_nan = str(field).lower() == "nan"
    is_nat = str(field).lower() == "nat"
    is_null = str(field).lower() == "null"
    is_none = str(field).lower() == "none"

    is_invalid = is_nan or is_nat or is_null or is_none

    return not is_invalid


def replace_invalid_fields_on_list_tuple(lst: List[Tuple]) -> List[Tuple]:
    """
    Replaces NaN values with empty string.

    Args:
        lst (List): The list to process.

    Returns:
        The list with NaN values replaced by None.
    """

    def clean_field_map(el):
        return "" if not is_field_valid(el) else el

    return operate_on_list_tuple(lst, clean_field_map)


def replace_invalid_fields_on_list_dict(lst: List[Dict]) -> List[Dict]:
    """
    Replaces NaN values with empty string.

    Args:
        lst (List): The list to process.

    Returns:
        The list with NaN values replaced by None.
    """

    def clean_field_map(el):
        return "" if not is_field_valid(el) else el

    return operate_on_list_dict(lst, clean_field_map)


# Define a function to format the date
DELIMITER = "/"


def format_database_date(date_str_: str, delimiter: str = DELIMITER) -> str:
    """
    Formats a date string to the database format.

    Args:
        date_str (str): The date string to format.
        delimiter (str): The delimiter to use.

    Returns:
        str: The formatted date string.
    """
    date_str_ = str(date_str_)
    if not is_field_valid(date_str) or not is_number(date_str_) or len(date_str_) != 8:
        return None

    return f"{date_str_[6:]}{delimiter}{date_str_[4:6]}{delimiter}{date_str_[:4]}"


def format_cep(cep_str: str):
    """
    Formats a CEP string.

    Args:
        cep_str (str): The CEP string to format.

    Returns:
        str: The formatted CEP string
    """
<<<<<<< HEAD
    cep_str=str(cep_str)
    is_valid_cep=is_database_field_valid(cep_str) and is_number(cep_str)
=======
    cep_str = str(cep_str)
    is_valid_cep = is_field_valid(cep_str) and is_number(cep_str)
>>>>>>> 2d6b359 (lint/ black backend/__init__.py)

    if not is_valid_cep:
        return ""

    # Remove decimal part if it exists
    cep_str = str(int(float(cep_str)))
    cep_str = cep_str.zfill(8)

    return f"{cep_str[0:2]}.{cep_str[2:5]}-{cep_str[5:8]}"


# Define a function to format the phone number
def format_phone(
    ddd_num: str,
    phone_num: str,
    ddd_ldelimiter: tuple = "(",
    ddd_rdelimiter: tuple = ")",
    phone_delimiter="-",
):
    """
    Formats a phone number.

    Args:
        ddd (str): The DDD part of the phone number.
        phone_num (str): The phone number.
        ddd_ldelimiter (tuple, optional): The left delimiter for the DDD. Defaults to '('.
        ddd_rdelimiter (tuple, optional): The right delimiter for the DDD. Defaults to ')'.
        phone_delimiter (str, optional): The delimiter for the phone number. Defaults to '-'.

    Returns:
        str: The formatted phone number.
    """

    def is_phone_valid(phone_):
        return is_number(phone_) and is_field_valid(phone_) and len(phone_) in (8, 9)

    def is_ddd_valid(ddd_):
        return is_number(ddd_) and is_field_valid(ddd_) and len(ddd_) in (1, 2)

    are_fields_valid = is_phone_valid(phone_num) and is_ddd_valid(ddd_num)

    if not are_fields_valid:
        return ""

    ddd_num = str(int(float(ddd_num)))
    phone_num = str(int(float(phone_num)))
    phone_num = phone_num.zfill(8)

    formated_ddd = f"{ddd_ldelimiter}{ddd_num}{ddd_rdelimiter}"
    formatted_phone = f"{phone_num[:4]}{phone_delimiter}{phone_num[4:]}"

    return f"{formated_ddd} {formatted_phone}"


def operate_on_list_tuple(lst: List[Tuple], operation: callable) -> List[Any]:
    """
    Operates on a list of tuples.

    Args:
        lst (List): The list to process.
        operation (str): The operation to perform.
        value (str): The value to operate with.

    Returns:
        The list with the operation performed.
    """

    def tuple_map(tuple_):
        return tuple(map(operation, tuple_))

    return list(map(tuple_map, lst))


def operate_on_list_dict(lst: List[Tuple], operation: callable) -> List[Any]:
    """
    Operates on a list of dictionaries.

    Args:
        lst (List): The list to process.
        operation (str): The operation to perform.
        value (str): The value to operate with.

    Returns:
        The list with the operation performed.
    """

    def item_map(item):
        return item[0], operation(item[1])

    def dict_map(dict_):
        return dict(map(item_map, dict_.items()))

    return list(map(dict_map, lst))


def replace_spaces_on_list_tuple(lst: List[Tuple]) -> List[str]:
    """
    Replaces multiple consecutive spaces with a single space.

    Args:
        lst (List): The list to process.

    Returns:
        The list with multiple spaces replaced by a single space.
    """

    def clean_spaces_map(el):
        return " ".join(str(el).split())

    return operate_on_list_tuple(lst, clean_spaces_map)


def makedir(folder_name: str, is_verbose: bool = False):
    """
    Creates a new directory if it doesn't already exist.

    Args:
        folder_name (str): The name of the folder to create.
        is_verbose (bool, optional): Whether to log verbose information. Defaults to False.
    """
    if not path.exists(folder_name):
        makedirs(folder_name)

        if is_verbose:
            logger.info(f"Folder {repr(str(folder_name))} created!")

    else:
        if is_verbose:
            logger.warning(f"Folder {repr(str(folder_name))} already exists!")


def replace_spaces(text):
    """
    This function replaces multiple consecutive spaces with a single space.

    Args:
        text: The string to process.

    Returns:
        The string with multiple spaces replaced by a single space.
    """
    return " ".join(text.split())


def remove_leading_zeros(text: str) -> str:
    """
    Removes leading zeros from a string.

    Args:
        text: The string to remove leading zeros from.

    Returns:
        The string with leading zeros removed.
    """
    if len(text) == 1 and text == "0":
        return text

    i = 0
    while i < len(text) and text[i] == "0":
        i += 1

    return text[i:]
