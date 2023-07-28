"""Revealed Comparative Advantage (RCA) module

The Revealed Comparative Advantage is an index introduced by Balassa (1965),
which is used to evaluate the main products to be exported by a country,
and their comparative advantages in relation to the level of world exports
(Hidalgo et al., 2007).
"""

import numpy as np
import pandas as pd


def rca(tbl: pd.DataFrame) -> pd.DataFrame:
    """Calculates the Revealed Comparative Advantage (RCA) for a pivoted matrix.

    It is important to note that even though the functions do not use a
    parameter in relation to time, the data used for the calculations must
    be per period; for example working with World Exports for the year 2020.
    Also, the index always has to be a geographic level.

    Arguments:
        tbl (pandas.DataFrame) -- A pivoted table using a geographic index,
            columns with the categories to be evaluated and the measurement of
            the data as values.

    Returns:
        (pandas.DataFrame) -- RCA matrix with real values.
    """
    # fill missing values with zeros
    tbl = tbl.fillna(value=0)

    col_sums = tbl.sum(axis=1) # 1:columns
    col_sums = col_sums.to_numpy().reshape((len(col_sums), 1))

    rca_numerator = np.divide(tbl, col_sums)
    row_sums = tbl.sum(axis=0) # 0:index

    total_sum = tbl.sum().sum()
    rca_denominator = row_sums / total_sum
    rcas = rca_numerator / rca_denominator

    return rcas
