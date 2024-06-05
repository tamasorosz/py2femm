import os
import statistics

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from examples.magnetics.reluctance_machine.shifting.case_3n import calc_cogging, calc_max_torque_angle, \
    calc_torque_avg_rip

# if __name__ == "__main__":
#     f = pd.read_csv('figures/data/case2_opt_f_cog.csv')
#     g = pd.read_csv('figures/data/case4_opt_f_cog.csv')
#     h = pd.read_csv('figures/data/case3_opt_f_cog.csv')
#
#     f['RES'] = f['RES'].apply(lambda x: list(map(float, x.strip('[]').split(','))))
#     g['RES'] = g['RES'].apply(lambda x: list(map(float, x.strip('[]').split(','))))
#     h['RES'] = h['RES'].apply(lambda x: list(map(float, x.strip('[]').split(','))))
#
#     colors = ["#B90276", '#50237F', '#005691', "#008ECF", '#00A8B0', '#78BE20', "#006249", '#525F6B', '#000']
#
#     # cogging ---------------------------------------------------------------------------------------------------------
#     fig, ax = plt.subplots(figsize=(10, 8))
#     ax.plot(f.iloc[0, 2], label='Base design (B)', color=colors[0], linewidth=5, linestyle='-', marker='',
#             markersize=8)
#     ax.plot(g.iloc[0, 2], label='Shifted design (S)', color=colors[1], linewidth=5, linestyle='-', marker='',
#             markersize=8)
#     ax.plot(h.iloc[0, 2], label='False design (F)', color=colors[6], linewidth=5, linestyle='-', marker='',
#             markersize=8)
#     ax.grid(True, which='both', linestyle='--', linewidth=0.5)
#     ax.set_xlabel('Rotor position [deg]', fontsize=20)
#     ax.set_ylabel('Torque [mNm]', fontsize=20)
#     ax.tick_params(axis='both', which='major', labelsize=20)
#     ax.set_yticks(np.linspace(-12, 12, 13), np.linspace(-12, 12, 13), minor=False)
#     ax.legend(fontsize=16)
#     # ax.annotate(f'{round(max(f.iloc[0, 2]), 1)}', (f.iloc[0, 2].index(max(f.iloc[0, 2])), max(f.iloc[0, 2]) + 0.5), fontsize=18,
#     #             ha='center', annotation_clip=False)
#     # ax.annotate(f'{round(min(f.iloc[0, 2]), 1)}', (f.iloc[0, 2].index(min(f.iloc[0, 2])), min(f.iloc[0, 2]) - 1), fontsize=18,
#     #             ha='center', annotation_clip=False)
#     # ax.annotate(f'{round(max(g.iloc[0, 2]), 1)}', (g.iloc[0, 2].index(max(g.iloc[0, 2])), max(g.iloc[0, 2]) + 0.5), fontsize=18,
#     #             ha='center', annotation_clip=False)
#     # ax.annotate(f'{round(min(g.iloc[0, 2]), 1)}', (g.iloc[0, 2].index(min(g.iloc[0, 2])), min(g.iloc[0, 2]) - 1), fontsize=18,
#     #             ha='center', annotation_clip=False)
#     textstr = 'peak-to-peak:' + '\n' + 'B: ' + f'{round(max(f.iloc[0, 2]) - min(f.iloc[0, 2]), 1)}' + ' mNm' + '\n' + 'S: ' + f'{round(max(g.iloc[0, 2]) - min(g.iloc[0, 2]), 1)}' + ' mNm' \
#     + '\n' + 'F: ' + f'{round(max(h.iloc[0, 2]) - min(h.iloc[0, 2]), 1)}' + ' mNm'
#     props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
#     ax.text(0.05, 0.25, textstr, transform=ax.transAxes, fontsize=20, verticalalignment='top', bbox=props)
#     plt.savefig('figures/comp_cog_t', bbox_inches='tight')
#     plt.show()

    # # thd -------------------------------------------------------------------------------------------------------------
    # f['FFT'] = f['FFT'].apply(lambda x: list(map(float, x.strip('[]').split(','))))
    # g['FFT'] = g['FFT'].apply(lambda x: list(map(float, x.strip('[]').split(','))))
    #
    # bar_width = 0.35
    # harmonics = 20
    # x = np.round(np.arange(1, harmonics/2+1), 0)
    #
    # fig, ax = plt.subplots(figsize=(10, 8))
    # ax.bar(x - bar_width / 2, f.iloc[0, 3][2:harmonics+1:2], bar_width, label='Base design (B)', color=colors[0],
    #        edgecolor='black')
    # ax.bar(x + bar_width / 2, g.iloc[0, 3][2:harmonics+1:2], bar_width, label='Shifted design (S)', color=colors[1],
    #        edgecolor='black')
    # ax.set_xlabel('i-th harmonics', fontsize=20)
    # ax.set_ylabel('Torque [mNm]', fontsize=20)
    # ax.set_xticks(np.linspace(1,10,10))
    # ax.set_xticklabels(np.linspace(1,19,10))
    # ax.tick_params(axis='both', which='major', labelsize=20)
    # ax.grid(True, which='both', linestyle='--', linewidth=0.5, axis='y')
    # ax.legend(fontsize=20)
    # plt.show()

