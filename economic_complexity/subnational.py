"""Subnational Method module
"""
from typing import Tuple
import numpy as np
import pandas as pd

def complexity_subnational(rcas: pd.DataFrame, pci_external:pd.Series)-> Tuple[pd.Series, pd.Series]:
    """
    Calculates the Economic Complexity Index for the subnational or external method. Here a RCA matrix and an external Product Complexity is used.
    Args:
        rcas (pd.DataFrame) -- 
        pci_external (pd.Series) -- 

    Returns:
        (pd.Series) -- A square matrix with the Export Similarity Index between the elements.

    """
    # This functions computes the ECI for a RCA matrix using an external PCI index.
    geo_col_name = geo_col_name + '_id'
    cat_col_name = cat_col_name + '_id'
    # Create an empty DataFrame to store the eci_external
    eci_external = pd.DataFrame()
    
    # Binarize rca input by converting values >= 1 to 1 and < 1 to 0
    rcas = rcas.applymap(lambda x : 1 if x >=1 else 0)

    # Drop rows or columns from rcas that are completely empty
    rcas = rcas.dropna(how="all")
    rcas = rcas.dropna(how="all", axis=1)
    # Iterate over each row in the binarized rca matrix
    for index, row in rcas.iterrows():
        # Create an empty DataFrame to store the selected categories
        spec_cat = pd.DataFrame()
        
        # Select the categories with an RCA of 1 for the current geography
        spec_cat['value'] = (row==1)
        spec_cat = spec_cat[spec_cat['value']==True]
        spec_cat = spec_cat.index.values
        
        # Retrieve the PCI values for the selected products from the external PCI matrix
        pci_rca = pci_external[pci_external[cat_col_name].isin(spec_cat)]        

        # Compute the ECI for the current country using the retrieved PCI values
        eci = pci_rca['pci'].sum()/len(pci_rca)
        
        # Append the ECI value to the eci_external DataFrame
        eci_external = eci_external.append({geo_col_name: index, 'eci': eci}, ignore_index=True)

    # Sort the eci_external DataFrame in descending order by ECI value
    eci_external = eci_external.sort_values(by='eci', ascending=False).reset_index(drop=True)

    # Standardize the ECI values by subtracting the mean and dividing by the standard deviation
    eci_external = eci_external.set_index(geo_col_name)['eci']
    eci_external = pd.DataFrame((eci_external-eci_external.mean())/eci_external.std()).reset_index() 

    eci_external[geo_col_name] = eci_external[geo_col_name].astype(rcas.index.dtype)
    
    # Return the standardized ECI values in a DataFrame with the geography IDs
    return eci_external, pci_external
