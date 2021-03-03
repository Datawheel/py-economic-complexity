# -*- coding: utf-8 -*-
import sys
import numpy as np
import pandas as pd

def cross_relatedness(rcas_a, cross_proximity):
    """ Catalan et al. (2020) incorporated the concept of cross-relatedness in order to quantify the relationship between scientific fields in the development of new technologies in a country. The density crossing takes values ​​between zero and one, mathematically it corresponds to the average cross proximity of a technology  and the scientific knowledge of a country during the period of time.

    Args:
        rcas_a (pandas dataframe): The pivot table obtained from the RCA function for the main characteristic to be evaluated
        cross_proximity ([type]): The pivot table obtained from the cross-prximity function

    Returns:
        cross_relatedness (pandas dataframe): matrix with the probability that a location generates comparative advantages in the characteristic to be evaluated considering its proximity with the other evaluated characteristic.
    """
    rcas_a = rcas_a.copy()
    rcas_a[rcas_a >= 1] = 1
    rcas_a[rcas_a < 1] = 0

    numerator = rcas_a.dot(cross_proximity)

    rcas_ones = rcas_a * 0
    rcas_ones = rcas_a + 1

    denominator = rcas_ones.dot(cross_proximity)

    cross_relatedness = numerator / denominator

    return cross_relatedness