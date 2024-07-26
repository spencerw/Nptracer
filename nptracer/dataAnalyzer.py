import numpy as np
import pandas as pd
import KeplerOrbit

from nptracer.collisionTree import CollisionTree

class DataAnalyzer:
    """Data Analyzer
    
    A Class to analyze the data from the simulation.
    
    Attributes:
        snap_data (pd.DataFrame): DataFrame containing the concatenated data from all snapshot files.
        snap_data (pd.DataFrame): DataFrame containing the collision log info.
        mCentral (float): mass of the central body 
    """
    def __init__(self, snap_data, coll_data, mCentral):
        a, e, inc, asc_node, omega, M = KeplerOrbit.cart2kep(snap_data['px'].values,
                                                             snap_data['py'].values,
                                                             snap_data['pz'].values,
                                                             snap_data['vx'].values,
                                                             snap_data['vy'].values,
                                                             snap_data['vz'].values,
                                                             mCentral, snap_data['m'].values)
        
        kep_df = pd.DataFrame(np.array([a, e, inc, asc_node, omega, M]).T, 
                              columns=['a', 'e', 'inc', 'asc_node', 'omega', 'M'])
        
        self.snap_data = pd.concat([snap_data.reset_index(drop=True),
                               kep_df.reset_index(drop=True)], axis=1)
        self.coll_data = coll_data
        
        self.t_0 = self.snap_data['t'].min()
        self.t_final = self.snap_data['t'].max()
        self.ids_final = self.snap_data[self.snap_data['t'].values == self.t_final]['id'].values

    def proc_collisions(self):
        """
        Read the collision logfile and place the entries into a tree structure. The root is
        an empty node, the children of the root are the final surviving particles, and the
        leaf nodes represent the initial particles in the simulation.
        """
        print('Building collision trees...')

        # TODO check if serialized version of tree already exists

        self.coll_tree = CollisionTree(self.coll_data)

        # Traverse the tree and verify that the masses match the snapshots
        snap_initial = self.snap_data[self.snap_data['t'].values == self.t_0]

        for idx, child in enumerate(self.coll_tree.root.children):
            t_final = self.snap_data[self.snap_data['id'] == child.id]['t'].max()
            snap_final = self.snap_data[self.snap_data['t'].values == t_final]

            tree_mass = self.coll_tree.get_tree_mass(child)
            child_delta_m = snap_final[snap_final['id'] == child.id]['m'].values[0] - \
                            snap_initial[snap_initial['id'] == child.id]['m'].values[0]

            assert np.isclose(tree_mass, child_delta_m, rtol=1e-5)

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
        df_id = self.snap_data.query(f'id == {id}')
        time = df_id['t'].values
        prop = df_id[prop_name].values

        return time, prop

    def get_time_func(self, prop_name, func='max'):
        """ 
        Get the statistc of the property at each snapshot time.
        
        Args:
            prop_name (string): string of the property name
            func (string): string of the function to apply to the property

        Returns:
            time (np.array): the time of the simulation.
            func_prop (np.array): the statistic of property at each time of the simulation.
        """
        if func == 'max':
            df_func_prop = self.snap_data.groupby('t')[prop_name].max().reset_index()
        elif func == 'min':
            df_func_prop = self.snap_data.groupby('t')[prop_name].min().reset_index()
        elif func == 'mean':
            df_func_prop = self.snap_data.groupby('t')[prop_name].mean().reset_index()
        elif func == 'median':
            df_func_prop = self.snap_data.groupby('t')[prop_name].median().reset_index()

        time = df_func_prop['t'].values
        func_prop = df_func_prop[prop_name].values

        return time, func_prop      
