"""Product Space module
"""

import pandas as pd
import numpy as np
import polars as pl


def proximity(rcas: pl.DataFrame, procedure="max"):
    """Calculates the Proximity index for a matrix of RCAs.

    Hidalgo et al. (2007), introduces the Proximity index which measures the
    minimum probability that a country has comparative advantages in the export
    of a product `i`, given that it has comparative advantages in a product `j`.

    This function only needs the pivot table obtained from the RCA function,
    and returns a square matrix with the proximity between the elements.

    Args:
        rcas (pl.DataFrame) -- A RCA matrix of pivotted values.
        procedure (str, optional) -- Determines how to calcule the denominator.
            Available options are "sqrt" and "max", defaults to "max".

    Returns:
        (pl.DataFrame) -- A square matrix with the proximity between the elements.
    """
    rcas = rcas.to_numpy()

    numerator_intersection = rcas.transpose().dot(rcas)

    kp0 = rcas.sum(axis=0)
    kp0_trans = kp0.reshape((len(kp0), 1))

    if procedure == "sqrt":
        # get square root for geometric mean
        denominator_union = kp0_trans.dot(kp0)
        denominator_union = np.power(denominator_union, .5)
    else:
        denominator_union = np.maximum(kp0, kp0_trans)

    # to get the proximities it is now a simple division of the untion sqrt
    # with the numerator intersections
    phi = np.divide(numerator_intersection, denominator_union)

    np.fill_diagonal(phi, 0)

    return phi


def relatedness(rcas: pl.DataFrame, proximities: np.ndarray):
    """Calculates the Relatedness, given a matrix of RCAs for the economic
    activities of a location, and a matrix of Proximities.

    The fact that the growth of an activity in a location is correlated with
    relatedness is known as The Principle of Relatedness, introduced by
    Hidalgo et al. (2018), which consists of a statistical law that tells us
    that the probability a location (a country, city, or region) enters an
    economic activity (e.g. a product, industry, technology), grows with the
    number of related activities present in that location.

    Scholars measure Relatedness between a location and an economic activity
    to predict the probability that a region will enter or exit that activity
    in the future.

    Args:
        rcas (pl.DataFrame) -- Matrix of RCAs for a certain location.
        proximities (np.ndarray) -- Matrix with the proximity between the elements.

    Returns:
        (np.ndarray) -- A matrix with the probability that a location
            generates comparative advantages in a economic activity.
    """
    rcas = rcas.to_numpy()

    # Get numerator by matrix multiplication of proximities with M_im
    density_numerator = rcas.dot(proximities)

    # Get denominator by multiplying proximities by all ones vector thus
    # getting the sum of all proximities
    rcas_ones = np.ones(rcas.shape)
    # print rcas_ones.shape, proximities.shape
    density_denominator = rcas_ones.dot(proximities)

    # We now have our densities matrix by dividing numerator by denomiator
    densities = density_numerator / density_denominator

    return densities


def distance(rcas: pd.DataFrame, proximities: pd.DataFrame):
    """Calculates the distance.

    In this context, the Distance for a Country and a certain Product is defined
    as the

    Args:
        rcas (pd.DataFrame) -- Matrix of RCAs for a certain location.
        proximities (pd.DataFrame) -- Matrix with the proximity between the elements.

    Returns:
        (pd.DataFrame) --
    """
    return 1 - relatedness(rcas, proximities)


def opportunity_gain(rcas: pd.DataFrame, proximities: pd.DataFrame, pci: pd.DataFrame):
    """Calculates the opportunity gain caused by the contribution of a certain
    characteristic, relative to how this affects other characteristics.

    Args:
        rcas (pd.DataFrame) -- Matrix of RCAs considering a
        proximities (pd.DataFrame) -- [description]
        pci (pd.DataFrame) -- [description]

    Returns:
        (pd.DataFrame) --
    """
    rcas = rcas.copy()
    rcas[rcas >= 1] = 1
    rcas[rcas < 1] = 0

    # turn proximities in to ratios out of total
    prox_ratio = proximities / proximities.sum()

    # get the inverse of the RCAs matrix. Since they are in the form of 1's and
    # 0's this will flip all of them i.e. 1 = 0 and 0 = 1
    inverse_rcas = 1 - rcas

    # here we now have the middle part of the equation
    middle = inverse_rcas.multiply(pci)

    # get the relatedness with the backwards bizzaro RCAs
    dcp = relatedness(inverse_rcas, proximities)
    # now get the inverse
    dcp = 1 - dcp
    # we now have the right-half of the equation
    right = dcp.multiply(pci)

    # matrix multiplication with proximities ratio
    opp_gain = middle.dot(prox_ratio) - right

    return opp_gain


