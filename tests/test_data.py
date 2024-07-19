from nptracer.gengaLoader import GengaLoader

def test_data_shape():
    loader = GengaLoader('../simdata/genga/')
    snaps = loader.read_snaps()

    assert snaps.shape == (118, 10)
