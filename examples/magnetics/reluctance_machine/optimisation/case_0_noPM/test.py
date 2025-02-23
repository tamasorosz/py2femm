import math
import os

import pandas as pd
from matplotlib import pyplot as plt

import machine_model_synrm
import calc_max_torque_angle
import calc_torque_avg_rip

if __name__ == "__main__":

    # df_base = pd.read_csv('results/nsga2_case1_p50o50g100_obj5_20240704.csv')

    # f = calc_max_torque_angle.max_torque_angle(30, 24.8, 13.9, 1.0, 2, 1.8, 1)
    # g = calc_max_torque_angle.max_torque_angle(30, 24.4, 119.8, 1.1, 0.5, 2.1, 1.5)

    # f = calc_torque_avg_rip.torque_avg_rip(30, 24.8, 139.0, 1.0, 0.5, 1.8, 1.5)
    g = calc_torque_avg_rip.torque_avg_rip(110, 24.8, 13.9, 1.0, 2, 1.8, 1)

    # df = pd.DataFrame({'V': f[2], 'E': g[2]})
    # current_file_path = os.path.abspath(__file__)
    # folder_path = os.path.dirname(current_file_path)
    # file_path = os.path.join(folder_path, f'results/cogmob_dynamic.csv')
    # df.to_csv(file_path, encoding='utf-8', index=False)
    #
    plt.plot(g[3])
    plt.show()