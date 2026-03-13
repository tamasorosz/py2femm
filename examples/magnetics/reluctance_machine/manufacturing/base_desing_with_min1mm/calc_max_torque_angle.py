import csv
import math
import os
import pathlib

import numpy as np
import machine_model_synrm as model

from multiprocessing import Pool
from src.executor import Executor


def execute_model(counter):
    try:
        femm = Executor()
        current_file_path = os.path.abspath(__file__)
        folder_path = os.path.dirname(current_file_path)

        lua_file = os.path.join(folder_path, f'temp_ang/ang{counter}.lua')
        femm.run(lua_file)

        with open(os.path.join(folder_path, f'temp_ang/ang{counter}.csv'), 'r') as file:
            csvfile = [i for i in csv.reader(file)]
            number = csvfile[0][0].replace('wTorque_0 = ', '')
            torque = float(number) * 4 * -1000

        try:
            del_lua = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.lua'))
            del_fem = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.fem'))
            del_ans = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.ans'))
            del_csv = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.csv'))

            del_lua.unlink()
            del_fem.unlink()
            del_ans.unlink()
            del_csv.unlink()

        except PermissionError:
            print(f'PermissionError at ang{counter}')
            pass

    except(IndexError):
        print(f'IndexError at ang{counter}')
        torque = 0.0

    return torque


def max_torque_angle(I0, ang_co, deg_co, bd, bw, bh, bgp, mh, ang_m, ang_mp, deg_m, deg_mp):
    if os.path.exists('../temp_ang'):
        pass
    else:
        os.makedirs('../temp_ang')

    resol = 2
    a = 40
    b = 41

    for counter, alpha in zip(range(0, resol), np.linspace(a, b, resol)):
        variables = model.VariableParameters(fold='ang',
                                             out='ang',
                                             counter=counter,
                                             IAp=I0 * math.cos(math.radians(alpha)),
                                             IAn=-I0 * math.cos(math.radians(alpha)),
                                             IBp=I0 * math.cos(math.radians(alpha + 120)),
                                             IBn=-I0 * math.cos(math.radians(alpha + 120)),
                                             ICp=I0 * math.cos(math.radians(alpha + 240)),
                                             ICn=-I0 * math.cos(math.radians(alpha + 240)),
                                             ang_co=ang_co,
                                             deg_co=deg_co * 10,
                                             bd=bd,
                                             bw=bw,
                                             bh=bh,
                                             bg=bgp * 0.5 + mh,
                                             ia=0,
                                             mh=mh,
                                             ang_m=ang_m,
                                             ang_mp=ang_mp,
                                             deg_m=deg_m,
                                             deg_mp=deg_mp)
        model.problem_definition(variables)

    with Pool(24) as p:
        res = list(p.map(execute_model, list(range(0, resol))))

    torque_ang = a + res.index((max(res))) * ((b - a) / (resol - 1))

    res.clear()

    return torque_ang
