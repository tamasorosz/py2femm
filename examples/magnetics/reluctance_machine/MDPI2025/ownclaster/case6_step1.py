import os
import pandas as pd
from numpy import average
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm
import numpy as np

df = pd.read_parquet('../eculidean/distance_df_case6_case6.parquet')
df_all = pd.read_csv('../refined/case6_all.csv')

del df_all['ANG']
scaler = MinMaxScaler()
scaler.fit(df_all)
df_all = pd.DataFrame(scaler.transform(df_all))
df_torq = df_all.iloc[:, -3:]
df_torq = df_torq.dropna(ignore_index=True)

length_df = len(df.columns)

clusters = []

out_path = ('../ownclaster/case6_m2_s001_e1_average_max_doublecluster_backward_all_noiloc_low.csv')
os.makedirs(os.path.dirname(out_path), exist_ok=True)

for threshold in tqdm(np.linspace(0.01, 0.25, 25)):
    diff_avg, diff_rip, diff_cog = [], [], []
    df_filtered = df.copy()

    for j in range(length_df, -1, -1):
        try:
            ind_int = df_filtered.index[df_filtered[str(j)] < round(threshold,3)].tolist()
            ind_str = [str(i) for i in ind_int]

            if len(ind_int) < 2:
                continue

            distance_matrix = df_filtered[ind_str].loc[ind_int].values

            total_distances = distance_matrix.sum(axis=1)

            medoid_index = ind_int[np.argmin(total_distances)]

            medoid_ind_int = df_filtered.index[df_filtered[str(medoid_index)] < round(threshold,3)].tolist()

            merged = list(set(ind_int + medoid_ind_int))

            df_avg = df_torq.iloc[merged, -3]
            df_rip = df_torq.iloc[merged, -2]
            df_cog = df_torq.iloc[merged, -1]

            avg = max([abs(df_torq.iloc[medoid_index, -3] - df_avg.max()),
                       abs(df_torq.iloc[medoid_index, -3] - df_avg.min())])
            rip = max([abs(df_torq.iloc[medoid_index, -2] - df_rip.max()),
                       abs(df_torq.iloc[medoid_index, -2] - df_rip.min())])
            cog = max([abs(df_torq.iloc[medoid_index, -1] - df_cog.max()),
                       abs(df_torq.iloc[medoid_index, -1] - df_cog.min())])

            diff_avg.append(avg)
            diff_rip.append(rip)
            diff_cog.append(cog)

            ind_remaining = [ind for ind in merged if ind != medoid_index]
            col_remaining = [str(i) for i in ind_remaining]

            df_filtered.drop(index=ind_remaining, columns=col_remaining, inplace=True)

        except Exception as e:
            continue

    row = {
        'threshold': round(threshold,3),
        'clusters': df_filtered.shape[0],
        'distance_avg_average': round(average(diff_avg),3) if diff_avg else np.nan,
        'distance_rip_average': round(average(diff_rip),3) if diff_rip else np.nan,
        'distance_cog_average': round(average(diff_cog),3),
        'distance_avg_max': round(max(diff_avg),3) if diff_avg else np.nan,
        'distance_rip_max': round(max(diff_rip),3) if diff_rip else np.nan,
        'distance_cog_max': round(max(diff_cog),3) if diff_cog else np.nan,
        'medoids': tuple(df_filtered.columns.tolist())
    }

    clusters.append(row)
    df_to_save = pd.DataFrame(clusters).drop_duplicates()
    df_to_save.to_csv(out_path, index=False)
