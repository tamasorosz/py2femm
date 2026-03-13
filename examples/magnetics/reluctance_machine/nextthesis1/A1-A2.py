import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

import matplotlib
matplotlib.use('Qt5Agg')

colors = ["#B90276", '#50237F', '#00A8B0', "#006249", '#525F6B', '#000']

with open('all_res_avg_case3_20250215.csv', 'r') as f:
    df_A1 = pd.read_csv(f)

with open('all_res_cog_case3_20250215.csv', 'r') as f:
    df_temp = pd.read_csv(f)
df_A1["COG"] = df_temp.iloc[:,-1]
df_A1["MOD"] = 'A1'

df_A1 = df_A1.drop_duplicates(ignore_index=True)

with open('all_res_avg_case4_20250221.csv', 'r') as f:
    df_A2 = pd.read_csv(f)

with open('all_res_cog_case4_20250221.csv', 'r') as f:
    df_temp = pd.read_csv(f)
df_A2["COG"] = df_temp.iloc[:,-1]
df_A2["MOD"] = 'A2'

df_A2 = df_A2.drop_duplicates(ignore_index=True)

df_A1 = df_A1[df_A1["RIP"] < 150]
df_A2 = df_A2[df_A2["RIP"] < 150]

# WITH ALL MODELS ------------------------------------------------------------------------------------------------------
# A1 - A2 - AVG - RIP --------------------------------------------------------------------------------------------------
sns.set_style("whitegrid")
plt.figure(figsize=(8, 6))

plt.scatter(df_A1['AVG'] * -1, df_A1['RIP'],
            color=colors[2], label='Case A1',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.scatter(df_A2['AVG'] * -1, df_A2['RIP'],
            color=colors[3], label='Case A2',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.xlabel("Average torque [mNm]", fontsize=16)
plt.ylabel("Torque ripple [%]", fontsize=16)
plt.xticks(np.linspace(500, 2200, 11), fontsize=16)
plt.yticks(np.linspace(10, 150, 8), fontsize=16)
plt.legend(fontsize=16, loc=1, frameon=True)
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig('comp_A1_A2_avg_rip_all.png')
plt.show()

# A1 - A2 - AVG - COG---------------------------------------------------------------------------------------------------
sns.set_style("whitegrid")
plt.figure(figsize=(8, 6))

plt.scatter(df_A2['AVG'] * -1, df_A2['COG'],
            color=colors[3], label='Case A2',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.scatter(df_A1['AVG'] * -1, df_A1['COG'],
            color=colors[2], label='Case A1',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.xlabel("Average torque [mNm]", fontsize=16)
plt.ylabel("Cogging torque [mNm]", fontsize=16)
plt.xticks(np.linspace(500, 2200, 11), fontsize=16)
plt.yticks(np.linspace(13, 23, 11), fontsize=16)
plt.legend(fontsize=16, loc=1, frameon=True)
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig('comp_A1_A2_avg_cog_all.png')
plt.show()

# A1 - A2 - RIP - COG---------------------------------------------------------------------------------------------------
sns.set_style("whitegrid")
plt.figure(figsize=(8, 6))

plt.scatter(df_A2['RIP'], df_A2['COG'],
            color=colors[3], label='Case A2',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.scatter(df_A1['RIP'], df_A1['COG'],
            color=colors[2], label='Case A1',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.xlabel("Torque ripple [%]", fontsize=16)
plt.ylabel("Cogging torque [mNm]", fontsize=16)
plt.xticks(np.linspace(10, 150, 8), fontsize=16)
plt.yticks(np.linspace(13, 23, 11), fontsize=16)
plt.legend(fontsize=16, loc=1, frameon=True)
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig('comp_A1_A2_rip_cog_all.png')
plt.show()

# FILTERED -------------------------------------------------------------------------------------------------------------
df_A1 = df_A1[df_A1["RIP"] < 50]
df_A1 = df_A1[df_A1["AVG"] < -1000]

df_A2 = df_A2[df_A2["RIP"] < 50]
df_A2 = df_A2[df_A2["AVG"] < -1000]

# A1 - A2 - AVG - RIP --------------------------------------------------------------------------------------------------
sns.set_style("whitegrid")
plt.figure(figsize=(8, 6))

plt.scatter(df_A1['AVG'] * -1, df_A1['RIP'],
            color=colors[2], label='Case A1',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.scatter(df_A2['AVG'] * -1, df_A2['RIP'],
            color=colors[3], label='Case A2',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.xlabel("Average torque [mNm]", fontsize=16)
plt.ylabel("Torque ripple [%]", fontsize=16)
plt.xticks(np.linspace(1000, 2200, 7), fontsize=16)
plt.yticks(np.linspace(9, 49, 11), fontsize=16)
plt.legend(fontsize=16, loc=1, frameon=True)
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig('comp_A1_A2_avg_rip.png')
plt.show()

# A1 - A2 - AVG - COG---------------------------------------------------------------------------------------------------
sns.set_style("whitegrid")
plt.figure(figsize=(8, 6))

plt.scatter(df_A2['AVG'] * -1, df_A2['COG'],
            color=colors[3], label='Case A2',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.scatter(df_A1['AVG'] * -1, df_A1['COG'],
            color=colors[2], label='Case A1',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.xlabel("Average torque [mNm]", fontsize=16)
plt.ylabel("Cogging torque [mNm]", fontsize=16)
plt.xticks(np.linspace(1000, 2200, 7), fontsize=16)
plt.yticks(np.linspace(13, 23, 11), fontsize=16)
plt.legend(fontsize=16, loc=1, frameon=True)
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig('comp_A1_A2_avg_cog.png')
plt.show()

# A1 - A2 - RIP - COG---------------------------------------------------------------------------------------------------
sns.set_style("whitegrid")
plt.figure(figsize=(8, 6))

plt.scatter(df_A2['RIP'], df_A2['COG'],
            color=colors[3], label='Case A2',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.scatter(df_A1['RIP'], df_A1['COG'],
            color=colors[2], label='Case A1',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.xlabel("Torque ripple [%]", fontsize=16)
plt.ylabel("Cogging torque [mNm]", fontsize=16)
plt.xticks(np.linspace(9, 49, 11), fontsize=16)
plt.yticks(np.linspace(13, 23, 11), fontsize=16)
plt.legend(fontsize=16, loc=1, frameon=True)
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig('comp_A1_A2_rip_cog.png')
plt.show()
