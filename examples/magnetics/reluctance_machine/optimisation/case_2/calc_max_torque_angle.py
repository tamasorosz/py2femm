import csv
import logging
import math
import os
import time

import numpy as np
import machine_model_synrm as model

from multiprocessing import Pool

from src.executor import Executor


def execute_model(counter):

    time.sleep(0.1)

    femm = Executor()
    current_file_path = os.path.abspath(__file__)
    folder_path = os.path.dirname(current_file_path)

    lua_file = os.path.join(folder_path, f'temp_ang/ang{counter}.lua')
    femm.run(lua_file)

    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        time.sleep(0.1)

        current_file_path = os.path.abspath(__file__)
        folder_path = os.path.dirname(current_file_path)

        with open(os.path.join(folder_path, f'temp_ang/ang{counter}.csv'), 'r') as file:
            csvfile = [i for i in csv.reader(file)]
            number = csvfile[0][0].replace('wTorque_0 = ', '')
            torque = float(number) * 4 * -1000

    except (csv.Error, IndexError) as e:
        logging.error(f'Error at ang{counter}: {e}')
        torque = 0.0

    # time.sleep(0.1)
    #
    # for filename in os.listdir(os.path.join(folder_path, f'temp_ang')):
    #     file_path = os.path.join(folder_path, f'temp_ang', filename)
    #     try:
    #         if os.path.isfile(file_path) or os.path.islink(file_path):
    #             os.unlink(file_path)
    #     except Exception as e:
    #         print(f"Failed to delete {file_path}. Reason: {e}")

    return torque


def max_torque_angle(J0, ang_co, deg_co, bd, bw, bh, bgp, ang_m, mh):
    resol = 361
    a = 0
    b = 360
    feasibility = 1
    for counter, alpha in zip(range(0, resol), np.linspace(a, b, resol)):
        JUp = J0 * math.cos(math.radians(alpha))
        JUn = -JUp
        JVp = J0 * math.cos(math.radians(alpha + 120))
        JVn = -JVp
        JWp = J0 * math.cos(math.radians(alpha + 240))
        JWn = -JWp

        variables = model.VariableParameters(fold='ang',
                                             out='ang',
                                             counter=counter,
                                             JAp=JUp,
                                             JAn=JUn,
                                             JBp=JVp,
                                             JBn=JVn,
                                             JCp=JWp,
                                             JCn=JWn,
                                             ang_co=ang_co,
                                             deg_co=deg_co*10,
                                             bd=bd,
                                             bw=bw,
                                             bh=bh,
                                             bg=bgp*0.5 + mh,
                                             ia=0,
                                             ang_m=ang_m,
                                             mh=mh
                                             )
        feasibility = model.problem_definition(variables)
        if feasibility == 0:
            break

    if feasibility == 1:
        with Pool(24) as p:
            res = p.map(execute_model, list(range(0, resol)))

        res = list(res)

        ind = res.index((max(res)))
        torque_ang = a + ind * ((b - a) / (resol - 1))
    else:
        torque_ang = None

    return torque_ang, res
