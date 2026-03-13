import os

import numpy as np
import pandas as pd
import taguchi01_def

file_path = os.getcwd() + '/fullfact_res_raw.csv'

df = pd.read_csv(file_path)
otg = taguchi01_def.data

decimal = 3  # rounding

SSB_all = []
for indexer in range(-3, 0):
    SSB = []
    for i in range(len(otg.columns)):
        L1 = []
        L2 = []
        L3 = []
        for j, k in enumerate(otg.iloc[:, i]):
            if k == 1:
                L1.append(df.iloc[j, indexer])
            elif k == 2:
                L2.append(df.iloc[j, indexer])
            else:
                L3.append(df.iloc[j, indexer])

        G = [np.round(np.average(L1), decimal), np.round(np.average(L2), decimal), np.round(np.average(L3), decimal)]
        SSB_L1 = len(L1) * (G[0] - np.mean(list(df.iloc[:, indexer]))) ** 2
        SSB_L2 = len(L2) * (G[1] - np.mean(list(df.iloc[:, indexer]))) ** 2
        SSB_L3 = len(L3) * (G[2] - np.mean(list(df.iloc[:, indexer]))) ** 2

        SSB.append(np.round(SSB_L1 + SSB_L2 + SSB_L3, 4))
    SSB_all.append(SSB)

df_res = pd.DataFrame(SSB_all, columns=otg.columns, index=['AVG', 'RIP', 'COG'])
df_res.loc['SUM'] = df_res.sum()

print(df_res)

current_dir = os.getcwd()
file_path = current_dir + f'/fullfact_res_all.csv'
df_res.to_csv(file_path, encoding='utf-8', index=False)
