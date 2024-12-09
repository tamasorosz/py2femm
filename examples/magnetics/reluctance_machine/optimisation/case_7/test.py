import csv
import math
import os
import re

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

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
from examples.magnetics.reluctance_machine.optimisation.case_7 import calc_torque_avg_rip
from examples.magnetics.reluctance_machine.optimisation.case_7 import calc_cogging
#
if __name__ == "__main__":
    # xl = np.array([15, 9, 1, 1, 1, 10]),
    # xu = np.array([25, 14, 4, 4, 2, 15]),

    # y = calc_torque_avg_rip.torque_avg_rip(30, 21, 14, 1, 0.5, 3, 1, 1.5, 10, 11, 16, 14)
    # z = calc_cogging.cogging(0, 21, 14, 1, 0.5, 3, 1, 1.5, 10, 11, 16, 14)
    # y = calc_torque_avg_rip.torque_avg_rip(30, 21, 14, 1, 0.5, 3, 1, 1.5, 9.85, 10.85, 15.85, 13.85)
    z = calc_cogging.cogging(0, 21, 14, 1, 0.5, 3, 1, 1.5, 9.85, 10.85, 15.85, 13.85)

    # print(y)
    print(z)
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
