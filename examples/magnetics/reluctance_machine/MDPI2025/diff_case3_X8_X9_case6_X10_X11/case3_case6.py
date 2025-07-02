import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.preprocessing import MinMaxScaler

with open('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025/refined\case3_all.csv', 'r') as f:
    df3 = pd.read_csv(f)

with open('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025/refined\case6_all.csv', 'r') as f:
    df6 = pd.read_csv(f)

# Convert 'COG' columns to numpy arrays
CX8 = df3['X8'].values[:, np.newaxis]  # shape (len(df1), 1)
DX9 = df6['X9'].values[np.newaxis, :]  # shape (1, len(df2))

# Broadcasted difference: shape (len(df1), len(df2))
cog_diff = (DX9 - CX8) / 2
cog_diff = np.round(cog_diff,3)
# Optionally, make it a DataFrame with matching indices
cog_diff_df = pd.DataFrame(cog_diff, index=df3.index, columns=df6.index)

print(cog_diff_df)

cog_diff_df.to_parquet("diff_DX9_CX8_case3_case6.parquet", index=False)


# Convert 'COG' columns to numpy arrays
CX9 = df3['X9'].values[:, np.newaxis]  # shape (len(df1), 1)
DX11 = df6['X11'].values[np.newaxis, :]  # shape (1, len(df2))

# Broadcasted difference: shape (len(df1), len(df2))
cog_diff = DX11 - CX9
cog_diff = np.round(cog_diff,3)
# Optionally, make it a DataFrame with matching indices
cog_diff_df = pd.DataFrame(cog_diff, index=df3.index, columns=df6.index)

print(cog_diff_df)

cog_diff_df.to_parquet("diff_DX11_CX9_case3_case6.parquet", index=False)