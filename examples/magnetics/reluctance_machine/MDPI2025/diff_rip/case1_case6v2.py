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
rip1 = df3['RIP'].values[:, np.newaxis]  # shape (len(df1), 1)
rip2 = df6['RIP'].values[np.newaxis, :]  # shape (1, len(df2))

# Broadcasted difference: shape (len(df1), len(df2))
rip_diff = rip2 - rip1
rip_diff = np.round(rip_diff,3)
# Optionally, make it a DataFrame with matching indices
rip_diff_df = pd.DataFrame(rip_diff, index=df3.index, columns=df6.index)
rip_diff_df.columns = rip_diff_df.columns.astype(str)
rip_diff_df.to_parquet("diff_rip_df_case1_case6v2.parquet", index=False)