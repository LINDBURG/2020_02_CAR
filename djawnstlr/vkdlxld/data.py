import pandas as pd
import numpy
import torch
from torch.utils.data import Dataset
from sklearn.preprocessing import StandardScaler


def process_rows(row):
    ret = []
    ret.append(row['Timestamp'])
    ret.append(numpy.int64(int(row['Arbitration_ID'], 16)))
    ret.append(row['DLC'])
    tmp = row['Data'].split(' ')
    tmp.extend(['00'] * (8 - len(tmp)))
    ret.extend(list(map(lambda x: numpy.int64(int(x, 16)), tmp)))
    if row['Class'] == 'Normal':
        t = 0
    else:
        t = 1
    ret.append(numpy.int64(t))
    print(ret)
    return ret


class CarDataset(Dataset):


    def __init__(self, csv_file):
        
        # Read CSV file
        data_frame = pd.read_csv(csv_file)
        mod_data_lst = []

        # Process rows
        for idx, row in data_frame.iterrows():
            mod_data_lst.append(process_rows(row))

        mod_data_frame = pd.DataFrame(mod_data_lst, columns = ['Timestamp', 'AID', 'DLC', 'Data0', 'Data1', 'Data2', 'Data3', 'Data4', 'Data5', 'Data6', 'Data7', 'Class'])

        n = len(mod_data_frame)
        x_train = mod_data_frame.iloc[0:n, 0:11].values
        y_train = mod_data_frame.iloc[0:n, 11].values
        
        self.x_train = torch.tensor(x_train, dtype=torch.float32)
        self.y_train = torch.tensor(y_train)

    def __len__(self):
        return len(self.y_train)

    def __getitem__(self, idx):
        return self_x_train[idx], self.y_train[idx]



"""
n = 3

data_frame = pd.read_csv('data/train/Cybersecurity_Car_Hacking_S_training-0.csv')

mod_data_lst = []

for idx, row in data_frame.iterrows():
    mod_data_lst.append(process_rows(row))

mod_data_frame = pd.DataFrame(mod_data_lst, columns = ['Timestamp', 'AID', 'DLC', 'Data0', 'Data1', 'Data2', 'Data3', 'Data4', 'Data5', 'Data6', 'Data7', 'Class'])

print(mod_data_frame.iloc[0, :])
"""
