import numpy as np
import pandas as pd
import KeplerOrbit

class DataAnalyzer:
    """Data Analyzer
    
    A Class to analyze the data from the simulation.
    
    Attributes:
        data (pd.DataFrame): DataFrame containing the concatenated data from all snapshot files.
        mCentral (float): mass of the central body 
    """
    def __init__(self, data, mCentral):
        a, e, inc, asc_node, omega, M = KeplerOrbit.cart2kep(data['px'].values, 
                                                             data['py'].values,
                                                             data['pz'].values, 
                                                             data['vx'].values,
                                                             data['vy'].values,
                                                             data['vz'].values, 
                                                             mCentral, data['m'].values)
        
        kep_df = pd.DataFrame(np.array([a, e, inc, asc_node, omega, M]).T, 
                              columns=['a', 'e', 'inc', 'asc_node', 'omega', 'M'])
        
        self.data = pd.concat([data.reset_index(drop=True), 
                               kep_df.reset_index(drop=True)], axis=1)
        
        self.t_final = self.data['t'].max()
        self.ids_final = self.data[self.data['t'].values == self.t_final]['id'].values

    def get_time_prop(self, id, prop_name):
        """
        Get the time and the property of the particale with the given id.
        
        Args:
            id (integer): id of the particle
            prop_name (string): string of the property name

        Returns:
            time (np.array): the time of the particle
            prop (np.array): the property of the particle
        """
        df_id = self.data.query(f'id == {id}')
        time = df_id['t'].values
        prop = df_id[prop_name].values

        return time, prop

    def get_time_max(self, prop_name):
        """ 
        Get the property of the particale with the given id.
        
        Args:
            prop_name (string): string of the property name

        Returns:
            time (np.array): the time [sec] of the particle.
            max_prop (np.array): the maximum of property at each time of the particle.
        """
        df_max_prop = self.data.groupby('t')[prop_name].max().reset_index()

        time = df_max_prop['t'].values
        max_prop = df_max_prop[prop_name].values

        return time, max_prop
        
