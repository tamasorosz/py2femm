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


def execute_model(counter):
    try:
        femm = Executor()
        current_file_path = os.path.abspath(__file__)
        folder_path = os.path.dirname(current_file_path)

        lua_file = os.path.join(folder_path, f'temp_cog/cog{counter}.lua')
        femm.run(lua_file)

        with open(os.path.join(folder_path, f'temp_cog/cog{counter}.csv'), 'r') as file:
            csvfile = [i for i in csv.reader(file)]
            number = csvfile[0][0].replace('wTorque_0 = ', '')
            torque = float(number) * 4 * -1000

        try:
            del_fem = pathlib.Path(os.path.join(folder_path, f'temp_cog/cog{counter}.fem'))
            del_ans = pathlib.Path(os.path.join(folder_path, f'temp_cog/cog{counter}.ans'))
            del_lua = pathlib.Path(os.path.join(folder_path, f'temp_cog/cog{counter}.lua'))
            del_csv = pathlib.Path(os.path.join(folder_path, f'temp_cog/cog{counter}.csv'))

            del_lua.unlink()
            del_fem.unlink()
            # del_ans.unlink()
            del_csv.unlink()

        except PermissionError:
            print(f'PermissionError at cog{counter}')
            pass

    except(IndexError):
        print(f'IndexError at cog{counter}')
        return None

    return torque

def cogging(I0, ang_co, deg_co, bd, bw, bh, bgp, mh, ang_m, deg_m):
    if os.path.exists('temp_cog'):
        pass
    else:
        os.makedirs('temp_cog')
    if mh >= 1.5:
        resol = 16
        e = 15

        for counter, ia in zip(range(0, resol), np.linspace(0, e, resol)):
            variables = model.VariableParameters(fold='cog',
                                                 out='cog',
                                                 counter=counter,
                                                 IAp=I0 * math.cos(math.radians(0)),
                                                 IAn=-I0 * math.cos(math.radians(0)),
                                                 IBp=I0 * math.cos(math.radians(0 + 120)),
                                                 IBn=-I0 * math.cos(math.radians(0 + 120)),
                                                 ICp=I0 * math.cos(math.radians(0 + 240)),
                                                 ICn=-I0 * math.cos(math.radians(0 + 240)),
                                                 ang_co=ang_co,
                                                 deg_co=deg_co * 10,
                                                 bd=bd,
                                                 bw=bw,
                                                 bh=bh,
                                                 bg=bgp * 0.5 + mh,
                                                 ia=ia,
                                                 mh=mh,
                                                 ang_m=ang_m,
                                                 deg_m=deg_m)

            model.problem_definition(variables)

        with Pool(16) as p:
            res = list(p.map(execute_model, list(range(0, resol))))

        if None in res:
            res.clear()
            return random.randint(30, 50)

        else:
            cogging_pp = np.round(np.max(list(res)) - np.min(list(res)), 2)

            # res.clear()  # To make sure that there is no memory leak

        df = pd.DataFrame({'X1': [ang_co], 'X2': [np.round(deg_co * 10, 2)], 'X3': [bd], 'X4': [bw],
                           'X5': [bh], 'X6': [np.round(bgp * 0.5 + mh, 2)], 'X7': [mh], 'X8': [ang_m],
                           'X9': [deg_m], 'COG': [cogging_pp]})

        current_file_path = os.path.abspath(__file__)
        folder_path = os.path.dirname(current_file_path)
        file_path = os.path.join(folder_path, f'results/all_res_cog_case3_20250421_all_variable.csv')

        # Check if the file exists
        file_exists = os.path.isfile(file_path)

        # Append the DataFrame to the CSV file
        with open(file_path, 'a', newline='') as f:
            df.to_csv(f, header=not file_exists, index=False)

        # Count the number of rows in a separate operation
        with open(file_path, 'r') as f:
            num_rows = sum(1 for _ in f)

        print('COG: ' + f'{cogging_pp}' + ', IND: ' + f'{num_rows}' +
              '\n-----------------------------------------------')

        return cogging_pp, res

    else:
        return random.randint(30, 50)