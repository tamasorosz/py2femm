import pandas as pd

# df = pd.read_parquet('../eculidean/distance_df_case1_case2.parquet')
#
# df_column = pd.read_csv('../ownclaster/case2_m2_s001_e2_average_doublecluster_forward_all.csv')
# df_row = pd.read_csv('../ownclaster/case1_m2_s001_e2_average_doublecluster_forward_all.csv')
#
# columns_to_keep = df_column.iloc[4,-1].replace("'", "").replace("(", "").replace(")", "").split(', ')
# # print(columns_to_keep)
#
# rows_to_keep =[int(i) for i in df_row.iloc[7, -1].replace("'", "").replace("(", "").replace(")", "").split(', ')]
# # print(rows_to_keep)
#
# df = df[columns_to_keep]
# df = df.loc[rows_to_keep]
# print(df)
#
# mask = df < 0.05
# print(mask)
#
# positions = mask.stack()[lambda x: x].index.tolist()
# result_df = pd.DataFrame(positions, columns=['Row', 'Column'])
#
# # for i in range(len(result_df)):
# #     a = result_df['Row'].iloc[i]
# #     b = result_df['Column'].iloc[i]
# #
# #     reversed_exists = ((result_df['Row'] == b) & (result_df['Column'] == a)).any()
# #
# #     if reversed_exists:
# #         print(f"Reversed pair of ({a}, {b}) found at index {i}")
#
# sorted_df = result_df.sort_values(by='Column')
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(sorted_df)
#
# # result_df.to_parquet('similarity_case1_case2.parquet', index=False)

df = pd.read_parquet('../eculidean/distance_df_case1_case2.parquet')
# print(df)

df_column = pd.read_csv('../ownclaster/case2_m2_s001_e1_average_max_doublecluster_backward_all_noiloc_low.csv')
df_row = pd.read_csv('../ownclaster/case1_m2_s001_e1_average_max_doublecluster_backward_all_noiloc_low.csv')

columns_to_keep = df_column.iloc[6,-1].replace("'", "").replace("(", "").replace(")", "").split(', ')
print(len(columns_to_keep))

rows_to_keep =[int(i) for i in df_row.iloc[6, -1].replace("'", "").replace("(", "").replace(")", "").split(', ')]
print(len(rows_to_keep))

df = df[columns_to_keep]
df = df.loc[rows_to_keep]
print(df)

# mask = (df > 0) & (df < 0.02)
mask = df < 0.05
positions = mask.stack()[lambda x: x].index.tolist()
result_df = pd.DataFrame(positions, columns=['Row', 'Column'])
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(result_df)

# result_df.to_parquet('similarity_case1_case2.parquet', index=False)