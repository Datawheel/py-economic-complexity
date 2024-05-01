import numpy as np
import pandas as pd


def pmi(
    tbl: pd.DataFrame,
    rcas: pd.DataFrame,
    measure: pd.DataFrame,
    *,
    cutoff: float = 1,
) -> pd.DataFrame:
    """Calculates the Product 'measure' Index.

    In this case 'measure' corresponds to a DataFrame with the measure values
    for each geography.

    In the literature this method has been applied to calculate the Product Gini
    Index (PGI) and the Product Emission Intensity Index (PEII).

    ### Args:
    * tbl (pd.DataFrame) -- A pivoted table using a geographic index, columns with the categories to be evaluated, and the measurement of the data as values.
    * rcas (pd.DataFrame) -- The RCA calculation obtained from the `tbl` data.
    * measure (pd.DataFrame) -- A table using a geographic index, with a single column with the measure values.

    ### Keyword Args:
    * cutoff (float, optional) -- Set the cutoff threshold value for the RCA matrix.
        Internally, RCA values under it will be set to zero, one otherwise.
        Default value: `1`.

    ### Returns:
    (pd.DataFrame) -- A square matrix with the Export Similarity Index between the elements.

    """
    # drop product with no exports and fill missing values with zeros
    tbl = tbl.dropna(how="all", axis=1).fillna(value=0)
    measure = measure.fillna(value=0)

    # get Mcp matrix
    m = rcas.ge(cutoff).astype(int)

    # Ensures that the matrices are aligned by removing geographies that don't exist in both matrices
    tbl_geo = tbl.index
    measure_geo = measure.index
    intersection_geo = list(set(tbl_geo) & set(measure_geo))
    tbl = tbl.filter(items=intersection_geo, axis=0)
    measure = measure.filter(items=intersection_geo, axis=0)
    m = m.filter(items=intersection_geo, axis=0)

    tbl = tbl.sort_index(ascending=True)
    measure = measure.sort_index(ascending=True)
    m = m.sort_index(ascending=True)

    # get Scp matrix
    col_sums = tbl.sum(axis=1)
    col_sums = col_sums.to_numpy().reshape((len(col_sums), 1))
    scp = np.divide(tbl, col_sums)

    # get Np array
    normp = m.multiply(scp).sum(axis=0)
    normp = pd.DataFrame(normp)

    num = m.multiply(scp).T.dot(measure)

    pmi: pd.DataFrame = np.divide(num, normp)  # type: ignore
    return pmi


def pgi(
    tbl: pd.DataFrame,
    rcas: pd.DataFrame,
    gini: pd.DataFrame,
    *,
    cutoff: float = 1,
    name: str = "pgi",
) -> pd.DataFrame:
    """Calculates the Product Gini Index (PGI) for a pivoted matrix.

    It is important to note that even though the functions do not use a
    parameter in relation to time, the data used for the calculations must
    be per period; for example working with World Exports for the year 2020.
    Also, the index always has to be a geographic level.
    It is also important to make sure that the input matrices are aligned,
    that is, that both matrices consider the same geographic units.

    ### Args:
    * tbl (pandas.DataFrame) -- A pivoted table using a geographic index, columns with the categories to be evaluated and the measurement of the data as values.
    * gini (pandas.DataFrame) -- A matrix of GINI indices using a geographic index.

    ### Keyword Args:
    * cutoff (float, optional) -- Set the cutoff threshold value for the RCA matrix.
        Internally, RCA values under it will be set to zero, one otherwise.
        Default value: `1`.

    ### Returns:
    (pandas.DataFrame) -- PGI matrix with categories evaluated as an index.
    """

    pgip = pmi(tbl=tbl, rcas=rcas, measure=gini, cutoff=cutoff)
    pgip.rename(columns={pgip.columns[0]: name}, inplace=True)
    return pgip


def peii(
    tbl: pd.DataFrame,
    rcas: pd.DataFrame,
    emissions: pd.DataFrame,
    *,
    cutoff: float = 1,
    name: str = "peii",
) -> pd.DataFrame:
    """
    Calculates the Product Emissions Intensity Index (PEII) for a pivoted matrix.

    It is important to note that even though the functions do not use a
    parameter in relation to time, the data used for the calculations must
    be per period; for example working with World Exports for the year 2020.
    Also, the index always has to be a geographic level.
    It is also important to make sure that the input matrices are aligned,
    that is, that both matrices consider the same geographic units.

    ### Args:
    * tbl (pandas.DataFrame) -- A pivoted table using a geographic index, columns with the categories to be evaluated and the measurement of the data as values.
    * emissions (pandas.DataFrame) -- A matrix of emissions intensity using a geographic index.

    ### Keyword Args:
    * cutoff (float, optional) -- Set the cutoff threshold value for the RCA matrix.
        Internally, RCA values under it will be set to zero, one otherwise.
        Default value: `1`.

    ### Returns:
    (pandas.DataFrame) -- PEII matrix with categories evaluated as an index.
    """

    peii = pmi(tbl=tbl, rcas=rcas, measure=emissions, cutoff=cutoff)
    peii.rename(columns={peii.columns[0]: name}, inplace=True)
    return peii
