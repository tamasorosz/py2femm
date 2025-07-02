import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.preprocessing import MinMaxScaler

with open('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025/refined\case1_all.csv', 'r') as f:
    df1 = pd.read_csv(f)

with open('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025/refined\case3_all.csv', 'r') as f:
    df3 = pd.read_csv(f)

# Convert 'COG' columns to numpy arrays
avg1 = df1['AVG'].values[:, np.newaxis]  # shape (len(df1), 1)
avg2 = df3['AVG'].values[np.newaxis, :]  # shape (1, len(df2))

# Broadcasted difference: shape (len(df1), len(df2))
avg_diff = avg2 - avg1
avg_diff = np.round(avg_diff,3)
# Optionally, make it a DataFrame with matching indices
avg_diff_df = pd.DataFrame(avg_diff, index=df1.index, columns=df3.index)

avg_diff_df.to_parquet("diff_avg_df_case1_case3.parquet", index=False)