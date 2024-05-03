import csv
import math
import os
import pathlib
import re
import time

import numpy as np
import machine_model_synrm as model

from multiprocessing import Pool

from src.executor import Executor


def execute_model(counter):
    time.sleep(1)

    try:
        femm = Executor()
        current_file_path = os.path.abspath(__file__)
        folder_path = os.path.dirname(current_file_path)

        lua_file = os.path.join(folder_path, f'temp_ang/ang{counter}.lua')
        femm.run(lua_file)

        time.sleep(1)

        with open(os.path.join(folder_path, f'temp_ang/ang{counter}.csv'), 'r') as file:
            csvfile = [i for i in csv.reader(file)]
            number = re.findall(r"[-+]?\d*\.\d+|\d+", csvfile[0][0])
            torque = float(number[1]) * 4 * -1000

        del_fem = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.lua'))
        del_ans = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.fem'))
        del_lua = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.ans'))
        del_csv = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.csv'))

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

        del_fem = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.lua'))
        del_ans = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.fem'))
        del_lua = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.ans'))
        del_csv = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.csv'))

        try:
            time.sleep(0.1)
            del_lua.unlink()
            del_fem.unlink()
            del_ans.unlink()
            del_csv.unlink()

        except PermissionError:
            pass

        print(f'Error at ang{counter}!')

    return torque


def max_torque_angle(J0, ang_co, deg_co, bd, bw, bh, bgp, ang_m, mh):

    resol = 51
    a = 0
    b = 50
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
                                             deg_co=deg_co,
                                             bd=bd,
                                             bw=bw,
                                             bh=bh,
                                             bg=mh + bgp,
                                             ia=0,
                                             ang_m=ang_m,
                                             mh=mh
                                             )
        model.problem_definition(variables)

    with Pool(10) as p:
        res = p.map(execute_model, list(range(0, resol)))

    res = list(res)

    for i in range(len(res)):
        if res[i] > 3000 or res[i] < -3000:
            res[i] = 0

    corr = sum(i < 0 for i in res)

    torque_ang = 0
    j = 0

    while torque_ang >= 50 or torque_ang <= 40:

        ind = res.index((max(res)))
        print(ind)
        print(j)
        torque_ang = corr + a + (ind) * ((b - a) / (resol - 1))
        if torque_ang >= 50 or torque_ang <= 40:
            res[ind] = 0
            j = j + 1
            if j > 10:
                torque_ang = 0
                break

    return torque_ang