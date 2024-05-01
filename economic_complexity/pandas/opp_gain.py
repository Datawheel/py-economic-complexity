from typing import Optional

import pandas as pd

from .proximity import proximity
from .relatedness import relatedness


def opportunity_gain(
    df_rca: pd.DataFrame,
    *,
    pci: pd.Series,
    cutoff: float = 1,
    proximities: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    """Calculates the opportunity gain caused by the contribution of a certain
    characteristic, relative to how this affects other characteristics.

    ### Args:
    * df_rca (pd.DataFrame) -- Matrix of RCAs for a certain location.

    ### Keyword Args:
    * pci (pd.Series) -- Calculated Product Complexity Index from the RCA data.
    * cutoff (float, optional) -- Set the cutoff value for the proximity calculation.
        This will not be used if the `proximities` matrix is provided.
        Default value: `1`.
    * proximities (pd.DataFrame, optional) -- Matrix with the proximity between the elements.
        If not provided, will be calculated using the "max" procedure, and the
        same cutoff value for this call.

    ### Returns:
    (pd.DataFrame) --
    """
    if proximities is None:
        proximities = proximity(df_rca, cutoff=cutoff)

    rcas = df_rca.ge(cutoff).astype(int)

    # turn proximities in to ratios out of total
    prox_ratio = proximities / proximities.sum()

    # get the inverse of the RCAs matrix. Since they are in the form of 1's and
    # 0's this will flip all of them i.e. 1 = 0 and 0 = 1
    inverse_rcas = 1 - rcas

    # here we now have the middle part of the equation
    middle = inverse_rcas.multiply(pci)

    # get the relatedness with the backwards bizzaro RCAs
    dcp = relatedness(inverse_rcas, proximities=proximities)
    # now get the inverse
    dcp = 1 - dcp
    # we now have the right-half of the equation
    right = dcp.multiply(pci)

    # matrix multiplication with proximities ratio
    opp_gain = middle.dot(prox_ratio) - right

    return opp_gain
