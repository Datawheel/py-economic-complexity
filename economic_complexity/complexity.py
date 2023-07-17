"""Complexity Indices module

Hidalgo & Hausmann (2009), calculate the Economic Complexity Indices from the
reflections method, which is defined based on a red bipartite that contains a
symmetric set of variables whose nodes correspond to countries and products.
"""

import logging
from typing import Tuple

import polars as pl

logger = logging.getLogger(__name__)


def complexity(rca: pl.DataFrame,
               index: str,
               iterations: int = 20) -> Tuple[pl.Series, pl.Series]:
    """Calculates Economic Complexity Index (ECI) and Product Complexity
    Index (PCI) from a RCA matrix.

    Args:
        rcas (pl.DataFrame) -- Pivotted RCA matrix, binary values.
        index (str) -- index column name
        iterations (int, optional) -- Limit of recursive calculations for
            kp and kc. Default value: 20.

    Returns:
        ((pl.Series, pl.Series)) -- A tuple of ECI and PCI values.
    """

    kp = rca.select(pl.all().exclude(index)).sum().transpose().to_series()
    kc = rca.select(pl.all().exclude(index)).sum(axis=1)

    kp0 = kp.clone()
    kc0 = kc.clone()

    for i in range(1, iterations):
        kc_temp = kc.clone()
        kp_temp = kp.clone()

        kp = (rca.select(pl.all().exclude(index)) * kc_temp).sum().transpose().to_series() / kp0
        
        if i < (iterations - 1):
            kc = (rca.select(pl.all().exclude(index)).transpose() * kp_temp).sum().transpose().to_series() / kc0

    geo_complexity = (kc - kc.mean()) / kc.std()
    prod_complexity = (kp - kp.mean()) / kp.std()

    return geo_complexity, prod_complexity
