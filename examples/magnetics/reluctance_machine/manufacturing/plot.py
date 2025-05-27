import pandas as pd

import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)  # Use full width of the terminal
pd.set_option('display.expand_frame_repr', False)  # Avoid wrapping into multiple lines

# with open('all_res_avg_case6_20250229.csv', 'r') as f:
#     df_B1 = pd.read_csv(f)
#
# with open('all_res_cog_case6_20250229.csv', 'r') as f:
#     df_temp = pd.read_csv(f)
#
# with open('all_res_avg_case6_20250125.csv', 'r') as f:
#     df_Bt1 = pd.read_csv(f)
#
# with open('all_res_cog_case6_20250125.csv', 'r') as f:
#     df_Bt2 = pd.read_csv(f)
#
# df_B1['COG'] = df_temp['COG']
# df_Bt1['COG'] = df_Bt2['COG']
# df_Bt1['X10'] = df_Bt2['X10'] / 2
# df_Bt1['X11'] = df_Bt2['X11'] / 2
#
# df = pd.concat([df_B1, df_Bt1])
# # df = df_B1
# print(len(df))
#
# df = df.drop_duplicates(ignore_index=True)
#
# print(len(df))
#
# #
# # Create 3D figure
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
#
# # Scatter plot
# ax.scatter(df['AVG'], df['RIP'], df['COG'], c=df['COG'], cmap='viridis', marker='o')
#
# # Labels
# ax.set_xlabel("X Axis")
# ax.set_ylabel("Y Axis")
# ax.set_zlabel("Z Axis")
# ax.set_title("3D Scatter Plot")
#
# # plt.show()
#
# # print(df[(df['COG'] < 13.7)])
# print(df[(df['RIP'] < 12) & (df['AVG'] < -1400)])
#
#
# # for i in range(0, 9):
# #     plt.scatter(df_A.iloc[:, i], df_A['COG'])
# #     plt.show()

with open('all_res_avg_case6_20250404_all_variable.csv', 'r') as f:
    df1 = pd.read_csv(f)

with open('all_res_cog_case6_20250404_all_variable.csv', 'r') as f:
    df2 = pd.read_csv(f)

# Get the first 11 columns from both DataFrames
df1_subset = df1.iloc[:, :11]
df2_subset = df2.iloc[:, :11]

# Create a mask of rows in df2 that are also in df1
# Use merge with indicator to find mismatches
merged = df2_subset.merge(df1_subset.drop_duplicates(), how='left', indicator=True)

merged['COG'] = df2['COG']

merged_y = merged[merged['_merge'] != 'left_only'].drop(columns=['_merge'])

# merged_y.to_csv('y.csv', index=False)

# Create a mask of rows in df2 that are also in df1
# Use merge with indicator to find mismatches
merged = df1_subset.merge(df2_subset.drop_duplicates(), how='left', indicator=True)

merged['ANG'] = df1['ANG']
merged['AVG'] = df1['AVG']
merged['RIP'] = df1['RIP']

merged_x = merged[merged['_merge'] != 'left_only'].drop(columns=['_merge'])

# merged_x.to_csv('x.csv', index=False)

dfx_subset = merged_x.iloc[:, :11]
dfy_subset = merged_y.iloc[:, :11]

are_identical = dfx_subset.reset_index(drop=True).equals(dfy_subset.reset_index(drop=True))

merged_x['COG'] = merged_y['COG']

df = merged_x

# df.to_csv('all.csv', index=False)

print(df[(df['COG'] < 16) & (df['RIP'] < 4)])
# print(df[df['X11'] > 6])