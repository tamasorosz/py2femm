import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse

similarities = pd.read_parquet('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025\similarity\similarity_case3_case6.parquet')

sim_row = similarities.iloc[:, 0].values.tolist()
sim_col = similarities.iloc[:, 1].values.tolist()

colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

# # COGGING %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cog = pd.read_parquet('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025\diff_cog\diff_cog_df_case3_case6.parquet')
#
# diff_cog = []
#
# for i in range(len(sim_row)):
#     diff_cog.append(cog.iloc[sim_row[i], int(sim_col[i])])
#
# plt.figure(figsize=(8, 6))
# plt.hist(diff_cog, bins=30, color=colors[2], edgecolor='black', alpha=0.85, label='case D - case C')
#
# # Add title and labels
# plt.xlabel("Difference in cogging torque [mNm]", fontsize=18)
# plt.ylabel("Frequency", fontsize=18)
#
# # Add grid behind the bars
# plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
# plt.gca().set_axisbelow(True)
#
# # Style ticks
# plt.xticks(fontsize=18)
# plt.yticks(fontsize=18)
# plt.legend(fontsize=18)
# plt.tight_layout()
# # plt.savefig('diff_cog_case3_case6.png', dpi=300)
# # plt.show()
#
# # AVERAGE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
# avg = pd.read_parquet('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025\diff_avg\diff_avg_df_case3_case6.parquet')
#
# diff_avg = []
#
# for i in range(len(sim_row)):
#     diff_avg.append(avg.iloc[sim_row[i], int(sim_col[i])])
#
# plt.figure(figsize=(8, 6))
# plt.hist(diff_avg, bins=30, color=colors[0], edgecolor='black', alpha=0.85, label='case D - case C')
#
# # Add title and labels
# plt.xlabel("Difference in average torque [mNm]", fontsize=18)
# plt.ylabel("Frequency", fontsize=18)
#
# # Add grid behind the bars
# plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
# plt.gca().set_axisbelow(True)
#
# # Style ticks
# plt.xticks(fontsize=18)
# plt.yticks(fontsize=18)
# plt.legend(fontsize=18)
# plt.tight_layout()
# # plt.savefig('diff_avg_case3_case6.png', dpi=300)
# # plt.show()
#
# # RIPPLE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# rip = pd.read_parquet('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025\diff_rip\diff_rip_df_case3_case6.parquet')
#
# diff_rip = []
#
# for i in range(len(sim_row)):
#     diff_rip.append(rip.iloc[sim_row[i], int(sim_col[i])])
#
# plt.figure(figsize=(8, 6))
# plt.hist(diff_rip, bins=30, color=colors[1], edgecolor='black', alpha=0.85, label='case D - case C')
#
# # Add title and labels
# plt.xlabel("Difference in torque ripple [%]", fontsize=18)
# plt.ylabel("Frequency", fontsize=18)
#
# # Add grid behind the bars
# plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
# plt.gca().set_axisbelow(True)
#
# # Style ticks
# plt.xticks(fontsize=18)
# plt.yticks(fontsize=18)
# plt.legend(fontsize=18)
# plt.tight_layout()
# # plt.savefig('diff_rip_case3_case6.png', dpi=300)
# # plt.show()

#### NOT COLLIDED ######################################################################################################
# X1 = pd.read_parquet('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025\diff_case3_X8_X9_case6_X10_X11\diff_DX9_CX8_case3_case6.parquet')
#
# X1_ = []
#
# for i in range(len(sim_row)):
#     j = X1.iloc[sim_row[i], int(sim_col[i])]
#     X1_.append(j)
#
# plt.figure(figsize=(8, 6))
# plt.hist(X1_, bins=30, color=colors[6], edgecolor='black', alpha=0.85, label=r'case D - case C ($\epsilon$=0.05)')
#
# # Add title and labels
# plt.xlabel("The width of the air gap next to the magnet [deg]", fontsize=18)
# plt.ylabel("Frequency", fontsize=18)
#
# # Add grid behind the bars
# plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
# plt.gca().set_axisbelow(True)
#
# # Add vertical dashed line at x=0
# plt.plot([0, 0], [0, 100], color='black', linestyle='--', linewidth=3)
#
# # Add red circle at (0, 10) with radius 2
# plt.scatter(0, 15, s=10000, facecolors='none', edgecolors='red', linewidths=2)
#
# plt.xlim(-0.15, 1)
# plt.ylim(0, 100)
#
# # Style ticks
# plt.xticks([-0.15, 0, 0.25, 0.5, 0.75, 1], fontsize=18)
# plt.yticks([25, 50, 75, 100], fontsize=18)
# plt.legend(fontsize=18)
# plt.tight_layout()
# plt.savefig('diff_X9X8_case3_case6_notcollided.png', dpi=300)
# plt.show()

#### COLLIDED ######################################################################################################
X1 = pd.read_parquet('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025\diff_case3_X8_X9_case6_X10_X11\diff_DX9_CX8_case3_case6.parquet')

X1_ = []

for i in range(len(sim_row)):
    j = X1.iloc[sim_row[i], int(sim_col[i])]
    X1_.append(j)

plt.figure(figsize=(8, 6))
plt.hist(X1_, bins=30, color=colors[6], edgecolor='black', alpha=0.85, label=r'case D - case C ($\epsilon$=0.06)')

# Add title and labels
plt.xlabel("The width of the air gap next to the magnet [deg]", fontsize=18)
plt.ylabel("Frequency", fontsize=18)

# Add grid behind the bars
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
plt.gca().set_axisbelow(True)

# Add vertical dashed line at x=0
plt.plot([0, 0], [0, 100], color='black', linestyle='--', linewidth=3)

# Add red ellipse at (0, 15) with width=0.2 and height=50
ellipse = Ellipse(
    xy=(0, 23),        # center
    width=0.2,         # in data units (x-axis)
    height=45,         # in data units (y-axis)
    edgecolor='red',
    facecolor='none',
    linewidth=2
)
plt.gca().add_patch(ellipse)

plt.xlim(-0.15, 1)
plt.ylim(0, 100)

# Style ticks
plt.xticks([-0.15, 0, 0.25, 0.5, 0.75, 1], fontsize=18)
plt.yticks([25, 50, 75, 100], fontsize=18)
plt.legend(fontsize=18)
plt.tight_layout()
plt.savefig('diff_X9X8_case3_case6_collided.png', dpi=300)
plt.show()
