import pytest

from backend.app.api.utils.misc import check_limit_and_offset, convert_to_bytes, MAX_LIMIT

def test_check_limit_and_offset_valid():
    limit, offset = check_limit_and_offset(20, 5)
    assert limit == 20
    assert offset == 5


def test_check_limit_and_offset_max_limit():
    limit, offset = check_limit_and_offset(MAX_LIMIT + 1, 5)
    assert limit == MAX_LIMIT
    assert offset == 5


def test_check_limit_and_offset_negative_limit():
    with pytest.raises(ValueError) as excinfo:
        check_limit_and_offset(-1, 5)

    assert "Limit must be positive" in str(excinfo.value)


def test_check_limit_and_offset_negative_offset():
    with pytest.raises(ValueError) as excinfo:
        check_limit_and_offset(10, -2)

    assert "Offset must be non-negative" in str(excinfo.value)


def test_convert_to_bytes_valid_cases():
    assert convert_to_bytes("10K") == 10240
    assert convert_to_bytes("2.5M") == int(2.5 * 1024**2)
    assert convert_to_bytes("1G") == 1024**3


def test_convert_to_bytes_invalid_unit():
    assert convert_to_bytes("10T") == 10995116277760


def test_convert_to_bytes_invalid_format():
    assert convert_to_bytes("invalid_size") is None
    assert convert_to_bytes("10") is None  # Missing unit


def test_convert_to_bytes_empty_string():
    assert convert_to_bytes("") is None
