import economic_complexity as ec


def test_complexity(df_rca):
    eci, pci = ec.complexity(df_rca)

    assert eci.size == 226
    assert pci.size == 21
