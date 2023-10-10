from typing import Literal, Union
import polars as pl

from .product_space import calculate_proximity, calculate_relatedness
from .complexity import calculate_complexity
from .rca import calculate_rca

AvailableModel = Literal["rca", "eci", "pci", "proximity", "relatedness"]


def run(
    model: AvailableModel,
    data: Union[pl.DataFrame, pl.LazyFrame],
    *,
    activity: str,
    location: str,
    measure: str,
    binary: bool = False,
    cutoff: float = 1.0,
    iterations: int = 20,
    procedure: Literal["max", "sqrt"] = "max",
) -> pl.DataFrame:
    """
    """

    res_rca = calculate_rca(data,
                            activity=activity,
                            location=location,
                            measure=measure,
                            binary=binary,
                            cutoff=cutoff)
    res_rca = res_rca.collect()

    if model == "rca":
        return res_rca

    elif model in ("eci", "pci"):
        res_eci, res_pci = calculate_complexity(res_rca,
                                                activity=activity,
                                                location=location,
                                                measure=measure,
                                                iterations=iterations)

        return res_eci if model == "eci" else res_pci

    elif model in ("proximity", "relatedness"):
        res_prx = calculate_proximity(res_rca, procedure=procedure)

        if model == "proximity":
            return res_prx

        res_rel = calculate_relatedness(res_rca, res_prx, location=location)
        return res_rel

    raise ValueError("Model '%s' is unknown" % model)
