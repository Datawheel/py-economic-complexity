"""Economic Complexity

This module contains functions to ease the calculation of Economic Complexity values.
"""

from .rca import rca
from .complexity import complexity
from .product_space import distance, opportunity_gain, proximity, relatedness, similarity, pgi, peii
from .cross_space import cross_proximity, cross_relatedness

__version_info__ = ('0', '1', '1')
__version__ = '.'.join(__version_info__)

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
)
