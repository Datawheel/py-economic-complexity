import economic_complexity as ec

# TODO add detail to the tests
# eg: check column names, coherent member order


def test_proximity(df_rca):
    prox = ec.proximity(df_rca)
    assert prox.shape == (21, 21)


def test_relatedness(df_rca):
    relt = ec.relatedness(df_rca)
    assert relt.shape == (226, 21)


def test_distance(df_rca):
    dist = ec.distance(df_rca)
    assert dist.shape == (226, 21)


def test_opportunity_gain(df_rca):
    df_eci, df_pci = ec.complexity(df_rca)
    oppg = ec.opportunity_gain(df_rca, pci=df_pci)
    assert oppg.shape == (226, 21)


def test_similarity(df_rca):
    simi = ec.similarity(df_rca)
    assert simi.shape == (226, 226)


def test_pgi(df_global_exports, df_rca):
    pass


def test_peii():
    pass

def test_relative_relatedness(df_rca):
    relt = ec.relative_relatedness(df_rca)
    pass