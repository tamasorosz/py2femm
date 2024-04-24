import csv
import math
import os
import pathlib
import re


import numpy as np
import machine_model_synrm as model
import matplotlib.pyplot as plt

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
            number = re.findall(r"[-+]?\d*\.\d+|\d+", csvfile[0][0])
            torque = float(number[1]) * 4 * -1000

        del_fem = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.lua'))
        del_ans = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.fem'))
        del_lua = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.ans'))
        del_csv = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.csv'))

        del_lua.unlink()
        del_fem.unlink()
        del_ans.unlink()
        del_csv.unlink()

    except IndexError:
        torque = 0.0

        current_file_path = os.path.abspath(__file__)
        folder_path = os.path.dirname(current_file_path)

        del_fem = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.lua'))
        del_ans = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.fem'))
        del_lua = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.ans'))
        del_csv = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.csv'))

        del_lua.unlink()
        del_fem.unlink()
        del_ans.unlink()
        del_csv.unlink()

        print(f'Error at ang{counter}!')

    return torque


def max_torque_angle(J0, ang_co, deg_co, bd, bw, bh, bg):

    resol = 90
    a = 0
    b = 89
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
                                             bg=bg,
                                             ia=0
                                             )
        model.problem_definition(variables)

    with Pool(8) as p:
        res = p.map(execute_model, list(range(0, resol)))

    ind = list(res).index((max(list(res))))
    torque_ang = a + (ind) * ((b - a) / (resol - 1))

    return torque_ang