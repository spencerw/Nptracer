import pynbody
import glob as gl
import pandas as pd
import numpy as np
from nptracer.dataLoader import DataLoader

class ChangaLoader(DataLoader):
    """ChangaLoader
    
    A class to load data from Changa simulations.

    Attributes:
        path_to_sim (str): Path to the simulation files.
    """
    def __init__(self, path_to_sim):
        """ChangaLoader
        
        Initializes the ChangaLoader with the given path to simulation.

        Args:
            path_to_sim (str): Path to the simulation files.
        """
        super().__init__()

        self.path_to_sim = path_to_sim

        # Get the central mass from the .param file
        filename = gl.glob(self.path_to_sim + '*.param')
        with open(filename[0], 'r') as file:
            for line in file:
                if 'dCentMass' in line:
                    # Split the line by '=' and strip any whitespace
                    parts = line.split('=')
                    # Convert the extracted part to a float and return it
                    self.central_mass = float(parts[1].strip())
                    break

        self.dDelta = self.read_dDelta()
        
    def read_dDelta(self):
        """Read the dDelta value
        
        Reads the dDelta value from the parameter file.

        Returns:
            float: The dDelta value extracted from the parameter file.
        """
        files_to_read = gl.glob(self.path_to_sim + '*.param')
        with open(files_to_read[0], 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'dDelta' in line:
                    dDelta = float(line.split('=')[1])
                    break
        return dDelta

    def read_coll(self):
        """Read the collision log file and load the results into a dataframe.

        Returns:
            pd.DataFrame: DataFrame containing all collision events in the simulation.
        """

        # TODO add collision file to example ChaNGa data
        return []

        filename = gl.glob(self.path_to_sim + 'collision.log')
        nam = ['time', 'collType', 'iord1', 'iord2', 'm1', 'm2', 'r1', 'r2', 'x1x', 'x1y', 'x1z', 'x2x', 'x2y',\
               'x2z',  'v1x', 'v1y', 'v1z', 'v2x', 'v2y', 'v2z', 'w1x', 'w1y', 'w1z', 'w2x', 'w2y', 'w2z']
        df_coll = pd.read_csv(filename, names=nam, sep=' ', index_col=False)

        return df_coll
        
    def read_snaps(self):
        """Read snapshots
        
        Reads the snapshot files and concatenates their data into a DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing the concatenated data from all snapshot files.
        """
        files_to_read = gl.glob(self.path_to_sim + '*.*[0-9]')
        alldata = []
        
        for i, fn in enumerate(files_to_read):
            step_num = int(fn.split('/')[-1].split('.')[-1])
            snap = pynbody.load(fn)
            
            id = snap['iord'].view(np.ndarray).reshape(-1, 1)
            pos = snap['pos'].view(np.ndarray) # x, y, z
            vel = snap['vel'].view(np.ndarray) # vx, vy, vz
            mass = snap['mass'].view(np.ndarray).reshape(-1, 1)  
            r = 2*snap['eps'].view(np.ndarray).reshape(-1, 1)          
            t = step_num*self.dDelta*np.ones((len(snap), 1))
            
            snaps = np.concatenate((t, id, mass, r, pos, vel), axis=1)
            df_snaps = pd.DataFrame(snaps, columns=self.columns)
            alldata.append(df_snaps)
            
        df_alldata = pd.concat(alldata, ignore_index=True)
        df_alldata.sort_values(by='t', inplace=True, ignore_index=True)

        return df_alldata