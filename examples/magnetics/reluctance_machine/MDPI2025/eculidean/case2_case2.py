import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.preprocessing import MinMaxScaler

with open('../refined/case2_all.csv', 'r') as f:
    df1 = pd.read_csv(f)

del df1['ANG']

scaler = MinMaxScaler()

print(df1)

filtered_df = df1[
    (df1.iloc[:, -1] < 20) &
    (df1.iloc[:, -2] < 12) &
    (df1.iloc[:, -3] < 1400)
]

print(filtered_df)
print(len(filtered_df))

# Ensure both dataframes have only the 8 feature columns in the same order
df1 = filtered_df.iloc[:, :-3]

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

distance_df.round(3).to_parquet("distance_df_case2_case2.parquet", index=False)

# print(distance_df)
