import os

import numpy as np
import pandas as pd
import taguchi01_def


file_path = os.getcwd() + '/results/' + 'taguchi_res_all.csv'

df = pd.read_csv(file_path)
otg = taguchi01_def.data

df_res = pd.DataFrame([], columns=otg.columns)

for i in range(len(otg.columns)):
    L1 = []
    L2 = []
    L3 = []
    for j, k in enumerate(otg.iloc[:, i]):
        if k == 1:
            L1.append(df.iloc[j,-3])
        elif k == 2:
            L2.append(df.iloc[j, -3])
        else:
            L3.append(df.iloc[j, -3])
    G = [np.round(np.average(L1), 3), np.round(np.average(L2), 3), np.round(np.average(L3), 3)]
    dif = np.round(max(G) - min(G), 3)

    df_res.iloc[:, i] = G + [dif]
    df_res = df_res.rename(index={0: 'L1', 1: 'L2', 2: 'L3', 3: 'R'})

current_dir = os.getcwd()
file_path = current_dir + '/results/' + f'taguchi_res_avg.csv'
df_res.to_csv(file_path, encoding='utf-8', index=False)