from nptracer.gengaLoader import GengaLoader
from nptracer.changaLoader import ChangaLoader
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
            self.data = loader.read_snaps()
        elif format == 'changa':
            loader = ChangaLoader(self.path_to_sim)
            self.data = loader.read_snaps()
        else:
            raise Exception(format + ' is not a valid data format')
        
        print('Loaded table with ' + str(len(self.data)) + ' rows and ' + \
              str(len(self.data.columns)) + ' columns')

        self.analyzer = DataAnalyzer(self.data, loader.central_mass)