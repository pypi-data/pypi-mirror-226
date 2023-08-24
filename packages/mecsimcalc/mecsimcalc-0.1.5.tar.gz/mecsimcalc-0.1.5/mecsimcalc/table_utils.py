import pandas as pd
from typing import List


def table_to_dataframe(
    column_headers: List[str], rows: List[List[str]]
) -> pd.DataFrame:
    """
    >>> table_to_dataframe(column_headers: List[str], rows: List[List[str]]) -> pd.DataFrame

    Create a DataFrame from given rows and column headers

    # Parameters

    column_headers : List[str]
        List of column headers.
    rows : List[List[str]]
        List of rows to be converted into a DataFrame. Each row is a list of strings.

    # Raises

    * `ValueError` :
        If length of rows is not equal to length of column headers.

    # Returns

    * `pd.DataFrame` :
        DataFrame constructed from rows and headers.

    # Example
    >>> column_headers = ["A", "B", "C"]
    >>> rows = [["1", "2", "3"], ["4", "5", "6"]]
    >>> df = msc.table_to_dataframe(column_headers, rows)
    >>> print(df)
       A  B  C
    0  1  2  3
    1  4  5  6

    """
    for row in rows:
        if len(row) != len(column_headers):
            raise ValueError("Each row must have the same length as the column headers")

    return pd.DataFrame(rows, columns=column_headers)


def print_table(
    column_headers: List[str], rows: List[List[str]], index: bool = True
) -> str:
    """
    >>> print_table(column_headers: List[str], rows: List[List[str]]) -> str

    Create an HTML table from given rows and column headers.

    # Parameters

    column_headers : List[str]
        The header for each column.
    rows : List[List[str]]
        A list of rows (each row is a list of strings).
    index : bool
        Whether to use the first column as the DataFrame's index. (Defaults to True)

    # Returns

    * `str` :
        HTML table.

    # Example
    >>> column_headers = ["A", "B", "C"]
    >>> rows = [["1", "2", "3"], ["4", "5", "6"]]
    >>> table = msc.print_table(column_headers, rows)
    >>> return {
        "table": table
    }
    """

    df = table_to_dataframe(column_headers, rows)
    return df.to_html(index=index, border=1, escape=True)
