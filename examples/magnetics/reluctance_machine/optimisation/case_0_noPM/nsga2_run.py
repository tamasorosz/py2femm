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
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.termination import get_termination
from pymoo.optimize import minimize
from pymoo.termination.default import DefaultMultiObjectiveTermination

import calc_torque_avg_rip

if __name__ == '__main__':
    class MyProblem(ElementwiseProblem):
        def __init__(self):
            super().__init__(n_var=6,
                             n_obj=2,
                             n_ieq_constr=0,
                             n_eq_constr=0,
                             xl=np.array([15, 10, 1, 1, 1, 1]),
                             xu=np.array([25, 15, 4, 2, 4, 5]),
                             vtype=int)

        def _evaluate(self, x, out, *args, **kwargs):

            f = calc_torque_avg_rip.torque_avg_rip(110, x[0], x[1], x[2], x[3], x[4], x[5])

            gc.collect()

            out['F'] = [f[0], f[1]]

    class MyRepair(Repair):
        problem = MyProblem()

        def _do(self, problem, x, **kwargs):

            for i in range(len(x)):
                g = (math.tan(math.radians(x[i][0] / 2)) * (22 - x[i][5]*0.5) + x[i][2] + x[i][4]) - 8
                if g > 0:
                    temp = np.round((8 - (math.tan(math.radians(x[i][0] / 2)) * (22 - x[i][5]*0.5)) - x[i][2]), 2)
                    if temp < 1:
                        x[i][4] = 1
                        x[i][2] = int(x[i][2] - (1 - temp))
                        if x[i][2] < 1:
                            x[i][2] = 1
                    else:
                        x[i][4] = temp

            return x

    problem = MyProblem()

    algorithm = NSGA2(
        pop_size=100,
        n_offsprings=100,
        sampling=IntegerRandomSampling(),
        crossover=SBX(prob=0.9, eta=15, vtype=float, repair=RoundingRepair()),
        mutation=PM(prob=1, eta=20, vtype=float, repair=RoundingRepair()),
        eliminate_duplicates=True,
        repair=MyRepair()
    )

    termination = get_termination("n_gen", 200)

    res = minimize(problem,
                   algorithm,
                   termination,
                   seed=1,
                   save_history=False,
                   verbose=True)

    F = res.F
    X = res.X

    print('Execution time: ' + str(res.exec_time / 60 / 60) + ' hours')

    df = pd.DataFrame({'X1': X[:, 0], 'X2': [i*10 for i in X[:, 1]], 'X3': X[:, 2], 'X4': X[:, 3],
                       'X5': X[:, 4], 'X6': [i*0.5 for i in X[:, 5]], 'AVG': F[:, 0], 'RIP': F[:, 1]})
    current_file_path = os.path.abspath(__file__)
    folder_path = os.path.dirname(current_file_path)

    if os.path.exists('results'):
        pass
    else:
        os.makedirs('results')

    file_path = os.path.join(folder_path, f'results/nsga2_case0_p100o100g200_var6_20250223.csv')
    df.to_csv(file_path, encoding='utf-8', index=False)
