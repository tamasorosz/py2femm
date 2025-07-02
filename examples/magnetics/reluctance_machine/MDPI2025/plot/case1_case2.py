import pandas as pd
from matplotlib import pyplot as plt

similarities = pd.read_parquet('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025\similarity\similarity_case1_case2.parquet')

sim_row = similarities.iloc[:, 0].values.tolist()
sim_col = similarities.iloc[:, 1].values.tolist()

colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

# COGGING %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
cog = pd.read_parquet('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025\diff_cog\diff_cog_df_case1_case2.parquet')

diff_cog = []

for i in range(len(sim_row)):
    diff_cog.append(cog.iloc[sim_row[i], int(sim_col[i])])

plt.figure(figsize=(8, 6))
plt.hist(diff_cog, bins=30, color=colors[2], edgecolor='black', alpha=0.85, label='case B - case A')

# Add title and labels
plt.xlabel("Difference in cogging torque [mNm]", fontsize=18)
plt.ylabel("Frequency", fontsize=18)

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

avg = pd.read_parquet('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025\diff_avg\diff_avg_df_case1_case2.parquet')

diff_avg = []

for i in range(len(sim_row)):
    diff_avg.append(avg.iloc[sim_row[i], int(sim_col[i])])

plt.figure(figsize=(8, 6))
plt.hist(diff_avg, bins=30, color=colors[0], edgecolor='black', alpha=0.85, label='case B - case A')

# Add title and labels
plt.xlabel("Difference in average torque [mNm]", fontsize=18)
plt.ylabel("Frequency", fontsize=18)

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
rip = pd.read_parquet('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025\diff_rip\diff_rip_df_case1_case2.parquet')

diff_rip = []

for i in range(len(sim_row)):
    diff_rip.append(rip.iloc[sim_row[i], int(sim_col[i])])

plt.figure(figsize=(8, 6))
plt.hist(diff_rip, bins=30, color=colors[1], edgecolor='black', alpha=0.85, label='case B - case A')

# Add title and labels
plt.xlabel("Difference in torque ripple [%]", fontsize=18)
plt.ylabel("Frequency", fontsize=18)

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

X = pd.read_parquet('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025\diff_case2_X8_X9\diff_X9X8.parquet')

diff_X = []

for i in sim_row:
    diff_X.append(X.iloc[int(i), 0])

plt.figure(figsize=(8, 6))
plt.hist(diff_X, bins=30, color=colors[6], edgecolor='black', alpha=0.85, label='case B - case A')

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