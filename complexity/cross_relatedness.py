# -*- coding: utf-8 -*-
import sys
import numpy as np
import pandas as pd

def relatedness(rcas_a, cross_proximity):
    rcas_a = rcas_a.copy()
    rcas_a[rcas_a >= 1] = 1
    rcas_a[rcas_a < 1] = 0

    numerator = rcas_a.dot(cross_proximity)

    rcas_ones = rcas_a * 0
    rcas_ones = rcas_a + 1

    denominator = rcas_ones.dot(cross_proximity)

    cross_relatedness = numerator / denominator

    return cross_relatedness