import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse

similarities = pd.read_parquet('../similarity/similarity_case3_case6v2.parquet')

sim_row = similarities.iloc[:, 0].values.tolist()
sim_col = similarities.iloc[:, 1].values.tolist()

colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

# # COGGING %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cog = pd.read_parquet('../diff_cog/diff_cog_df_case3_case6v2.parquet')
#
# diff_cog = []
#
# for i in range(len(sim_row)):
#     diff_cog.append(cog.iloc[sim_row[i], int(sim_col[i])])
#     diff_cog = sorted(diff_cog)
#
# plt.figure(figsize=(8, 6))
# plt.scatter(range(len(sim_row)), diff_cog, label='COG (case D - case C)', color=colors[5])
#
# a = len(diff_cog)
# b = len([i for i in diff_cog if i <= 0])
# c = len([i for i in diff_cog if i > 0])
# print(a, b, c)
#
# plt.axvline(x=38, color='gray', linestyle='--', linewidth=1.5)
# plt.axhline(y=0, color='gray', linestyle='--', linewidth=1.5)
#
# plt.fill_between([-2, 38], 0, -7.5, color=colors[3], alpha=0.3)
# plt.text(36, -7.25, f"{round(b/a*100,1)}%",
#          fontsize=24, color="black",
#          ha="right", va="bottom")
#
# plt.fill_between([38, 58], 0, 2.5, color=colors[4], alpha=0.3)
# plt.text(40, 2.25, f"{round(c/a*100,1)}%",
#          fontsize=24, color="black",
#          ha="left", va="top")
#
# # Add title and labels
# plt.xlabel("Index of differences [-]", fontsize=18)
# plt.ylabel("Cogging torque difference [mNm]", fontsize=18)
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
# plt.savefig('diff_cog_case3_case6v2.png', dpi=300)
# plt.show()

# AVERAGE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# avg = pd.read_parquet('../diff_avg/diff_avg_df_case3_case6v2.parquet')
#
# diff_avg = []
#
# for i in range(len(sim_row)):
#     diff_avg.append(avg.iloc[sim_row[i], int(sim_col[i])])
#     diff_avg.sort()
#
# plt.figure(figsize=(8, 6))
# plt.scatter(range(len(sim_row)), diff_avg, label='AVG (case D - case C)', color=colors[1])
#
# a = len(diff_avg)
# b = len([i for i in diff_avg if i <= 0])
# c = len([i for i in diff_avg if i > 0])
# print(a, b, c)
#
# plt.axvline(x=35, color='gray', linestyle='--', linewidth=1.5)
# plt.axhline(y=0, color='gray', linestyle='--', linewidth=1.5)
#
# plt.fill_between([-2, 35], 0, -130, color=colors[4], alpha=0.3)
# plt.text(33, -114, f"{round(b/a*100,1)}%",
#          fontsize=24, color="black",
#          ha="right", va="bottom")
#
# plt.fill_between([35, 58], 0, 90, color=colors[3], alpha=0.3)
# plt.text(37, 85, f"{round(c/a*100,1)}%",
#          fontsize=24, color="black",
#          ha="left", va="top")
#
# # Add title and labels
# plt.xlabel("Index of differences [-]", fontsize=18)
# plt.ylabel("Average torque difference [mNm]", fontsize=18)
#
# # Add grid behind the bars
# plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
# plt.gca().set_axisbelow(True)
#
# # Style ticks
# plt.xticks(fontsize=18)
# plt.yticks(fontsize=18)
# plt.legend(fontsize=18, loc = 4)
# plt.tight_layout()
# plt.savefig('diff_avg_case3_case6v2.png', dpi=300)
# plt.show()
# #
# # RIPPLE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# rip = pd.read_parquet('../diff_rip/diff_rip_df_case3_case6v2.parquet')
#
# diff_rip = []
#
# for i in range(len(sim_row)):
#     diff_rip.append(rip.iloc[sim_row[i], int(sim_col[i])])
#     diff_rip.sort()
# 3
# plt.figure(figsize=(8, 6))
# plt.scatter(range(len(sim_row)), diff_rip, label='RIP (case D - case C)', color=colors[2])
#
# a = len(diff_rip)
# b = len([i for i in diff_rip if i <= 0])
# c = len([i for i in diff_rip if i > 0])
# print(a, b, c)
#
# plt.axvline(x=23, color='gray', linestyle='--', linewidth=1.5)
# plt.axhline(y=0, color='gray', linestyle='--', linewidth=1.5)
#
# plt.fill_between([-2, 23], 0, -15, color=colors[3], alpha=0.3)
# plt.text(21, -14, f"{round(b/a*100,1)}%",
#          fontsize=24, color="black",
#          ha="right", va="bottom")
#
# plt.fill_between([23, 58], 0, 10, color=colors[4], alpha=0.3)
# plt.text(25, 9, f"{round(c/a*100,1)}%",
#          fontsize=24, color="black",
#          ha="left", va="top")
#
# # Add title and labels
# plt.xlabel("Index of differences [-]", fontsize=18)
# plt.ylabel("Torque ripple difference [%]", fontsize=18)
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
# plt.savefig('diff_rip_case3_case6v2.png', dpi=300)
# plt.show()

