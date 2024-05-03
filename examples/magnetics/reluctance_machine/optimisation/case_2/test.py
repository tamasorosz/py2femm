import math
import os

import pandas as pd
from matplotlib import pyplot as plt

import machine_model_synrm
import calc_max_torque_angle

variables = machine_model_synrm.VariableParameters(fold='ang',
                                                   out='ang',
                                                   counter=0,
                                                   JAp=10,
                                                   JAn=-10,
                                                   JBp=-5,
                                                   JBn=5,
                                                   JCp=-5,
                                                   JCn=5,

                                                   ang_co=24.3,
                                                   deg_co=91.5,
                                                   bd=1.0,
                                                   bw=0.5,
                                                   bh=2.4,
                                                   bg=1.5,

                                                   ia=0,
                                                   ang_m=20,
                                                   mh=1.5
                                                   )

if __name__ == "__main__":

    x = calc_max_torque_angle.max_torque_angle(30, 24.3, 91.5, 1.0, 0.5, 2.4, 0.5, 16, 2)

    df = pd.DataFrame({'Torque': x[1], 'MaxAngle': x[0]})
    current_file_path = os.path.abspath(__file__)
    folder_path = os.path.dirname(current_file_path)
    file_path = os.path.join(folder_path, f'results/pmasynrm_static_torqu_ang18_h2.csv')
    df.to_csv(file_path, encoding='utf-8', index=False)

    plt.plot(x[1])
    plt.show()

