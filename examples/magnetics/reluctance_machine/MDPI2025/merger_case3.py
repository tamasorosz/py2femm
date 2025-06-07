import pandas as pd

with open('all_res_avg_case3_20250421_all_variable.csv', 'r') as f:
    df1 = pd.read_csv(f)

with open('all_res_cog_case3_20250421_all_variable.csv', 'r') as f:
    df2 = pd.read_csv(f)

# Get the first 9 columns from both DataFrames
df1_subset = df1.iloc[:, :9]
df2_subset = df2.iloc[:, :9]

# Create a mask of rows in df2 that are also in df1
# Use merge with indicator to find mismatches
merged = df2_subset.merge(df1_subset.drop_duplicates(), how='left', indicator=True)

merged['COG'] = df2['COG']

merged_y = merged[merged['_merge'] != 'left_only'].drop(columns=['_merge'])

# merged_x.to_csv('case3_cogging.csv', index=False)

# Create a mask of rows in df1 that are also in df2
# Use merge with indicator to find mismatches
merged = df1_subset.merge(df2_subset.drop_duplicates(), how='left', indicator=True)

merged['ANG'] = df1['ANG']
merged['AVG'] = df1['AVG']
merged['RIP'] = df1['RIP']

merged_x = merged[merged['_merge'] != 'left_only'].drop(columns=['_merge'])

# merged_x.to_csv('case3_average.csv', index=False)

dfx_subset = merged_x.iloc[:, :9]
dfy_subset = merged_y.iloc[:, :9]

are_identical = dfx_subset.reset_index(drop=True).equals(dfy_subset.reset_index(drop=True))
print(are_identical)

merged_x['COG'] = merged_y['COG']

merged_x.to_csv('case3_all.csv', index=False)
