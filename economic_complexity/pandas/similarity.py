import numpy as np
import pandas as pd


def similarity(
    df_rca: pd.DataFrame,
    *,
    epsilon: float = 0.1,
) -> pd.DataFrame:
    """
    Calculates the Export Similarity Index for a matrix of RCAs.

    Bahar et al. (2014) introduces this measure of similarity in the export
    structure of a pair of countries c and c'. It's defined as the Pearson
    correlation between the logarithm of the RCA vectors of the two countries.

    This function only needs the pivot table obtained from the RCA function,
    and returns a square matrix with the Export Similarity Index between the
    elements.

    ### Args:
    * rcas (pd.DataFrame) -- A RCA matrix of pivotted values.

    ### Keyword Args:
    * epsilon (float, optional) -- A low value to prevent the calculation of logarithm to output `-Inf`.
        Default value: `0.1`.

    ### Returns:
    (pd.DataFrame) -- A square matrix with the Export Similarity Index between the elements.
    """
    # Take the log of rcas (adding \epsilon)
    rcas: pd.DataFrame = np.log(df_rca + epsilon)  # type: ignore

    # calculate the matrix through the pearson correlation
    scc = pd.DataFrame(np.corrcoef(rcas), columns=rcas.index, index=rcas.index)

    return scc
