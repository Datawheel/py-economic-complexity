# -*- coding: utf-8 -*-
import sys
import numpy as np
import pandas as pd

def cross_proximity(rcas_a, rcas_b):
    """ cross-proximity index correspond to the minimum probability that a country presents comparative advantages in a patent in a given area given that it has comparative advantages in an area of ​​knowledge, or vice versa, where values ​​that are more close to unity indicate a stronger relationship between the patent area and the knowledge area.

    Args:
        rcas_a (pandas dataframe): The pivot table obtained from the RCA function for a one characteristic to evaluate
        rcas_b (pandas dataframe): The pivot table obtained from the RCA function for the other characteristic to evaluate 

    Returns:
        cross_proximity (pandas dataframe): matrix with the proximity between the two types of elements evaluated that can be used in the calculation of the *cross-relatedness*.
    """
    # Converts RCA values to 0-1
    rcas_a[rcas_a >= 1] = 1
    rcas_a[rcas_a < 1] = 0
    rcas_b[rcas_b >= 1] = 1
    rcas_b[rcas_b < 1] = 0

    # Calculates numerator of array
    numerator = rcas_a.T.dot(rcas_b)

    # Calculates kp0 for rcas_a and rcas_b
    kp0_a = rcas_a.sum(axis=0)
    kp0_a = kp0_a.values.reshape((1, len(kp0_a)))

    kp0_b = rcas_b.sum(axis=0)
    kp0_b = kp0_b.values.reshape((1, len(kp0_b)))

    # Calculates two possible cross proximity values and replace posibles NaN values
    a = numerator.divide(kp0_b).fillna(0)
    b = numerator.divide(kp0_a.T).fillna(0)

    # Compares the two previous arrays, and keeps minimum value of each cell
    cross_proximity = pd.DataFrame(
        [np.minimum(x, y) for x, y in zip(a.values, b.values)],
        index=a.index,
        columns=a.columns
    )

    return cross_proximity
