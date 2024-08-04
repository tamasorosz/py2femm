import csv
import math
import os
import re

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import machine_model_synrm
import calc_max_torque_angle

# variables = machine_model_synrm.VariableParameters(fold='ang',
#                                                    out='ang',
#                                                    counter=0,
#                                                    JAp=10,
#                                                    JAn=-10,
#                                                    JBp=-5,
#                                                    JBn=5,
#                                                    JCp=-5,
#                                                    JCn=5,
#
#                                                    ang_co=24.3,
#                                                    deg_co=91.5,
#                                                    bd=1.0,
#                                                    bw=0.5,
#                                                    bh=2.4,
#                                                    bg=1.5,
#
#                                                    ia=0,
#                                                    ang_m=20,
#                                                    mh=1.5
#                                                    )
#
from examples.magnetics.reluctance_machine.optimisation.case_2 import calc_torque_avg_rip
#
if __name__ == "__main__":
    #     # xl = np.array([15, 9, 1, 1, 1, 10]),
    #     # xu = np.array([25, 14, 4, 4, 2, 15]),
    #
    #     x = [23, 11, 3, 2, 2, 15]
    #     g = (math.tan(math.radians(x[0] / 2)) * (22 - (x[4] * 0.5 + 1.5)) + x[2] + x[3]) - 8
    #     if g > 0:
    #         temp_x3 = np.round(8 - (math.tan(math.radians(x[0] / 2)) * (22 - (x[4] * 0.5 + 1.5))) - x[2], 1)
    #         if temp_x3 < 1:
    #             x[3] = 1
    #             x[2] = np.round(x[2] - (1 - temp_x3), 1)
    #             if x[2] < 1:
    #                 x[2] = 1
    #         else:
    #             x[3] = temp_x3
    #     print(x)
    #     y = calc_max_torque_angle.max_torque_angle(30, x[0], x[1], x[2], 0.5, x[3], x[4], x[5], 1.5)
    #
    #     # x = [25, 15, 4, 4, 1, 15]
    #     # g = (math.tan(math.radians(x[0] / 2)) * (22 - (x[4] * 0.5 + 1.5)) + x[2] + x[3]) - 8
    #     # if g > 0:
    #     #     temp_x3 = int(8 - (math.tan(math.radians(x[0] / 2)) * (22 - (x[4] * 0.5 + 1.5))) - x[2])
    #     #     if temp_x3 < 1:
    #     #         x[3] = 1
    #     #         x[2] = x[2] - (1 - temp_x3)
    #     #         if x[2] < 1:
    #     #             x[2] = 1
    #     #     else:
    #     #         x[3] = temp_x3
    #     # print(x)
    #     # y = calc_max_torque_angle.max_torque_angle(30, x[0], x[1], x[2], 0.5, x[3], x[4], x[5], 1.5)

    f = calc_max_torque_angle.max_torque_angle(30, 20, 150, 1, 0.5, 1, 1, 15, 1.5)

    plt.plot(f[1])
    plt.show()
