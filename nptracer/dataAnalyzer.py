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

    def get_time_prop(self, prop, id):

        #return np array of times, np array of property at each time
        pass

    def get_time_max(self, prop):

        #return np array of times, np array maximum of property at each time
        pass
        
