import pandas as pd
from matplotlib import pyplot as plt

similarities = pd.read_parquet('..\similarity\similarity_case1_case2.parquet')

sim_row = similarities.iloc[:, 0].values.tolist()
sim_col = similarities.iloc[:, 1].values.tolist()

colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

# COGGING %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
cog = pd.read_parquet('..\diff_cog\diff_cog_df_case1_case2.parquet')

diff_cog = []

for i in range(len(sim_row)):
    diff_cog.append(cog.iloc[sim_row[i], int(sim_col[i])])
    diff_cog.sort()

plt.figure(figsize=(8, 6))
plt.scatter(range(len(sim_row)), diff_cog, label='COG (case B - case A)', color=colors[5])

a = len(diff_cog)
b = len([i for i in diff_cog if i <= 0])
c = len([i for i in diff_cog if i > 0])

plt.axvline(x=359, color='gray', linestyle='--', linewidth=1.5)
plt.axhline(y=0, color='gray', linestyle='--', linewidth=1.5)

plt.fill_between([-5, 359], 0, -6, color=colors[3], alpha=0.3)
plt.text(340, -5.8, f"{round(b/a*100,1)}%",
         fontsize=24, color="black",
         ha="right", va="bottom")

plt.fill_between([359, 513], 0, 3, color=colors[4], alpha=0.3)
plt.text(370, 2.5, f"{round(c/a*100,1)}%",
         fontsize=24, color="black",
         ha="left", va="top")

# Add title and labels
plt.xlabel("Medoid design [-]", fontsize=18)
plt.ylabel("Cogging torque difference [mNm]", fontsize=18)

# Add grid behind the bars
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
plt.gca().set_axisbelow(True)

# Style ticks
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize=18)
plt.tight_layout()
plt.savefig('diff_cog_case1_case2.png', dpi=300)
plt.show()

# AVERAGE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

avg = pd.read_parquet('..\diff_avg\diff_avg_df_case1_case2.parquet')

diff_avg = []

for i in range(len(sim_row)):
    diff_avg.append(avg.iloc[sim_row[i], int(sim_col[i])])
    diff_avg.sort()

plt.figure(figsize=(8, 6))
plt.scatter(range(len(sim_row)), diff_avg, label='AVG (case B - case A)', color=colors[1])

a = len(diff_avg)
b = len([i for i in diff_avg if i <= 0])
c = len([i for i in diff_avg if i > 0])
print(a, b, c)

plt.axvline(x=277, color='gray', linestyle='--', linewidth=1.5)
plt.axhline(y=0, color='gray', linestyle='--', linewidth=1.5)

plt.fill_between([-5, 277], 0, -300, color=colors[3], alpha=0.3)
plt.text(250, -250, f"{round(b/a*100,1)}%",
         fontsize=24, color="black",
         ha="right", va="bottom")

plt.fill_between([277, 513], 0, 300, color=colors[4], alpha=0.3)
plt.text(290, 250, f"{round(c/a*100,1)}%",
         fontsize=24, color="black",
         ha="left", va="top")

# Add title and labels
plt.xlabel("Medoid design [-]", fontsize=18)
plt.ylabel("Average torque difference [mNm]", fontsize=18)

# Add grid behind the bars
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
plt.gca().set_axisbelow(True)

# Style ticks
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize=18)
plt.tight_layout()
plt.savefig('diff_avg_case1_case2.png', dpi=300)
plt.show()

# RIPPLE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
rip = pd.read_parquet('..\diff_rip\diff_rip_df_case1_case2.parquet')

diff_rip = []

for i in range(len(sim_row)):
    diff_rip.append(rip.iloc[sim_row[i], int(sim_col[i])])
    diff_rip.sort()

plt.figure(figsize=(8, 6))
plt.scatter(range(len(sim_row)), diff_rip, label='RIP (case B - case A)', color=colors[2])

a = len(diff_rip)
b = len([i for i in diff_rip if i <= 0])
c = len([i for i in diff_rip if i > 0])
print(a, b, c)

plt.axvline(x=273, color='gray', linestyle='--', linewidth=1.5)
plt.axhline(y=0, color='gray', linestyle='--', linewidth=1.5)

plt.fill_between([-5, 273], 0, -35, color=colors[3], alpha=0.3)
plt.text(250, -32, f"{round(b/a*100,1)}%",
         fontsize=24, color="black",
         ha="right", va="bottom")

plt.fill_between([273, 513], 0, 55, color=colors[4], alpha=0.3)
plt.text(290, 50, f"{round(c/a*100,1)}%",
         fontsize=24, color="black",
         ha="left", va="top")

# Add title and labels
plt.xlabel("Medoid design [-]", fontsize=18)
plt.ylabel("Torque ripple difference [%]", fontsize=18)

# Add grid behind the bars
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
plt.gca().set_axisbelow(True)

# Style ticks
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize=18)
plt.tight_layout()
plt.savefig('diff_rip_case1_case2.png', dpi=300)
plt.show()


X = pd.read_parquet('..\diff_case2_X8_X9\diff_BX9_AX8_case1_case2.parquet')

diff_X = []

for i, j in zip(sim_row, sim_col):
    diff_X.append(X.iloc[int(i), int(j)])

plt.figure(figsize=(8, 6))
plt.hist(diff_X, bins=30, color=colors[6], edgecolor='black', alpha=0.85, label='GAP (case B - case A')

# Add title and labels
plt.xlabel("The width of the gap next to the magnet [deg]", fontsize=18)
plt.ylabel("Frequency", fontsize=18)

# Add grid behind the bars
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
plt.gca().set_axisbelow(True)

# Style ticks
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize=18)
plt.tight_layout()
plt.savefig('diff_X_case1_case2.png', dpi=300)
plt.show()