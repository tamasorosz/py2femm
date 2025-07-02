import pandas as pd

df = pd.read_parquet('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025\eculidean\distance_df_case1_case2.parquet')

mask = df < 0.05
positions = mask.stack()[lambda x: x].index.tolist()
result_df = pd.DataFrame(positions, columns=['Row', 'Column'])
print(result_df)
result_df.to_parquet('similarity_case1_case2.parquet', index=False)