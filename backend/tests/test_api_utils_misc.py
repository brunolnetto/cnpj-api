import pytest

import re

from backend.app.api.utils.misc import (
    check_limit_and_offset,
    convert_to_bytes,
    build_condition,
    zfill_factory,
    paginate_dict,
    remove_quotes,
    normalize_json,
    comma_stringify_list,
    commify_list,
    MAX_LIMIT,
)


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
    assert convert_to_bytes("invalid_size") == 0
    assert convert_to_bytes("10") == 0  # Missing unit


def test_convert_to_bytes_empty_string():
    assert convert_to_bytes("") == 0


@pytest.mark.parametrize(
    "column, value, condition_type, array_condition, expected",
    [
        ("age", "30", "eq", False, "age='30'"),
        ("price", "100", "gt", False, "price>'100'"),
        ("salary", "5000", "ge", False, "salary>='5000'"),
        ("score", "75", "lt", False, "score<'75'"),
        ("height", "180", "le", False, "height<='180'"),
        ("tags", "'Python'", "contains", True, "tags @> Array['Python']"),
        ("username", "", "eq", False, "1=1"),  # Empty value should return "1=1"
        ("username", None, "eq", False, "1=1"),  # None should return "1=1"
        ("status", "active", "unknown", False, "1=1"),  # Unknown condition should return "1=1"
    ],
)
def test_build_condition(column, value, condition_type, array_condition, expected):
    assert build_condition(column, value, condition_type, array_condition) == expected

def test_zfill_factory():
    # Create different zfill functions using the factory
    zfill_5 = zfill_factory(5)
    zfill_10 = zfill_factory(10)
    
    # Test zfill with length 5
    assert zfill_5("123") == "00123"  # 3 digits, fill with 2 leading zeros
    assert zfill_5("98765") == "98765"  # Already the right length
    assert zfill_5("1") == "00001"  # 1 digit, fill with 4 leading zeros

    # Test zfill with length 10
    assert zfill_10("123") == "0000000123"  # 3 digits, fill with 7 leading zeros
    assert zfill_10("hello") == "00000hello"  # String of length 5, fill with 5 leading zeros
    assert zfill_10("1234567890") == "1234567890"  # Already the right length
    
    # Test non-string input (this can be adjusted depending on your needs)
    assert zfill_5(123) == "00123"  # Integer input should be converted to string and padded
    assert zfill_5(3.14) == "03.14"  # Float input should be converted to string and padded

    # Test edge case of empty string
    assert zfill_5("") == "00000"  # Empty string, should return 5 leading zeros

    # Test with larger numbers
    assert zfill_10("12345678901234567890") == "12345678901234567890"  # String longer than 10 should not change

@pytest.mark.parametrize(
    "n, value, expected",
    [
        (5, "123", "00123"),
        (5, "98765", "98765"),
        (5, "1", "00001"),
        (10, "123", "0000000123"),
        (10, "hello", "00000hello"),
        (10, "1234567890", "1234567890"),
    ],
)
def test_zfill_parametrized(n, value, expected):
    zfill = zfill_factory(n)
    assert zfill(value) == expected

def test_remove_quotes():
    # Test with single quotes
    assert remove_quotes("'hello'") == "hello"
    assert remove_quotes("this is a 'quote'") == "this is a quote"
    
    # Test with double quotes
    assert remove_quotes('"hello"') == "hello"
    assert remove_quotes('this is a "quote"') == 'this is a quote'
    
    # Test with both single and double quotes
    assert remove_quotes("'hello' and \"world\"") == "hello and world"
    
    # Test with text containing no quotes
    assert remove_quotes("hello world") == "hello world"
    
    # Test with empty string
    assert remove_quotes("") == ""

def test_normalize_json():
    # Test that single quotes are replaced by double quotes
    assert normalize_json("{'name': 'John'}") == '{"name": "John"}'
    assert normalize_json("{'age': 30, 'city': 'New York'}") == '{"age": 30, "city": "New York"}'
    
    # Test no change when already using double quotes
    assert normalize_json('{"name": "John"}') == '{"name": "John"}'
    
    # Test with escaped quotes
    assert normalize_json(r"{'name': 'John', 'quote': 'He said, \"hello!\"'}") == r'{"name": "John", "quote": "He said, \"hello!\""}'
    
    # Test an empty string
    assert normalize_json("") == ""
    
    # Test that only non-escaped single quotes are replaced
    assert normalize_json(r"({'name': 'John'})") == r'({"name": "John"})'