# ang ----------------------------------------------------------------------------------------------------------------
# if __name__ == "__main__":
#     def tri(lst):
#         for i in range(len(lst) - 1):
#             if lst[i] < 0 and lst[i + 1] >= 0:
#                 return i + 1
#
#     f = pd.read_csv('figures/data/case1_opt_f_ang.csv')
#     g = pd.read_csv('figures/data/case2_opt_f_ang.csv')
#     h = pd.read_csv('figures/data/case4_opt_f_ang.csv')
#     j = pd.read_csv('figures/data/case3_opt_f_ang.csv')
#
#     f['RES'] = f['RES'].apply(lambda x: list(map(float, x.strip('[]').split(','))))
#     g['RES'] = g['RES'].apply(lambda x: list(map(float, x.strip('[]').split(','))))
#     h['RES'] = h['RES'].apply(lambda x: list(map(float, x.strip('[]').split(','))))
#     j['RES'] = j['RES'].apply(lambda x: list(map(float, x.strip('[]').split(','))))
#
#     colors = ["#B90276", '#50237F', '#005691', "#008ECF", '#00A8B0', '#78BE20', "#006249", '#525F6B', '#000']
#
#     fig, ax = plt.subplots(figsize=(10, 8))
#     ax.plot(np.linspace(0, 180, 181), f.iloc[0, 1], label='Initial design (I)', color=colors[0],
#             linewidth=5, linestyle='-', marker='', markersize=8)
#     ax.plot(np.linspace(4, 184, 181), g.iloc[0, 1], label='Base design (B)', color=colors[1], linewidth=5, linestyle='-', marker='',
#             markersize=8)
#     ax.plot(np.linspace(6, 186, 181), h.iloc[0, 1], label='Shifted design (S)', color=colors[4], linewidth=5, linestyle='-', marker='',
#             markersize=8)
#     ax.plot(np.linspace(35, 215, 181), j.iloc[0, 1], label='False design (F)', color=colors[6], linewidth=5,
#             linestyle='-', marker='',
#             markersize=8)
#     ax.grid(True, which='both', linestyle='--', linewidth=0.5)
#     ax.set_xlabel('Rotor position [deg]', fontsize=18)
#     ax.set_ylabel('Torque [mNm]', fontsize=18)
#     ax.tick_params(axis='both', which='major', labelsize=18)
#     ax.set_xticks(np.linspace(0, 220, 11), np.linspace(-90, 130, 11, dtype=int), minor=False)
#     ax.axvline(x=f.iloc[0, 1].index(max(f.iloc[0, 1])), color=colors[0], linestyle='--', linewidth=2,
#                label='max(I): ' + f'{round(f.iloc[0, 0], 0)}' + ' deg')
#     ax.axvline(x=g.iloc[0, 1].index(max(g.iloc[0, 1]))+4, color=colors[1], linestyle='--', linewidth=2,
#                label='max(B): ' + f'{round(g.iloc[0, 0]+4, 0)}' + ' deg')
#     ax.axvline(x=h.iloc[0, 1].index(max(h.iloc[0, 1]))+6, color=colors[4], linestyle='--', linewidth=2,
#                label='max(S): ' + f'{round(h.iloc[0, 0]+6, 0)}' + ' deg')
#     ax.axvline(x=j.iloc[0, 1].index(max(j.iloc[0, 1])) + 35, color=colors[6], linestyle='--', linewidth=2,
#                label='max(F): ' + f'{round(j.iloc[0, 0] + 35, 0)}' + ' deg')
#     # ax.axvline(x=tri(f.iloc[0,1]), color=colors[0], linestyle='--', linewidth=2,  # helps to find the shift
#     #            label=f'{tri(f.iloc[0,1])}' + ' deg')
#     # ax.axvline(x=tri(g.iloc[0, 1]), color=colors[0], linestyle='--', linewidth=2, # helps to find the shift
#     #            label=f'{tri(g.iloc[0, 1])}' + ' deg')
#     # ax.axvline(x=tri(h.iloc[0, 1]), color=colors[0], linestyle='--', linewidth=2, # helps to find the shift
#     #            label=f'{tri(h.iloc[0, 1])}' + ' deg')
#     ax.axvline(x=90, color=colors[3], linestyle='--', linewidth=2, # helps to find the shift
#                label=f'0' + ' deg')
#     ax.legend(fontsize=16)
#     plt.savefig('figures/comp_ang_g', bbox_inches='tight')
#     plt.show()

