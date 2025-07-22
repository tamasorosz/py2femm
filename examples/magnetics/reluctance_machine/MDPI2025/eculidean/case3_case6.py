import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.preprocessing import MinMaxScaler

with open('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025/refined\case3_all.csv', 'r') as f:
    df3 = pd.read_csv(f)

with open('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025/refined\case6_all.csv', 'r') as f:
    df6 = pd.read_csv(f)

del df3['ANG']
del df6['ANG']

#%%%%%%%%%IMPORTANT%%%%%%%%%%%%
#Here I removed df6 X9 and renamed X10 to X9 to keep consistent with the comparison, but do not forget that it is not X9
del df6['X9']
df6.rename(columns={'X10': 'X9'}, inplace=True)

scaler = MinMaxScaler()

# Ensure both dataframes have only the 8 feature columns in the same order
df3 = df3.iloc[:,:-3]
df6 = df6.iloc[:, :-4]

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

# distance_df.round(3).to_parquet("distance_df_case3_case6.parquet", index=False)

print(distance_df.round(4))