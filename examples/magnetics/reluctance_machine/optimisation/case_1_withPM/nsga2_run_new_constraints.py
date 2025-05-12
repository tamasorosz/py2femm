import gc
import math
import os
import random
import shutil

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
import calc_cogging

if __name__ == '__main__':
    class MyProblem(ElementwiseProblem):
        def __init__(self):
            super().__init__(n_var=8,
                             n_obj=4,
                             n_ieq_constr=0,
                             n_eq_constr=0,
                             xl=np.array([15,  6,  .5, .001, .5, 1, 1.5, 10]),
                             xu=np.array([25, 14,   4,    1,  4, 2,   2, 15]),
                             vtype=float)

        def _evaluate(self, x, out, *args, **kwargs):
            f1 = calc_torque_avg_rip.torque_avg_rip(30, x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7])
            f2 = calc_cogging.cogging(0, x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7])

            gc.collect()

            out['F'] = [f1[0], f1[1], f1[2], f2]

    class MyRepair(Repair):
        problem = MyProblem()

        def _do(self, problem, x, **kwargs):

            for i in range(len(x)):

                midpoint = np.cos(np.radians(x[i][0] / 2)) * 22
                distance = 2 * np.sin(np.radians(x[i][0] / 2)) * 22
                R = (distance / (2 * np.tan(np.radians(x[i][1] * 10 / 2))))
                centerpoint = midpoint + R
                radius = np.sqrt(22 ** 2 + centerpoint ** 2 - (2 * 22 * centerpoint * np.cos(np.radians(x[i][0] / 2))))
                selection_point = centerpoint - radius

                if x[i][5] / 2 + x[i][6] > 22 - selection_point:
                    x[i][5] = (22 - selection_point - x[i][6]) * 2
                    if x[i][5] < 0.5 * 2:
                        x[i][5] = 0.5 * 2
                        x[i][6] = (22 - selection_point - 0.5)

                a = radius + x[i][2] + x[i][4]
                b = 22 - x[i][5] / 2
                c = centerpoint
                x1 = (b ** 2 + c ** 2 - a ** 2) / (2 * c)
                y1 = np.sqrt(b ** 2 - x1 ** 2)
                x_rot1 = x1 * math.cos(np.radians(45)) - y1 * math.sin(np.radians(45))
                y_rot1 = x1 * math.sin(np.radians(45)) + y1 * math.cos(np.radians(45))

                a = radius + x[i][2]
                b = 22 - x[i][5] / 2
                c = centerpoint
                x2 = (b ** 2 + c ** 2 - a ** 2) / (2 * c)
                y2 = np.sqrt(b ** 2 - x2 ** 2)
                x_rot2 = x2 * math.cos(np.radians(45)) - y2 * math.sin(np.radians(45))
                y_rot2 = x2 * math.sin(np.radians(45)) + y2 * math.cos(np.radians(45))

                m1 = (y_rot2 - y_rot1) / (x_rot2 - x_rot1)
                b1 = y_rot1 - m1 * x_rot1

                x_intersect_r = -b1 / (m1 - 1)
                y_intersect_r = x_intersect_r

                x_intersect_l = - b1 / (m1 - np.tan(np.radians(67.5)))
                y_intersect_l = m1 * x_intersect_l + b1

                # constraint_distance = np.sqrt((x_intersect_r - x_rot1) ** 2 + (y_intersect_r - y_rot1) ** 2)
                constraining_distance = np.sqrt((x_intersect_l - x_rot1) ** 2 + (y_intersect_l - y_rot1) ** 2)

                if random.choice([True, False]):
                    if x_rot1 - x_intersect_l > 0:
                        if constraining_distance < 0.25:
                            g = x[i][4] - (0.25 - constraining_distance)
                            x[i][4] = g
                            if g < 0.5:
                                x[i][4] = 0.5
                                x[i][2] = x[i][2] - (0.5 - g)
                                if x[i][2] < 0.5:
                                    x[i][2] = 0.5
                    else:
                        g = x[i][4] - (constraining_distance + 0.5)
                        x[i][4] = g
                        if g < 0.5:
                            x[i][4] = 0.5
                            x[i][2] = x[i][2] + g - 0.25
                            if x[i][2] < 0.5:
                                x[i][2] = 0.5
                else:
                    if x_rot1 - x_intersect_l > 0:
                        if constraining_distance < 0.25:
                            g = x[i][2] - (0.25 - constraining_distance)
                            x[i][2] = g
                            if g < 0.5:
                                x[i][2] = 0.5
                                x[i][4] = x[i][4] - (0.5 - g)
                                if x[i][4] < 0.5:
                                    x[i][4] = 0.5
                    else:
                        g = x[i][2] - (constraining_distance + 0.5)
                        x[i][2] = g
                        if g < 0.5:
                            x[i][2] = 0.5
                            x[i][4] = x[i][4] + g - 0.25
                            if x[i][4] < 0.5:
                                x[i][4] = 0.5

                x[i][0] = np.round(x[i][0], 2)
                x[i][1] = np.round(x[i][1], 2)
                x[i][2] = np.round(x[i][2], 2)
                x[i][3] = np.round(x[i][3], 2)
                x[i][4] = np.round(x[i][4], 2)
                x[i][5] = np.round(x[i][5], 2)
                x[i][6] = np.round(x[i][6], 2)
                x[i][7] = np.round(x[i][7], 2)

            return x


    problem = MyProblem()

    algorithm = NSGA2(
        pop_size=100,
        n_offsprings=100,
        sampling=FloatRandomSampling(),
        crossover=SBX(prob=0.9, eta=15, vtype=float),
        mutation=PM(prob=1, eta=20, vtype=float),
        eliminate_duplicates=True,
        repair=MyRepair()
    )

    current_file_path = os.path.abspath(__file__)
    folder_path = os.path.dirname(current_file_path)
    file_path = os.path.join(folder_path, f'results/all_res_cog_case1_20250506_all_variable.csv')

    termination = get_termination("n_size", file_path, 20000)

    res = minimize(problem,
                   algorithm,
                   termination,
                   seed=1,
                   save_history=False,
                   verbose=True)

    F = res.F
    X = res.X

    print('Execution time: ' + str(res.exec_time / 60 / 60) + ' hours')

    df = pd.DataFrame({
        'X1': X[:, 0], 'X2': [np.round(i * 10,2) for i in X[:, 1]], 'X3': X[:, 2], 'X4': X[:, 3],
        'X5': X[:, 4], 'X6': [np.round(i / 2 + j, 2) for i, j in zip(X[:, 5], X[:, 6])], 'X7': X[:, 6],
        'ANG': F[:, 2], 'AVG': F[:, 0], 'RIP': F[:, 1], 'COG': F[:, 3]})

    if os.path.exists('results'):
        pass
    else:
        os.makedirs('results')

    file_path = os.path.join(folder_path, f'results/nsga2_case1_20250506_all_variable.csv')
    df.to_csv(file_path, encoding='utf-8', index=False)

    folder_path = ['temp_ang', 'temp_avg_rip', 'temp_cog']

    for i in folder_path:
        if os.path.exists(i):
            shutil.rmtree(i)
