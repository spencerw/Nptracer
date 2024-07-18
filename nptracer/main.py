from nptracer.gengaLoader import GengaLoader
from nptracer.changaLoader import ChangaLoader

loader = GengaLoader('simdata/genga/')
print(loader.read_snaps())

#loader = ChangaLoader('simdata/changa/')
#all_snaps = loader.read_snaps()