import os

import numpy as np
import pandas as pd

file_path1 = os.getcwd() + '/taguchi_res_raw.csv'
file_path2 = os.getcwd() + '/fullfact_res_raw.csv'

df1 = pd.read_csv(file_path1)
df2 = pd.read_csv(file_path2)

del df1['X5']
del df1['X6']

print('TAGUCHI (AVG): ', min(df1['Tavg']), np.round(np.mean(df1['Tavg']), 2), max(df1['Tavg']))
print('FULLFACT (AVG): ', min(df2['Tavg']), np.round(np.mean(df2['Tavg']), 2), max(df2['Tavg']))
print()
print('TAGUCHI (RIP): ', min(df1['Trip']), np.round(np.mean(df1['Trip']), 2), max(df1['Trip']))
print('FULLFACT (RIP): ', min(df2['Trip']), np.round(np.mean(df2['Trip']), 2), max(df2['Trip']))
print()
print('TAGUCHI (COG): ', min(df1['Tcog']), np.round(np.mean(df1['Tcog']), 2), max(df1['Tcog']))
print('FULLFACT (COG): ', min(df2['Tcog']), np.round(np.mean(df2['Tcog']), 2), max(df2['Tcog']))