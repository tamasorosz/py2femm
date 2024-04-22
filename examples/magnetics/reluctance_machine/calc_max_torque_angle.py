import csv
import math
import os
import pathlib

import numpy as np
import machine_model_synrm as mod

from multiprocessing import Pool

from src.executor import Executor


def execute_model(counter):
    femm = Executor()
    current_file_path = os.path.abspath(__file__)
    folder_path = os.path.dirname(current_file_path)
    femm.run(os.path.join(folder_path, f'temp_ang/ang{counter}.lua'))
    with open(os.path.join(folder_path, f'temp_ang/ang{counter}.csv'), 'r') as file:
        torque = float(list(csv.reader(file))[0][0]) * 4 * -1000

    del_fem = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.lua'))
    del_ans = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.fem'))
    del_lua = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.ans'))
    del_csv = pathlib.Path(os.path.join(folder_path, f'temp_ang/ang{counter}.csv'))

    del_lua.unlink()
    del_fem.unlink()
    del_ans.unlink()
    del_csv.unlink()

    return torque


def max_torque_angle(J0, h_co, ang_co, deg_co,  bhu, bdu, bwu, bho, bdo,
                     bwo, deg_bu, deg_bo, out, fold):

    # Finding the maximum torque angle
    resol = 11
    a = 40
    b = 50
    for counter, alpha in zip(range(0, resol), np.linspace(a, b, resol)):
        JUp = J0 * math.cos(math.radians(90 + alpha))
        JUn = -JUp
        JVp = J0 * math.cos(math.radians(90 + alpha + 120))
        JVn = -JVp
        JWp = J0 * math.cos(math.radians(90 + alpha + 240))
        JWn = -JWp
        mod.build(counter=counter, h_co=h_co, ang_co=ang_co, deg_co=deg_co, bhu=bhu, bdu=bdu, bwu=bwu, bho=bho,
                  bdo=bdo, bwo=bwo, deg_bu=deg_bu, deg_bo=deg_bo, oa=0, JUp=JUp, JUn=JUn, JVp=JVp, JVn=JVn, JWp=JWp,
                  JWn=JWn, out=out, fold=fold)

    with Pool(11) as p:
        res = p.map(execute_model, list(range(0, resol)))

    ind = list(res).index((max(list(res))))
    torque_ang = a + (ind) * ((b - a) / (resol - 1))

    return torque_ang
