import csv
import math
import os
import re

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import calc_max_torque_angle
import calc_torque_avg_rip
import calc_cogging

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
#
if __name__ == "__main__":
    # xl = np.array([15, 9, 1, 1, 1, 10]),
    # xu = np.array([25, 14, 4, 4, 2, 15]),

    y = calc_cogging.cogging(0, 18, 150, 1, 0.5, 1, 1, 1.5, 12, 14, 12, 16)
    print(y[1])
    plt.plot(y[1])
    plt.show()

    # x = [25, 15, 4, 4, 1, 15]
    # g = (math.tan(math.radians(x[0] / 2)) * (22 - (x[4] * 0.5 + 1.5)) + x[2] + x[3]) - 8
    # if g > 0:
    #     temp_x3 = int(8 - (math.tan(math.radians(x[0] / 2)) * (22 - (x[4] * 0.5 + 1.5))) - x[2])
    #     if temp_x3 < 1:
    #         x[3] = 1
    #         x[2] = x[2] - (1 - temp_x3)
    #         if x[2] < 1:
    #             x[2] = 1
    #     else:
    #         x[3] = temp_x3
    # print(x)
    # y = calc_max_torque_angle.max_torque_angle(30, x[0], x[1], x[2], 0.5, x[3], x[4], x[5], 1.5)
