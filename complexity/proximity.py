# -*- coding: utf-8 -*-
import sys
import numpy as np

def proximity(rcas, how="max"):
    rcas = rcas.copy()
    rcas[rcas >= 1] = 1
    rcas[rcas < 1] = 0

    # transpose the matrix so that it is now industries as rows and munics as
    # columns
    rcas_t = rcas.T.fillna(0)

    # Matrix multiplication on M_mi matrix and transposed version,
    # number of products = number of rows and vice versa on transposed
    # version, thus the shape of this result will be length of products by
    # by the length of products (symetric)
    numerator_intersection = rcas_t.dot(rcas_t.T)

    # kp0 is a vector of the number of munics with RCA in the given product
    kp0 = rcas.sum(axis=0)
    kp0 = kp0.values.reshape((1, len(kp0)))

    # transpose this to get the unions
    kp0_trans = kp0.T

    # multiply these two vectors, take the squre root
    # and then we have the denominator
    if how == "sqrt":
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
