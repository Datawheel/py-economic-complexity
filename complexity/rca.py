import sys
import numpy as np
import pandas as pd

def rca(tbl):
    """ this function return the RCA matrix from a pivot table using a geographic index, columns with the categories to be evaluated and the measurement of the data as values.

    Args:
        tbl (pandas dataframe): pivot table using a geographic index, columns with the categories to be evaluated and the measurement of the data as values.

    Returns:
        rcas (pandas dataframe): RCA matrix with real values.
    """

    # fill missing values with zeros
    tbl = tbl.fillna(0)

    col_sums = tbl.sum(axis=1)
    col_sums = col_sums.values.reshape((len(col_sums), 1))

    rca_numerator = np.divide(tbl, col_sums)
    row_sums = tbl.sum(axis=0)

    total_sum = tbl.sum().sum()
    rca_denominator = row_sums / total_sum
    rcas = rca_numerator / rca_denominator

    # rcas[rcas >= 1] = 1
    # rcas[rcas < 1] = 0

    return rcas
