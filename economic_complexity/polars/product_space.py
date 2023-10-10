"""Product Space module
"""

from typing import Literal, Union
import numpy as np
import polars as pl


def calculate_proximity(
    rca: Union[pl.LazyFrame, pl.DataFrame],
    *,
    procedure: Literal["max", "sqrt"] = "max",
):
    """Calculates the Proximity index for a matrix of RCAs.

    Hidalgo et al. (2007), introduces the Proximity index which measures the
    minimum probability that a country has comparative advantages in the export
    of a product `i`, given that it has comparative advantages in a product `j`.

    This function only needs the pivot table obtained from the RCA function,
    and returns a square matrix with the proximity between the elements.

    Args:
        rca (pl.DataFrame) -- A RCA matrix of pivotted values.
        procedure (str, optional) -- Determines how to calcule the denominator.
            Available options are "sqrt" and "max", defaults to "max".

    Returns:
        (np.ndarray) -- A square matrix with the proximity between the elements.
    """
    rcas = (rca.collect() if isinstance(rca, pl.LazyFrame) else rca).to_numpy()

    # Matrix multiplication on M_mi matrix and transposed version,
    # number of products = number of rows and vice versa on transposed
    # version, thus the shape of this result will be length of products
    # by the length of products (symetric)
    numerator_intersection = rcas.transpose().dot(rcas)

    # kp0 is a vector of the number of munics with RCA in the given product
    kp0 = rcas.sum(axis=0)
    kp0_trans = kp0.reshape((len(kp0), 1))

    # multiply these two vectors, take the squre root
    # and then we have the denominator
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


def calculate_relatedness(
    rca: pl.DataFrame,
    proximities: np.ndarray,
    *,
    location: str,
):
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
    # Save index
    index_col = rca[location]
    headers = rca.columns[1:]
    rcas = rca.drop(location).to_numpy()

    # Get numerator by matrix multiplication of proximities with M_im
    density_numerator = rcas.dot(proximities)

    # Get denominator by multiplying proximities by all ones vector thus
    # getting the sum of all proximities
    rcas_ones = np.ones(rcas.shape)
    # print rcas_ones.shape, proximities.shape
    density_denominator = rcas_ones.dot(proximities)

    # We now have our densities matrix by dividing numerator by denomiator
    densities = density_numerator / density_denominator

    densities = pl.DataFrame(densities, schema=headers)
    densities = densities.with_columns(pl.Series(name=location, values=index_col))

    return densities
