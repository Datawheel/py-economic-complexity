import numpy as np
import pandas as pd

import economic_complexity as ecplx


def test_rca(df_exports: pd.DataFrame):
    pv_exports = pd.pivot_table(df_exports, values="Trade Value",
                                            index="Country",
                                            columns="HS4 ID",
                                            aggfunc=np.sum)
    rca = ecplx.rca(pv_exports)

    hs4_0201 = rca[10201].describe().round(6)
    assert hs4_0201["count"] == 226
    assert hs4_0201["mean"] == 1.076052
    assert hs4_0201["std"] ==  4.715384
    assert hs4_0201["min"] ==  0.000000
    assert hs4_0201["25%"] ==  0.000000
    assert hs4_0201["50%"] ==  0.000293
    assert hs4_0201["75%"] ==  0.094575
    assert hs4_0201["max"] == 44.864227

    hs4_9615 = rca[209615].describe().round(6)
    assert hs4_9615["count"] == 226
    assert hs4_9615["mean"] == 0.223670
    assert hs4_9615["std"]  == 0.695201
    assert hs4_9615["min"]  == 0.000000
    assert hs4_9615["25%"]  == 0.000033
    assert hs4_9615["50%"]  == 0.023735
    assert hs4_9615["75%"]  == 0.146443
    assert hs4_9615["max"]  == 6.930755
