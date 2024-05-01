"""Complexity Indices module

Hidalgo & Hausmann (2009), calculate the Economic Complexity Indices from the
reflections method, which is defined based on a red bipartite that contains a
symmetric set of variables whose nodes correspond to countries and products.
"""

import logging
from typing import Tuple

import pandas as pd

logger = logging.getLogger(__name__)


def complexity(
    df_rca: pd.DataFrame,
    *,
    cutoff: float = 1,
    drop: bool = True,
    iterations: int = 20,
) -> Tuple[pd.Series, pd.Series]:
    """Calculates Economic Complexity Index (ECI) and Product Complexity
    Index (PCI) from a RCA matrix.

    Note that to display the resulting values, the series must be transformed
    into a dataframe in an tidy format as shown below:

    ```
    eci_value, pci_value = complexity(rca)
    eci = eci_value.to_frame(name="ECI").reset_index()
    pci = pci_value.to_frame(name="PCI").reset_index()
    ```

    ### Args:
    * df_rca (pd.DataFrame) -- Pivotted RCA matrix.

    ### Keyword Args:
    * cutoff (float, optional) -- Set the cutoff threshold value for the RCA matrix.
    * drop (bool, optional) -- Boolean to ensure that returns include NaN values.
        Default value: `True`.
    * iterations (int, optional) -- Limit of recursive calculations for kp and kc.
        Default value: `20`.

    ### Returns:
    ((pd.Series, pd.Series)) -- A tuple of ECI and PCI values.
    """
    # Binarize input RCA
    rcas = df_rca.ge(cutoff).astype(int)

    # drop columns / rows only if completely nan
    rcas_clone = rcas.copy(deep=True)
    rcas_clone = rcas_clone.dropna(how="all")
    rcas_clone = rcas_clone.dropna(how="all", axis=1)

    if rcas_clone.shape != rcas.shape:
        logger.warning(
            "RCAs contain columns or rows that are entirely comprised of NaN values."
        )
    if drop:
        rcas = rcas_clone

    kp = rcas.sum(axis=0)  # sum columns
    kc = rcas.sum(axis=1)  # sum rows
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
    geo_col_name = df_rca.index.name

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
