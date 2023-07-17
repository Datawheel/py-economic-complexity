"""Revealed Comparative Advantage (RCA) module

The Revealed Comparative Advantage is an index introduced by Balassa (1965),
which is used to evaluate the main products to be exported by a country,
and their comparative advantages in relation to the level of world exports
(Hidalgo et al., 2007).
"""

import polars as pl

def rca(
        lf: pl.LazyFrame,
        *,
        activity: str,
        location: str,
        measure: str,
        binary=False
    ) -> pl.DataFrame:
    """Calculates the Revealed Comparative Advantage (RCA) for a pivoted matrix.

    It is important to note that even though the functions do not use a
    parameter in relation to time, the data used for the calculations must
    be per period; for example working with World Exports for the year 2020.
    Also, the index always has to be a geographic level.

    Arguments:
        lf (polars.Lazyframe) -- A table using a geographic index,
            columns with the categories to be evaluated and the measurement of
            the data as values.
        binary: binarize RCA values to 1 if RCA >= 1 or 0 in other case
        
    Returns:
        (polars.DataFrame) -- RCA matrix with real values.
    """
    lf = lf.fill_nan(0).fill_null(0)

    # Calculate sum of measure per activity
    total_activity = lf.groupby(by=activity).agg(
        pl.sum(measure).alias("_sum_by_activity")
    )

    # Calculate sum of measure per location
    total_location = lf.groupby(by=location).agg(
        pl.sum(measure).alias("_sum_by_location")
    )

    # Merge sums of measure per activity and per location
    merged = lf.join(total_activity, on=activity).join(total_location, on=location)

    # Calculate the total sum of the measure
    total_measure = total_activity.select(
        pl.col("_sum_by_activity").alias("_total_measure_sum")
    ).sum()

    # Build the expression for the column division that calculates the RCA
    rca_expr = (
        (pl.col(measure) / pl.col("_sum_by_location"))
        / (pl.col("_sum_by_activity") / pl.first("_total_measure_sum"))
    )
    # Do the calculation
    rca = merged\
        .with_context(total_measure)\
        .with_columns(rca_expr.alias(measure + " RCA"))\
        .drop(["_sum_by_activity", "_sum_by_location"])
    
    if binary:
        rca = rca.with_columns([
            pl.when(pl.col(measure + " RCA") >= 1).then(1.0).otherwise(0.0).alias(measure + " RCA")
        ])

    return rca.collect()
