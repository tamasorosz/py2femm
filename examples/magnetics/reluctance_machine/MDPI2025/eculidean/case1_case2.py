import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.preprocessing import MinMaxScaler

with open('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025/refined\case1_all.csv', 'r') as f:
    df1 = pd.read_csv(f)

with open('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025/refined\case2_all.csv', 'r') as f:
    df2 = pd.read_csv(f)

del df1['ANG']
del df2['ANG']

scaler = MinMaxScaler()

# Ensure both dataframes have only the 8 feature columns in the same order
df1 = df1.iloc[:,:-3]
df2 = df2.iloc[:,:-4]

# Fit on combined data to ensure consistent scaling
combined = pd.concat([df1, df2], axis=0)
scaler.fit(combined)

# Transform both DataFrames
X1_scaled = scaler.transform(df1)
X2_scaled = scaler.transform(df2)

# Compute pairwise Euclidean distances: shape (len(df1), len(df2))
distance_matrix = cdist(X1_scaled, X2_scaled, metric='euclidean')

distance_df = pd.DataFrame(
    distance_matrix,
    index=df1.index,
    columns=df2.index
)

# distance_df.round(3).to_parquet("distance_df_case1_case2.parquet", index=False)

print(distance_df)