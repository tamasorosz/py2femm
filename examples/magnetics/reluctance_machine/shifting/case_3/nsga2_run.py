# --------------------------------------------------------------------------------------------------------------------
import math
import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pymoo.core.callback import Callback
from pymoo.core.population import Population
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.repair import Repair
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.operators.sampling.rnd import FloatRandomSampling, IntegerRandomSampling
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
                             xl=np.array([10, 10, -8, -8]),
                             xu=np.array([15, 18, 8, 8]),
                             vtype=int)

        def _evaluate(self, x, out, *args, **kwargs):
            f1 = calc_torque_avg_rip.torque_avg_rip(30, 22.1, 146.5, 1.0, 1.0, 3.0, 0.5, 1.5, x[0], x[1], x[2], x[3])
            f2 = calc_cogging.cogging(0, 22.1, 146.5, 1.0, 1.0, 3.0, 0.5, 1.5, x[0], x[1], x[2], x[3])

            out['F'] = [f1[0], f1[1], f2[0], f2[1]]


    problem = MyProblem()


    class MyRepair(Repair):
        problem = MyProblem()

        def _do(self, problem, x, **kwargs):

            for i in range(len(x)):
                x[i][2] = x[i][2] * 2
                x[i][3] = x[i][3] * 2

            for i in range(len(x)):
                if x[i][1] + abs(x[i][3]) > 26:
                    x[i][1] = 18 - abs(x[i][3]) / 2

                if x[i][0] > x[i][1]:
                    x[i][0] = x[i][1]
                    x[i][2] = x[i][3]
                else:
                    if x[i][2] > (x[i][1] - x[i][0]) * 2 + x[i][3]:
                        x[i][2] = (x[i][1] - x[i][0]) * 2 + x[i][3]
                    if x[i][2] < -(x[i][1] - x[i][0]) * 2 + x[i][3]:
                        x[i][2] = -(x[i][1] - x[i][0]) * 2 + x[i][3]

            return x


    class MyCallback(Callback):

        def __init__(self) -> None:
            super().__init__()
            self.data["best"] = []

        def notify(self, algorithm):
            self.data["best"].append(algorithm.pop.get("F").min())


    algorithm = NSGA2(
        pop_size=25,
        n_offsprings=25,
        sampling=IntegerRandomSampling(),
        crossover=SBX(prob=0.9, eta=15, vtype=float, repair=RoundingRepair()),
        mutation=PM(prob=1, eta=20, vtype=float, repair=RoundingRepair()),
        eliminate_duplicates=True,
        repair=MyRepair()
    )

    termination = DefaultMultiObjectiveTermination(
        xtol=1e-8,
        cvtol=1e-6,
        ftol=0.0025,
        period=10,
        n_max_gen=40,
        n_max_evals=3000
    )

    res = minimize(problem,
                   algorithm,
                   termination,
                   seed=1,
                   save_history=True,
                   callback=MyCallback(),
                   verbose=True)

    F = res.F
    X = res.X

    print('Execution time: ' + str(res.exec_time / 60 / 60) + ' hours')

    df = pd.DataFrame({'X1': X[:, 0], 'X2': X[:, 1], 'X3': X[:, 2], 'X4': X[:, 3], 'AVG': F[:, 0], 'RIP': F[:, 1],
                       'P2P': F[:, 2], 'THD': F[:, 3]})
    current_file_path = os.path.abspath(__file__)
    folder_path = os.path.dirname(current_file_path)
    file_path = os.path.join(folder_path, f'results/nsga2_case3_p25o25g40_pareto.csv')
    df.to_csv(file_path, encoding='utf-8', index=False)

    # temp = [e.opt.get("F") for e in res.history]
    # temp = temp[0]
    # conv = [list(sub_array) for sub_array in temp]
    #
    # df_nd = pd.DataFrame(res.X, columns=[f"X{i + 1}" for i in range(problem.n_var)])
    # df_nd['AVG'] = [-i[0] for i in conv]
    # df_nd['RIP'] = [i[1] for i in conv]
    # df_nd['P2P'] = [i[2] for i in conv]
    # df_nd['THD'] = [i[3] for i in conv]
    #
    # current_file_path = os.path.abspath(__file__)
    # folder_path = os.path.dirname(current_file_path)
    # file_path = os.path.join(folder_path, f'results/nsga2_case3_p25o25g40_nd.csv')
    # df_nd.to_csv(file_path, encoding='utf-8', index=False)
    #
    # all_pop = Population()
    #
    # for algorithm in res.history:
    #     all_pop = Population.merge(all_pop, algorithm.off)
    #
    # df_pop = pd.DataFrame(all_pop.get("X"), columns=[f"X{i + 1}" for i in range(problem.n_var)])
    # current_file_path = os.path.abspath(__file__)
    # folder_path = os.path.dirname(current_file_path)
    # file_path = os.path.join(folder_path, f'results/nsga2_case3_p25o25g40_pop.csv')
    # df_pop.to_csv(file_path, encoding='utf-8', index=False)

