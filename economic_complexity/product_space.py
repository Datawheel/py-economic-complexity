"""Product Space module"""

from typing import Literal, Optional

import numpy as np
import pandas as pd


def proximity(
    df_rca: pd.DataFrame,
    *,
    cutoff: float = 1,
    procedure: Literal["max", "sqrt"] = "max",
) -> pd.DataFrame:
    """Calculates the Proximity index for a matrix of RCAs.

    Hidalgo et al. (2007), introduces the Proximity index which measures the
    minimum probability that a country has comparative advantages in the export
    of a product `i`, given that it has comparative advantages in a product `j`.

    This function only needs the pivot table obtained from the RCA function,
    and returns a square matrix with the proximity between the elements.

    ### Args:
    * df_rca (pd.DataFrame) -- A RCA matrix of pivotted values.

    ### Keyword Args:
    * cutoff (float, optional) -- Set the cutoff threshold value.
        Internally, RCA values under it will be set to zero, one otherwise.
        Default value: `1`.
    * procedure (str, optional) -- Determines how to calcule the denominator.
        Available options are "sqrt" and "max". Default value: `"max"`.

    ### Returns:
    (pd.DataFrame) -- A square matrix with the proximity between the elements.
    """
    # Apply cutoff to RCA values
    rcas = df_rca.ge(cutoff).astype(int)

    # transpose the matrix so that it is now industries as rows
    # and munics as columns
    rcas_t = rcas.T.fillna(0)

    # Matrix multiplication on M_mi matrix and transposed version,
    # number of products = number of rows and vice versa on transposed
    # version, thus the shape of this result will be length of products
    # by the length of products (symetric)
    numerator_intersection = rcas_t.dot(rcas_t.T)

    # kp0 is a vector of the number of munics with RCA in the given product
    kp0 = rcas.sum(axis=0)
    kp0 = kp0.to_numpy().reshape((1, len(kp0)))

    # transpose this to get the unions
    kp0_trans = kp0.T

    # multiply these two vectors, take the squre root
    # and then we have the denominator
    if procedure == "sqrt":
        # get square root for geometric mean
        denominator_union = kp0_trans.dot(kp0)
        denominator_union = np.power(denominator_union, 0.5)
    else:
        denominator_union = np.maximum(kp0, kp0_trans)

    # to get the proximities it is now a simple division of the untion sqrt
    # with the numerator intersections
    phi: pd.DataFrame = np.divide(numerator_intersection, denominator_union)  # type: ignore
    np.fill_diagonal(phi.values, 0)

    return phi


