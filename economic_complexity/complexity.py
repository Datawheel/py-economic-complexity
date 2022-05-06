"""Complexity Indices module

Hidalgo & Hausmann (2009), calculate the Economic Complexity Indices from the
reflections method, which is defined based on a red bipartite that contains a
symmetric set of variables whose nodes correspond to countries and products.
"""

import logging
from typing import Optional, Tuple

import numpy.typing as nptype
import pandas as pd

logger = logging.getLogger(__name__)


def complexity(rca: nptype.NDArray,
               iterations: int = 20,
               drop: Optional[bool] = True) -> Tuple[pd.Series, pd.Series]:
    """Calculates Economic Complexity Index (ECI) and Product Complexity
    Index (PCI) from a RCA matrix.

    Note that to display the resulting values, the series must be transformed
    into a dataframe in an tidy format as shown below:

        eci_value, pci_value = complexity(rca)
        eci = eci_value.to_frame(name="ECI").reset_index()
        pci = pci_value.to_frame(name="PCI").reset_index()

    Args:
        rcas (pd.DataFrame) -- Pivotted RCA matrix.
        iterations (int, optional) -- Limit of recursive calculations for
            kp and kc. Default value: 20.
        drop (bool, optional) -- Boolean to ensure that returns include NaN
            values. Default value: True.

    Returns:
        ((pd.Series, pd.Series)) -- A tuple of ECI and PCI values.
    """
    # Binarize rca input
    rcas = pd.DataFrame(rca.copy())
    rcas[rcas >= 1] = 1
    rcas[rcas < 1] = 0

    # drop columns / rows only if completely nan
    rcas_clone = rcas.copy()
    rcas_clone = rcas_clone.dropna(how="all")
    rcas_clone = rcas_clone.dropna(how="all", axis=1)

    if rcas_clone.shape != rcas.shape:
        logger.warning("RCAs contain columns or rows that are entirely comprised of NaN values.")
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
