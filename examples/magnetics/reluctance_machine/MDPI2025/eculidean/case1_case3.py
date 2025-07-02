import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.preprocessing import MinMaxScaler

with open('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025/refined\case1_all.csv', 'r') as f:
    df1 = pd.read_csv(f)

with open('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025/refined\case3_all.csv', 'r') as f:
    df3 = pd.read_csv(f)

del df1['ANG']
del df3['ANG']

scaler = MinMaxScaler()

# Ensure both dataframes have only the 8 feature columns in the same order
df1 = df1.iloc[:,:-3]
df3 = df3.iloc[:,:-4]

# Fit on combined data to ensure consistent scaling
combined = pd.concat([df1, df3], axis=0)
scaler.fit(combined)

# Transform both DataFrames
X1_scaled = scaler.transform(df1)
X2_scaled = scaler.transform(df3)

# Compute pairwise Euclidean distances: shape (len(df1), len(df3))
distance_matrix = cdist(X1_scaled, X2_scaled, metric='euclidean')

distance_df = pd.DataFrame(
    distance_matrix,
    index=df1.index,
    columns=df3.index
)

print(distance_df.min())

distance_df.round(3).to_parquet("distance_df_case1_case3.parquet", index=False)