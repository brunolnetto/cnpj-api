from os import rmdir, makedirs
import pytest
import json
from json import JSONDecodeError

from backend.utils.misc import (
    is_field_valid,
    format_database_date,
    format_cep,
    format_phone,
    replace_spaces_on_list_tuple,
    replace_invalid_fields_on_list_tuple,
    replace_invalid_fields_on_list_dict,
    makedir,
    replace_spaces,
    remove_leading_zeros,
    is_number,
    format_decimal,
    string_to_json,
)

def test_is_number():
    """Tests the is_number function."""

    # Valid numbers (should return True)
    assert is_number("0")
    assert is_number("0.0")
    assert is_number("0.123")

    # Invalid numbers (should return False)
    assert not is_number("invalid_number")
    assert not is_number("0.")
    assert not is_number("0.0.0")


def test_is_database_field_valid():
    """Tests the is_database_field_valid function."""

    # Valid fields (should return True)
    assert is_field_valid("valid_data")
    assert is_field_valid("0")  # Numbers are considered valid

    # Invalid fields (should return False)
    assert not is_field_valid(None)
    assert not is_field_valid("nan")
    assert not is_field_valid("NaT")  # Case-insensitive
    assert not is_field_valid("NULL")
    assert not is_field_valid("None")  # Case-insensitive

def test_format_database_date():
    """Tests the format_database_date function."""

    assert format_database_date("20240613") == "13/06/2024"
    assert format_database_date("invalid_date") is None
    assert format_database_date("20240613", delimiter="/") == "13/06/2024"

def test_format_phone():
    """Tests the format_phone function."""

    assert format_phone("12", "34567890") == "(12) 3456-7890"
    assert format_phone("12", "34567890", ddd_ldelimiter="") == "12) 3456-7890"
    assert format_phone("12", "34567890", ddd_rdelimiter="") == "(12 3456-7890"
    assert format_phone("12", "34567890", phone_delimiter="") == "(12) 34567890"
    assert format_phone(
        "12", "34567890", 
        ddd_rdelimiter="",
        ddd_ldelimiter="", 
        phone_delimiter=""
    ) == "12 34567890"

    assert format_phone("nan", "invalid_phone") == ""


def test_format_cep():
    """Tests the format_cep function."""

    assert format_cep("12345678") == "12.345-678"
    assert format_cep(12345678.0) == "12.345-678"  # Accepts floats
    assert format_cep("00000000") == "00.000-000"  # Leading zeros
    assert format_cep("invalid_cep") == ""

def test_replace_spaces_on_list_tuple():
    """Tests the replace_spaces_on_list_tuple function."""

    data = [("  text  ", "another"), ("  multiple   ", "spaces")]
    expected = [("text", "another"), ("multiple", "spaces")]
    assert replace_spaces_on_list_tuple(data) == expected

def test_replace_invalid_fields_on_list_dict():
    """Tests the replace_invalid_fields_on_list_dict function."""

    data = [
        {"valid": "data", "invalid": "nan"},
        {"valid": "data", "invalid": "NaT"},
        {"valid": "data", "invalid": "NULL"},
        {"valid": "data", "invalid": "None"},
    ]
    expected = [
        {"valid": "data", "invalid": ""},
        {"valid": "data", "invalid": ""},
        {"valid": "data", "invalid": ""},
        {"valid": "data", "invalid": ""},
    ]

    assert replace_invalid_fields_on_list_dict(data) == expected


def test_replace_nan_on_list_tuple():
    """Tests the replace_nan_on_list_tuple function."""

    data = [("valid", "data"), ("nan", "value"), ("", "empty")]
    expected = [("valid", "data"), ("", "value"), ("", "empty")]
    assert replace_invalid_fields_on_list_tuple(data) == expected


# Test with pytest.mock
def test_makedir(mocker):
    # Mock logger methods
    mocker.patch('backend.setup.logging.logger.info')
    mocker.patch('backend.setup.logging.logger.warning')

    # Test case 1: Folder created (no warning)
    folder_name = "new_folder"
    makedir(folder_name, is_verbose=True)
    rmdir(folder_name)
    
    # Assert logger.info was called with the correct message
    from backend.setup.logging import logger 

    assert logger.info.call_count == 1
    assert logger.info.call_args[0][0] == f"Folder: '{folder_name}'"

    # Test case 2: Folder already exists (warning)
    folder_name = "existing_folder"
    makedirs(folder_name, exist_ok=True)  # Create the folder for the test
    makedir(folder_name, is_verbose=True)

    # Assert logger.warning was called
    assert logger.warning.call_count == 1
    assert logger.warning.call_args[0][0] == f"Folder '{folder_name}' already exists!"

    # Clean up (optional)
    rmdir(folder_name)  # Remove the created folder



def test_replace_spaces():
    """Tests the replace_spaces function."""

    assert replace_spaces("  multiple  spaces  ") == "multiple spaces"
    assert replace_spaces("no spaces") == "no spaces"


def test_remove_leading_zeros():
    """Tests the remove_leading_zeros function."""

    assert remove_leading_zeros("00123") == "123"
    assert remove_leading_zeros("no leading zeros") == "no leading zeros"
    assert remove_leading_zeros("0") == "0"  # Handles single zero

def test_format_decimal_default_decimal_places():
  """Tests the format_decimal function with a default number of decimal places."""
  decimal_number = '3.14159'
  formatted_number = format_decimal(decimal_number)
  assert formatted_number == '3.14'

def test_format_decimal_custom_decimal_places():
  """Tests the format_decimal function with a custom number of decimal places."""
  decimal_number = '3.14159'
  formatted_number = format_decimal(decimal_number, 3)
  assert formatted_number == '3.142'

def test_string_to_json_valid_string():
  """Tests the string_to_json function with a valid JSON string."""
  valid_string = '{"key": "value"}'
  json_data = string_to_json(valid_string)
  assert json_data == {'key': 'value'}

def test_string_to_json_invalid_json():
  """Tests the string_to_json function with an invalid JSON string (raises json.JSONDecodeError)."""
  invalid_string = '{"key": "value" unbalanced'
  with pytest.raises(JSONDecodeError):
    string_to_json(invalid_string)

def test_string_to_json_empty_string():
  """Tests the string_to_json function with an empty string."""
  empty_string = ''
  with pytest.raises(JSONDecodeError):
    string_to_json(empty_string)

