import pytest

from backend.app.api.models.cnpj import CNPJ


def test_valid_cnpj():
    """
    Tests if a valid CNPJ number is correctly identified.
    """
    valid_cnpj = CNPJ(12345678, 9012, 30)
    validation_result = valid_cnpj.is_valid_dict()
    assert validation_result["is_valid"] is True
    assert validation_result["reason"] == ""
    
def test_cnpj_to_tuple():
    """
    Tests if a valid CNPJ number is correctly identified.
    """
    valid_cnpj = CNPJ(12345678, 9012, 30)
    base, order, digits = valid_cnpj.to_tuple()
    
    assert base == '12345678'
    assert order == '9012'
    assert digits == '30'


def test_cnpj_to_raw():
    """
    Tests if a valid CNPJ number is correctly identified.
    """
    valid_cnpj = CNPJ(12345678, 9012, 30)
    raw_cnpj = valid_cnpj.to_raw()
    
    assert raw_cnpj == '12345678901230'


def test_invalid_length_cnpj():
    """
    Tests if a CNPJ with an invalid length is correctly identified.
    """
    invalid_cnpj = CNPJ("123456789", "9012", "34")
    validation_result = invalid_cnpj.is_valid_dict()
    assert validation_result["is_valid"] is False
    assert validation_result["reason"] == "Invalid length. CNPJ should have 14 digits."


def test_invalid_characters_cnpj():
    """
    Tests if a CNPJ with non-numeric characters is correctly identified.
    """
    with pytest.raises(ValueError):
        CNPJ("123A5678", "9012", "34")

    with pytest.raises(ValueError):
        CNPJ("12345678", "9L12", "34")

    with pytest.raises(ValueError):
        CNPJ("12345678", "9012", "3A")


def test_cnpj_dict():
    """
    Tests if a CNPJ with non-numeric characters is correctly identified.
    """
    cnpj_obj = CNPJ("12345678", "9012", "34")

    cnpj_dict = cnpj_obj.__dict__()

    assert cnpj_dict["basico"] == "12345678"
    assert cnpj_dict["ordem"] == "9012"
    assert cnpj_dict["digitos_verificadores"] == "34"
    assert cnpj_dict["is_valid"] is False
    assert cnpj_dict["reason"] == "Invalid verification digits."


def test_cnpj_repr():
    """
    Tests if a CNPJ with non-numeric characters is correctly identified.
    """
    cnpj_obj = CNPJ("12345678", "9012", "34")

    cnpj_repr = cnpj_obj.__repr__()

    assert cnpj_repr == "12.345.678/9012-34"


def test_invalid_verification_digits():
    """
    Tests if a CNPJ with invalid verification digits is correctly identified.
    """
    invalid_cnpj = CNPJ(
        "14741321", "0001", "80"
    )  # One digit off in the verification code
    validation_result = invalid_cnpj.is_valid_dict()
    assert validation_result["is_valid"] is False
    assert validation_result["reason"] == "Invalid verification digits."


def test_string_representation():
    """
    Tests if the string representation of a CNPJ object is formatted correctly.
    """
    valid_cnpj = CNPJ("14741321", "0001", "81")
    expected_string = "14.741.321/0001-81"
    assert str(valid_cnpj) == expected_string
