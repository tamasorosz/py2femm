import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.preprocessing import MinMaxScaler

with open('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025/refined\case1_all.csv', 'r') as f:
    df1 = pd.read_csv(f)

with open('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025/refined\case2_all.csv', 'r') as f:
    df2 = pd.read_csv(f)

# Convert 'COG' columns to numpy arrays
rip1 = df1['RIP'].values[:, np.newaxis]  # shape (len(df1), 1)
rip2 = df2['RIP'].values[np.newaxis, :]  # shape (1, len(df2))

# Broadcasted difference: shape (len(df1), len(df2))
rip_diff = rip2 - rip1
rip_diff = np.round(rip_diff,3)
# Optionally, make it a DataFrame with matching indices
rip_diff_df = pd.DataFrame(rip_diff, index=df1.index, columns=df2.index)

rip_diff_df.to_parquet("diff_rip_df_case1_case2.parquet", index=False)