import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from examples.magnetics.reluctance_machine.shifting.case_3n import calc_cogging, calc_max_torque_angle, \
    calc_torque_avg_rip

# if __name__ == "__main__":
#     f = calc_cogging.cogging(0, 22.1, 146.5, 1.0, 1.0, 3.0, 0.5, 1.5, 15, 18, 2, -4)
#
#     df = pd.DataFrame({'P2P': round(f[0], 3), 'THD': round(f[1], 3), 'RES': [[round(i, 3) for i in f[2]]], 'FFT': [[round(i, 3) for i in f[3]]]})
#     current_file_path = os.path.abspath(__file__)
#     folder_path = os.path.dirname(current_file_path)
#     file_path = os.path.join(folder_path, f'results/case3_opt_f_cog.csv')
#     df.to_csv(file_path, encoding='utf-8', index=False)
#
#     f = pd.read_csv('results/case3_opt_f_cog.csv')
#
#     f['RES'] = f['RES'].apply(lambda x: list(map(float, x.strip('[]').split(','))))
#     f['FFT'] = f['FFT'].apply(lambda x: list(map(float, x.strip('[]').split(','))))
#
#     colors = ["#B90276", '#50237F', '#005691', "#008ECF", '#00A8B0', '#78BE20', "#006249", '#525F6B', '#000']
#
#     # cogging
#     fig, ax = plt.subplots(figsize=(10, 8))
#     ax.plot(f.iloc[0, 2], label='Shifted design (S)', color=colors[0], linewidth=2, linestyle='-', marker='', markersize=8)
#     ax.grid(True, which='both', linestyle='--', linewidth=0.5)
#     ax.set_xlabel('Rotor position [deg]', fontsize=14)
#     ax.set_ylabel('Torque [mNm]', fontsize=14)
#     ax.tick_params(axis='both', which='major', labelsize=14)
#     ax.set_yticks(np.linspace(-12, 12, 13), np.linspace(-12, 12, 13), minor=False)
#     ax.legend(fontsize=12)
#     ax.annotate(f'{max(f.iloc[0, 2])}', (f.iloc[0, 2].index(max(f.iloc[0, 2])), max(f.iloc[0, 2])+1), fontsize=14, ha='center', annotation_clip=False)
#     ax.annotate(f'{min(f.iloc[0, 2])}', (f.iloc[0, 2].index(min(f.iloc[0, 2])), min(f.iloc[0, 2])-1), fontsize=14, ha='center', annotation_clip=False)
#     plt.show()
#
#     bar_width = 0.35
#     x = np.arange(1, 4)
#
#     # thd
#     fig, ax = plt.subplots(figsize=(10, 8))
#     bars2 = ax.bar(x + bar_width/2, f.iloc[0, 3][1:4], bar_width, label='Shifted design (S)', color=colors[0], edgecolor='black')
#     ax.set_xlabel('Category', fontsize=14)
#     ax.set_ylabel('Values', fontsize=14)
#     ax.set_xticks(x)
#     ax.set_xticklabels(x)
#     ax.tick_params(axis='both', which='major', labelsize=14)
#     ax.grid(True, which='both', linestyle='--', linewidth=0.5, axis='y')
#     ax.legend(fontsize=14)
#     plt.show()

# if __name__ == "__main__":
#     f = calc_max_torque_angle.max_torque_angle(30, 22.1, 146.5, 1.0, 1.0, 3.0, 0.5, 1.5, 15, 18, 2, -4)
#
#     df = pd.DataFrame({'ANG': round(f[0], 3), 'RES': [[round(i, 3) for i in f[1]]]})
#     current_file_path = os.path.abspath(__file__)
#     folder_path = os.path.dirname(current_file_path)
#     file_path = os.path.join(folder_path, f'results/case3_opt_f_ang.csv')
#     df.to_csv(file_path, encoding='utf-8', index=False)
#
#     f = pd.read_csv('results/case3_opt_f_ang.csv')
#
#     f['RES'] = f['RES'].apply(lambda x: list(map(float, x.strip('[]').split(','))))
#
#     colors = ["#B90276", '#50237F', '#005691', "#008ECF", '#00A8B0', '#78BE20', "#006249", '#525F6B', '#000']
#
#     fig, ax = plt.subplots(figsize=(10, 8))
#     ax.plot(f.iloc[0, 1], label='Shifted design (S)', color=colors[0], linewidth=2, linestyle='-', marker='', markersize=8)
#     ax.grid(True, which='both', linestyle='--', linewidth=0.5)
#     ax.set_xlabel('Rotor position [deg]', fontsize=14)
#     ax.set_ylabel('Torque [mNm]', fontsize=14)
#     ax.tick_params(axis='both', which='major', labelsize=14)
#     # ax.set_yticks(np.linspace(-12, 12, 13), np.linspace(-12, 12, 13), minor=False)
#     ax.set_xticks(np.linspace(0, 15, 16), np.round(np.linspace(-90, 90, 16), 0), minor=False)
#     plt.show()
#
# #
# if __name__ == "__main__":
#     f = calc_torque_avg_rip.torque_avg_rip(30, 22.1, 146.5, 1.0, 1.0, 3.0, 0.5, 1.5, 15, 18, 2, -4)
#
#     df = pd.DataFrame({'AVG': round(f[0], 3), 'RIP': round(f[1], 3), 'RES': [[round(i, 3) for i in f[2]]]})
#     current_file_path = os.path.abspath(__file__)
#     folder_path = os.path.dirname(current_file_path)
#     file_path = os.path.join(folder_path, f'results/case3_opt_f_torq.csv')
#     df.to_csv(file_path, encoding='utf-8', index=False)
#
#     f = pd.read_csv('results/case3_opt_f_torq.csv')
#
#     f['RES'] = f['RES'].apply(lambda x: list(map(float, x.strip('[]').split(','))))
#
#     colors = ["#B90276", '#50237F', '#005691', "#008ECF", '#00A8B0', '#78BE20', "#006249", '#525F6B', '#000']
#
#     fig, ax = plt.subplots(figsize=(10, 8))
#     ax.plot(f.iloc[0, 2], label='Shifted design (S)', color=colors[0], linewidth=2, linestyle='-', marker='', markersize=8)
#     ax.grid(True, which='both', linestyle='--', linewidth=0.5)
#     ax.set_xlabel('Rotor position [deg]', fontsize=14)
#     ax.set_ylabel('Torque [mNm]', fontsize=14)
#     ax.tick_params(axis='both', which='major', labelsize=14)
#     # ax.set_yticks(np.linspace(-12, 12, 13), np.linspace(-12, 12, 13), minor=False)
#     ax.legend(fontsize=12)
#     plt.show()