def relatedness(
    df_rca: pd.DataFrame,
    *,
    cutoff: float = 1,
    proximities: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
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

    ### Args:
    * rcas (pd.DataFrame) -- Matrix of RCAs for a certain location.

    ### Keyword Args:
    * cutoff (float, optional) -- Set the cutoff threshold value.
        Internally, RCA values under it will be set to zero, one otherwise.
        Default value: `1`.
    * proximities (pd.DataFrame, optional) -- Matrix with the proximity between the elements.
        If not provided, will be calculated using the "max" procedure, and
        the same cutoff value for this call.

    ### Returns:
    (pd.DataFrame) -- A matrix with the probability that a location generates
        comparative advantages in a economic activity.
    """
    if proximities is None:
        proximities = proximity(df_rca, cutoff=cutoff)

    rcas = df_rca.ge(cutoff).astype(int)

    # Get numerator by matrix multiplication of proximities with M_im
    density_numerator = rcas.dot(proximities)

    # Get denominator by multiplying proximities by all ones vector thus
    # getting the sum of all proximities
    # rcas_ones = pd.DataFrame(np.ones_like(rcas))
    rcas_ones = rcas * 0
    rcas_ones = rcas_ones + 1
    # print rcas_ones.shape, proximities.shape
    density_denominator = rcas_ones.dot(proximities)

    # We now have our densities matrix by dividing numerator by denomiator
    densities = density_numerator / density_denominator

    return densities


def distance(
    df_rca: pd.DataFrame,
    *,
    cutoff: float = 1,
    proximities: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    """Calculates the distance.

    In this context, the Distance for a Country and a certain Product is defined
    as the

    ### Args:
    * df_rca (pd.DataFrame) -- Matrix of RCAs for a certain location.

    ### Keyword Args:
    * cutoff (float, optional) -- Set the cutoff value for the proximity calculation.
        This will not be used if the `proximities` matrix is provided.
        Default value: `1`.
    * proximities (pd.DataFrame, optional) -- Matrix with the proximity between the elements.
        If not provided, will be calculated using the "max" procedure, and the
        same cutoff value for this call.

    ### Returns:
    (pd.DataFrame) --
    """
    return 1 - relatedness(df_rca, cutoff=cutoff, proximities=proximities)


def opportunity_gain(
    df_rca: pd.DataFrame,
    *,
    pci: pd.Series,
    cutoff: float = 1,
    proximities: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    """Calculates the opportunity gain caused by the contribution of a certain
    characteristic, relative to how this affects other characteristics.

    ### Args:
    * df_rca (pd.DataFrame) -- Matrix of RCAs for a certain location.

    ### Keyword Args:
    * pci (pd.Series) -- Calculated Product Complexity Index from the RCA data.
    * cutoff (float, optional) -- Set the cutoff value for the proximity calculation.
        This will not be used if the `proximities` matrix is provided.
        Default value: `1`.
    * proximities (pd.DataFrame, optional) -- Matrix with the proximity between the elements.
        If not provided, will be calculated using the "max" procedure, and the
        same cutoff value for this call.

    ### Returns:
    (pd.DataFrame) --
    """
    if proximities is None:
        proximities = proximity(df_rca, cutoff=cutoff)

    rcas = df_rca.ge(cutoff).astype(int)

    # turn proximities in to ratios out of total
    prox_ratio = proximities / proximities.sum()

    # get the inverse of the RCAs matrix. Since they are in the form of 1's and
    # 0's this will flip all of them i.e. 1 = 0 and 0 = 1
    inverse_rcas = 1 - rcas

    # here we now have the middle part of the equation
    middle = inverse_rcas.multiply(pci)

    # get the relatedness with the backwards bizzaro RCAs
    dcp = relatedness(inverse_rcas, proximities=proximities)
    # now get the inverse
    dcp = 1 - dcp
    # we now have the right-half of the equation
    right = dcp.multiply(pci)

    # matrix multiplication with proximities ratio
    opp_gain = middle.dot(prox_ratio) - right

    return opp_gain


def similarity(
    df_rca: pd.DataFrame,
    *,
    epsilon: float = 0.1,
) -> pd.DataFrame:
    """
    Calculates the Export Similarity Index for a matrix of RCAs.

    Bahar et al. (2014) introduces this measure of similarity in the export
    structure of a pair of countries c and c'. It's defined as the Pearson
    correlation between the logarithm of the RCA vectors of the two countries.

    This function only needs the pivot table obtained from the RCA function,
    and returns a square matrix with the Export Similarity Index between the
    elements.

    ### Args:
    * rcas (pd.DataFrame) -- A RCA matrix of pivotted values.

    ### Keyword Args:
    * epsilon (float, optional) -- A low value to prevent the calculation of logarithm to output `-Inf`.
        Default value: `0.1`.

    ### Returns:
    (pd.DataFrame) -- A square matrix with the Export Similarity Index between the elements.
    """
    # Take the log of rcas (adding \epsilon)
    rcas: pd.DataFrame = np.log(df_rca + epsilon)  # type: ignore

    # calculate the matrix through the pearson correlation
    scc = pd.DataFrame(np.corrcoef(rcas), columns=rcas.index, index=rcas.index)

    return scc


def _pmi(
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

    pgip = _pmi(tbl=tbl, rcas=rcas, measure=gini, cutoff=cutoff)
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

    peii = _pmi(tbl=tbl, rcas=rcas, measure=emissions, cutoff=cutoff)
    peii.rename(columns={peii.columns[0]: name}, inplace=True)
    return peii


def relative_relatedness(
    rcas: pd.DataFrame,
    *,
    cutoff: float = 1,
    proximities: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    """Calculates the Relative Relatedness, given a matrix of RCAs for the economic
    activities of a location, and a matrix of Proximities.

    ### Args:
    * rcas (pd.DataFrame) -- Matrix of RCAs for a certain location.

    ### Keyword Args:
    * cutoff (float, optional) -- Set the cutoff threshold value.
        Internally, RCA values under it will be set to zero, one otherwise.
        Default value: `1`.
    * proximities (pd.DataFrame, optional) -- Matrix with the proximity between the elements.
        If not provided, will be calculated using the "max" procedure, and
        the same cutoff value for this call.

    ### Returns:
    (pd.DataFrame) -- A matrix with the probability that a location generates
        comparative advantages in a economic activity.
    """

    opp = rcas.copy()

    if cutoff == 0: #all activities
            opp[:] = 1
    elif cutoff > 0: #cuttoff = 1 activities with comparative advantages
        opp[opp >= cutoff] = 1
        opp[opp < cutoff] = pd.NA
    else: #<0 cutoff = -1 activities without comparative advantages,
        opp[opp >= cutoff * -1] = pd.NA
        opp[opp < cutoff * -1] = 1

    wcp = relatedness(rcas, proximities=proximities)

    wcp_opp = opp * wcp
    wcp_mean = wcp_opp.mean(axis=1)
    wcp_std = wcp_opp.std(axis=1)

    return wcp.transform(lambda x: (x - wcp_mean) / wcp_std)
