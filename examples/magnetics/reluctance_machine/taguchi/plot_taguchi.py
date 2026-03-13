import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

current_dir = os.getcwd()

# ----------------------------------------------------------------
#  Plot average torque and torque ripple parameter sensitivity for
#  an average on current of [5, 10, 15, 20, 25, 30, 50, 100]

df_avg = [pd.read_csv(current_dir + '/results/' + f'res_avg_taguchi_{j}A.csv') for j in [5, 10, 15, 20, 25, 30, 35, 40,
                                                                                         45, 50, 55, 60, 65, 70, 75]]
df_rip = [pd.read_csv(current_dir + '/results/' + f'res_rip_taguchi_{j}A.csv') for j in [5, 10, 15, 20, 25, 30, 35, 40,
                                                                                         45, 50, 55, 60, 65, 70, 75]]

df_avg = pd.concat(df_avg, ignore_index=False).groupby(level=0).agg(list)
df_rip = pd.concat(df_rip, ignore_index=False).groupby(level=0).agg(list)

df_avg = df_avg.apply(lambda col: col.apply(lambda x: np.mean(x)))
df_rip = df_rip.apply(lambda col: col.apply(lambda x: np.mean(x)))

df_avg = df_avg.T.sort_values(df_avg.index[-1], ascending=False).T
df_rip = df_rip.T.sort_values(df_avg.index[-1], ascending=False).T

y1_values = list(df_avg.iloc[5])
y2_values = list(df_rip.iloc[5])

for i in range(len(y1_values)):
    plt.scatter(df_avg.iloc[5].index[i], y1_values[i], label='AVG', color='blue', marker='x', s=100)
    plt.scatter(df_avg.iloc[5].index[i], y2_values[i], label='RIP', color='green', s=100)

plt.xlabel('Parameters', fontsize=14)
plt.ylabel('\u0394S/N [db]', fontsize=14)
plt.xticks(rotation=45, fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True)
plt.legend(['AVG', 'RIP'], fontsize=14)
plt.tight_layout()
plt.savefig('figures/' + f'sens_synrm.png', bbox_inches='tight')
plt.show()

# ----------------------------------------------------------------
#  Plot average torque and torque ripple parameter sensitivity for
#  on current of [5, 10, 15, 20, 25, 30, 50, 100]

# df_avg = [pd.read_csv(current_dir + '/results/' + f'res_avg_taguchi_{j}A.csv') for j in [5, 10, 15, 20, 25, 30, 35, 40,
#                                                                                          45, 50, 55, 60, 65, 70, 75]]
# df_rip = [pd.read_csv(current_dir + '/results/' + f'res_rip_taguchi_{j}A.csv') for j in [5, 10, 15, 20, 25, 30, 35, 40,
#                                                                                          45, 50, 55, 60, 65, 70, 75]]
#
# df_avg = pd.concat(df_avg, ignore_index=False).groupby(level=0).agg(list)
# df_rip = pd.concat(df_rip, ignore_index=False).groupby(level=0).agg(list)
#
# j = 0
#
# print(df_avg)
# print(df_rip)
# colors = ['blue', 'green', 'red', 'magenta', 'orange', 'purple']
# for i in range(6):
#     plt.scatter([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], df_avg.iloc[j, i],  label='AVG ' +
#                                                                                               f'{df_avg.columns[i]}',
#                 c=colors[i], marker='x')
#
# for i in range(6):
#     plt.scatter([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], df_rip.iloc[j, i], label='RIP ' +
#                                                                                               f'{df_rip.columns[i]}',
#                 c=colors[i])
# plt.xlabel('Excitation current [A]', fontsize=14)
# plt.ylabel('S/N [db]', fontsize=14)
# plt.title(f' Level {j+1}', fontsize=14)
# plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], ['5', '10', '15', '20', '25', '30', '35', '40', '45',
#                                                                 '50', '55', '60', '65', '70', '75'], rotation=45,
#            fontsize=14)
# plt.yticks(fontsize=14)
# plt.grid(True)
# plt.legend(loc='center right', ncol=2)
# plt.tight_layout()
# # plt.show()
#
# plt.savefig('figures/' + f'avg_rip{j+1}.png', bbox_inches='tight')

# ----------------------------------------------------------------
#  Plot average torque and torque ripple parameter sensitivity for
#  on current of [5, 10, 15, 20, 25, 30, 50, 100]

df_avg = [pd.read_csv(current_dir + '/results/' + f'res_avg_taguchi_{j}A.csv') for j in [5, 10, 15, 20, 25, 30, 35, 40,
                                                                                         45, 50, 55, 60, 65, 70, 75]]
df_rip = [pd.read_csv(current_dir + '/results/' + f'res_rip_taguchi_{j}A.csv') for j in [5, 10, 15, 20, 25, 30, 35, 40,
                                                                                         45, 50, 55, 60, 65, 70, 75]]
# x1... levels and i is currents
x1 = []
x2 = []
x3 = []
x4 = []
x5 = []
x6 = []

y1 = []
y2 = []
y3 = []
y4 = []
y5 = []
y6 = []

for i in range(len(df_avg)):
    x1.append(df_avg[i].iloc[0].tolist())
    x2.append(df_avg[i].iloc[1].tolist())
    x3.append(df_avg[i].iloc[2].tolist())
    x4.append(df_avg[i].iloc[3].tolist())
    x5.append(df_avg[i].iloc[4].tolist())
    x6.append(df_avg[i].iloc[5].tolist())

for i in range(len(df_rip)):
    y1.append(df_rip[i].iloc[0].tolist())
    y2.append(df_rip[i].iloc[1].tolist())
    y3.append(df_rip[i].iloc[2].tolist())
    y4.append(df_rip[i].iloc[3].tolist())
    y5.append(df_rip[i].iloc[4].tolist())
    y6.append(df_rip[i].iloc[5].tolist())

for i in [1, 2, 3, 4, 5]:
    x = globals()['x' + str(i)]
    y = globals()['y' + str(i)]
    plt.boxplot(x, positions=[i for i in range(len(x))], widths=1/2, patch_artist=True)
    plt.boxplot(y, positions=[i for i in range(len(y))], widths=1/2, patch_artist=True)

    plt.xlabel('Excitation current [A]', fontsize=14)
    plt.ylabel('\u0394S/N [db]', fontsize=14)
    plt.title(f' Level {i}', fontsize=14)
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], ['5', '10', '15', '20', '25', '30', '35', '40', '45',
                                                                    '50', '55', '60', '65', '70', '75'], rotation=45,
               fontsize=14)
    plt.yticks( fontsize=14)

    plt.grid(True)
    textbox_props = dict(boxstyle='square', facecolor='white', alpha=0.5)
    plt.annotate('Average Torque [Nm]', xy=(11, 55), xytext=(9, 40),
                 arrowprops=dict(facecolor='black', arrowstyle='->'),
                 fontsize=12, color='black', bbox=textbox_props)
    plt.annotate('Torque Ripple [Nm]', xy=(11, 10), xytext=(9, 20),
                 arrowprops=dict(facecolor='black', arrowstyle='->'),
                 fontsize=12, color='black', bbox=textbox_props)

    plt.tight_layout()
    plt.savefig('figures/' + f'avg_rip_box{i}.png', bbox_inches='tight')
    plt.show()



