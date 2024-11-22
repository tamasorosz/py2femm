import os

import pandas as pd
from matplotlib import pyplot as plt
import calc_max_torque_angle
import calc_torque_avg_rip
import calc_cogging

if __name__ == "__main__":
#     # 14
#     # 22
#     # 140
#     # 1
#     # 3
#     # 0.5
#     # 11
#     # 16 - 1539.23
#     # 21.67
#     # 20.20
#     # 34.31
#     # y = calc_max_torque_angle.max_torque_angle(30, 22, 14, 1, 0.5, 3, 1, 1.5, 11, 16)
#     # y = calc_torque_avg_rip.torque_avg_rip(30, 22, 14, 1, 0.5, 3, 1, 1.5, 11, 16)
#     y = calc_cogging.cogging(30, 22, 14, 1, 0.5, 3, 1, 1.5, 11, 16)
#     plt.plot(y[2])
#     print(y[0], y[1])
#     plt.show()
#
    y = calc_max_torque_angle.max_torque_angle(30, 22, 11, 1, 0.5, 2, 1, 2, 10, 12)
#
#     plt.plot(y[1])
#     plt.show()
#
# file_path = os.getcwd() + '/results/' + 'taguchi_res_raw.csv'
# df = pd.read_csv(file_path)
#
# print(df.head(5).to_string())
