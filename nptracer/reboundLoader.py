import glob as gl
import pandas as pd
import numpy as np
import rebound
from nptracer.dataLoader import DataLoader

class ReboundLoader(DataLoader):
    """ReboundLoader
            
    Initializes the ReboundLoader with the given path to simulation.

    Attributes:
        path_to_sim (str): Path to the simulation archive file.
    """
    def __init__(self, path_to_sim):
        super().__init__()

        self.path_to_sim = path_to_sim
        self.cols_to_use = ['t', 'index', 'm', 'r', 'x', 'y', 'z', \
                        'vx', 'vy', 'vz']
        self.simarchive = rebound.Simulationarchive(self.path_to_sim)

        # Assume particle 0 is the central mass
        self.central_mass =  self.simarchive[0].particles[0].m

    """
    Get the entire Simarchive object loaded by rebound.

    Returns:
            rebound.Simulationarchive: Simulationarchive object created by Rebound
    """
    def get_simarchive(self):
        return self.simarchive

    def read_coll(self):
        # TODO
        return None

    def read_snaps(self):
        """Read Snapshots
        
        Iterate over the time steps and particles in the Simarchive and concatenates the 
        data into a DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing the concatenated data from all times.
        """

        alldata = np.empty((0, len(self.cols_to_use)))

        # Timestep
        for i, sim in enumerate(self.simarchive):

            # Particle
            for j, part in enumerate(sim.particles[1:]):
                row = np.empty(len(self.cols_to_use))
                row[0] = sim.t

                # Column
                for idx, attr in enumerate(self.cols_to_use[1:]):
                    row[idx + 1] = getattr(part, attr)

                alldata = np.append(alldata, [row], axis=0)

        df_alldata = pd.DataFrame(alldata, columns=self.cols_to_use)
        df_alldata.sort_values(by='t', inplace=True, ignore_index=True)

        for idx, c in enumerate(df_alldata.columns):
            df_alldata.rename(columns={c: self.columns[idx]}, inplace=True)

        return df_alldata