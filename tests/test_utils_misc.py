from os import rmdir, makedirs

from backend.utils.misc import (
    is_field_valid,
    format_database_date,
    format_cep,
    replace_spaces_on_list_tuple,
    replace_invalid_fields_on_list_tuple,
    makedir,
    replace_spaces,
    remove_leading_zeros,
)


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


def test_format_cep():
    """Tests the format_cep function."""

    assert format_cep("12345678") == "12.345-678"
    assert format_cep("invalid_cep") is None
    assert format_cep(12345678.0) == "12.345-678"  # Accepts floats
    assert format_cep("00000000") == "00.000-000"  # Leading zeros


def test_replace_spaces_on_list_tuple():
    """Tests the replace_spaces_on_list_tuple function."""

    data = [("  text  ", "another"), ("  multiple   ", "spaces")]
    expected = [("text", "another"), ("multiple", "spaces")]
    assert replace_spaces_on_list_tuple(data) == expected


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
