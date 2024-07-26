import glob as gl
import pandas as pd
import numpy as np
from nptracer.dataLoader import DataLoader

class GengaLoader(DataLoader):
    """GengaLoader
            
    Initializes the GengaLoader with the given path to simulation.

    Attributes:
        path_to_sim (str): Path to the simulation files.
    """
    def __init__(self, path_to_sim):
        super().__init__()

        self.path_to_sim = path_to_sim
        self.file_columns = ['t', 'i1', 'm1', 'r1', 'x1', 'y1', 'z1', 'vx1', 'vy1', 'vz1', 'Sx1', 'Sy1', 'Sz1',\
                         'amin1', 'amax1', 'emin1', 'emax1', 'aecount1', 'aecountT1', 'enccountT1', 'test1']
        self.cols_to_use = self.file_columns[0:10]

        # Get the central mass from the .par file
        with open(self.path_to_sim + 'param.dat', 'r') as file:
            for line in file:
                if 'Central Mass' in line:
                    # Split the line by '=' and strip any whitespace
                    parts = line.split('=')
                    # Convert the extracted part to a float and return it
                    self.central_mass = float(parts[1].strip())
                    break

    def read_coll(self):
        """Read the collision log file and load the results into a dataframe.

        Returns:
            pd.DataFrame: DataFrame containing all collision events in the simulation.
        """

        filename = gl.glob(self.path_to_sim + 'Collisions*')[0]
        nam = ['time', 'indexi', 'mi', 'ri', 'xi', 'yi', 'zi', 'vxi', 'vyi', 'vzi', 'Sxi', \
               'Syi', 'Szi', 'indexj', 'mj', 'rj', 'xj', 'yj', 'zj', 'vxj', 'vyj', 'vzj', 'Sxj', 'Syj', 'Szj']
        df = pd.read_csv(filename, names=nam, sep=' ', index_col=False)

        # Create two new columns indicating which particle survived and which particle as deleted
        # in each collision. For genga, this is determined as follows:
        #    The particle with the larger mass survives
        #    For equal masses, the particle with the larger id survives
        df['s_id'] = np.where(df['mi'] > df['mj'], df['indexi'],
                     np.where(df['mi'] < df['mj'], df['indexj'],
                     np.where(df['indexi'] > df['indexj'], df['indexi'], df['indexj'])))

        df['d_id'] = np.where(df['mi'] > df['mj'], df['indexj'],
                     np.where(df['mi'] < df['mj'], df['indexi'],
                     np.where(df['indexi'] > df['indexj'], df['indexj'], df['indexi'])))

        return df

    def read_snaps(self):
        """Read Snapshots
        
        Reads the snapshot files and concatenates their data into a DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing the concatenated data from all snapshot files.
        """
        files_to_read = gl.glob(self.path_to_sim + '*[0-9]*[0-9].dat')

        alldata = []

        for fn in files_to_read:
            df = pd.read_csv(fn, names=self.file_columns, sep=' ', index_col=False)
            df = df[self.cols_to_use]
            alldata.append(df)

        df_alldata = pd.concat(alldata, ignore_index=True)
        df_alldata.sort_values(by='t', inplace=True, ignore_index=True)

        for idx, c in enumerate(df_alldata.columns):
            df_alldata.rename(columns={c: self.columns[idx]}, inplace=True)

        return df_alldata