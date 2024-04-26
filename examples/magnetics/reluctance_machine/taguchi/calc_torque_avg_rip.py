import csv
import math
import os
import pathlib
import re
import time

import numpy as np
import machine_model_synrm as model
import calc_max_torque_angle as maxang
import matplotlib.pyplot as plt

from multiprocessing import Pool

from src.executor import Executor


def execute_model(counter):
    time.sleep(1)

    try:
        femm = Executor()
        current_file_path = os.path.abspath(__file__)
        folder_path = os.path.dirname(current_file_path)

        lua_file = os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.lua')
        femm.run(lua_file)

        time.sleep(1)

        with open(os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.csv'), 'r') as file:
            csvfile = [i for i in csv.reader(file)]
            number = re.findall(r"[-+]?\d*\.\d+|\d+", csvfile[0][0])
            torque = float(number[1]) * 4 * 1000

        del_fem = pathlib.Path(os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.lua'))
        del_ans = pathlib.Path(os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.fem'))
        del_lua = pathlib.Path(os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.ans'))
        del_csv = pathlib.Path(os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.csv'))
        try:
            time.sleep(0.1)
            del_lua.unlink()
            del_fem.unlink()
            del_ans.unlink()
            del_csv.unlink()

        except PermissionError:
            pass

    except IndexError:
        torque = 0.0

        current_file_path = os.path.abspath(__file__)
        folder_path = os.path.dirname(current_file_path)

        del_fem = pathlib.Path(os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.lua'))
        del_ans = pathlib.Path(os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.fem'))
        del_lua = pathlib.Path(os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.ans'))
        del_csv = pathlib.Path(os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.csv'))

        try:
            time.sleep(0.1)
            del_lua.unlink()
            del_fem.unlink()
            del_ans.unlink()
            del_csv.unlink()

        except PermissionError:
            pass

        print(f'Error at avg_rip{counter}!')

    return torque


def torque_avg_rip(J0, ang_co, deg_co, bd, bw, bh, bg):
    initial = 90 + maxang.max_torque_angle(J0, ang_co, deg_co, bd, bw, bh, bg)

    resol = 16
    e = 15
    for counter, ia, alpha in zip(range(0, resol), np.linspace(0, e, resol), np.linspace(0, 4 * e, resol)):
        JUp = J0 * math.cos(math.radians(initial + alpha))
        JUn = -JUp
        JVp = J0 * math.cos(math.radians(initial + alpha + 120))
        JVn = -JVp
        JWp = J0 * math.cos(math.radians(initial + alpha + 240))
        JWn = -JWp

        variables = model.VariableParameters(fold='avg_rip',
                                             out='avg_rip',
                                             counter=counter,
                                             JAp=JUp,
                                             JAn=JUn,
                                             JBp=JVp,
                                             JBn=JVn,
                                             JCp=JWp,
                                             JCn=JWn,
                                             ang_co=ang_co,
                                             deg_co=deg_co,
                                             bd=bd,
                                             bw=bw,
                                             bh=bh,
                                             bg=bg,
                                             ia=ia
                                             )
        model.problem_definition(variables)

    with Pool(8) as p:
        res = p.map(execute_model, list(range(0, resol)))

    torque_avg = np.average(list(res))
    torque_ripple = (np.max(list(res)) - np.min(list(res))) / torque_avg

    return torque_avg, torque_ripple
