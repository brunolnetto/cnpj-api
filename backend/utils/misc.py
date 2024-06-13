from typing import List, Tuple
from os import makedirs, path
from typing import List, Any
import re

from backend.setup.logging import logger

def is_number(text: str) -> bool:
    # Matches digits with an optional decimal part
    pattern = r"^\d+(\.\d+)?$"  
    return bool(re.match(pattern, text))

def is_database_field_valid(field: str) -> bool:
    """
    Checks if a field is valid.
    
    Args:
        field (str): The field to check.
        
    Returns:
        bool: Whether the field is valid.    
    """
    is_nan=str(field).lower() == 'nan'
    is_nat=str(field).lower() == 'nat'
    is_null=str(field).lower() == 'null'
    is_none=str(field).lower() == 'none'
    
    is_invalid=is_nan or is_nat or is_null or is_none
    
    return not is_invalid

# Define a function to format the date
DELIMITER='-'
def format_database_date(date_str: str, delimiter: str = DELIMITER) -> str:
    """
    Formats a date string to the database format.
    
    Args:
        date_str (str): The date string to format.
        delimiter (str): The delimiter to use.
        
    Returns:
        str: The formatted date string.
    """
    date_str=str(date_str)
    if not is_database_field_valid(date_str) or \
        not is_number(date_str) or \
            len(date_str) != 8:
        return None

    return f"{date_str[:4]}{delimiter}{date_str[4:6]}{delimiter}{date_str[6:]}"
    
def format_cep(cep_str: str):
    """
    Formats a CEP string.
    
    Args:
        cep_str (str): The CEP string to format.
        
    Returns:
        str: The formatted CEP string
    """
    cep_str=str(cep_str)
    if not is_number(cep_str):
        return None
    
    # Remove decimal part if it exists
    cep_str=str(int(float(cep_str)))
    cep_str=cep_str.zfill(8)
    
    is_valid_cep=is_database_field_valid(cep_str) and len(cep_str) == 8
    
    if not is_valid_cep:
        return None    
    
    return f"{cep_str[0:2]}.{cep_str[2:5]}-{cep_str[5:8]}"

# Define a function to format the phone number
def format_phone(ddd, phone_num):
    campos_validos=\
        is_database_field_valid(ddd) and \
        is_database_field_valid(phone_num)
    
    if not campos_validos:
        return ""
    
    ddd=str(int(float(ddd)))
    phone_num=str(int(float(phone_num)))
    phone_num=phone_num.zfill(8)

    return f"({ddd}) {phone_num[:4]}-{phone_num[4:]}"

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
    return list(map(lambda row: tuple(map(operation, row)), lst))

def replace_spaces_on_list_tuple(lst: List[Tuple]) -> List[str]:
    """
    Replaces multiple consecutive spaces with a single space.

    Args:
        lst (List): The list to process.

    Returns:
        The list with multiple spaces replaced by a single space.
    """
    clean_spaces_map=lambda el: " ".join(str(el).split())
    return operate_on_list_tuple(lst, clean_spaces_map) 
    

def replace_nan_on_list_tuple(lst: List[Tuple]) -> List[str]:
    """
    Replaces NaN values with empty string.

    Args:
        lst (List): The list to process.

    Returns:
        The list with NaN values replaced by None.
    """
    clean_field_map=lambda el: '' if str(el).lower()=='nan' else el
    return operate_on_list_tuple(lst, clean_field_map) 


def makedir(folder_name: str, is_verbose: bool = False):
    """
    Creates a new directory if it doesn't already exist.

    Args:
        folder_name (str): The name of the folder to create.
        is_verbose (bool, optional): Whether to log verbose information. Defaults to False.
    """
    if not path.exists(folder_name):
        makedirs(folder_name)
        
        if(is_verbose):
            logger.info('Folder: ' + repr(str(folder_name)))

    else:
        if(is_verbose):
            logger.warning(f'Folder {repr(str(folder_name))} already exists!')

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