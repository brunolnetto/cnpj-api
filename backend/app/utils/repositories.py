from typing import List, Optional
from datetime import datetime

from backend.app.utils.misc import are, is_number, is_field_valid


# Define a function to format the date
def format_database_date(date_str_: str, delimiter: str = "/") -> str:
    """
    Formats a date string to the database format.

    Args:
        date_str (str): The date string to format.
        delimiter (str): The delimiter to use.

    Returns:
        str: The formatted date string.
    """
    date_str_ = str(date_str_)
    if not is_field_valid(date_str_) or not is_number(date_str_) or len(date_str_) != 8:
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
    cep_str = str(cep_str)
    is_valid_cep = is_field_valid(cep_str) and is_number(cep_str)

    if not is_valid_cep:
        return ""

    # Remove decimal part if it exists
    cep_str = str(int(float(cep_str)))
    cep_str = cep_str.zfill(8)

    return f"{cep_str[0:2]}.{cep_str[2:5]}-{cep_str[5:8]}"


# Define a function to format the phone number
def format_phone(
    ddd_num: str, phone_num: str, ddd_ldelimiter: tuple = "(", ddd_rdelimiter: tuple = ")",
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
