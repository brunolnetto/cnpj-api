from json import JSONDecodeError
from unittest.mock import patch

import pytest

from backend.app.utils.misc import (
    is_field_valid,
    replace_spaces_on_list_tuple,
    replace_invalid_fields_on_list_tuple,
    replace_invalid_fields_on_list_dict,
    replace_spaces,
    remove_leading_zeros,
    is_number,
    are_numbers,
    format_decimal,
    string_to_json,
    humanize_string,
    date_str,
    time_str,
    are_positive,
    are_non_negative,
    are_negative,
    are_non_positive,
    number_string_to_number,
)


def test_are_positive():
    """Tests the are_positive function."""
    assert are_positive([1, 2, 3, 4, 5])
    assert not are_positive([1, 2, 3, 4, -5])
    assert not are_positive([-1, 2, 3, 4, 5])
    assert not are_positive([1, 2, 3, 4, 0])
    assert not are_positive([1, 2, 3, 4, 0])


def test_are_non_negative():
    """Tests the are_non_negative function."""
    assert are_non_negative([1, 2, 3, 4, 5])
    assert not are_non_negative([1, 2, 3, 4, -5])
    assert not are_non_negative([-1, 2, 3, 4, 5])
    assert are_non_negative([1, 2, 3, 4, 0])


def test_are_negative():
    """Tests the are_negative function."""
    assert not are_negative([1, 2, 3, 4, 5])
    assert are_negative([-1, -2, -3, -4, -5])
    assert not are_negative([1, 2, 3, 4, 0])


def test_are_non_positive():
    """Tests the are_non_positive function."""
    assert are_non_positive([-1, -2, -3, -4, -5])
    assert not are_non_positive([1, 2, 3, 4, 5])
    assert not are_non_positive([-1, 2, 3, 4, 5])
    assert are_non_positive([-1, -2, -3, -4, 0])


def test_date_str():
    """Tests the date_str function."""
    with patch("backend.app.utils.misc.datetime") as mock_datetime:
        mock_datetime.now().strftime.return_value = "2024-06-13"
        assert date_str() == "2024-06-13"


def test_time_str():
    """Tests the time_str function."""
    with patch("backend.app.utils.misc.datetime") as mock_datetime:
        mock_datetime.now().strftime.return_value = "12:34:56"
        assert time_str() == "12:34:56"


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
    decimal_number = "3.14159"
    formatted_number = format_decimal(decimal_number)
    assert formatted_number == "3.14"


def test_format_decimal_custom_decimal_places():
    """Tests the format_decimal function with a custom number of decimal places."""
    decimal_number = "3.14159"
    formatted_number = format_decimal(decimal_number, 3)
    assert formatted_number == "3.142"


def test_string_to_json_valid_string():
    """Tests the string_to_json function with a valid JSON string."""
    valid_string = '{"key": "value"}'
    json_data = string_to_json(valid_string)
    assert json_data == {"key": "value"}


def test_string_to_json_invalid_json():
    """
    Tests the string_to_json function with an invalid JSON string
    (raises json.JSONDecodeError).
    """
    invalid_string = '{"key": "value" unbalanced'
    with pytest.raises(JSONDecodeError):
        string_to_json(invalid_string)


def test_string_to_json_empty_string():
    """Tests the string_to_json function with an empty string."""
    empty_string = ""
    with pytest.raises(JSONDecodeError):
        string_to_json(empty_string)


def test_humanize_string_basic():
    assert (
        humanize_string("QUADRA101 SALA03 SALA04 LOTE0016")
        == "Quadra 101 Sala 3 Sala 4 Lote 16"
    )


def test_humanize_string_no_numbers():
    assert humanize_string("QUADRA SALA LOTE") == "Quadra Sala Lote"


def test_humanize_string_only_numbers():
    assert humanize_string("101 03 04 0016") == "101 3 4 16"


def test_humanize_string_mixed_case():
    assert (
        humanize_string("Quadra101 SaLa03 sala04 lotE0016")
        == "Quadra 101 Sala 3 Sala 4 Lote 16"
    )


def test_humanize_string_multiple_spaces():
    assert (
        humanize_string("QUADRA  101   SALA  03  SALA   04  LOTE  0016")
        == "Quadra 101 Sala 3 Sala 4 Lote 16"
    )


