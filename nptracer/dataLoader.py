class DataLoader:
    """DataLoader
    
    A class to load data from simulation files.
    """
    def __init__(self):
        """Initializes the DataLoader with predefined column names."""
        self.columns = ['t', 'id', 'px', 'py', 'pz', 'vx', 'vy', 'vz',\
                        'm', 'r']