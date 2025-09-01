import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.preprocessing import MinMaxScaler

with open('../refined\case2_all.csv', 'r') as f:
    df2 = pd.read_csv(f)

with open('../refined\case1_all.csv', 'r') as f:
    df1 = pd.read_csv(f)

AX8 = df1['X8'].values[:, np.newaxis]  # shape (len(df1), 1)
BX9 = df2['X9'].values[np.newaxis, :]  # shape (1, len(df2))

# Broadcasted difference: shape (len(df1), len(df2))
cog_diff = (BX9 - AX8) / 2
cog_diff = np.round(cog_diff,3)
# Optionally, make it a DataFrame with matching indices
cog_diff_df = pd.DataFrame(cog_diff, index=df1.index, columns=df2.index)

print(cog_diff_df)

cog_diff_df.to_parquet("diff_BX9_AX8_case1_case2.parquet", index=False)
#
# # Broadcasted difference: shape (len(df1), len(df2))
# diff = (df2['X9'] - df1['X8']) / 2
# diff = np.round(diff,3)
#
# # Optionally, make it a DataFrame with matching indices
# diff_df = pd.DataFrame({'diff': diff})
#
# print(diff_df)
#
# # diff_df.to_parquet("diff_X9X8.parquet", index=False)