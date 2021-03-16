# -*- coding: utf-8 -*-

"""Product Space module
"""

import pandas as pd


def proximity(rcas: pd.DataFrame, procedure="max"):
    """Calculates the Proximity index for a matrix of RCAs.

    Hidalgo et al. (2007), introduces the Proximity index which measures the
    minimum probability that a country has comparative advantages in the export
    of a product `i`, given that it has comparative advantages in a product `j`.

    This function only needs the pivot table obtained from the RCA function,
    and returns a square matrix with the proximity between the elements.

    Args:
        rcas (pd.DataFrame) -- A RCA matrix of pivotted values.
        procedure (str, optional) -- Determines how to calcule the denominator.
            Available options are "sqrt" and "max", defaults to "max".

    Returns:
        (pd.DataFrame) -- A square matrix with the proximity between the elements.
    """
    rcas = rcas.copy()
    rcas[rcas >= 1] = 1
    rcas[rcas < 1] = 0

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
    kp0 = kp0.values.reshape((1, len(kp0)))

    # transpose this to get the unions
    kp0_trans = kp0.T

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
    np.fill_diagonal(phi.values, 0)

    return phi


def relatedness(rcas: pd.DataFrame, proximities: pd.DataFrame):
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
        rcas (pd.DataFrame) -- Matrix of RCAs for a certain location.
        proximities (pd.DataFrame) -- Matrix with the proximity between the elements.

    Returns:
        (pd.DataFrame) -- A matrix with the probability that a location
            generates comparative advantages in a economic activity.
    """
    rcas = rcas.copy()
    rcas[rcas >= 1] = 1
    rcas[rcas < 1] = 0

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
