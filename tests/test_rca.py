import numpy as np
import pandas as pd

import economic_complexity as ec


def test_rca(df_exports):
    pv_exports = pd.pivot_table(
        df_exports,
        values="Trade Value",
        index="Exporter Country ID",
        columns="Section ID",
        aggfunc=np.sum,
    )
    rca = ec.rca(pv_exports)

    section_1 = rca[1].describe().round(6)
    assert section_1["count"] == 226
    assert section_1["mean"] == 3.484895
    assert section_1["std"] == 8.261088
    assert section_1["min"] == 0.000000
    assert section_1["25%"] == 0.129100
    assert section_1["50%"] == 0.718371
    assert section_1["75%"] == 2.165564
    assert section_1["max"] == 47.724923

    section_9 = rca[9].describe().round(6)
    assert section_9["count"] == 226
    assert section_9["mean"] == 1.959028
    assert section_9["std"] == 6.469812
    assert section_9["min"] == 0.000000
    assert section_9["25%"] == 0.040933
    assert section_9["50%"] == 0.267903
    assert section_9["75%"] == 1.264129
    assert section_9["max"] == 75.963223
