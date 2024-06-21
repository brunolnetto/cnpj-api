import pandas as pd
import pytest

from backend.app.utils.dataframe import dataframe_to_nested_dict


def test_converts_dataframe_with_existing_index():
    """Tests converting a DataFrame with an existing index."""
    data = {"A": [1, 2, 3], "B": ["a", "b", "c"], "C": [10, 20, 30]}
    df = pd.DataFrame(data).set_index("A")
    expected_result = {
        1: {"B": "a", "C": 10},
        2: {"B": "b", "C": 20},
        3: {"B": "c", "C": 30},
    }

    result = dataframe_to_nested_dict(df)

    assert result == expected_result


def test_converts_dataframe_with_specified_index():
    """Tests converting a DataFrame with a specified index column."""
    data = {"A": [1, 2, 3], "B": ["a", "b", "c"], "C": [10, 20, 30]}
    df = pd.DataFrame(data)
    expected_result = {
        1: {"B": "a", "C": 10},
        2: {"B": "b", "C": 20},
        3: {"B": "c", "C": 30},
    }

    result = dataframe_to_nested_dict(df, index_col="A")

    assert result == expected_result


def test_raises_error_for_missing_index_col():
    """Tests that the function raises an error for a non-existent index column."""
    data = {"A": [1, 2, 3], "B": ["a", "b", "c"], "C": [10, 20, 30]}
    df = pd.DataFrame(data)

    with pytest.raises(ValueError) as excinfo:
        dataframe_to_nested_dict(df, index_col="D")

    assert str(excinfo.value) == "Column 'D' does not exist in the DataFrame."


def test_handles_dataframe_without_index():
    """Tests converting a DataFrame without an existing index."""
    data = {"A": [1, 2, 3], "B": ["a", "b", "c"], "C": [10, 20, 30]}
    df = pd.DataFrame(data)
    expected_result = {
        0: {"A": 1, "B": "a", "C": 10},
        1: {"A": 2, "B": "b", "C": 20},
        2: {"A": 3, "B": "c", "C": 30},
    }

    result = dataframe_to_nested_dict(df)

    assert result == expected_result
