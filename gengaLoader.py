import glob as gl
import pandas as pd
from DataLoader import DataLoader

class GengaLoader(DataLoader):
    def __init__(self, path_to_sim):
        super().__init__()

        self.path_to_sim = path_to_sim
        self.file_columns = ['t', 'i1', 'm1', 'r1', 'x1', 'y1', 'z1', 'vx1', 'vy1', 'vz1', 'Sx1', 'Sy1', 'Sz1',\
                         'amin1', 'amax1', 'emin1', 'emax1', 'aecount1', 'aecountT1', 'enccountT1', 'test1']
        self.cols_to_use = self.file_columns[0:10]

    def read_snaps(self):
        files_to_read = gl.glob(self.path_to_sim + '*[0-9]*[0-9].dat')[0:10]

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