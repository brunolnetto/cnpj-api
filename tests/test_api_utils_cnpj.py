import pytest

from backend.api.utils.cnpj import (
  is_cnpj_str_valid, 
  parse_cnpj_str, 
  format_cnpj,
  calculate_cnpj_verification_digits,
)

def test_calculate_cnpj_verification_digits_valid_cnpj():
  """Tests the calculate_cnpj_verification_digits function with a valid CNPJ."""
  valid_cnpj = "12345678901234"
  digit1, digit2 = calculate_cnpj_verification_digits(valid_cnpj)
  assert digit1 == 3
  assert digit2 == 0

def test_calculate_cnpj_verification_digits_invalid_length_cnpj():
  """Tests the calculate_cnpj_verification_digits function with an invalid length CNPJ."""
  invalid_cnpj = "1234567890123"  # Missing last digit
  with pytest.raises(ValueError):
    calculate_cnpj_verification_digits(invalid_cnpj)

def test_calculate_cnpj_verification_digits_non_numeric_cnpj():
  """Tests the calculate_cnpj_verification_digits function with a CNPJ containing non-numeric characters."""
  invalid_cnpj = "12345a678901234"
  with pytest.raises(ValueError):
    calculate_cnpj_verification_digits(invalid_cnpj)

def test_calculate_cnpj_verification_digits_custom_cnpj():
  """Tests the calculate_cnpj_verification_digits function with a custom CNPJ and expected digits."""
  custom_cnpj = "34111019000191"
  expected_digit1, expected_digit2 = 2, 4
  digit1, digit2 = calculate_cnpj_verification_digits(custom_cnpj)
  assert digit1 == expected_digit1
  assert digit2 == expected_digit2

def test_is_cnpj_str_valid_valid_cnpj():
  """Tests the is_cnpj_str_valid function with a valid CNPJ."""
  valid_cnpj = "12345678901230"
  validation_result = is_cnpj_str_valid(valid_cnpj)
  assert validation_result['is_valid'] is True
  assert validation_result['reason'] == ''

def test_is_cnpj_str_valid_invalid_length():
  """Tests the is_cnpj_str_valid function with an invalid length CNPJ."""
  invalid_cnpj = "123456789012345"
  validation_result = is_cnpj_str_valid(invalid_cnpj)
  assert validation_result['is_valid'] is False
  assert validation_result['reason'] == 'Invalid length. CNPJ should have 14 digits.'

def test_is_cnpj_str_valid_non_numeric():
  """Tests the is_cnpj_str_valid function with a CNPJ containing non-numeric characters."""
  invalid_cnpj = "12345678901a34"
  validation_result = is_cnpj_str_valid(invalid_cnpj)
  assert validation_result['is_valid'] is False
  assert validation_result['reason'] == 'CNPJ contains non-numeric characters.'

def test_is_cnpj_str_valid_invalid_verification_digits():
  """Tests the is_cnpj_str_valid function with a CNPJ with invalid verification digits."""
  invalid_cnpj = "12345678901234"
  validation_result = is_cnpj_str_valid(invalid_cnpj)
  assert validation_result['is_valid'] is False
  assert validation_result['reason'] == 'Invalid verification digits.'

def test_parse_cnpj_str_valid_cnpj():
  """Tests the parse_cnpj_str function with a valid CNPJ."""
  valid_cnpj = "12345678901230"
  parsed_cnpj = parse_cnpj_str(valid_cnpj)
  assert parsed_cnpj == ["12345678", "9012", "30"]

def test_parse_cnpj_str_invalid_cnpj():
  """Tests the parse_cnpj_str function with an invalid CNPJ (raises ValueError)."""
  invalid_cnpj = "12345a78901234"
  with pytest.raises(ValueError) as e:
    parse_cnpj_str(invalid_cnpj)
  assert str(e.value) == 'CNPJ contains non-numeric characters.'

def test_format_cnpj_valid_cnpj():
  """Tests the format_cnpj function with a valid CNPJ."""
  valid_cnpj = "12345678901230"
  formatted_cnpj = format_cnpj(valid_cnpj)
  assert formatted_cnpj == "12.345.678/9012-30"

def test_format_cnpj_invalid_cnpj():
  """Tests the format_cnpj function with an invalid CNPJ (raises ValueError)."""
  invalid_cnpj = "12345a78901234"
  with pytest.raises(ValueError) as e:
    format_cnpj(invalid_cnpj)
  assert str(e.value) == 'CNPJ contains non-numeric characters.'

