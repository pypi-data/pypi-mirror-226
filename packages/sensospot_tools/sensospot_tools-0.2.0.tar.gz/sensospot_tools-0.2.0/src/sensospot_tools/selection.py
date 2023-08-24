from __future__ import annotations

from typing import Any, Iterator

import pandas


def select(
    data: pandas.DataFrame, column: str, value: Any
) -> pandas.DataFrame:
    """Selects rows of a dataframe based on a value in a column

    Examples:
        >>> print(data)
          category  value
        0      dog      1
        1      cat      2
        2    horse      3
        3      cat      4
        >>> print(select(data, "category", "cat"))
          category  value
        1      cat      2
        3      cat      4


    Args:
        data:    a data DataFrame to select from
        column:  name of a column in a dataframe
        value:   rows with this value in the column will be selected

    Returns:
        a copy of the DataFrame that has the value in the column
    """
    selector = data[column] == value
    return data.loc[selector].copy()


def split(
    data: pandas.DataFrame, *on: tuple[Any]
) -> Iterator[tuple[Any, pandas.DataFrame]]:
    """Splits a data frame on unique values in columns

    Returns a generator of tuples with at least two elements.
    The _last_ element is the resulting partial data frame,
    the element(s) before are the values used to split up the original data.

    Examples:

        >>> print(data)
          category  value
        0      dog      1
        1      cat      2
        2    horse      3
        3      cat      4
        >>> result = dict( split(data, column="category") )
        >>> print(result["dog"])
          category  value
        0      dog      1
        >>> print(result["cat"])
          category  value
        1      cat      2
        3      cat      4
        >>> print(result["horse"])
          category  value
        2    horse      3


        >>> for well, pos, partial in split_uniques(full_data, "Well", "Pos"):
            # `well` is one of the unique values in full_data["Well"]
            # `pos` is one of the unique values in full_data["Pos"]
            # `parital` is a slice of full_data for this well and pos

    Args:
        data:   DataFrame to process
        *on:    one or multiple column identifiers to split on unique values
    Yields:
        a tuple with the unique values as key(s) and the resulting data frame
        as last object
    """
    yield from _iter_uniques(data, *on)


def _iter_uniques(
    data: pandas.DataFrame,
    *on: tuple[Any],
    _prev_values: None | tuple[Any] = None,
) -> tuple[Any, ..., pandas.DataFrame]:
    """Splits a data frame on uniques values in a column

    Returns a generator of tuples with at least two elements.
    The _last_ element is the resulting partial data frame,
    the element(s) before are the values used to split up the original data.

    Example:

      >>> for well, pos, partial in split_uniques(full_data, "Well", "Pos"):
          # `well` is one of the unique values in full_data["Well"]
          # `pos` is one of the unique values in full_data["Pos"]
          # `parital` is a slice of full_data for this well and pos

    Args:
        data:         pandas DataFrame to process
        *on:          one or multiple column names to split on unique values
        _prev_values: cache of unique values for recursion
    Yields:
        a tuple with the unique values as key(s) and the resulting data frame
        as last object
    """
    if _prev_values is None:
        _prev_values = ()
    current_column, *rest = on
    for current_value in data[current_column].unique():
        selected = select(data, current_column, current_value)
        values = (*_prev_values, current_value)
        if rest:
            yield from _iter_uniques(selected, *rest, _prev_values=values)
        else:
            yield *values, selected
