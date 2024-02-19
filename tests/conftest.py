from pathlib import Path

import pandas as pd
import pytest

import economic_complexity as ec

activity = "Section ID"
location = "Country ID"
measure = "Trade Value"


@pytest.fixture
def df_exports():
    # TODO deprecate in favor of df_global_exports
    path = Path(__file__).joinpath("../fixture_exports.csv").resolve()
    return pd.read_csv(path)


@pytest.fixture
def df_global_exports():
    # ?cube=trade_i_baci_a_92
    # &measures=Trade+Value&drilldowns=Exporter+Country,Section
    # &Year=2019,2020,2021&Trade+Flow=2
    path = Path(__file__) / ".." / "global_exports.csv"
    return pd.read_csv(path.resolve())


@pytest.fixture
def df_rca(df_global_exports):
    df = df_global_exports.pivot(index=location, columns=activity, values=measure)
    return ec.rca(df)


@pytest.fixture
def df_subnat_exports():
    # ?cube=trade_s_esp_m_hs
    # &measures=Trade+Value&drilldowns=Subnat+Geography,Section
    # &Year=2022&Trade+Flow=2
    path = Path(__file__) / ".." / "subnat_exports.csv"
    return pd.read_csv(path.resolve())
