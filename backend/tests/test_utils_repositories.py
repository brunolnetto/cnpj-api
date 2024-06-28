from backend.app.utils.repositories import (
    format_database_date,
    format_phone,
    format_cep,
)

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
    assert (
        format_phone(
            "12", "34567890", ddd_rdelimiter="", ddd_ldelimiter="", phone_delimiter=""
        )
        == "12 34567890"
    )

    assert format_phone("nan", "invalid_phone") == ""


def test_format_cep():
    """Tests the format_cep function."""

    assert format_cep("12345678") == "12.345-678"
    assert format_cep(12345678.0) == "12.345-678"  # Accepts floats
    assert format_cep("00000000") == "00.000-000"  # Leading zeros
    assert format_cep("invalid_cep") == ""
