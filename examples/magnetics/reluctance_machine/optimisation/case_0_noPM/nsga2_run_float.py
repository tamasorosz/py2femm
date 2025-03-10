import gc
import math
import os

import numpy as np
import pandas as pd

from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.repair import Repair
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.operators.sampling.rnd import IntegerRandomSampling, FloatRandomSampling
from pymoo.termination import get_termination
from pymoo.optimize import minimize
from pymoo.termination.default import DefaultMultiObjectiveTermination

import calc_torque_avg_rip

if __name__ == '__main__':
    initial = True

    class MyProblem(ElementwiseProblem):
        def __init__(self):
            super().__init__(n_var=6,
                             n_obj=2,
                             n_ieq_constr=0,
                             n_eq_constr=0,
                             xl=np.array([15, 9, 1, 1, 1, 3]),
                             xu=np.array([25, 15, 4, 4, 1, 5]),
                             vtype=float)

        def _evaluate(self, x, out, *args, **kwargs):

            f = calc_torque_avg_rip.torque_avg_rip(30, x[0], x[1], x[2], x[3], x[4], x[5])

            gc.collect()

            out['F'] = [f[0], f[1]]

    class MyRepair(Repair):
        problem = MyProblem()

        def _do(self, problem, x, **kwargs):

            # global initial
            # if initial:
            #
            #     with open('results/nsga2_case0_p100o100g200_var6_20250202.csv', 'r') as f:
            #         df = pd.read_csv(f)
            #
            #     df.iloc[:, 1] = (df.iloc[:, 1] / 10).astype(int)
            #     df.iloc[:, 5] = df.iloc[:, 5]  / 0.5
            #
            #     x = [row.tolist() for _, row in df.iloc[:, :6].iterrows()]
            #
            #     while len(x) < 100:
            #         x = x + x
            #     x = x[:3]
            #
            #     initial = False
            #     print(x)
            #     return x


            for i in range(len(x)):
                g = (math.tan(math.radians(x[i][0] / 2)) * (22 - x[i][5]*0.5) + x[i][2] + x[i][4]) - 8
                if g > 0:
                    temp = np.round((8 - (math.tan(math.radians(x[i][0] / 2)) * (22 - x[i][5]*0.5)) - x[i][2]), 2)
                    if temp < 1:
                        x[i][4] = 1
                        x[i][2] = np.round(x[i][2] - (1 - temp), 2)
                        if x[i][2] < 1:
                            x[i][2] = 1
                    else:
                        x[i][4] = temp

                x[i][0] = np.round(x[i][0], 2)
                x[i][1] = np.round(x[i][1], 2)
                x[i][2] = np.round(x[i][2], 2)
                x[i][3] = np.round(x[i][3], 2)
                x[i][4] = np.round(x[i][4], 2)
                x[i][5] = np.round(x[i][5], 2)

            return x

    problem = MyProblem()

    algorithm = NSGA2(
        pop_size=100,
        n_offsprings=100,
        eliminate_duplicates=True,
        repair=MyRepair()
    )

    termination = get_termination("n_gen", 300)

    res = minimize(problem,
                   algorithm,
                   termination,
                   seed=1,
                   save_history=False,
                   verbose=True)

    F = res.F
    X = res.X

    print('Execution time: ' + str(res.exec_time / 60 / 60) + ' hours')

    df = pd.DataFrame({'X1': X[:, 0], 'X2': [np.round(i*10,2) for i in X[:, 1]], 'X3': X[:, 2], 'X4': X[:, 3],
                       'X5': X[:, 4], 'X6': [np.round(i*0.5,2) for i in X[:, 5]], 'AVG': F[:, 0], 'RIP': F[:, 1]})
    current_file_path = os.path.abspath(__file__)
    folder_path = os.path.dirname(current_file_path)

    if os.path.exists('results'):
        pass
    else:
        os.makedirs('results')

    file_path = os.path.join(folder_path, f'results/nsga2_case0_p100o100g200_var6_20250310.csv')
    df.to_csv(file_path, encoding='utf-8', index=False)
