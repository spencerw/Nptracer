from gengaLoader import GengaLoader
from changaLoader import ChangaLoader

# loader = GengaLoader('simdata/genga/')
# print(loader.read_snaps())

loader = ChangaLoader('simdata/changa/')
all_snaps = loader.read_snaps()