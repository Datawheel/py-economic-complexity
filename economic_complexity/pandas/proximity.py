import numpy as np
import pandas as pd
from typing_extensions import Literal


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
