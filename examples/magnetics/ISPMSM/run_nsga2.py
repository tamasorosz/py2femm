import os
import shutil
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd

from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.termination import get_termination
from pymoo.optimize import minimize

import calculate_average_torque_and_ripple as objective_function
import machine_model as model

if __name__ == '__main__':
    class MyProblem(ElementwiseProblem):
        def __init__(self):
            super().__init__(n_var=3,
                             n_obj=2,
                             n_ieq_constr=0,
                             n_eq_constr=0,
                             xl=np.array([1, 35, 1]),
                             xu=np.array([10, 45, 5]),
                             vtype=int)

        def _evaluate(self, x, out, *args, **kwargs):
            variables = model.VariableParameters(current_density=30,
                                                 rotor_diameter=45 - x[0] / 10,
                                                 shaft_diameter=10,
                                                 magnet_width=x[1],
                                                 magnet_height=x[2],
                                                 pole_pairs=4,
                                                 stack_lenght=40,
                                                 winding_scheme='ABCABCABCABC',
                                                 initial_current_angle=-120
                                                 )

            f1, f2 = objective_function.average_torque_and_ripple(variables, resolution_angle=8, start_position_angle=19,
                                                                  end_position_angle=26, resolution_average_ripple=16,
                                                                  start_position_average_ripple=0,
                                                                  end_position_average_ripple=15,
                                                                  rounding=2, delete_after=True)

            out['F'] = [f1, f2]

    problem = MyProblem()

    algorithm = NSGA2(
        pop_size=3,
        n_offsprings=3,
        sampling=IntegerRandomSampling(),
        crossover=SBX(prob=0.9, eta=15, vtype=float, repair=RoundingRepair()),
        mutation=PM(prob=1, eta=20, vtype=float, repair=RoundingRepair()),
        eliminate_duplicates=True
    )

    termination = get_termination("n_gen", 3)

    res = minimize(problem,
                   algorithm,
                   termination,
                   seed=1,
                   save_history=False,
                   verbose=True)

    F = res.F
    X = res.X

    print('Execution time: ' + str(res.exec_time / 60 / 60) + ' hours')

    df = pd.DataFrame({'X1': [i / 10 for i in X[:, 0]], 'X2': X[:, 1], 'X3': X[:, 2],
                       'AVG': F[:, 0], 'RIP': F[:, 1]})

    folder_path = Path(__file__).resolve().parent
    results_path = folder_path / 'results'
    results_path.mkdir(exist_ok=True)
    date_str = datetime.today().strftime('%Y%m%d')
    df.to_csv(results_path / f'nsga2_result_{date_str}.csv', index=False)

    folder_path = ['ang', 'avg']

    for i in folder_path:
        if os.path.exists(i):
            shutil.rmtree(i)
