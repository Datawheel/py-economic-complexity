"""Economic Complexity

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
    similarity,
    relative_relatedness
)
from .rca import rca
from .subnational import complexity_subnational

__version_info__ = ("0", "2", "3")
__version__ = ".".join(__version_info__)

__all__ = (
    "rca",
    "complexity",
    "distance",
    "opportunity_gain",
    "proximity",
    "relatedness",
    "cross_proximity",
    "cross_relatedness",
    "similarity",
    "pgi",
    "peii",
    "complexity_subnational",
    "relative_relatedness"
)
