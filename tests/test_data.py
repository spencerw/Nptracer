import nptracer.gengaLoader

def test_data_shape():
    loader = gengaLoader.GengaLoader('../simdata/genga/')
    snaps = loader.read_snaps()

    assert snaps.shape == (118, 10)