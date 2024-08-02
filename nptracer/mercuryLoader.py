import glob as gl
import re
import pandas as pd
import numpy as np
import KeplerOrbit as ko
from nptracer.dataLoader import DataLoader

class MercuryLoader(DataLoader):
    """ReboundLoader
            
    Initializes the ReboundLoader with the given path to simulation.

    Attributes:
        path_to_sim (str): Path to the simulation archive file.
    """
    def __init__(self, path_to_sim):
        super().__init__()

        self.path_to_sim = path_to_sim

         # Get the central mass from the .param file
        with open(self.path_to_sim + 'param.in', 'r') as file:
            for line in file:
                if 'central mass' in line:
                    # Split the line by '=' and strip any whitespace
                    parts = line.split('=')
                    # Convert the extracted part to a float and return it
                    self.central_mass = float(parts[1].strip().replace('d', 'e'))
                    break

        # Get densities from initial condition file
        self.den = {}
        pattern = re.compile(r'(\w+)\s+m=[\d\.D\-+]+ r=[\d\.d]+ d=([\d\.D\-]+)')
        with open(self.path_to_sim + 'big.in', 'r') as file:
            lines = file.readlines()
            for line in lines:
                match = pattern.search(line)
                if match:
                    pname = match.group(1)
                    d_value = match.group(2)
                    self.den[pname] = float(d_value.replace('D', 'e'))

    def read_coll(self):
        # TODO
        return None

    def read_snaps(self):
        """Read Snapshots
        
        Iterate over the outputs (one file per particle) and concatenate the results
        in a Pandas dataframe.

        Returns:
            pd.DataFrame: DataFrame containing the concatenated data for all particles.
        """

        files_to_read = gl.glob(self.path_to_sim + '*.aei')

        alldata = []

        colnames = ['Time (years)', 'long', 'M', 'a', 'e', 'i', 'peri', 'node', 'mass']
        for fn in files_to_read:
            df_particle = pd.read_csv(fn, delim_whitespace=True, skiprows=4, header=None, \
                                      names=colnames)
            # Particles in mercury have names
            # Use the filename as the id here
            id = fn.split('.')[0].split('\\')[-1]
            df_particle['id'] = id

            if id in self.den:
                density = self.den[id]
                df_particle['r'] = (3.*df_particle['mass']/(4.*np.pi*density))**(1./3.)
            else:
                df_particle['r'] = 0.0 # Test particle

            alldata.append(df_particle)

        df = pd.concat(alldata, ignore_index=True)
        df.rename(columns={colnames[0]: 't'}, inplace=True)
        df.rename(columns={colnames[-1]: 'm'}, inplace=True)
        df['i'] /= 2*np.pi
        df['node'] /= 2*np.pi
        df['peri'] /= 2*np.pi
        df['M'] /= 2*np.pi

        # Mercury provides keplerian orbital elements
        # Need to convert to cartesian
        for idx, row in df.iterrows():
            X, Y, Z, vx, vy, vz = ko.kep2cart(row['a'], row['e'], row['i'], row['node'], \
                                              row['peri'], row['M'], row['m'], self.central_mass)
            
            df['px'], df['py'], df['pz'] = X, Y, Z
            df['vx'], df['vy'], df['vz'] = vx, vy, vz
        df_alldata = df[['t', 'id', 'm', 'r', 'px', 'py', 'pz', 'vx', 'vy', 'vz']]

        return df_alldata