import pandas as pd

import matplotlib
import seaborn as sns

matplotlib.use('Qt5Agg')

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)  # Use full width of the terminal
pd.set_option('display.expand_frame_repr', False)  # Avoid wrapping into multiple lines

with open('all_res_avg_case3_20250215.csv', 'r') as f:
    df_A1 = pd.read_csv(f)

with open('all_res_cog_case3_20250215.csv', 'r') as f:
    df_temp = pd.read_csv(f)
df_A1["COG"] = df_temp.iloc[:,-1]
df_A1["MOD"] = 'A1'
df_A1["COL"] = 'red'
# print(len(df_A1))
df_A1 = df_A1.drop_duplicates()
# print(len(df_A1))

with open('all_res_avg_case4_20250221.csv', 'r') as f:
    df_A2 = pd.read_csv(f)

with open('all_res_cog_case4_20250221.csv', 'r') as f:
    df_temp = pd.read_csv(f)
df_A2["COG"] = df_temp.iloc[:,-1]
df_A2["MOD"] = 'A2'
df_A2["COL"] = 'blue'
# print(len(df_A2))
df_A2 = df_A2.drop_duplicates()
# print(len(df_A2))

with open('all_res_avg_case6_20250229.csv', 'r') as f:
    df_B1 = pd.read_csv(f)

with open('all_res_cog_case6_20250229.csv', 'r') as f:
    df_temp = pd.read_csv(f)

with open('all_res_avg_case6_20250125.csv', 'r') as f:
    df_Bt1 = pd.read_csv(f)

with open('all_res_cog_case6_20250125.csv', 'r') as f:
    df_Bt2 = pd.read_csv(f)

df_B1['COG'] = df_temp['COG']
df_Bt1['COG'] = df_Bt2['COG']
df_Bt1['X10'] = df_Bt2['X10'] / 2
df_Bt1['X11'] = df_Bt2['X11'] / 2

df_B1 = pd.concat([df_B1, df_Bt1])
df_B1["MOD"] = 'B1'
df_B1["COL"] = 'yellow'

# print(len(df_B1))
df_B1 = df_B1.drop_duplicates()
# print(len(df_B1))

with open('all_res_avg_case7_20250120.csv', 'r') as f:
    df_B2 = pd.read_csv(f)

with open('all_res_cog_case7_20250120.csv', 'r') as f:
    df_temp = pd.read_csv(f)
df_B2["COG"] = df_temp.iloc[:,-1]
df_B2["MOD"] = 'B2'
df_B2["COL"] = 'purple'

# print(len(df_B2))
df_B2 = df_B2.drop_duplicates()
# print(len(df_B2))

with open('all_res_avg_case1_20250205.csv', 'r') as f:
    df_C1 = pd.read_csv(f)

with open('all_res_cog_case1_20250205.csv', 'r') as f:
    df_temp = pd.read_csv(f)
df_C1["COG"] = df_temp["COG"]
df_C1["MOD"] = 'C1'
df_C1["COL"] = 'black'

with open('all_res_avg_case2_20250210.csv', 'r') as f:
    df_C2 = pd.read_csv(f)

with open('all_res_cog_case2_20250210.csv', 'r') as f:
    df_temp = pd.read_csv(f)
df_C2["COG"] = df_temp["COG"]
df_C2["MOD"] = 'C2'
df_C2["COL"] = 'brown'

# print(len(df_C2))
df_C2 = df_C2.drop_duplicates(ignore_index=True)
# print(len(df_C2))
#
# print(df_C1.head())
# print(df_C2.head())


df_all = pd.concat([df_C1.iloc[:,-5:],  df_C2.iloc[:,-5:], df_A1.iloc[:,-5:], df_A2.iloc[:,-5:], df_B1.iloc[:,-5:], df_B2.iloc[:,-5:]], ignore_index=True)
# # print(df_all.head())
df_A = pd.concat([df_A1, df_A2])
df_B = pd.concat([df_B1, df_B2])

# plt.scatter(df_B1['AVG'] * -1, df_B1['RIP'])
# plt.scatter(df_C2['AVG'] * -1, df_C2['RIP'])
# plt.show()
#
# df_B1 = df_B1[df_B1["RIP"] < 50]
# df_B1 = df_B1[df_B1["AVG"] < -500]
#
# df_C2 = df_C2[df_C2["RIP"] < 50]
# df_C2 = df_C2[df_C2["AVG"] < -500]
#
# plt.scatter(df_B1['AVG'] * -1, df_B1['RIP'])
# plt.scatter(df_C2['AVG'] * -1, df_C2['RIP'])
# plt.show()

# plt.scatter(df_B1['AVG'] * -1, df_B1['COG'])
# plt.scatter(df_C2['AVG'] * -1, df_C2['COG'])
# plt.show()
#
# df_B1 = df_B1[df_B1["COG"] < 16]
# df_B1 = df_B1[df_B1["AVG"] < -1000]
#
# df_C2 = df_C2[df_C2["COG"] < 16]
# df_C2 = df_C2[df_C2["AVG"] < -1000]
#
# plt.scatter(df_B1['AVG'] * -1, df_B1['COG'])
# plt.scatter(df_C2['AVG'] * -1, df_C2['COG'])
# plt.show()

# plt.scatter(df_C1['AVG'] * -1, df_C1['RIP'])
# plt.scatter(df_C2['AVG'] * -1, df_C2['RIP'])
# plt.show()
#
# df_C1 = df_C1[df_C1["RIP"] < 50]
# df_C1 = df_C1[df_C1["AVG"] < -1000]
#
# df_C2 = df_C2[df_C2["RIP"] < 50]
# df_C2 = df_C2[df_C2["AVG"] < -1000]
#
# plt.scatter(df_C1['AVG'] * -1, df_C1['RIP'])
# plt.scatter(df_C2['AVG'] * -1, df_C2['RIP'])
# plt.show()



