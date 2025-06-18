"""Economic Complexity calculations module.

This module contains functions to ease the calculation of Economic Complexity values.
"""

from .complexity import complexity
from .cross_space import cross_proximity, cross_relatedness
from .product_space import (
    distance,
    opportunity_gain,
    peii,
    pgi,
    proximity,
    relatedness,
    relative_relatedness,
    similarity,
)
from .rca import rca
from .subnational import complexity_subnational

__version_info__ = ("0", "3", "0")
__version__ = ".".join(__version_info__)

__all__ = (
    "complexity",
    "complexity_subnational",
    "cross_proximity",
    "cross_relatedness",
    "distance",
    "opportunity_gain",
    "peii",
    "pgi",
    "proximity",
    "rca",
    "relatedness",
    "relative_relatedness",
    "similarity",
)
