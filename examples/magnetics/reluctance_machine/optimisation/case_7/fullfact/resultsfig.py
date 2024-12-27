import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# 0.0,11.0,16.0,14.0,1463.4,18.81,20.74
colors = ["#B90276", '#50237F', '#005691', "#008ECF", '#00A8B0', '#78BE20', "#006249", '#525F6B', '#000']
ft = 12

file_path1 = os.getcwd() + '/taguchi_res_raw.csv'
file_path2 = os.getcwd() + '/fullfact_res_raw.csv'

df1 = pd.read_csv(file_path1)
df2 = pd.read_csv(file_path2)

del df1['X5']
del df1['X6']
print('               ', 'MIN   ', 'MEAN   ', 'MAX  ')
print('TAGUCHI (AVG): ', min(df1['Tavg']), np.round(np.mean(df1['Tavg']), 2), max(df1['Tavg']))
print('FULLFACT (AVG): ', min(df2['Tavg']), np.round(np.mean(df2['Tavg']), 2), max(df2['Tavg']))
print()
print('TAGUCHI (RIP): ', min(df1['Trip']), np.round(np.mean(df1['Trip']), 2), max(df1['Trip']))
print('FULLFACT (RIP): ', min(df2['Trip']), np.round(np.mean(df2['Trip']), 2), max(df2['Trip']))
print()
print('TAGUCHI (COG): ', min(df1['Tcog']), np.round(np.mean(df1['Tcog']), 2), max(df1['Tcog']))
print('FULLFACT (COG): ', min(df2['Tcog']), np.round(np.mean(df2['Tcog']), 2), max(df2['Tcog']))
print()

# df_t_avg = df1["Tavg"].sort_values(ignore_index=True)
# df_f_avg = df2["Tavg"].sort_values(ignore_index=True)

