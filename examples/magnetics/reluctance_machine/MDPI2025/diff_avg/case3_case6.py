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
avg1 = df3['AVG'].values[:, np.newaxis]  # shape (len(df1), 1)
avg2 = df6['AVG'].values[np.newaxis, :]  # shape (1, len(df2))

# Broadcasted difference: shape (len(df1), len(df2))
avg_diff = avg2 - avg1
avg_diff = np.round(avg_diff,3)
# Optionally, make it a DataFrame with matching indices
avg_diff_df = pd.DataFrame(avg_diff, index=df3.index, columns=df6.index)

avg_diff_df.to_parquet("diff_avg_df_case3_case6.parquet", index=False)