import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

import matplotlib
matplotlib.use('Qt5Agg')

colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",  
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

with open('all_res_avg_case2_20250210.csv', 'r') as f:
    df_C2 = pd.read_csv(f)

with open('all_res_cog_case2_20250210.csv', 'r') as f:
    df_temp = pd.read_csv(f)
df_C2["COG"] = df_temp["COG"]
df_C2["MOD"] = 'C2'

df_C2 = df_C2.drop_duplicates(ignore_index=True)

with open('all_res_avg_case7_20250120.csv', 'r') as f:
    df_B2 = pd.read_csv(f)

with open('all_res_cog_case7_20250120.csv', 'r') as f:
    df_temp = pd.read_csv(f)
df_B2["COG"] = df_temp.iloc[:,-1]
df_B2["MOD"] = 'B2'
df_B2["COL"] = 'purple'

df_B2 = df_B2.drop_duplicates()

df_B2 = df_B2[df_B2["RIP"] < 150]
df_C2 = df_C2[df_C2["RIP"] < 150]

# WITH ALL MODELS ------------------------------------------------------------------------------------------------------
# C2 - B2 - AVG - RIP --------------------------------------------------------------------------------------------------
sns.set_style("whitegrid")
plt.figure(figsize=(8, 6))

plt.scatter(df_C2['AVG'] * -1, df_C2['RIP'],
            color=colors[1], label='Case C2',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.scatter(df_B2['AVG'] * -1, df_B2['RIP'],
            color=colors[5], label='Case B2',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.xlabel("Average torque [mNm]", fontsize=16)
plt.ylabel("Torque ripple [%]", fontsize=16)
plt.xticks(np.linspace(500, 2200, 11), fontsize=16)
plt.yticks(np.linspace(10, 150, 8), fontsize=16)
plt.legend(fontsize=16, loc=1, frameon=True)
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig('comp_C2_B2_avg_rip_all.png')
plt.show()

# C2 - B2 - AVG - COG---------------------------------------------------------------------------------------------------
sns.set_style("whitegrid")
plt.figure(figsize=(8, 6))

plt.scatter(df_B2['AVG'] * -1, df_B2['COG'],
            color=colors[5], label='Case B2',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.scatter(df_C2['AVG'] * -1, df_C2['COG'],
            color=colors[1], label='Case C2',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.xlabel("Average torque [mNm]", fontsize=16)
plt.ylabel("Cogging torque [mNm]", fontsize=16)
plt.xticks(np.linspace(500, 2200, 11), fontsize=16)
plt.yticks(np.linspace(13, 23, 11), fontsize=16)
plt.legend(fontsize=16, loc=1, frameon=True)
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig('comp_C2_B2_avg_cog_all.png')
plt.show()

# C2 - B2 - RIP - COG---------------------------------------------------------------------------------------------------
sns.set_style("whitegrid")
plt.figure(figsize=(8, 6))

plt.scatter(df_B2['RIP'], df_B2['COG'],
            color=colors[5], label='Case B2',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.scatter(df_C2['RIP'], df_C2['COG'],
            color=colors[1], label='Case C2',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.xlabel("Torque ripple [%]", fontsize=16)
plt.ylabel("Cogging torque [mNm]", fontsize=16)
plt.xticks(np.linspace(10, 150, 8), fontsize=16)
plt.yticks(np.linspace(13, 23, 11), fontsize=16)
plt.legend(fontsize=16, loc=1, frameon=True)
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig('comp_C2_B2_rip_cog_all.png')
plt.show()

# FILTERED -------------------------------------------------------------------------------------------------------------
df_C2 = df_C2[df_C2["RIP"] < 50]
df_C2 = df_C2[df_C2["AVG"] < -1000]

df_B2 = df_B2[df_B2["RIP"] < 50]
df_B2 = df_B2[df_B2["AVG"] < -1000]

# C2 - B2 - AVG - RIP --------------------------------------------------------------------------------------------------
sns.set_style("whitegrid")
plt.figure(figsize=(8, 6))

plt.scatter(df_C2['AVG'] * -1, df_C2['RIP'],
            color=colors[1], label='Case C2',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.scatter(df_B2['AVG'] * -1, df_B2['RIP'],
            color=colors[5], label='Case B2',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.xlabel("Average torque [mNm]", fontsize=16)
plt.ylabel("Torque ripple [%]", fontsize=16)
plt.xticks(np.linspace(1000, 2200, 7), fontsize=16)
plt.yticks(np.linspace(9, 49, 11), fontsize=16)
plt.legend(fontsize=16, loc=1, frameon=True)
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig('comp_C2_B2_avg_rip.png')
plt.show()

# C2 - B2 - AVG - COG---------------------------------------------------------------------------------------------------
sns.set_style("whitegrid")
plt.figure(figsize=(8, 6))

plt.scatter(df_B2['AVG'] * -1, df_B2['COG'],
            color=colors[5], label='Case B2',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.scatter(df_C2['AVG'] * -1, df_C2['COG'],
            color=colors[1], label='Case C2',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.xlabel("Average torque [mNm]", fontsize=16)
plt.ylabel("Cogging torque [mNm]", fontsize=16)
plt.xticks(np.linspace(1000, 2200, 7), fontsize=16)
plt.yticks(np.linspace(13, 23, 11), fontsize=16)
plt.legend(fontsize=16, loc=1, frameon=True)
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig('comp_C2_B2_avg_cog.png')
plt.show()

# C2 - B2 - RIP - COG---------------------------------------------------------------------------------------------------
sns.set_style("whitegrid")
plt.figure(figsize=(8, 6))

plt.scatter(df_B2['RIP'], df_B2['COG'],
            color=colors[5], label='Case B2',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.scatter(df_C2['RIP'], df_C2['COG'],
            color=colors[1], label='Case C2',
            marker='o', s=80, edgecolors='black', alpha=0.7)

plt.xlabel("Torque ripple [%]", fontsize=16)
plt.ylabel("Cogging torque [mNm]", fontsize=16)
plt.xticks(np.linspace(9, 49, 11), fontsize=16)
plt.yticks(np.linspace(13, 23, 11), fontsize=16)
plt.legend(fontsize=16, loc=1, frameon=True)
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig('comp_C2_B2_rip_cog.png')
plt.show()
