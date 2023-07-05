from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture
def df_exports():
    path = Path(__file__).joinpath("../fixture_exports.csv").resolve()
    return pd.read_csv(path)
