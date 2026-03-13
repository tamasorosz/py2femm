import csv
import math
import os
import pathlib
import re
import time

import numpy as np
import machine_model_synrm as model
import calc_max_torque_angle as maxang

from multiprocessing import Pool

from src.executor import Executor


def execute_model(counter):
    time.sleep(0.1)

    try:
        femm = Executor()
        current_file_path = os.path.abspath(__file__)
        folder_path = os.path.dirname(current_file_path)

        lua_file = os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.lua')
        femm.run(lua_file)

        time.sleep(0.1)

        with open(os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.csv'), 'r') as file:
            csvfile = [i for i in csv.reader(file)]
            number = csvfile[0][0].replace('wTorque_0 = ', '')
            torque = float(number) * 4 * -1000

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


def torque_avg_rip(J0, ang_co, deg_co, bd, bw, bh, bgp, mh, ang_ml, ang_mr, ang_mpl, ang_mpr):
    initial = maxang.max_torque_angle(J0, ang_co, deg_co, bd, bw, bh, bgp, mh, ang_ml, ang_mr, ang_mpl, ang_mpr)

    resol = 31
    e = 30
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
                                             bg=bgp + mh,
                                             ia=ia,
                                             mh=mh,
                                             ang_ml=ang_ml,
                                             ang_mr=ang_mr,
                                             ang_mpl=ang_mpl,
                                             ang_mpr=ang_mpr
                                             )
        model.problem_definition(variables)

    with Pool(8) as p:
        res = p.map(execute_model, list(range(0, resol)))

    torque_avg = -1 * np.average(list(res))
    torque_ripple = -1 * (np.max(list(res)) - np.min(list(res))) / torque_avg

    return torque_avg, torque_ripple
