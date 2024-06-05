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

    try:
        time.sleep(0.1)

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

    except IndexError:
        print(f'Error1 at avg_rip{counter}!')
        torque = 0.0

    try:
        time.sleep(0.1)

        current_file_path = os.path.abspath(__file__)
        folder_path = os.path.dirname(current_file_path)

        del_fem = pathlib.Path(os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.lua'))
        del_ans = pathlib.Path(os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.fem'))
        del_lua = pathlib.Path(os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.ans'))
        del_csv = pathlib.Path(os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.csv'))

        del_lua.unlink()
        del_fem.unlink()
        del_ans.unlink()
        del_csv.unlink()

    except PermissionError or FileNotFoundError:
        print(f'Error1 at avg_rip{counter}!')
        pass

    return torque


def torque_avg_rip(J0, ang_co, deg_co, bd, bw, bh, bgp, mh, ang_m, ang_mp, deg_m, deg_mp):
    initial = maxang.max_torque_angle(J0, ang_co, deg_co, bd, bw, bh, bgp, mh, ang_m, ang_mp, deg_m, deg_mp)

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
                                             bg=bgp + mh,
                                             ia=ia,
                                             mh=mh,
                                             ang_m=ang_m,
                                             ang_mp=ang_mp,
                                             deg_m=deg_m,
                                             deg_mp=deg_mp
                                             )
        model.problem_definition(variables)

    with Pool(8) as p:
        res = p.map(execute_model, list(range(0, resol)))

    torque_avg = -1 * np.average(list(res))
    torque_ripple = -1 * (np.max(list(res)) - np.min(list(res))) / torque_avg

    return torque_avg, torque_ripple
