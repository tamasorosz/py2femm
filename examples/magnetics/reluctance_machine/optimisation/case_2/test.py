import csv
import math
import os
import re

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
    # x = calc_max_torque_angle.max_torque_angle(30, 25.0, 147.1, 1.1, 1.0, 2.5, 0.5, 5.1, 1.5)
    # x = calc_torque_avg_rip.torque_avg_rip(0, 25.0, 147.1, 1.1, 1.0, 2.5, 0.5, 5.1, 1.5)

    x = calc_max_torque_angle.max_torque_angle(30, 20, 90, 1.0, 1.0, 3.0, 1.0, 10, 1.5)
    # x = calc_torque_avg_rip.torque_avg_rip(0, 22.1, 146.5, 1.0, 1.0, 3.0, 0.5, 14.9, 1.5)


    # df = pd.DataFrame({'Torque': x[2], 'MaxAngle': list(range(0, 121))})
    # current_file_path = os.path.abspath(__file__)
    # folder_path = os.path.dirname(current_file_path)
    # file_path = os.path.join(folder_path, f'results/pmasynrm_span15_cogging.csv')
    # df.to_csv(file_path, encoding='utf-8', index=False)
    print(x[0])
    plt.plot(x[1])
    plt.show()

