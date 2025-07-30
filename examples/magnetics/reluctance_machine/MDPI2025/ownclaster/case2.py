import os

import matplotlib.pyplot as plt
import pandas as pd
from numpy.ma.extras import average
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm
import numpy as np

# Importing precomputed distance matrix and model matrix
df = pd.read_parquet('../eculidean/distance_df_case2_case2.parquet')
df_all = pd.read_csv('../refined/case2_all.csv')

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
out_path = '../ownclaster/case2_s001_e1_p19_average.csv'
os.makedirs(os.path.dirname(out_path), exist_ok=True)

df_filtered = df.copy()

for threshold in tqdm(np.concatenate((np.linspace(0.05, 0.1, 6), np.linspace(0.2, 1, 9)))):
    diff_avg, diff_rip, diff_cog = [], [], []
    df_filtered = df.copy()

    for j in range(length_df):
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

            # Extract torque characteristics
            df_avg = df_torq.iloc[ind_int, -3]
            df_rip = df_torq.iloc[ind_int, -2]
            df_cog = df_torq.iloc[ind_int, -1]

            avg = max([abs(df_torq.iloc[medoid_index, -3] - df_avg.max()),
                       abs(df_torq.iloc[medoid_index, -3] - df_avg.min())])
            rip = max([abs(df_torq.iloc[medoid_index, -2] - df_rip.max()),
                       abs(df_torq.iloc[medoid_index, -2] - df_rip.min())])
            cog = max([abs(df_torq.iloc[medoid_index, -1] - df_cog.max()),
                       abs(df_torq.iloc[medoid_index, -1] - df_cog.min())])

            diff_avg.append(avg)
            diff_rip.append(rip)
            diff_cog.append(cog)

            # Remove all members except medoid
            ind_remaining = [ind for ind in ind_int if ind != medoid_index]
            col_remaining = [str(i) for i in ind_remaining]

            df_filtered.drop(index=ind_remaining, columns=col_remaining, inplace=True)

        except Exception as e:
            continue

    # Save after each threshold
    row = {
        'threshold': threshold,
        'clusters': df_filtered.shape[0],
        'distance_avg': average(diff_avg) if diff_avg else np.nan,
        'distance_rip': average(diff_rip) if diff_rip else np.nan,
        'distance_cog': average(diff_cog) if diff_cog else np.nan
    }

    clusters.append(row)
    df_to_save = pd.DataFrame(clusters).drop_duplicates()
    df_to_save.to_csv(out_path, index=False)
