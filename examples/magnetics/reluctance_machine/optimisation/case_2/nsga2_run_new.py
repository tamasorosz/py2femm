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
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.operators.sampling.rnd import FloatRandomSampling, IntegerRandomSampling
from pymoo.termination import get_termination
from pymoo.termination.default import DefaultMultiObjectiveTermination
from pymoo.optimize import minimize

import calc_torque_avg_rip
from examples.magnetics.reluctance_machine.optimisation.case_2 import calc_cogging

if __name__ == '__main__':
    class MyProblem(ElementwiseProblem):
        def __init__(self):
            super().__init__(n_var=5,
                             n_obj=4,
                             n_ieq_constr=0,
                             n_eq_constr=0,
                             xl=np.array([15, 9, 1, 1, 10]),
                             xu=np.array([25, 15, 4, 4, 15]),
                             vtype=int)

        def _evaluate(self, x, out, *args, **kwargs):
            f1 = calc_torque_avg_rip.torque_avg_rip(30, x[0], x[1], x[2], 1, x[3], 1, x[4], 1.5)
            f2 = calc_cogging.cogging(0, x[0], x[1], x[2], 1, x[3], 1, x[4], 1.5)

            out['F'] = [f1[0], f1[1], f2[0], f2[1]]

    problem = MyProblem()


    class MyRepair(Repair):
        problem = MyProblem()

        def _do(self, problem, x, **kwargs):
            for i in range(len(x)):
                x[i][1] = x[i][1] * 10

            for i in range(len(x)):
                g = (math.tan(math.radians(x[i][0] / 2)) * (22 - (0.5 + 1.5)) + x[i][2] + x[i][3]) - 8
                if g > 0:
                    temp_x3 = round(8 - (math.tan(math.radians(x[i][0] / 2)) * (22 - (0.5 + 1.5))) - x[i][2], 1)
                    if temp_x3 < 1:
                        x[i][3] = 1
                        x[i][2] = x[i][2] - (1 - temp_x3)
                        if x[i][2] < 1:
                            x[i][2] = 1
                    else:
                        x[i][3] = round(temp_x3, 1)

            return x


    algorithm = NSGA2(
        pop_size=50,
        n_offsprings=50,
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
        n_max_gen=100,
        n_max_evals=5000
    )

    res = minimize(problem,
                   algorithm,
                   termination,
                   seed=1,
                   save_history=False,
                   verbose=True)

    F = res.F
    X = res.X

    print('Execution time: ' + str(res.exec_time / 60 / 60) + ' hours')

    df = pd.DataFrame({'X1': X[:, 0], 'X2': X[:, 1], 'X3': X[:, 2], 'X4': X[:, 3], 'X5': X[:, 4],
                       'AVG': F[:, 0], 'RIP': F[:, 1], 'COG': F[:, 2], 'THD': F[:, 3]})
    current_file_path = os.path.abspath(__file__)
    folder_path = os.path.dirname(current_file_path)
    file_path = os.path.join(folder_path, f'results/nsga2_case2_p50o50g100_obj6_20240629.csv')
    df.to_csv(file_path, encoding='utf-8', index=False)
