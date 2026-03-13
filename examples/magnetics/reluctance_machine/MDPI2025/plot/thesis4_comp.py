import pandas as pd
from matplotlib import pyplot as plt

similarities = pd.read_parquet('../similarity/similarity_case1_case6v2.parquet')

sim_row = similarities.iloc[:, 0].values.tolist()
sim_col = similarities.iloc[:, 1].values.tolist()

colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

# AVERAGE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
avg = pd.read_parquet('../diff_avg/diff_avg_df_case1_case6v2.parquet')

diff_avg = []

for i in range(len(sim_row)):
    diff_avg.append(avg.iloc[sim_row[i], int(sim_col[i])])
    diff_avg.sort()
diff_avg = diff_avg[6:-3]

plt.figure(figsize=(8, 6))
plt.scatter(range(len(diff_avg)), diff_avg, label='Average torque (case D-A)', color=colors[1])

a = len(diff_avg)
b = len([i for i in diff_avg if i <= 0])
c = len([i for i in diff_avg if i > 0])
print(a, b, c)

plt.axvline(x=624, color='gray', linestyle='--', linewidth=1.5)
plt.axhline(y=0, color='gray', linestyle='--', linewidth=1.5)

plt.fill_between([-5, 624], 0, -230, color=colors[4], alpha=0.3)
plt.text(610, -180, f"{round(b/a*100,1)}%",
         fontsize=24, color="black",
         ha="right", va="bottom")

plt.fill_between([624, 1010], 0, 210, color=colors[3], alpha=0.3)
plt.text(640, 200, f"{round(c/a*100,1)}%",
         fontsize=24, color="black",
         ha="left", va="top")

# Add title and labels
plt.xlabel("Index of compared models [-]", fontsize=18)
plt.ylabel("Difference in average torque [mNm]", fontsize=18)

# Add grid behind the bars
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
plt.gca().set_axisbelow(True)

# Style ticks
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize=18, loc = 4)
plt.tight_layout()
plt.savefig('thesis4_diff_avg.png', dpi=300)
plt.show()
#
# # RIPPLE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
rip = pd.read_parquet('../diff_rip/diff_rip_df_case1_case6v2.parquet')

diff_rip = []

for i in range(len(sim_row)):
    diff_rip.append(rip.iloc[sim_row[i], int(sim_col[i])])
    diff_rip.sort()
diff_rip = diff_rip[5:]

plt.figure(figsize=(8, 6))
plt.scatter(range(len(diff_rip)), diff_rip, label='Torque ripple (case D-A)', color=colors[2])

a = len(diff_rip)
b = len([i for i in diff_rip if i <= 0])
c = len([i for i in diff_rip if i > 0])
print(a, b, c)

plt.axvline(x=824, color='gray', linestyle='--', linewidth=1.5)
plt.axhline(y=0, color='gray', linestyle='--', linewidth=1.5)

plt.fill_between([-5, 824], 0, -30, color=colors[3], alpha=0.3)
plt.text(805, -25, f"{round(b/a*100,1)}%",
         fontsize=24, color="black",
         ha="right", va="bottom")

plt.fill_between([824, 1010], 0, 45, color=colors[4], alpha=0.3)
plt.text(840, 40, f"{round(c/a*100,1)}%",
         fontsize=24, color="black",
         ha="left", va="top")

# Add title and labels
plt.xlabel("Index of compared models [-]", fontsize=18)
plt.ylabel("Difference in torque ripple [%]", fontsize=18)

# Add grid behind the bars
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
plt.gca().set_axisbelow(True)

# Style ticks
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize=18)
plt.tight_layout()
plt.savefig('thesis4_diff_rip.png', dpi=300)
plt.show()

# COGGING %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
cog = pd.read_parquet('../diff_cog/diff_cog_df_case1_case6v2.parquet')

diff_cog = []

for i in range(len(sim_row)):
    diff_cog.append(cog.iloc[sim_row[i], int(sim_col[i])])
    diff_cog = sorted(diff_cog)

plt.figure(figsize=(8, 6))
plt.scatter(range(len(sim_row)), diff_cog, label='Cogging torque (case D-A)', color=colors[5])

a = len(diff_cog)
b = len([i for i in diff_cog if i <= 0])
c = len([i for i in diff_cog if i > 0])
print(a, b, c)

plt.axvline(x=797, color='gray', linestyle='--', linewidth=1.5)
plt.axhline(y=0, color='gray', linestyle='--', linewidth=1.5)

plt.fill_between([-5, 797], 0, -7.75, color=colors[3], alpha=0.3)
plt.text(780, -7.5, f"{round(b/a*100,1)}%",
         fontsize=24, color="black",
         ha="right", va="bottom")

plt.fill_between([797, 1006], 0, 3.5, color=colors[4], alpha=0.3)
plt.text(815, 3.25, f"{round(c/a*100,1)}%",
         fontsize=24, color="black",
         ha="left", va="top")

# Add title and labels
plt.xlabel("Index of compared models [-]", fontsize=18)
plt.ylabel("Difference in cogging torque [mNm]", fontsize=18)

# Add grid behind the bars
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
plt.gca().set_axisbelow(True)

# Style ticks
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize=18)
plt.tight_layout()
plt.savefig('thesis4_comp_cog', dpi=300)
plt.show()
