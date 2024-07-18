import os 
cwd = os.getcwd()
print(cwd)

from nptracer.gengaLoader import GengaLoader
from nptracer.changaLoader import ChangaLoader
from nptracer.dataAnalyzer import DataAnalyzer

loader = GengaLoader('/simdata/genga/')
analyzer = DataAnalyzer(loader.read_snaps(), 0.08)
print('hello')

#loader = ChangaLoader('simdata/changa/')
#all_snaps = loader.read_snaps()