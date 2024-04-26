import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
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
                             xl=np.array([16, 120, 1, 2, 1.5]),
                             xu=np.array([18, 160, 2, 3, 2.5]))

        def _evaluate(self, x, out, *args, **kwargs):
            res = calc_torque_avg_rip.torque_avg_rip(30, x[0], x[1], x[2], 1, x[3], x[4])
            out['F'] = [res[0], res[1]]


    problem = MyProblem()

    algorithm = NSGA2(
        pop_size=50,
        n_offsprings=25,
        sampling=FloatRandomSampling(),
        crossover=SBX(prob=0.9, eta=15),
        mutation=PM(eta=20),
        eliminate_duplicates=True
    )

    termination = get_termination("n_gen", 280)

    res = minimize(problem,
                   algorithm,
                   termination,
                   seed=1,
                   save_history=True,
                   verbose=True)

    F = res.F
    X = res.X
    print('Execution time: ' + str(res.exec_time / 60) + ' minutes')

    df = pd.DataFrame({'X1': X[:, 0], 'X2': X[:, 1], 'X3': X[:, 2], 'X4': X[:, 3], 'X5': X[:, 4], 'AVG': F[:, 0],
                       'RIP': F[:, 1]})
    current_file_path = os.path.abspath(__file__)
    folder_path = os.path.dirname(current_file_path)
    file_path = os.path.join(folder_path, f'results/nsga2_g280.csv')
    df.to_csv(file_path, encoding='utf-8', index=False)

    plt.figure(figsize=(7, 5))
    plt.scatter(F[:, 0], F[:, 1], s=30, facecolors='none', edgecolors='blue')
    plt.title("Objective Space")
    plt.show()