def test_humanize_string_leading_zeros():
    assert humanize_string("LOTE00016") == "Lote 16"


def test_humanize_string_no_trailing_dot():
    assert humanize_string("Quadra101") == "Quadra 101"


def test_humanize_string_already_has_dot():
    assert humanize_string("Quadra101.") == "Quadra 101."


def test_humanize_string_empty_string():
    assert humanize_string("") == ""


def test_humanize_string_special_characters():
    assert humanize_string("QUADRA#101") == "Quadra# 101"


def test_converts_valid_float_string_to_int():
    """Tests conversion of a valid float string to an integer."""
    assert number_string_to_number("10.0") == 10


def test_converts_positive_float_string_to_int():
    """Tests conversion of a positive float string to an integer."""
    assert number_string_to_number("12.34") == 12.34


def test_converts_negative_float_string_to_int():
    """Tests conversion of a negative float string to an integer."""
    assert number_string_to_number("-5") == -5


def test_handles_zero_float_string():
    """Tests conversion of a zero float string."""
    assert number_string_to_number("0.0") == 0


def test_returns_float_for_non_zero_remainder():
    """Tests that the function returns a float for non-zero remainders."""
    assert number_string_to_number("12.5") == 12.5


def test_raises_error_for_non_numeric_string():
    """Tests that the function raises an error for non-numeric strings."""
    with pytest.raises(ValueError):
        number_string_to_number("abc")


def test_raises_error_for_empty_string():
    """Tests that the function raises an error for an empty string."""
    with pytest.raises(ValueError):
        number_string_to_number("")


def test_empty_list_all_numbers_strict():
    """Tests if an empty list returns True with strict type checking."""
    assert are_numbers([], is_strict=True)


def test_empty_list_all_numbers_non_strict():
    """Tests if an empty list returns True with non-strict type checking."""
    assert are_numbers([])


def test_list_of_integers_strict():
    """Tests if a list of integers returns True with strict type checking."""
    assert are_numbers([1, 2, 3], is_strict=True)


def test_list_of_integers_non_strict():
    """Tests if a list of integers returns True with non-strict type checking."""
    assert are_numbers([1, 2, 3])


def test_list_of_floats_strict():
    """Tests if a list of floats returns True with strict type checking."""
    assert are_numbers([1.5, 2.25, 3.14], is_strict=True)


def test_list_of_floats_non_strict():
    """Tests if a list of floats returns True with non-strict type checking."""
    assert are_numbers([1.5, 2.25, 3.14])


def test_list_of_mixed_numbers_strict():
    """Tests if a list of mixed numbers returns True with strict type checking."""
    assert are_numbers([1, 2.5, 3], is_strict=True)


def test_list_of_mixed_numbers_non_strict():
    """Tests if a list of mixed numbers returns True with non-strict type checking."""
    assert are_numbers([1, 2.5, 3])


def test_list_with_strings_strict():
    """Tests if a list with strings returns False with strict type checking."""
    assert not are_numbers(["abc", "def", "ghi"], is_strict=True)


def test_list_with_strings_non_strict():
    """
    Tests if a list with strings returns False with non-strict type checking
    (for non-numeric strings).
    """
    assert not are_numbers(["abc", "123", "def"], is_strict=False)


def test_list_with_empty_strings_non_strict():
    """Tests if a list with empty strings returns False with non-strict type checking."""
    assert not are_numbers(["", "123", ""], is_strict=False)


def test_list_with_non_numeric_strings_non_strict():
    """Tests if a list with non-numeric strings returns False with non-strict type checking."""
    assert not are_numbers(["abc", "def", "xyz"], is_strict=False)


def test_list_with_numeric_strings_non_strict():
    """Tests if a list with numeric strings returns True with non-strict type checking."""
    assert are_numbers(["123", "456", "789"], is_strict=False)


def test_list_with_none_values():
    """Tests if a list with None values returns False."""
    assert not are_numbers([1, None, 3], is_strict=True)
    assert not are_numbers([1, None, 3], is_strict=False)


def test_list_with_booleans():
    """Tests if a list with booleans returns False."""
    assert not are_numbers([True, False, 1], is_strict=True)
    assert not are_numbers([True, False, 1], is_strict=False)
