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
            del_ans.unlink()
            del_csv.unlink()

        except PermissionError:
            print(f'PermissionError at cog{counter}')
            pass

    except(IndexError):
        print(f'IndexError at cog{counter}')
        torque = 0.0

    return torque

def cogging(I0, ang_co, deg_co, bd, bw, bh, bgp, mh, ang_m, ang_mp, deg_m, deg_mp):
    # Get the absolute path of the current script
    folder_path = pathlib.Path(__file__).parent
    file_path = folder_path / "results" / "all_res_cog_case6_20250306.csv"

    # Check if the file exists and is not empty
    if not file_path.exists() or file_path.stat().st_size == 0:
        if os.path.exists('../temp_cog'):
            pass
        else:
            os.makedirs('../temp_cog')

        if ang_m != ang_mp:
            if not (deg_m == 0 and deg_mp == 0):
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
                                                         ang_mp=ang_mp,
                                                         deg_m=deg_m,
                                                         deg_mp=deg_mp)

                    model.problem_definition(variables)

                with Pool(16) as p:
                    res = list(p.map(execute_model, list(range(0, resol))))

                if None in res:
                    cogging_pp = 1000

                else:
                    cogging_pp = np.round(np.max(list(res)) - np.min(list(res)), 2)

                    res.clear()  # To make sure that there is no memory leak

                df = pd.DataFrame({'X1': [ang_co], 'X2': [deg_co * 10], 'X3': [bd], 'X4': [bw],
                                   'X5': [bh], 'X6': [bgp * 0.5 + mh], 'X7': [mh], 'X8': [ang_m], 'X9': [ang_mp],
                                   'X10': [deg_m],
                                   'X11': [deg_mp], 'COG': [cogging_pp]})

                # Append the DataFrame to the CSV file
                with open(file_path, 'a', newline='') as f:
                    df.to_csv(f, header=False, index=False)

                # Count the number of rows in a separate operation
                with open(file_path, 'r') as f:
                    num_rows = sum(1 for _ in f)

                print('COG: ' + f'{cogging_pp}' + ', IND: ' + f'{num_rows}' +
                      '\n-----------------------------------------------')

                return cogging_pp

            else:
                return random.randint(30, 50)

        else:
            return random.randint(30, 50)
    else:
        df = pd.read_csv(file_path)

        row_to_check = [ang_co, deg_co * 10, bd, bw, bh, bgp * 0.5 + mh, mh, ang_m, ang_mp, deg_m, deg_mp]

        exists = ((df.iloc[:, :11] == row_to_check).all(axis=1)).any()

        if exists:
            return random.randint(-300, 0), random.randint(100, 150), random.randint(-20, 0)

        else:

            if os.path.exists('../temp_cog'):
                pass
            else:
                os.makedirs('../temp_cog')

            if ang_m != ang_mp:
                if not (deg_m == 0 and deg_mp == 0):
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
                                                             ang_mp=ang_mp,
                                                             deg_m=deg_m,
                                                             deg_mp=deg_mp)

                        model.problem_definition(variables)

                    with Pool(16) as p:
                        res = list(p.map(execute_model, list(range(0, resol))))

                    if None in res:
                        cogging_pp = 1000

                    else:
                        cogging_pp = np.round(np.max(list(res)) - np.min(list(res)), 2)

                        res.clear()  # To make sure that there is no memory leak

                    df = pd.DataFrame({'X1': [ang_co], 'X2': [deg_co * 10], 'X3': [bd], 'X4': [bw],
                                       'X5': [bh], 'X6': [bgp * 0.5 + mh], 'X7': [mh], 'X8': [ang_m], 'X9': [ang_mp], 'X10': [deg_m],
                                       'X11': [deg_mp], 'COG': [cogging_pp]})

                    # Append the DataFrame to the CSV file
                    with open(file_path, 'a', newline='') as f:
                        df.to_csv(f, header=False, index=False)

                    # Count the number of rows in a separate operation
                    with open(file_path, 'r') as f:
                        num_rows = sum(1 for _ in f)

                    print('COG: ' + f'{cogging_pp}' + ', IND: ' + f'{num_rows}' +
                          '\n-----------------------------------------------')

                    return cogging_pp

                else:
                    return random.randint(30, 50)

            else:
                return random.randint(30, 50)