# bins = [min(df_f_avg) + ((max(df_f_avg)-min(df_f_avg)) / 10) * i for i in range(10)]
# print(bins)
#
# binnum = [0 if bins[0] <= i < bins[1] else 1 if bins[1] <= i < bins[2] else 2 if bins[2] <= i < bins[3]
# else 3 if bins[3] <= i < bins[4] else 4 if bins[4] <= i < bins[5] else 5 if bins[5] <= i < bins[6]
#           else 6 if bins[6] <= i < bins[7] else 7 if bins[7] <= i < bins[8]
#           else 8 if bins[8] <= i < bins[9] else 9 if bins[9] <= i else 10 for i in df_t_avg]
#
# taguchinum = [binnum.count(0), binnum.count(1), binnum.count(2), binnum.count(3), binnum.count(4),
#               binnum.count(5), binnum.count(6), binnum.count(7), binnum.count(8), binnum.count(9)]
#
# binnumff = [0 if bins[0] <= i < bins[1] else 1 if bins[1] <= i < bins[2] else 2 if bins[2] <= i < bins[3]
# else 3 if bins[3] <= i < bins[4] else 4 if bins[4] <= i < bins[5] else 5 if bins[5] <= i < bins[6]
#           else 6 if bins[6] <= i < bins[7] else 7 if bins[7] <= i < bins[8]
#           else 8 if bins[8] <= i < bins[9] else 9 if bins[9] <= i else 10 for i in df_f_avg]
#
# ffnum = [binnumff.count(0), binnumff.count(1), binnumff.count(2), binnumff.count(3), binnumff.count(4),
#          binnumff.count(5), binnumff.count(6), binnumff.count(7), binnumff.count(8), binnumff.count(9)]
#
# fig, ax = plt.subplots(figsize=(5, 4), dpi=150, tight_layout=True)
# plt.grid(axis='y', linestyle='--', alpha=0.7, zorder=1)
# plt.bar(list(range(10)), ffnum, color=colors[2], zorder=2, label='Full Factorial')
# plt.bar(list(range(10)), taguchinum, color=colors[0], zorder=3, label='Taguchi')
# plt.vlines(9, 0, 30, color=colors[8], linestyle='--', label='Optimal')
# plt.xlabel("Average torque range [mNm]", fontsize=ft)
# plt.ylabel("Number of models [u.]", fontsize=ft)
# plt.xticks(fontsize=ft)
# plt.yticks(fontsize=ft)
# plt.legend(loc='best', fontsize=ft)
#
# ax.set_xlim(-1, 10)
# ax.set_ylim(0, 100)
# ax.set_xticks(np.arange(0, 10, 1))  # X-axis ticks from 0 to 10
# # ax.set_yticks(np.arange(0, 10, 1))  # Y-axis ticks from 0 to 10
# # plt.savefig('ff_avg.png', format='png', dpi=300)
# # plt.show()
#
# df_t_avg = df1["Trip"].sort_values(ignore_index=True)
# df_f_avg = df2["Trip"].sort_values(ignore_index=True)
#
# bins = [min(df_f_avg) + ((max(df_f_avg)-min(df_f_avg)) / 10) * i for i in range(10)]
# print(bins)
#
# binnum = [0 if bins[0] <= i < bins[1] else 1 if bins[1] <= i < bins[2] else 2 if bins[2] <= i < bins[3]
# else 3 if bins[3] <= i < bins[4] else 4 if bins[4] <= i < bins[5] else 5 if bins[5] <= i < bins[6]
#           else 6 if bins[6] <= i < bins[7] else 7 if bins[7] <= i < bins[8]
#           else 8 if bins[8] <= i < bins[9] else 9 if bins[9] <= i else 10 for i in df_t_avg]
#
# taguchinum = [binnum.count(0), binnum.count(1), binnum.count(2), binnum.count(3), binnum.count(4),
#               binnum.count(5), binnum.count(6), binnum.count(7), binnum.count(8), binnum.count(9)]
#
# binnumff = [0 if bins[0] <= i < bins[1] else 1 if bins[1] <= i < bins[2] else 2 if bins[2] <= i < bins[3]
# else 3 if bins[3] <= i < bins[4] else 4 if bins[4] <= i < bins[5] else 5 if bins[5] <= i < bins[6]
#           else 6 if bins[6] <= i < bins[7] else 7 if bins[7] <= i < bins[8]
#           else 8 if bins[8] <= i < bins[9] else 9 if bins[9] <= i else 10 for i in df_f_avg]
#
# ffnum = [binnumff.count(0), binnumff.count(1), binnumff.count(2), binnumff.count(3), binnumff.count(4),
#          binnumff.count(5), binnumff.count(6), binnumff.count(7), binnumff.count(8), binnumff.count(9)]
#
# fig, ax = plt.subplots(figsize=(5, 4), dpi=150, tight_layout=True)
# plt.grid(axis='y', linestyle='--', alpha=0.7, zorder=1)
# plt.bar(list(range(10)), ffnum, color=colors[2], zorder=2, label='Full Factorial')
# plt.bar(list(range(10)), taguchinum, color=colors[0], zorder=3, label='Taguchi')
# plt.vlines(2, 0, 130, color=colors[8], linestyle='--', label='Optimal')
# plt.xlabel("Torque ripple range [%]", fontsize=ft)
# plt.ylabel("Number of models [u.]", fontsize=ft)
# plt.xticks(fontsize=ft)
# plt.yticks(fontsize=ft)
# plt.legend(loc='best', fontsize=ft)
#
# ax.set_xlim(-1, 10)
# # ax.set_ylim(0, 100)
# ax.set_xticks(np.arange(0, 10, 1))  # X-axis ticks from 0 to 10
# # ax.set_yticks(np.arange(0, 10, 1))  # Y-axis ticks from 0 to 10
# # plt.savefig('ff_rip.png', format='png', dpi=300)
# # plt.show()
#
# df_t_avg = df1["Tcog"].sort_values(ignore_index=True)
# df_f_avg = df2["Tcog"].sort_values(ignore_index=True)
#
# bins = [min(df_f_avg) + ((max(df_f_avg)-min(df_f_avg)) / 10) * i for i in range(10)]
# print(bins)
#
# binnum = [0 if bins[0] <= i < bins[1] else 1 if bins[1] <= i < bins[2] else 2 if bins[2] <= i < bins[3]
# else 3 if bins[3] <= i < bins[4] else 4 if bins[4] <= i < bins[5] else 5 if bins[5] <= i < bins[6]
#           else 6 if bins[6] <= i < bins[7] else 7 if bins[7] <= i < bins[8]
#           else 8 if bins[8] <= i < bins[9] else 9 if bins[9] <= i else 10 for i in df_t_avg]
#
# taguchinum = [binnum.count(0), binnum.count(1), binnum.count(2), binnum.count(3), binnum.count(4),
#               binnum.count(5), binnum.count(6), binnum.count(7), binnum.count(8), binnum.count(9)]
#
# binnumff = [0 if bins[0] <= i < bins[1] else 1 if bins[1] <= i < bins[2] else 2 if bins[2] <= i < bins[3]
# else 3 if bins[3] <= i < bins[4] else 4 if bins[4] <= i < bins[5] else 5 if bins[5] <= i < bins[6]
#           else 6 if bins[6] <= i < bins[7] else 7 if bins[7] <= i < bins[8]
#           else 8 if bins[8] <= i < bins[9] else 9 if bins[9] <= i else 10 for i in df_f_avg]
#
# ffnum = [binnumff.count(0), binnumff.count(1), binnumff.count(2), binnumff.count(3), binnumff.count(4),
#          binnumff.count(5), binnumff.count(6), binnumff.count(7), binnumff.count(8), binnumff.count(9)]
#
# fig, ax = plt.subplots(figsize=(5, 4), dpi=150, tight_layout=True)
# plt.grid(axis='y', linestyle='--', alpha=0.7, zorder=1)
# plt.bar(list(range(10)), ffnum, color=colors[2], zorder=2, label='Full Factorial')
# plt.bar(list(range(10)), taguchinum, color=colors[0], zorder=3, label='Taguchi')
# plt.vlines(5, 0, 121, color=colors[8], linestyle='--', label='Optimal')
# plt.xlabel("Cogging torque range [mNm]", fontsize=ft)
# plt.ylabel("Number of models [u.]", fontsize=ft)
# plt.xticks(fontsize=ft)
# plt.yticks(fontsize=ft)
# plt.legend(loc='best', fontsize=ft)
#
# ax.set_xlim(-1, 10)
# # ax.set_ylim(0, 100)
# ax.set_xticks(np.arange(0, 10, 1))  # X-axis ticks from 0 to 10
# # ax.set_yticks(np.arange(0, 10, 1))  # Y-axis ticks from 0 to 10
# # plt.savefig('ff_cog.png', format='png', dpi=300)
# # plt.show()