# # ### GAP #####################################################################################xx
# X = pd.read_parquet('../diff_case3_X8_X9_case6_X10_X11/diff_DX10_CX8_case3_case6v2.parquet')
#
# diff_X = []
#
# for i, j in zip(sim_row, sim_col):
#     diff_X.append(X.iloc[int(i), int(j)])
#
# plt.figure(figsize=(8, 6))
# plt.hist(diff_X, bins=30, color=colors[6], edgecolor='black', alpha=0.85, label='GAP (case D - case C')
#
# # Add title and labels
# plt.xlabel("The width of the gap next to the magnet [deg]", fontsize=18)
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
# plt.savefig('diff_X_case3_case6v2.png', dpi=300)
# plt.show()

### NOT COLLIDED ######################################################################################################
# X1 = pd.read_parquet('../diff_case3_X8_X9_case6_X10_X11/diff_DX10_CX8_case3_case6v2.parquet')
#
# X1_ = []
#
# for i in range(len(sim_row)):
#     j = X1.iloc[sim_row[i], int(sim_col[i])]
#     X1_.append(j)
#
# plt.figure(figsize=(8, 6))
# plt.hist(X1_, bins=30, color=colors[6], edgecolor='black', alpha=0.85, label=r'case D - case C ($t_c$=0.05)')
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
# plt.plot([0, 0], [0, 10], color='black', linestyle='--', linewidth=3)
#
# # Add red circle at (0, 10) with radius 2
# plt.scatter(0, 1, s=10000, facecolors='none', edgecolors='red', linewidths=2)
#
# plt.xlim(-0.15, 1)
# plt.ylim(0, 10)
#
# # Style ticks
# plt.xticks([-0.15, 0, 0.25, 0.5, 0.75, 1], fontsize=18)
# plt.yticks([1,2,4,6,8,10], fontsize=18)
# plt.legend(fontsize=18)
# plt.tight_layout()
# plt.savefig('diff_X9X8_case3_case6v2_notcollided.png', dpi=300)
# plt.show()

#### COLLIDED ######################################################################################################
X1 = pd.read_parquet('../diff_case3_X8_X9_case6_X10_X11/diff_DX10_CX8_case3_case6v2.parquet')

X1_ = []

for i in range(len(sim_row)):
    j = X1.iloc[sim_row[i], int(sim_col[i])]
    X1_.append(j)

plt.figure(figsize=(8, 6))
plt.hist(X1_, bins=30, color=colors[6], edgecolor='black', alpha=0.85, label=r'case D - case C ($t_c$=0.06)')

# Add title and labels
plt.xlabel("The width of the air gap next to the magnet [deg]", fontsize=18)
plt.ylabel("Frequency", fontsize=18)

# Add grid behind the bars
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
plt.gca().set_axisbelow(True)

# Add vertical dashed line at x=0
plt.plot([0, 0], [0, 10], color='black', linestyle='--', linewidth=3)

# Add red circle at (0, 10) with radius 2
plt.scatter(0, 1, s=10000, facecolors='none', edgecolors='red', linewidths=2)

plt.xlim(-0.15, 1)
plt.ylim(0, 10)

# Style ticks
plt.xticks([-0.15, 0, 0.25, 0.5, 0.75, 1], fontsize=18)
plt.yticks([1,2,4,6,8,10], fontsize=18)
plt.legend(fontsize=18)
plt.tight_layout()
plt.savefig('diff_X9X8_case3_case6v2_collided.png', dpi=300)
plt.show()