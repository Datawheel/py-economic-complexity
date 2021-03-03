# -*- coding: utf-8 -*-
import sys
import numpy as np
import pandas as pd

def relatedness(rcas, proximities):
    """probability that a location (a country, city, or region), enters an economic activity (e.g. a product, industry, technology), grows with the number of related activities present in a location.

    Args:
        rcas (pandas dataframe): RCA pivot table 
        proximities (pandas dataframe): matrix with the proximity between the elements

    Returns:
        densities: a matrix with the probability that a location generates comparative advantages in a economic activity..
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
