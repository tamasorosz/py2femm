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

        lua_file = os.path.join(folder_path, f'temp_cog/cog{counter}.lua')
        femm.run(lua_file)

        time.sleep(0.1)

        with open(os.path.join(folder_path, f'temp_cog/cog{counter}.csv'), 'r') as file:
            csvfile = [i for i in csv.reader(file)]
            number = csvfile[0][0].replace('wTorque_0 = ', '')
            torque = float(number) * 4 * -1000

        del_fem = pathlib.Path(os.path.join(folder_path, f'temp_cog/cog{counter}.lua'))
        del_ans = pathlib.Path(os.path.join(folder_path, f'temp_cog/cog{counter}.fem'))
        del_lua = pathlib.Path(os.path.join(folder_path, f'temp_cog/cog{counter}.ans'))
        del_csv = pathlib.Path(os.path.join(folder_path, f'temp_cog/cog{counter}.csv'))
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

        del_fem = pathlib.Path(os.path.join(folder_path, f'temp_cog/cog{counter}.lua'))
        del_ans = pathlib.Path(os.path.join(folder_path, f'temp_cog/cog{counter}.fem'))
        del_lua = pathlib.Path(os.path.join(folder_path, f'temp_cog/cog{counter}.ans'))
        del_csv = pathlib.Path(os.path.join(folder_path, f'temp_cog/cog{counter}.csv'))

        try:
            time.sleep(0.1)
            del_lua.unlink()
            del_fem.unlink()
            del_ans.unlink()
            del_csv.unlink()

        except PermissionError:
            pass

        print(f'Error at cog{counter}!')

    return torque

def fftPlot(sig, dt=None):

    if dt is None:
        dt = 1
        t = np.arange(0, sig.shape[-1])
        xLabel = 'samples'
    else:
        t = np.arange(0, sig.shape[-1]) * dt
        xLabel = 'freq [Hz]'

    if sig.shape[0] % 2 != 0:
        t = t[0:-1]
        sig = sig[0:-1]

    sigFFT = np.fft.fft(sig) / t.shape[0]

    freq = np.fft.fftfreq(t.shape[0], d=dt)

    firstNegInd = np.argmax(freq < 0)
    freqAxisPos = freq[0:firstNegInd]
    sigFFTPos = 2 * sigFFT[0:firstNegInd]

    return sigFFTPos, freqAxisPos

def thd(abs_data):
    sq_sum = 0.0
    for r in range(len(abs_data)):
        sq_sum = sq_sum + (abs_data[r]) ** 2

    sq_harmonics = sq_sum - ((abs_data[1])) ** 2.0
    thd = 100 * sq_harmonics ** 0.5 / abs_data[1]

    return thd


def cogging(J0, ang_co, deg_co, bd, bw, bh, bgp, mh, ang_ml1, ang_mr1, ang_mpl1, ang_mpr1, ang_ml2, ang_mr2, ang_mpl2,
            ang_mpr2):

    resol = 31
    e = 15
    for counter, ia in zip(range(0, resol), np.linspace(0, e, resol)):
        JUp = J0
        JUn = -JUp
        JVp = J0
        JVn = -JVp
        JWp = J0
        JWn = -JWp

        variables = model.VariableParameters(fold='cog',
                                             out='cog',
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
                                             ang_ml1=ang_ml1,
                                             ang_mr1=ang_mr1,
                                             ang_mpl1=ang_mpl1,
                                             ang_mpr1=ang_mpr1,
                                             ang_ml2=ang_ml2,
                                             ang_mr2=ang_mr2,
                                             ang_mpl2=ang_mpl2,
                                             ang_mpr2=ang_mpr2
                                             )
        model.problem_definition(variables)

    with Pool(8) as p:
        res = p.map(execute_model, list(range(0, resol)))

    cogging_pp = (np.max(list(res)) - np.min(list(res)))

    y = np.round(np.abs(fftPlot(np.array(res), 1 / (3 * 120))[0]), 3)
    y[0] = 0
    try:
        fund = next((i for i, v in enumerate(y) if v > 1), None)
        if fund is None:
            raise StopIteration
        refined_y = [i for i, j in zip(y, range(len(y))) if j % fund == 0]
        res_thd = thd(refined_y)
    except StopIteration:
        try:
            fund = next((i for i, v in enumerate(y) if v > 0.5), None)
            if fund is None:
                raise StopIteration
            refined_y = [i for i, j in zip(y, range(len(y))) if j % fund == 0]
            res_thd = thd(refined_y)
        except StopIteration:
            try:
                fund = next((i for i, v in enumerate(y) if v > 0.25), None)
                if fund is None:
                    raise StopIteration
                refined_y = [i for i, j in zip(y, range(len(y))) if j % fund == 0]
                res_thd = thd(refined_y)
            except StopIteration:
                try:
                    fund = next((i for i, v in enumerate(y) if v > 0.1), None)
                    if fund is None:
                        raise StopIteration
                    refined_y = [i for i, j in zip(y, range(len(y))) if j % fund == 0]
                    res_thd = thd(refined_y)
                except StopIteration:
                    res_thd = 100
                    print('Fourth safety case')

    return cogging_pp, res_thd
