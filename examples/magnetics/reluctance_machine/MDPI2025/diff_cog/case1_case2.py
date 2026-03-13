import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.preprocessing import MinMaxScaler

with open('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025/refined\case1_all.csv', 'r') as f:
    df1 = pd.read_csv(f)

with open('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025/refined\case2_all.csv', 'r') as f:
    df2 = pd.read_csv(f)

# Convert 'COG' columns to numpy arrays
cog1 = df1['COG'].values[:, np.newaxis]  # shape (len(df1), 1)
cog2 = df2['COG'].values[np.newaxis, :]  # shape (1, len(df2))

# Broadcasted difference: shape (len(df1), len(df2))
cog_diff = cog2 - cog1
cog_diff = np.round(cog_diff,3)
# Optionally, make it a DataFrame with matching indices
cog_diff_df = pd.DataFrame(cog_diff, index=df1.index, columns=df2.index)

cog_diff_df.to_parquet("diff_cog_df_case1_case2.parquet", index=False)