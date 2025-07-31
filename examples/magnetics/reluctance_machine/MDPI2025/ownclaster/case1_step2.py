import os

import matplotlib.pyplot as plt
import pandas as pd
from numpy.ma.extras import average
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm
import numpy as np

# Importing precomputed distance matrix and model matrix
df = pd.read_parquet('../eculidean/distance_df_case1_case1.parquet')
df_all = pd.read_csv('../refined/case1_all.csv')

# Normalisation of the base data
del df_all['ANG']
scaler = MinMaxScaler()
scaler.fit(df_all)
df_all = pd.DataFrame(scaler.transform(df_all))
df_geom = df_all.iloc[:, :-3]
df_torq = df_all.iloc[:, -3:]

# Creating lists and variables to store data
length_df = len(df)  # length of the precomputed distance matrix for filtering

clusters = []
out_path = '../ownclaster/case1_th015.csv'
os.makedirs(os.path.dirname(out_path), exist_ok=True)

df_filtered = df.copy()

threshold = 0.15

for j in tqdm(range(length_df)):
    try:
        # Find cluster members (rows & columns with distance < threshold)
        ind_int = df_filtered.index[df_filtered[str(j)] < threshold].tolist()
        # print(ind_int)
        if len(ind_int) < 2:
            continue  # Not enough for a cluster

        # Compute distance matrix among cluster members
        distance_matrix = pairwise_distances(df_geom.iloc[ind_int, :], metric='euclidean')
        total_distances = distance_matrix.sum(axis=1)
        medoid_index = ind_int[np.argmin(total_distances)]

        # Remove all members except medoid
        ind_remaining = [ind for ind in ind_int if ind != medoid_index]
        col_remaining = [str(i) for i in ind_remaining]

        df_filtered.drop(index=ind_remaining, columns=col_remaining, inplace=True)

    except Exception as e:
        continue

list_to_save = df_filtered.columns.tolist()
print(len(list_to_save))
with open(out_path, 'w') as f:
    f.write(','.join(list_to_save))