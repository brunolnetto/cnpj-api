def dataframe_to_nested_dict(df, index_col=None):
    """
    Converts a DataFrame to a dictionary with nested structure.

    Args:
        df (pandas.DataFrame): The DataFrame to convert.
        index_col (str, optional): The column to set as the index. Defaults to "A".

    Returns:
        dict: A dictionary with keys as values from the index column,
            and values as dictionaries containing other columns as key-value pairs.

    Raises:
        ValueError: If the provided index_col doesn't exist in the DataFrame.
    """
    if index_col is not None:
        if index_col not in df.columns:
            raise ValueError(
                f"Column '{index_col}' does not exist in the DataFrame.")

    if index_col is None:
        index_col = df.index

    result = {}

    for index, row in df.set_index(index_col).iterrows():
        # Convert remaining columns to dictionary with row values
        other_cols_dict = row.to_dict()
        # Add the dictionary for this index value to the result
        result[index] = other_cols_dict

    return result