# 0.0,11.0,16.0,14.0,1463.4,18.81,20.74
ft = 12

df_t_avg = df1["Tavg"].sort_values(ignore_index=True)
df_f_avg = df2["Tavg"].sort_values(ignore_index=True)

fig, ax = plt.subplots(figsize=(5, 4), dpi=150, tight_layout=True)
plt.grid(axis='both', linestyle='--', alpha=0.7, zorder=1)

plt.scatter(df_f_avg.index, df_f_avg, color=colors[0], s=10, label='Full Factorial')
plt.scatter(df_f_avg.index[df_f_avg.isin(df_t_avg)].tolist(), df_f_avg[df_f_avg.isin(df_t_avg)].tolist(), color=colors[3], s=50, label='Taguchi')
plt.scatter(df_f_avg.index[df_f_avg.isin([1463.4])].tolist(), df_f_avg[df_f_avg.isin([1463.4])].tolist(), color=colors[8], marker='*', s=150, label='Optimal')

plt.xlabel("Number of models [u.]", fontsize=ft)
plt.ylabel("Average torque [mNm]", fontsize=ft)
plt.xticks(fontsize=ft)
plt.yticks(fontsize=ft)
plt.legend(loc='best', fontsize=ft)
plt.savefig('ff1_avg.png', format='png', dpi=300)
plt.show()

df_t_avg = df1["Trip"].sort_values(ignore_index=True)
df_f_avg = df2["Trip"].sort_values(ignore_index=True)

fig, ax = plt.subplots(figsize=(5, 4), dpi=150, tight_layout=True)
plt.grid(axis='both', linestyle='--', alpha=0.7, zorder=1)

plt.scatter(df_f_avg.index, df_f_avg, color=colors[0], s=10, label='Full Factorial')
plt.scatter(df_f_avg.index[df_f_avg.isin(df_t_avg)].tolist(), df_f_avg[df_f_avg.isin(df_t_avg)].tolist(), color=colors[3], s=50, label='Taguchi')
plt.scatter(df_f_avg.index[df_f_avg.isin([18.81])].tolist(), df_f_avg[df_f_avg.isin([18.81])].tolist(), color=colors[8], marker='*', s=150, label='Optimal')

plt.xlabel("Number of models [u.]", fontsize=ft)
plt.ylabel("Torque ripple [%]", fontsize=ft)
plt.xticks(fontsize=ft)
plt.yticks(fontsize=ft)
plt.legend(loc='best', fontsize=ft)
plt.savefig('ff1_rip.png', format='png', dpi=300)
plt.show()

df_t_avg = df1["Tcog"].sort_values(ignore_index=True)
df_f_avg = df2["Tcog"].sort_values(ignore_index=True)

fig, ax = plt.subplots(figsize=(5, 4), dpi=150, tight_layout=True)
plt.grid(axis='both', linestyle='--', alpha=0.7, zorder=1)

plt.scatter(df_f_avg.index, df_f_avg, color=colors[0], s=10, label='Full Factorial')
plt.scatter(df_f_avg.index[df_f_avg.isin(df_t_avg)].tolist(), df_f_avg[df_f_avg.isin(df_t_avg)].tolist(), color=colors[3], s=50, label='Taguchi')
plt.scatter(323, 20.74, color=colors[8], marker='*', s=150, label='Optimal')

plt.xlabel("Number of models [u.]", fontsize=ft)
plt.ylabel("Cogging torque [mNm]", fontsize=ft)
plt.xticks(fontsize=ft)
plt.yticks(fontsize=ft)
plt.legend(loc='best', fontsize=ft)
plt.savefig('ff1_cog.png', format='png', dpi=300)
plt.show()