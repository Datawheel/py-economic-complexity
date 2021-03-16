"""Economic Complexity

This module contains functions to ease the calculation of Economic Complexity values.
"""

from .rca import rca
from .complexity import complexity
from .product_space import distance, opportunity_gain, proximity, relatedness
from .cross_space import cross_proximity, cross_relatedness

__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)
