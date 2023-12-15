"""Subnational Method module
"""
from typing import Tuple

import pandas as pd


def complexity_subnational(
    df_rca: pd.DataFrame,
    pci_external: pd.Series,
    *,
    cutoff: float = 1,
    standardize: bool = False,
) -> Tuple[pd.Series, pd.Series]:
    """
    Calculates the Economic Complexity Index for the subnational (AKA external method). Here a RCA matrix and an external Product Complexity is used.

    ### Args:
    rcas (pd.DataFrame) -- Pivotted RCA matrix.
    pci_external (pd.Series) -- PCI values from an external source.

    ### Keyword Args:
    cutoff (float, optional) -- Set the cutoff threshold value for the RCA matrix.
        Default value: `1`.
    standardize (bool, optional) -- Specifies if the ECI vector should be standardized: `x-µ/σ`.
        Default value: `False`.

    ### Returns:
    ((pd.Series, pd.Series)) -- A tuple of ECI and PCI values using the subnational method.
    """

    # This functions computes the ECI for a RCA matrix using an external PCI index.
    geo_col_name = rcas.index.name

    # Create an empty Series to store the eci_external values
    eci_external = pd.Series(dtype=float)

    # Binarize rca input by converting values >= 1 to 1 and < 1 to 0
    rcas = df_rca.ge(cutoff).astype(int)

    # Drop rows or columns from rcas that are completely empty
    rcas = rcas.dropna(how="all")
    rcas = rcas.dropna(how="all", axis=1)

    # Iterate over each row in the rca matrix
    for index, row in rcas.iterrows():
        # Create an empty DataFrame to store the selected categories
        spec_cat = pd.DataFrame()

        # Select the categories with an RCA of 1 for the current geography
        spec_cat["value"] = row == 1
        spec_cat = spec_cat[spec_cat["value"] == True]
        spec_cat = spec_cat.index.values

        # Retrieve the PCI values for the selected products from the external PCI matrix
        pci_rca = pci_external[pci_external.index.isin(spec_cat)]

        # Compute the ECI for the current country using the retrieved PCI values
        eci = pci_rca.sum() / len(pci_rca)

        # Append the ECI value to the eci_external DataFrame
        eci_external = pd.concat(
            [eci_external, pd.Series({index: eci})],
            axis=0,
            ignore_index=False,
        )

    if standardize == True:
        # Standardize the ECI values by subtracting the mean and dividing by the standard deviation
        eci_external = (eci_external - eci_external.mean()) / eci_external.std()

    eci_external.index.name = geo_col_name

    return eci_external, pci_external
