import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.preprocessing import MinMaxScaler

df1 = pd.read_csv('../refined/case6v2_all.csv')

del df1['ANG']

scaler = MinMaxScaler()

print(len(df1))
df1 = df1.dropna(ignore_index=True)
print(len(df1))

# print(df1)

# Ensure both dataframes have only the 8 feature columns in the same order
df1 = df1.iloc[:, :-3]

# Fit on combined data to ensure consistent scaling
combined = pd.concat([df1, df1], axis=0)
scaler.fit(combined)

# Transform both DataFrames
X1_scaled = scaler.transform(df1)

# Compute pairwise Euclidean distances: shape (len(df1), len(df2))
distance_matrix = cdist(X1_scaled, X1_scaled, metric='euclidean')

distance_df = pd.DataFrame(
    distance_matrix,
    index=df1.index,
    columns=[str(i) for i in df1.index]
)

distance_df.round(3).to_parquet("distance_df_case6v2_case6v2.parquet", index=False)

print(distance_df)
