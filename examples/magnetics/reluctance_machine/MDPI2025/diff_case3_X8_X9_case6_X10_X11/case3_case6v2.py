import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.preprocessing import MinMaxScaler

with open('../refined/case3_all.csv', 'r') as f:
    df3 = pd.read_csv(f)

with open('../refined/case6v2_all.csv', 'r') as f:
    df6 = pd.read_csv(f)
df6 = df6.dropna(ignore_index=True)
# Convert 'COG' columns to numpy arrays
CX8 = df3['X8'].values[:, np.newaxis]  # shape (len(df1), 1)
DX10 = df6['X10'].values[np.newaxis, :]  # shape (1, len(df2))

# Broadcasted difference: shape (len(df1), len(df2))
cog_diff = (DX10 - CX8) / 2
cog_diff = np.round(cog_diff,3)
# Optionally, make it a DataFrame with matching indices
cog_diff_df = pd.DataFrame(cog_diff, index=df3.index, columns=df6.index)

print(cog_diff_df)
cog_diff_df.columns = cog_diff_df.columns.astype(str)
cog_diff_df.to_parquet("diff_DX10_CX8_case3_case6v2.parquet", index=False)