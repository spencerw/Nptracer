import numpy as np
import pandas as pd
import KeplerOrbit

class DataAnalyzer:
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

        #return np array of times, np array of property at each time

        df_id = self.data.query(f'id == {id}')
        time = df_id['t'].values
        prop = df_id[prop_name].values

        return time, prop

    def get_time_func(self, prop_name, func='max'):
        #return np array of times, np array maximum of property at each time
        if func == 'max':
            df_func_prop = self.data.groupby('t')[prop_name].max().reset_index()
        elif func == 'min':
            df_func_prop = self.data.groupby('t')[prop_name].min().reset_index()
        elif func == 'mean':
            df_func_prop = self.data.groupby('t')[prop_name].mean().reset_index()
        elif func == 'median':
            df_func_prop = self.data.groupby('t')[prop_name].median().reset_index()

        time = df_func_prop['t'].values
        func_prop = df_func_prop[prop_name].values

        return time, func_prop
        
