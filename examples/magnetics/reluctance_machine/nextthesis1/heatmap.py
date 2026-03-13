import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

with open('all_res_avg_case3_20250215.csv', 'r') as f:
    df_A1 = pd.read_csv(f)

with open('all_res_cog_case3_20250215.csv', 'r') as f:
    df_temp = pd.read_csv(f)
df_A1["COG"] = df_temp.iloc[:,-1]
df_A1["MOD"] = 'A1'
df_A1["COL"] = 'red'

df_A1 = df_A1.drop_duplicates()

with open('all_res_avg_case4_20250221.csv', 'r') as f:
    df_A2 = pd.read_csv(f)

with open('all_res_cog_case4_20250221.csv', 'r') as f:
    df_temp = pd.read_csv(f)
df_A2["COG"] = df_temp.iloc[:,-1]
df_A2["MOD"] = 'A2'
df_A2["COL"] = 'blue'

df_A2 = df_A2.drop_duplicates()

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

df_B1 = df_B1.drop_duplicates()

with open('all_res_avg_case7_20250120.csv', 'r') as f:
    df_B2 = pd.read_csv(f)

with open('all_res_cog_case7_20250120.csv', 'r') as f:
    df_temp = pd.read_csv(f)
df_B2["COG"] = df_temp.iloc[:,-1]
df_B2["MOD"] = 'B2'
df_B2["COL"] = 'purple'

df_B2 = df_B2.drop_duplicates()

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

df_C2 = df_C2.drop_duplicates(ignore_index=True)

df_all = pd.concat([df_C1.iloc[:,-5:],  df_C2.iloc[:,-5:], df_A1.iloc[:,-5:], df_A2.iloc[:,-5:], df_B1.iloc[:,-5:], df_B2.iloc[:,-5:]], ignore_index=True)

df_A = pd.concat([df_A1, df_A2])
df_B = pd.concat([df_B1, df_B2])

# # C1 -------------------------------------------------------------------------------------------------------------------
# df_C1['AVG'] = df_C1['AVG'] * -1
# df_C1['ANG'] = df_C1['ANG'] * -1
# df_C1 = df_C1.drop('MOD', axis=1)
# df_C1 = df_C1.drop('COL', axis=1)
# correlation_matrix = df_C1.corr()
# plt.figure(figsize=(8, 6))
# subset = correlation_matrix.iloc[-3:, :8]
# sns.heatmap(subset, annot=True, cmap='coolwarm', fmt='.2f')
# plt.xticks(fontsize=14, rotation=0, ha='center')
# plt.yticks(fontsize=14, rotation=0)
#
# for text in plt.gca().texts:
#     text.set_fontsize(14)
#     text.set_fontweight('bold')
#
# plt.tight_layout()
# plt.savefig('heatmap_C1.png', dpi=300)
# plt.show()

# # C2 -------------------------------------------------------------------------------------------------------------------
# df_C2['AVG'] = df_C2['AVG'] * -1
# df_C2['ANG'] = df_C2['ANG'] * -1
# df_C2 = df_C2.drop('MOD', axis=1)
# df_C2 = df_C2.drop('COL', axis=1)
# correlation_matrix = df_C2.corr()
# plt.figure(figsize=(8, 6))
# subset = correlation_matrix.iloc[-3:, :9]
# sns.heatmap(subset, annot=True, cmap='coolwarm', fmt='.2f')
# plt.xticks(fontsize=14, rotation=0, ha='center')
# plt.yticks(fontsize=14, rotation=0)
#
# for text in plt.gca().texts:
#     text.set_fontsize(14)
#     text.set_fontweight('bold')
#
# plt.tight_layout()
# plt.savefig('heatmap_C2.png', dpi=300)
# plt.show()

# # A1 -------------------------------------------------------------------------------------------------------------------
# df_A1['AVG'] = df_A1['AVG'] * -1
# df_A1['ANG'] = df_A1['ANG'] * -1
# df_A1 = df_A1.drop('MOD', axis=1)
# df_A1 = df_A1.drop('COL', axis=1)
# correlation_matrix = df_A1.corr()
# plt.figure(figsize=(8, 6))
# subset = correlation_matrix.iloc[-3:, :9]
# sns.heatmap(subset, annot=True, cmap='coolwarm', fmt='.2f')
# plt.xticks(fontsize=14, rotation=0, ha='center')
# plt.yticks(fontsize=14, rotation=0)
#
# for text in plt.gca().texts:
#     text.set_fontsize(14)
#     text.set_fontweight('bold')
#
# plt.tight_layout()
# plt.savefig('heatmap_A1.png', dpi=300)
# plt.show()

# # A2 -------------------------------------------------------------------------------------------------------------------
# df_A2['AVG'] = df_A2['AVG'] * -1
# df_A2['ANG'] = df_A2['ANG'] * -1
# df_A2 = df_A2.drop('MOD', axis=1)
# df_A2 = df_A2.drop('COL', axis=1)
# correlation_matrix = df_A2.corr()
# plt.figure(figsize=(8, 6))
# subset = correlation_matrix.iloc[-3:, :9]
# sns.heatmap(subset, annot=True, cmap='coolwarm', fmt='.2f')
# plt.xticks(fontsize=14, rotation=0, ha='center')
# plt.yticks(fontsize=14, rotation=0)
#
# for text in plt.gca().texts:
#     text.set_fontsize(14)
#     text.set_fontweight('bold')
#
# plt.tight_layout()
# plt.savefig('heatmap_A2.png', dpi=300)
# plt.show()

# # B1 -------------------------------------------------------------------------------------------------------------------
# df_B1['AVG'] = df_B1['AVG'] * -1
# df_B1['ANG'] = df_B1['ANG'] * -1
# df_B1 = df_B1.drop('MOD', axis=1)
# df_B1 = df_B1.drop('COL', axis=1)
# correlation_matrix = df_B1.corr()
# plt.figure(figsize=(8, 6))
# subset = correlation_matrix.iloc[-3:, :11]
# sns.heatmap(subset, annot=True, cmap='coolwarm', fmt='.2f')
# plt.xticks(fontsize=14, rotation=0, ha='center')
# plt.yticks(fontsize=14, rotation=0)
#
# for text in plt.gca().texts:
#     text.set_fontsize(10)
#     text.set_fontweight('bold')
#
# plt.tight_layout()
# plt.savefig('heatmap_B1.png', dpi=300)
# plt.show()

# B2 -------------------------------------------------------------------------------------------------------------------
df_B2['AVG'] = df_B2['AVG'] * -1
df_B2['ANG'] = df_B2['ANG'] * -1
df_B2 = df_B2.drop('MOD', axis=1)
df_B2 = df_B2.drop('COL', axis=1)
correlation_matrix = df_B2.corr()
plt.figure(figsize=(8, 6))
subset = correlation_matrix.iloc[-3:, :11]
sns.heatmap(subset, annot=True, cmap='coolwarm', fmt='.2f')
plt.xticks(fontsize=14, rotation=0, ha='center')
plt.yticks(fontsize=14, rotation=0)

for text in plt.gca().texts:
    text.set_fontsize(10)
    text.set_fontweight('bold')

plt.tight_layout()
plt.savefig('heatmap_B2.png', dpi=300)
plt.show()


# df_B['AVG'] = df_B['AVG'] * -1
# df_B['ANG'] = df_B['ANG'] * -1
# df_B = df_B.drop('MOD', axis=1)
# correlation_matrix = df_B.corr()
#
# subset = correlation_matrix.iloc[-3:, :11]
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
#
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