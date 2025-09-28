import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.preprocessing import MinMaxScaler

with open('../refined/case1_all.csv', 'r') as f:
    df3 = pd.read_csv(f)

with open('../refined/case6v2_all.csv', 'r') as f:
    df6 = pd.read_csv(f)
df6 = df6.dropna(ignore_index=True)
# Convert 'COG' columns to numpy arrays
avg1 = df3['AVG'].values[:, np.newaxis]  # shape (len(df1), 1)
avg2 = df6['AVG'].values[np.newaxis, :]  # shape (1, len(df2))

# Broadcasted difference: shape (len(df1), len(df2))
avg_diff = avg2 - avg1
avg_diff = np.round(avg_diff,3)
# Optionally, make it a DataFrame with matching indices
avg_diff_df = pd.DataFrame(avg_diff, index=df3.index, columns=df6.index)
avg_diff_df.columns = avg_diff_df.columns.astype(str)
avg_diff_df.to_parquet("diff_avg_df_case1_case6v2.parquet", index=False)