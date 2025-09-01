import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.preprocessing import MinMaxScaler

with open('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025/refined\case3_all.csv', 'r') as f:
    df3 = pd.read_csv(f)

with open('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025/refined\case6_all.csv', 'r') as f:
    df6 = pd.read_csv(f)
df6 = df6.dropna(ignore_index=True)
# Convert 'COG' columns to numpy arrays
cog1 = df3['COG'].values[:, np.newaxis]  # shape (len(df1), 1)
cog2 = df6['COG'].values[np.newaxis, :]  # shape (1, len(df2))

# Broadcasted difference: shape (len(df1), len(df2))
cog_diff = cog2 - cog1
cog_diff = np.round(cog_diff,3)
# Optionally, make it a DataFrame with matching indices
cog_diff_df = pd.DataFrame(cog_diff, index=df3.index, columns=df6.index)

cog_diff_df.to_parquet("diff_cog_df_case3_case6.parquet", index=False)