def test_comma_stringify_list():
    # Test with simple list of integers
    assert comma_stringify_list([1, 2, 3]) == "'1','2','3'"
    
    # Test with strings
    assert comma_stringify_list(["apple", "banana", "cherry"]) == "'apple','banana','cherry'"
    
    # Test with mixed types
    assert comma_stringify_list([1, "apple", 3.14, True]) == "'1','apple','3.14','True'"
    
    # Test with an empty list
    assert comma_stringify_list([]) == ""
    
    # Test with single item list
    assert comma_stringify_list([5]) == "'5'"
    
    # Test with boolean values
    assert comma_stringify_list([True, False]) == "'True','False'"
    
    # Test with floating point numbers
    assert comma_stringify_list([1.1, 2.2, 3.3]) == "'1.1','2.2','3.3'"

def test_comma_stringify_list():
    # Test with simple list of integers
    assert comma_stringify_list([1, 2, 3]) == "'1','2','3'"
    
    # Test with strings
    assert comma_stringify_list(["apple", "banana", "cherry"]) == "'apple','banana','cherry'"
    
    # Test with mixed types
    assert comma_stringify_list([1, "apple", 3.14, True]) == "'1','apple','3.14','True'"
    
    # Test with an empty list
    assert comma_stringify_list([]) == ""
    
    # Test with single item list
    assert comma_stringify_list([5]) == "'5'"
    
    # Test with boolean values
    assert comma_stringify_list([True, False]) == "'True','False'"
    
    # Test with floating point numbers
    assert comma_stringify_list([1.1, 2.2, 3.3]) == "'1.1','2.2','3.3'"


def test_paginate_dict():
    data_dict = {f"key{i}": i for i in range(1, 21)}  # {key1: 1, key2: 2, ..., key20: 20}
    
    # Test for valid pagination
    assert len(paginate_dict(data_dict, 5, 0)) == 5
    assert len(paginate_dict(data_dict, 5, 1)) == 5
    assert len(paginate_dict(data_dict, 5, 2)) == 5
    
    # Test with a page that exceeds available pages (empty result)
    assert paginate_dict(data_dict, 5, 10) == {}
    
    # Test with a single page and smaller page size
    assert len(paginate_dict(data_dict, 2, 0)) == 2
    
    # Test with data smaller than page size (returns all data)
    assert len(paginate_dict(data_dict, 25, 0)) == len(data_dict)  

    # Test with page_number = 1, different page_size
    assert len(paginate_dict(data_dict, 3, 1)) == 3

    # Test empty dictionary
    assert paginate_dict({}, 5, 1) == {}

    # Test pagination with large page size (larger than the dictionary size)
    assert len(paginate_dict(data_dict, 50, 0)) == len(data_dict)
    
    # Dataset with nested dictionaries for sorting
    data_dict_nested = {
        "a": {"sort_value": 10},
        "b": {"sort_value": 5},
        "c": {"sort_value": 15},
        "d": {"sort_value": 1},
        "e": {"sort_value": 7}
    }

    # Test sorting by 'sort_value'
    sorted_page = paginate_dict(data_dict_nested, page_size=2, page_number=0, sort_by="sort_value")
    sorted_keys = list(sorted_page.keys())

    # The first two elements should be sorted in ascending order of "sort_value"
    assert sorted_keys == ["d", "b"]

    # Test sorting with page 1
    sorted_page_2 = paginate_dict(data_dict_nested, page_size=2, page_number=1, sort_by="sort_value")
    sorted_keys_2 = list(sorted_page_2.keys())

    assert sorted_keys_2 == ["e", "a"]

    # Test sorting with page 2 (last remaining element)
    sorted_page_3 = paginate_dict(data_dict_nested, page_size=2, page_number=2, sort_by="sort_value")
    sorted_keys_3 = list(sorted_page_3.keys())

    assert sorted_keys_3 == ["c"]

    # Test sorting with a non-existent key (should return unsorted)
    unsorted_page = paginate_dict(data_dict_nested, page_size=2, page_number=0, sort_by="non_existent")
    assert set(unsorted_page.keys()) == {"a", "b"}  # Since sorting fails, it keeps original order


def test_commify_list():
    assert commify_list([1, 2, 3]) == "1,2,3"
    assert commify_list(["apple", "banana", "cherry"]) == "apple,banana,cherry"
    assert commify_list([1, "apple", 3.14, True]) == "1,apple,3.14,True"
    assert commify_list([]) == ""
    assert commify_list([5]) == "5"
    assert commify_list([True, False]) == "True,False"