if __name__ == "__main__":
    f = pd.read_csv('figures/data/case1_opt_f_torq.csv')
    g = pd.read_csv('figures/data/case2_opt_f_torq.csv')
    h = pd.read_csv('figures/data/case4_opt_f_torq.csv')
    j = pd.read_csv('figures/data/case3_opt_f_torq.csv')

    f['RES'] = f['RES'].apply(lambda x: list(map(float, x.strip('[]').split(','))))
    g['RES'] = g['RES'].apply(lambda x: list(map(float, x.strip('[]').split(','))))
    h['RES'] = h['RES'].apply(lambda x: list(map(float, x.strip('[]').split(','))))
    j['RES'] = j['RES'].apply(lambda x: list(map(float, x.strip('[]').split(','))))

    colors = ["#B90276", '#50237F', '#005691', "#008ECF", '#00A8B0', '#78BE20', "#006249", '#525F6B', '#000']

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(f.iloc[0, 2], label='Initial design (I)', color=colors[0],
            linewidth=5, linestyle='-', marker='', markersize=8)
    ax.plot(g.iloc[0, 2], label='Base design (B)', color=colors[1], linewidth=5, linestyle='-', marker='',
            markersize=8)
    ax.plot(h.iloc[0, 2], label='Shifted design (S)', color=colors[4], linewidth=5, linestyle='-', marker='',
            markersize=8)
    ax.plot(j.iloc[0, 2], label='False design (F)', color=colors[6], linewidth=5, linestyle='-', marker='',
            markersize=8)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_xlabel('Rotor position [deg]', fontsize=18)
    ax.set_ylabel('Torque [mNm]', fontsize=18)
    ax.tick_params(axis='both', which='major', labelsize=18)
    ax.axhline(y=np.mean(f.iloc[0, 2]), color=colors[0], linestyle='--', linewidth=2,
               label='avg(I): ' + f'{int(np.mean(f.iloc[0, 2]))}' + ' mNm')
    ax.axhline(y=np.mean(g.iloc[0, 2]), color=colors[1], linestyle='--', linewidth=2,
               label='avg(B): ' + f'{int(np.mean(g.iloc[0, 2]))}' + ' mNm')
    ax.axhline(y=np.mean(h.iloc[0, 2]), color=colors[4], linestyle='--', linewidth=2,
               label='avg(S): ' + f'{int(np.mean(h.iloc[0, 2]))}' + ' mNm')
    ax.axhline(y=np.mean(j.iloc[0, 2]), color=colors[6], linestyle='--', linewidth=2,
               label='avg(F): ' + f'{int(np.mean(j.iloc[0, 2]))}' + ' mNm')
    ax.plot([], color=colors[0], linestyle='None', label='rip(I): ' + f'{f.iloc[0, 1] * 100}' + ' %')
    ax.plot([], color=colors[1], linestyle='None', label='rip(B): ' + f'{g.iloc[0, 1] * 100}' + ' %')
    ax.plot([], color=colors[2], linestyle='None', label='rip(S): ' + f'{h.iloc[0, 1] * 100}' + ' %')
    ax.plot([], color=colors[2], linestyle='None', label='rip(F): ' + f'{j.iloc[0, 1] * 100}' + ' %')
    ax.legend(fontsize=14,loc='upper center', ncol=3, bbox_to_anchor=(0.5, -0.125))
    plt.subplots_adjust(bottom=0.25)
    ax.set_yticks(np.linspace(1000, 2200, 7), np.linspace(1000, 2200, 7))
    plt.savefig('figures/comp_torq_g', bbox_inches='tight')
    plt.show()