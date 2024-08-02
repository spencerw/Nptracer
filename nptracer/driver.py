from nptracer.gengaLoader import GengaLoader
from nptracer.changaLoader import ChangaLoader
from nptracer.reboundLoader import ReboundLoader
from nptracer.mercuryLoader import MercuryLoader
from nptracer.dataAnalyzer import DataAnalyzer

class Driver:
    """Driver
    
    A Class to drive the simulation data loading and analysis.
    
    Attributes:
        path_to_sim (str): Path to the simulation files.
        format (str): The format of the simulation files.
    """
    def __init__(self, path_to_sim, format):
        self.path_to_sim = path_to_sim
        self.format = format

        if format == 'genga':
            loader = GengaLoader(self.path_to_sim)
        elif format == 'changa':
            loader = ChangaLoader(self.path_to_sim)
        elif format == 'rebound':
            loader = ReboundLoader(self.path_to_sim)
        elif format == 'mercury':
            loader = MercuryLoader(self.path_to_sim)
        else:
            raise Exception(format + ' is not a valid data format')

        self.snap_data = loader.read_snaps()
        self.coll_data = loader.read_coll()
        
        print('Loaded table with ' + str(len(self.snap_data)) + ' rows and ' + \
              str(len(self.snap_data.columns)) + ' columns')

        self.analyzer = DataAnalyzer(self.snap_data, self.coll_data, loader.central_mass)