from typing import Optional

import pandas as pd

from .proximity import proximity


def relatedness(
    df_rca: pd.DataFrame,
    *,
    cutoff: float = 1,
    proximities: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    """Calculates the Relatedness, given a matrix of RCAs for the economic
    activities of a location, and a matrix of Proximities.

    The fact that the growth of an activity in a location is correlated with
    relatedness is known as The Principle of Relatedness, introduced by
    Hidalgo et al. (2018), which consists of a statistical law that tells us
    that the probability a location (a country, city, or region) enters an
    economic activity (e.g. a product, industry, technology), grows with the
    number of related activities present in that location.

    Scholars measure Relatedness between a location and an economic activity
    to predict the probability that a region will enter or exit that activity
    in the future.

    ### Args:
    * rcas (pd.DataFrame) -- Matrix of RCAs for a certain location.

    ### Keyword Args:
    * cutoff (float, optional) -- Set the cutoff threshold value.
        Internally, RCA values under it will be set to zero, one otherwise.
        Default value: `1`.
    * proximities (pd.DataFrame, optional) -- Matrix with the proximity between the elements.
        If not provided, will be calculated using the "max" procedure, and
        the same cutoff value for this call.

    ### Returns:
    (pd.DataFrame) -- A matrix with the probability that a location generates
        comparative advantages in a economic activity.
    """
    if proximities is None:
        proximities = proximity(df_rca, cutoff=cutoff)

    rcas = df_rca.ge(cutoff).astype(int)

    # Get numerator by matrix multiplication of proximities with M_im
    density_numerator = rcas.dot(proximities)

    # Get denominator by multiplying proximities by all ones vector thus
    # getting the sum of all proximities
    # rcas_ones = pd.DataFrame(np.ones_like(rcas))
    rcas_ones = rcas * 0
    rcas_ones = rcas_ones + 1
    # print rcas_ones.shape, proximities.shape
    density_denominator = rcas_ones.dot(proximities)

    # We now have our densities matrix by dividing numerator by denomiator
    densities = density_numerator / density_denominator

    return densities


def distance(
    df_rca: pd.DataFrame,
    *,
    cutoff: float = 1,
    proximities: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    """Calculates the distance.

    In this context, the Distance for a Country and a certain Product is defined
    as the

    ### Args:
    * df_rca (pd.DataFrame) -- Matrix of RCAs for a certain location.

    ### Keyword Args:
    * cutoff (float, optional) -- Set the cutoff value for the proximity calculation.
        This will not be used if the `proximities` matrix is provided.
        Default value: `1`.
    * proximities (pd.DataFrame, optional) -- Matrix with the proximity between the elements.
        If not provided, will be calculated using the "max" procedure, and the
        same cutoff value for this call.

    ### Returns:
    (pd.DataFrame) --
    """
    return 1 - relatedness(df_rca, cutoff=cutoff, proximities=proximities)


def relative_relatedness(
    rcas: pd.DataFrame,
    *,
    cutoff: float = 1,
    proximities: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    """Calculates the Relative Relatedness, given a matrix of RCAs for the economic
    activities of a location, and a matrix of Proximities.

    ### Args:
    * rcas (pd.DataFrame) -- Matrix of RCAs for a certain location.

    ### Keyword Args:
    * cutoff (float, optional) -- Set the cutoff threshold value.
        Internally, RCA values under it will be set to zero, one otherwise.
        Default value: `1`.
    * proximities (pd.DataFrame, optional) -- Matrix with the proximity between the elements.
        If not provided, will be calculated using the "max" procedure, and
        the same cutoff value for this call.

    ### Returns:
    (pd.DataFrame) -- A matrix with the probability that a location generates
        comparative advantages in a economic activity.
    """

    opp = rcas.copy()

    if cutoff == 0:
        opp = 1
    else:
        opp[opp >= cutoff] = pd.NA
        opp[opp < cutoff] = 1

    if proximities is None:
        wcp = relatedness(rcas, cutoff)
    else:
        wcp = relatedness(rcas, cutoff, proximities)

    wcp_opp = opp * wcp
    wcp_mean = wcp_opp.mean(axis=1)
    wcp_std = wcp_opp.std(axis=1)

    return wcp.transform(lambda x: (x - wcp_mean) / wcp_std)