def similarity(rcas: pd.DataFrame):
    """
    Calculates the Export Similarity Index for a matrix of RCAs.

    Bahar et al. (2014) introduces this measure of similarity in the export structure of a pair of countries c and c'. It's defined as the Pearson correlation between the logarithm of the RCA vectors of the two countries.

    This function only needs the pivot table obtained from the RCA function,
    and returns a square matrix with the Export Similarity Index between the elements.

    Args:
        rcas (pd.DataFrame) -- A RCA matrix of pivotted values.

    Returns:
        (pd.DataFrame) -- A square matrix with the Export Similarity Index between the elements.
    """

    # Take the log of rcas (add 0.1 as \epsilon)
    rcas = np.log(rcas + 0.1)

    # calculate the matrix through the pearson correlation
    scc = pd.DataFrame(np.corrcoef(rcas), columns=rcas.index, index = rcas.index)

    return scc


def _pmi(tbl: pd.DataFrame, rcas: pd.DataFrame, measure: pd.DataFrame, measure_name: str) -> pd.DataFrame:
    """
    Calculates the Product 'measure' Index, where measure corresponds to a dataframe with the measure values for each geography.
    For example, in the literature this method has been applied to calculate the Product Gini Index (PGI) and the Product Emission Intensity Index.

    Args:
        tbl (pd.DataFrame) -- A pivoted table using a geographic index,
            columns with the categories to be evaluated and the measurement of
            the data as values.
        measure (pd.DataFrame) -- A table using a geographic index, with a single column with the measure values.
        measure_name (str) -- A string with the name of the measure

    Returns:
        (pd.DataFrame) -- A square matrix with the Export Similarity Index between the elements.

    """
    # drop product with no exports and fill missing values with zeros
    tbl = tbl.dropna(how="all", axis=1).fillna(value=0)
    measure = measure.fillna(value=0)

    # get Mcp matrix
    m = rcas.copy()
    m[rcas >= 1] = 1
    m[rcas < 1] = 0

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

    pmi = np.divide(num, normp)
    pmi.rename(columns={pmi.columns[0]: measure_name}, inplace=True)

    return pmi

def pgi(tbl: pd.DataFrame, rcas: pd.DataFrame, gini: pd.DataFrame) -> pd.DataFrame:

    """Calculates the Product Gini Index (PGI) for a pivoted matrix.
    It is important to note that even though the functions do not use a
    parameter in relation to time, the data used for the calculations must
    be per period; for example working with World Exports for the year 2020.
    Also, the index always has to be a geographic level.
    It is also important to make sure that the input matrices are aligned,
    that is, that both matrices consider the same geographic units.
    Arguments:
        tbl (pandas.DataFrame) -- A pivoted table using a geographic index,
            columns with the categories to be evaluated and the measurement of
            the data as values.
        gini (pandas.DataFrame) -- A matrix of GINI indices using a geographic index.
    Returns:
        (pandas.DataFrame) -- PGI matrix with categories evaluated as an index.
    """

    pgip = _pmi(tbl = tbl, rcas = rcas, measure = gini, measure_name='pgi')

    return pgip

def peii(tbl: pd.DataFrame, rcas: pd.DataFrame, emissions: pd.DataFrame) -> pd.DataFrame:

    """
    Calculates the Product Emissions Intensity Index (PEII) for a pivoted matrix.
    It is important to note that even though the functions do not use a
    parameter in relation to time, the data used for the calculations must
    be per period; for example working with World Exports for the year 2020.
    Also, the index always has to be a geographic level.
    It is also important to make sure that the input matrices are aligned,
    that is, that both matrices consider the same geographic units.
    Arguments:
        tbl (pandas.DataFrame) -- A pivoted table using a geographic index,
            columns with the categories to be evaluated and the measurement of
            the data as values.
        emissions (pandas.DataFrame) -- A matrix of emissions intensity using a geographic index.
    Returns:
        (pandas.DataFrame) -- PEII matrix with categories evaluated as an index.
    """

    peii = _pmi(tbl = tbl, rcas = rcas, measure=emissions, measure_name='peii')
    return peii
