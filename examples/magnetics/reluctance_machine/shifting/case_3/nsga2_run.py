# --------------------------------------------------------------------------------------------------------------------
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
from pymoo.termination.default import DefaultMultiObjectiveTermination
from pymoo.optimize import minimize

import calc_torque_avg_rip
import calc_cogging

if __name__ == '__main__':
    class MyProblem(ElementwiseProblem):
        def __init__(self):
            super().__init__(n_var=4,
                             n_obj=4,
                             n_ieq_constr=0,
                             n_eq_constr=0,
                             xl=np.array([1, 1, 1, 1]),
                             xu=np.array([10, 10, 10, 10]))

        def _evaluate(self, x, out, *args, **kwargs):
            f1 = calc_torque_avg_rip.torque_avg_rip(30, 22.1, 146.5, 1.0, 1.0, 3.0, 0.5, 1.5, x[0], x[1], x[2], x[3])
            f2 = calc_cogging.cogging(0, 22.1, 146.5, 1.0, 1.0, 3.0, 0.5, 1.5, x[0], x[1], x[2], x[3])

            out['F'] = [f1[0], f1[1], f2[0], f2[1]]


    problem = MyProblem()


    class MyRepair(Repair):
        problem = MyProblem()

        def _do(self, problem, x, **kwargs):
            for i in range(len(x)):  # ROUNDING FOR 0.1 SEGMENTS
                x[i] = [round(j, 1) for j in x[i]]

            for i in range(len(x)):  # SAFE SWITCH FOR BIGGER MAGNET THAN POCKET
                if x[i][0] > x[i][2]:
                    x[i][0] = x[i][2]
                if x[i][1] > x[i][3]:
                    x[i][1] = x[i][3]

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

    termination = DefaultMultiObjectiveTermination(
        xtol=1e-8,
        cvtol=1e-6,
        ftol=0.0025,
        period=10,
        n_max_gen=100,
        n_max_evals=3000
    )

    res = minimize(problem,
                   algorithm,
                   termination,
                   seed=1,
                   save_history=True,
                   verbose=True)

    F = res.F
    X = res.X
    print('Execution time: ' + str(res.exec_time / 60 / 60) + ' hours')

    df = pd.DataFrame({'X1': X[:, 0], 'X2': X[:, 1], 'X3': X[:, 2], 'X4': X[:, 3], 'AVG': F[:, 0], 'RIP': F[:, 1],
                       'P2P': F[:, 2], 'THD': F[:, 3]})
    current_file_path = os.path.abspath(__file__)
    folder_path = os.path.dirname(current_file_path)
    file_path = os.path.join(folder_path, f'results/nsga2_case3_p50o25g100.csv')
    df.to_csv(file_path, encoding='utf-8', index=False)
