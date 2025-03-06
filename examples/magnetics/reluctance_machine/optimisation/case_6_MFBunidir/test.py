import math

import numpy as np
import pandas as pd
import itertools

from matplotlib import pyplot as plt

# # Specify the path to your CSV file
# csv_file_path = "results/torq_res_avg.csv"
#
# # Open the file using open() and read it with pandas
# with open(csv_file_path, 'r') as file:
#     df = pd.read_csv(file)
#
# for i in range(len(df['AVG'])):
#     df.loc[i, 'AVG'] = [float(j) for j in df.loc[i, 'AVG'].split(',')]
#
# range1 = range(4, 7)
# range2 = range(7, 10)
# range3 = range(11, 14)
# range4 = range(14, 17)
#
#
# combinations = list(itertools.combinations(range(21), 4))
# lst=[]
# for x1, x2, x3, x4 in combinations:
#     result = [(a + b + c + d + e) / 5 for a, b, c, d, e in zip(df['AVG'][x1], df['AVG'][x2], df['AVG'][5], df['AVG'][x3], df['AVG'][x4])]
#
#     avg = np.average(result)
#     rip = 100 * (np.max(result) - np.min(result)) / avg
#
#
#     lst.append(rip)
# print(min(lst))
import calc_torque_avg_rip
from examples.magnetics.reluctance_machine.optimisation.case_6_MFBunidir import calc_max_torque_angle

if __name__ == '__main__':

    # x =[24,13,2,1,1,11,16,2,5]
    #
    # x[7] = int(x[7] * 2)
    # x[8] = int(x[8] * 2)
    #
    # g = (math.tan(math.radians(x[0] / 2)) * (22 - (x[4] * 0.5 + 1.5)) + x[2] + x[3]) - 8
    # if g > 0:
    #     temp_x3 = np.round(
    #         (8 - (math.tan(math.radians(x[0] / 2)) * (22 - (x[4] * 0.5 + 1.5))) - x[2]), 1)
    #     if temp_x3 < 1:
    #         x[3] = 1
    #         x[2] = int(x[2] - (1 - temp_x3))
    #         if x[2] < 1:
    #             x[2] = 1
    #     else:
    #         x[3] = temp_x3
    #
    # if x[6] + x[8] + x[0] > 43:
    #     x[8] = (43 - x[6] - x[0])
    #
    # if x[5] > x[6]:
    #     x[5] = x[6]
    #
    # if x[7] > int((x[6] - x[5])) + x[8]:
    #     x[7] = int((x[6] - x[5])) + x[8]
    #
    # if x[8] > int((x[6] - x[5])) + x[7]:
    #     x[8] = int((x[6] - x[5])) + x[7]
    #
    # print(x)
    
    a, b, c, d = calc_torque_avg_rip.torque_avg_rip(30, 21, 14, 1.25, 1, 3, 2, 2, 15, 18, 3, 0)
    plt.plot(d)
    # a, b, c, d = calc_torque_avg_rip.torque_avg_rip(30, 21, 14, 1, 0.5, 3, 1, 1.5, 12, 17, 5.5, 4)
    # plt.plot(d)
    # a, b, c, d = calc_torque_avg_rip.torque_avg_rip(30, 21, 14, 1, 0.5, 3, 1, 1.5, 12, 17, 8, 4)
    # plt.plot(d)
    # a, b, c, d = calc_torque_avg_rip.torque_avg_rip(30, 21, 14, 1, 0.5, 3, 1, 1.5, 12, 17, 6, 5)
    # plt.plot(d)
    # a, b, c, d = calc_torque_avg_rip.torque_avg_rip(30, 21, 14, 1, 0.5, 3, 1, 1.5, 12, 17, 5.5, 3.5)
    # plt.plot(d)
    plt.show()

# 3327   21  140   1  0.5   3  2.0  1.5  12  17  4.0  1.0 -40.0 -1500.03  11.29  19.65
# 7226   21  140   1  0.5   3  2.0  1.5  12  17  5.5  4.0 -40.0 -1500.03  11.29  19.65
# 8160   21  140   1  0.5   3  2.0  1.5  12  17  8.0  4.0 -40.0 -1500.03  11.29  19.65
# 11637  21  140   1  0.5   3  2.0  1.5  12  17  6.0  5.0 -40.0 -1500.03  11.29  19.65
# 14686  21  140   1  0.5   3  2.0  1.5  12  17  4.5  3.5 -40.0 -1500.03  11.29  19.65
