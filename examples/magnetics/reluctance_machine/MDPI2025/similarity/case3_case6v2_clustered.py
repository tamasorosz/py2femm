import pandas as pd

df = pd.read_parquet('../eculidean/distance_df_case3_case6v2.parquet')

df_column = pd.read_csv('../ownclaster/case6v2_m2_s001_e1_average_max_doublecluster_backward_all_noiloc_low.csv')
df_row = pd.read_csv('../ownclaster/case3_m2_s001_e1_average_max_doublecluster_backward_all_noiloc_low.csv')

columns_to_keep = df_column.iloc[6,-1].replace("'", "").replace("(", "").replace(")", "").split(', ')
print(len(columns_to_keep))

rows_to_keep =[int(i) for i in df_row.iloc[4, -1].replace("'", "").replace("(", "").replace(")", "").split(', ')]
print(len(rows_to_keep))

df = df[columns_to_keep]
df = df.loc[rows_to_keep]
print(df)

# mask = (df > 0) & (df < 0.02)
mask = df < 0.06
positions = mask.stack()[lambda x: x].index.tolist()
result_df = pd.DataFrame(positions, columns=['Row', 'Column'])
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(result_df)

result_df.to_parquet('similarity_case3_case6v2.parquet', index=False)