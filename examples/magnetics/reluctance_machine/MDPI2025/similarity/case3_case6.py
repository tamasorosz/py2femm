import pandas as pd

df = pd.read_parquet('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025\eculidean\distance_df_case3_case6.parquet')

mask = df < 0.07
positions = mask.stack()[lambda x: x].index.tolist()
result_df = pd.DataFrame(positions, columns=['Row', 'Column'])
print(result_df)
result_df.to_parquet('similarity_case3_case6.parquet', index=False)