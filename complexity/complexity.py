import sys
import numpy as np
import pandas as pd

def complexity(rcas, iterations=20, drop=True):
    """compute the ECI and PCI from a RCA matrix  

    Args:
        rcas (pandas dataframe): RCA marix in a pandas dataframe type.
        iterations (int, optional): cutoff of recursive calculation of kp and kc. Defaults to 20.
        drop (bool, optional): validation variable to ensure that return include NaN values. Defaults to True.

    Returns:
        geo_complexity, prod_complexity (pandas series): the complexity of the rows (countries int the EC theoretical framework) and columns (products) respectively. 
    """
    #Binarize rca input 
    rcas = rcas.copy()
    rcas[rcas >= 1] = 1
    rcas[rcas < 1] = 0

    # drop columns / rows only if completely nan
    rcas_clone = rcas.copy()
    rcas_clone = rcas_clone.dropna(how="all")
    rcas_clone = rcas_clone.dropna(how="all", axis=1)


    if rcas_clone.shape != rcas.shape:
        print("[Warning] RCAs contain columns or rows that are entirely comprised of NaN values.")
    if drop:
        rcas = rcas_clone

    kp = rcas.sum(axis=0) #sum columns
    kc = rcas.sum(axis=1) #sum rows 
    kp0 = kp.copy()
    kc0 = kc.copy()

    for i in range(1, iterations):
        kc_temp = kc.copy()
        kp_temp = kp.copy()
        kp = rcas.T.dot(kc_temp) / kp0
        if i < (iterations - 1):
            kc = rcas.dot(kp_temp) / kc0

    geo_complexity = (kc - kc.mean()) / kc.std()
    prod_complexity = (kp - kp.mean()) / kp.std()

    return geo_complexity, prod_complexity
