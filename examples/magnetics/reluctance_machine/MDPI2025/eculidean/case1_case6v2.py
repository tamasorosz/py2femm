import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.preprocessing import MinMaxScaler

with open('../refined/case1_all.csv', 'r') as f:
    df3 = pd.read_csv(f)

with open('../refined/case6v2_all.csv', 'r') as f:
    df6 = pd.read_csv(f)

del df3['ANG']
del df6['ANG']
df6 = df6.dropna(ignore_index=True)

print(df6.head())

scaler = MinMaxScaler()

# Ensure both dataframes have only the 8 feature columns in the same order
df3 = df3.iloc[:,:-3]
df6 = df6.iloc[:, :-5]

# Fit on combined data to ensure consistent scaling
combined = pd.concat([df3, df6], axis=0)
scaler.fit(combined)

# Transform both DataFrames
X1_scaled = scaler.transform(df3)
X2_scaled = scaler.transform(df6)

# Compute pairwise Euclidean distances: shape (len(df1), len(df3))
distance_matrix = cdist(X1_scaled, X2_scaled, metric='euclidean')

distance_df = pd.DataFrame(
    distance_matrix,
    index=df3.index,
    columns=df6.index
)

distance_df.columns = distance_df.columns.astype(str)
distance_df.round(3).to_parquet("distance_df_case1_case6v2.parquet", index=False)

print(distance_df.round(4))