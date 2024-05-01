"""Revealed Comparative Advantage (RCA) module

The Revealed Comparative Advantage is an index introduced by Balassa (1965),
which is used to evaluate the main products to be exported by a country,
and their comparative advantages in relation to the level of world exports
(Hidalgo et al., 2007).
"""

from typing import Union

import polars as pl


def rca(
    df: Union[pl.DataFrame, pl.LazyFrame],
    *,
    activity: str,
    location: str,
    measure: str,
    binary: bool = False,
    cutoff: float = 1,
) -> pl.LazyFrame:
    """Calculates the Revealed Comparative Advantage (RCA) for a tidy-data formatted DataFrame.

    It is important to note that even though the functions do not use a
    parameter in relation to time, the data used for the calculations must
    be relative to a time period; for example, considering World Exports for
    the year 2020.

    Arguments:
        df (polars.DataFrame | polars.LazyFrame) --
            A tidy-data formatted DataFrame with the information to calculate
            the RCA values. Must contain at least qualitative columns for the
            economic activity and associated location, and a quantitative column
            with the measure to use for calculation.

    Keyword Arguments:
        activity (str) --
            The name of the column to use as economic activity.
        location (str) --
            The name of the column to use as associated location.
        measure (str) --
            The name of the column to use as measure.
        binary (bool, optional) --
            Binarize RCA values to 1 if RCA >= cutoff, or 0 if not.
            Default is `False`
        cutoff (bool, optional) --
            Defines the value to establish the binarization criteria.
            Default is `1.0`

    Returns:
        (polars.LazyFrame) --
            Tidy-data formatted RCA LazyFrame. Note both the input data and the
            output calculation is in tidy-data format.
            Remember to call `.collect()` on the resulting LazyFrame to perform
            the calculation.
    """

    # Get LazyFrame
    lf = df if isinstance(df, pl.LazyFrame) else df.lazy()

    lf = lf.fill_nan(0).fill_null(0)

    # Calculate sum of measure per activity
    total_activity = lf.group_by(activity).agg(
        pl.sum(measure).alias("_sum_by_activity")
    )

    # Calculate sum of measure per location
    total_location = lf.group_by(location).agg(
        pl.sum(measure).alias("_sum_by_location")
    )

    # Merge sums of measure per activity and per location
    merged = lf.join(total_activity, on=activity).join(total_location, on=location)

    # Build the expression for the column division that calculates the RCA
    rca_expr = (pl.col(measure) / pl.col("_sum_by_location")) / (
        pl.col("_sum_by_activity") / pl.sum(measure)
    )
    # Do the calculation
    rca = merged.with_columns(rca_expr.alias(measure + " RCA")).drop(
        ["_sum_by_activity", "_sum_by_location"]
    )

    # Apply binarization of matrix
    if binary:
        rca = rca.with_columns(
            pl.when(pl.col(measure + " RCA") >= cutoff)
            .then(1.0)
            .otherwise(0.0)
            .alias(measure + " RCA")
        )

    return rca
