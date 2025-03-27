import csv
import math
import os
import pathlib
import random

import numpy as np
import pandas as pd

import machine_model_synrm as model

from multiprocessing import Pool
from src.executor import Executor

import calc_max_torque_angle


def execute_model(counter):
    try:
        femm = Executor()
        current_file_path = os.path.abspath(__file__)
        folder_path = os.path.dirname(current_file_path)

        lua_file = os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.lua')
        femm.run(lua_file)

        with open(os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.csv'), 'r') as file:
            csvfile = [i for i in csv.reader(file)]
            number = csvfile[0][0].replace('wTorque_0 = ', '')
            torque = float(number) * 4 * -1000

        try:
            del_lua = pathlib.Path(os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.lua'))
            del_fem = pathlib.Path(os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.fem'))
            del_ans = pathlib.Path(os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.ans'))
            del_csv = pathlib.Path(os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.csv'))

            del_lua.unlink()
            del_fem.unlink()
            del_ans.unlink()
            del_csv.unlink()

        except PermissionError:
            print(f'PermissionError at avg_rip{counter}')
            pass

    except IndexError:
        print(f'IndexError at avg_rip{counter}')
        torque = 0.0

    return torque


def torque_avg_rip(I0, ang_co, deg_co, bd, bw, bh, bgp, mh, ang_m, ang_mp, deg_m, deg_mp):
    if ang_m != ang_mp:
        if not (deg_m == 0 and deg_mp == 0):
            initial = calc_max_torque_angle.max_torque_angle(I0, ang_co, deg_co, bd, bw, bh, bgp, mh, ang_m, ang_mp,
                                                             deg_m, deg_mp)
            if os.path.exists('temp_avg_rip'):
                pass
            else:
                os.makedirs('temp_avg_rip')

            resol = 16
            e = 15

            for counter, ia, alpha in zip(range(0, resol), np.linspace(0, e, resol), np.linspace(0, 4 * e, resol)):
                variables = model.VariableParameters(fold='avg_rip',
                                                     out='avg_rip',
                                                     counter=counter,
                                                     IAp=I0 * math.cos(math.radians(initial + alpha)),
                                                     IAn=-I0 * math.cos(math.radians(initial + alpha)),
                                                     IBp=I0 * math.cos(math.radians(initial + 120 + alpha)),
                                                     IBn=-I0 * math.cos(math.radians(initial + 120 + alpha)),
                                                     ICp=I0 * math.cos(math.radians(initial + 240 + alpha)),
                                                     ICn=-I0 * math.cos(math.radians(initial + 240 + alpha)),
                                                     ang_co=ang_co,
                                                     deg_co=deg_co * 10,
                                                     bd=bd,
                                                     bw=bw,
                                                     bh=bh,
                                                     bg=bgp * 0.5 + mh,
                                                     ia=ia,
                                                     mh=mh,
                                                     ang_m=ang_m,
                                                     ang_mp=ang_mp,
                                                     deg_m=deg_m,
                                                     deg_mp=deg_mp)
                model.problem_definition(variables)

            with Pool(16) as p:
                res = list(p.map(execute_model, list(range(0, resol))))

            if None in res:
                torque_avg = 0
                torque_ripple = 1000
            else:
                torque_avg = np.round(-1 * np.average(res), 2)
                torque_ripple = np.round(-100 * (np.max(res) - np.min(res)) / torque_avg, 2)

            res.clear()  # To make sure that there is no memory leak

            torque_angle = -1 * initial

            print(f'{int(ang_co), int(deg_co), int(bd), int(bw), int(bh), int(bgp), int(mh), int(ang_m), int(ang_mp), int(deg_m), int(deg_mp)}' +
                  '\n' + 'ANG: ' + f'{initial}' + ', AVG: ' + f'{-1 * torque_avg}' + ', RIP: ' + f'{torque_ripple}')

            df = pd.DataFrame({
                'X1': [ang_co], 'X2': [deg_co * 10], 'X3': [bd], 'X4': [bw],
                'X5': [bh], 'X6': [bgp * 0.5 + mh], 'X7': [mh], 'X8': [ang_m], 'X9': [ang_mp], 'X10': [deg_m],
                'X11': [deg_mp], 'ANG': [torque_angle], 'AVG': [torque_avg], 'RIP': [torque_ripple]
            })

            current_file_path = os.path.abspath(__file__)
            folder_path = os.path.dirname(current_file_path)
            file_path = os.path.join(folder_path, f'results/all_res_avg_case6_20250327_no_rib.csv')

            # Check if the file exists
            file_exists = os.path.isfile(file_path)

            # Write to CSV
            with open(file_path, 'a', newline='') as f:
                df.to_csv(f, header=not file_exists, index=False)

            return torque_avg, torque_ripple, torque_angle

        else:
            return random.randint(-300, 0), random.randint(100, 150), random.randint(-20, 0)

    else:
        return random.randint(-300, 0), random.randint(100, 150), random.randint(-20, 0)