# plt.scatter(df_C2['AVG'] * -1, df_C2['COG'])
# plt.scatter(df_C1['AVG'] * -1, df_C1['COG'])
# plt.show()



#
print((df_all[(df_all["COG"] < 15)]))
#
# df_all = df_all[df_all['RIP'] < 40]
# df_all = df_all[df_all['AVG'] < -1400]
#
# # Create 3D figure
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
#
# # Scatter plot
# ax.scatter(df_all['AVG'], df_all['RIP'], df_all['COG'], c=df_all['COL'], cmap='viridis', marker='o')
#
# # Labels
# ax.set_xlabel("X Axis")
# ax.set_ylabel("Y Axis")
# ax.set_zlabel("Z Axis")
# ax.set_title("3D Scatter Plot")
#
# plt.show()
#
# print(len(df_all))
#
# print(df_all[df_all['COG'] < 15])

# for i in range(0, 11):
#     plt.scatter(df_B.iloc[:, i], df_B['COG'])
#     plt.title(f'BX{i+1}')
#     plt.show()
# df_B['AVG'] = df_B['AVG'] * -1
# df_B['ANG'] = df_B['ANG'] * -1
# df_B = df_B.drop('MOD', axis=1)
# # df_B = df_B.drop('X4', axis=1)
# # df_B = df_B.drop('X7', axis=1)
# correlation_matrix = df_B.corr()
# # Select the last 4 columns for the X-axis and first 7 columns for the Y-axis
# subset = correlation_matrix.iloc[-3:, :11]
#
# # Plotting the heatmap
# plt.figure(figsize=(8, 6))
# sns.heatmap(subset, annot=True, cmap='coolwarm', fmt='.2f')
#
# # Show the plot
# plt.show()

# df_A['AVG'] = df_A['AVG'] * -1
# df_A['ANG'] = df_A['ANG'] * -1
# df_A = df_A.drop('MOD', axis=1)
# df_A = df_A.drop('X4', axis=1)
# df_A = df_A.drop('X6', axis=1)
# df_A = df_A.drop('X7', axis=1)
# correlation_matrix = df_A.corr()
# # Select the last 4 columns for the X-axis and first 7 columns for the Y-axis
# subset = correlation_matrix.iloc[-4:, :6]
#
# # Plotting the heatmap
# plt.figure(figsize=(8, 6))
# sns.heatmap(subset, annot=True, cmap='coolwarm', fmt='.2f')
#
# # Show the plot
# plt.show()

# df_C1['AVG'] = df_C1['AVG'] * -1
# df_C1['ANG'] = df_C1['ANG'] * -1
# df_C1 = df_C1.drop('MOD', axis=1)
# # df_A = df_A.drop('X4', axis=1)
# # df_A = df_A.drop('X6', axis=1)
# # df_A = df_A.drop('X7', axis=1)
# correlation_matrix = df_C1.corr()
# # Select the last 4 columns for the X-axis and first 7 columns for the Y-axis
# subset = correlation_matrix.iloc[-3:, :8]
#
# # Plotting the heatmap
# plt.figure(figsize=(8, 6))
# sns.heatmap(subset, annot=True, cmap='coolwarm', fmt='.2f')
#
# # Show the plot
# plt.show()
#
# df_A['AVG'] = df_A['AVG'] * -1
# df_A['ANG'] = df_A['ANG'] * -1
# df_A = df_A.drop('MOD', axis=1)
# # df_A = df_A.drop('X4', axis=1)
# # df_A = df_A.drop('X6', axis=1)
# # df_A = df_A.drop('X7', axis=1)
# correlation_matrix = df_A.corr()
# # Select the last 4 columns for the X-axis and first 7 columns for the Y-axis
# subset = correlation_matrix.iloc[-3:, :9]
#
# # Plotting the heatmap
# plt.figure(figsize=(8, 6))
# sns.heatmap(subset, annot=True, cmap='coolwarm', fmt='.2f')
#
# # Show the plot
# plt.show()
#
# df_C2['AVG'] = df_C2['AVG'] * -1
# df_C2['ANG'] = df_C2['ANG'] * -1
# df_C2 = df_C2.drop('MOD', axis=1)
# # df_A = df_A.drop('X4', axis=1)
# # df_A = df_A.drop('X6', axis=1)
# # df_A = df_A.drop('X7', axis=1)
# correlation_matrix = df_C2.corr()
# # Select the last 4 columns for the X-axis and first 7 columns for the Y-axis
# subset = correlation_matrix.iloc[-3:, :9]
#
# # Plotting the heatmap
# plt.figure(figsize=(8, 6))
# sns.heatmap(subset, annot=True, cmap='coolwarm', fmt='.2f')
#
# # Show the plot
# plt.show()
#
# df_B['AVG'] = df_B['AVG'] * -1
# df_B['ANG'] = df_B['ANG'] * -1
# df_B = df_B.drop('MOD', axis=1)
# # df_B = df_B.drop('X4', axis=1)
# # df_B = df_B.drop('X7', axis=1)
# correlation_matrix = df_B.corr()
# # Select the last 4 columns for the X-axis and first 7 columns for the Y-axis
# subset = correlation_matrix.iloc[-3:, :11]
#
# # Plotting the heatmap
# plt.figure(figsize=(8, 6))
# sns.heatmap(subset, annot=True, cmap='coolwarm', fmt='.2f')
#
# # Show the plot
# plt.show()


