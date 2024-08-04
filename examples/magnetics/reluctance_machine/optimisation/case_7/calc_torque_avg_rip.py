import csv
import logging
import math
import os
import shutil
import time

import numpy as np
import machine_model_synrm as model
import calc_max_torque_angle as maxang

from multiprocessing import Pool

from src.executor import Executor

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
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

        os.unlink(os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.lua'))
        os.unlink(os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.fem'))
        os.unlink(os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.ans'))
        os.unlink(os.path.join(folder_path, f'temp_avg_rip/avg_rip{counter}.csv'))

    except (csv.Error, IndexError) as e:
        logging.error(f'Error at avg_rip{counter}: {e}')
        torque = None

    return torque

def torque_avg_rip(J0, ang_co, deg_co, bd, bw, bh, bgp, mh, ang_m, ang_mp, deg_m, deg_mp):

    initial = maxang.max_torque_angle(J0, ang_co, deg_co, bd, bw, bh, bgp, mh, ang_m, ang_mp, deg_m, deg_mp)

    if initial is None:
        torque_avg = 0
        torque_ripple = 1000

    else:
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
                                                 deg_co=deg_co*10,
                                                 bd=bd,
                                                 bw=bw,
                                                 bh=bh,
                                                 bg=bgp*0.5 + mh,
                                                 ia=ia,
                                                 mh=mh,
                                                 ang_m=ang_m,
                                                 ang_mp=ang_mp,
                                                 deg_m=deg_m,
                                                 deg_mp=deg_mp
                                                 )
            model.problem_definition(variables)

        with Pool(16) as p:
            res = p.map(execute_model, list(range(0, resol)))

        if None in res:
            torque_avg = 0
            torque_ripple = 1000
        else:
            torque_avg = np.round(-1 * np.average(list(res)), 2)
            torque_ripple = np.round(-100 * (np.max(list(res)) - np.min(list(res))) / torque_avg, 2)

    # print('ANG: ' + f'{initial}' + ', AVG: ' + f'{torque_avg}' + ', RIP: ' + f'{torque_ripple}')

    return torque_avg, torque_ripple
