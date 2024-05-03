import math
import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.repair import Repair
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.termination import get_termination
from pymoo.optimize import minimize

import calc_torque_avg_rip

if __name__ == '__main__':
    class MyProblem(ElementwiseProblem):
        def __init__(self):
            super().__init__(n_var=5,
                             n_obj=2,
                             n_ieq_constr=0,
                             n_eq_constr=0,
                             xl=np.array([1, 1, 0.5, 5, 1]),
                             xu=np.array([4, 4, 1.5, 15, 2]))

        def _evaluate(self, x, out, *args, **kwargs):
            f = calc_torque_avg_rip.torque_avg_rip(30, 24.3, 91.5, x[0], 1, x[1], x[2], x[3], x[4])

            out['F'] = [f[0], f[1]]

    problem = MyProblem()

    class MyRepair(Repair):
        problem = MyProblem()

        def _do(self, problem, x, **kwargs):
            for i in range(len(x)):
                g = (math.tan(math.radians(24.3 / 2)) * (22 - (x[i][2] + x[i][4])) + x[i][0] + x[i][1]) - 8
                if g > 0:
                    temp = 8 - (math.tan(math.radians(24.3 / 2)) * (22 - (x[i][2] + x[i][4]))) - x[i][0]
                    if temp < 1:
                        x[i][1] = 1
                        x[i][0] = x[i][0] - (1 - temp)
                    else:
                        x[i][1] = temp
                else:
                    x[i][1] = x[i][1]

            for i in range(len(x)):
                g = x[i][2] + x[i][4]
                if g > 2.5:
                    x[i][2] = 2.5 - x[i][4]
                else:
                    x[i][2] = x[i][2]

            return x


    algorithm = NSGA2(
        pop_size=50,
        n_offsprings=25,
        sampling=FloatRandomSampling(),
        crossover=SBX(prob=0.9, eta=15),
        mutation=PM(eta=20),
        eliminate_duplicates=True,
        repair=MyRepair()
    )

    termination = get_termination("n_gen", 25)

    res = minimize(problem,
                   algorithm,
                   termination,
                   seed=1,
                   save_history=True,
                   verbose=True)

    F = res.F
    X = res.X
    print('Execution time: ' + str(res.exec_time / 60 / 60) + ' hours')

    df = pd.DataFrame({'X1': X[:, 0], 'X2': X[:, 1], 'X3': X[:, 2], 'X4': X[:, 3], 'X5': X[:, 4], 'AVG': F[:, 0],
                       'RIP': F[:, 1]})
    current_file_path = os.path.abspath(__file__)
    folder_path = os.path.dirname(current_file_path)
    file_path = os.path.join(folder_path, f'results/nsga2_test.csv')
    df.to_csv(file_path, encoding='utf-8', index=False)

    plt.figure(figsize=(7, 5))
    plt.scatter(F[:, 0], F[:, 1], s=30, facecolors='none', edgecolors='blue')
    plt.title("Objective Space")
    plt.show()
