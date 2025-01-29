import csv
import copy

from pathlib import Path
import numpy as np
import machine_model as model

from multiprocessing import Pool
from src.executor import Executor


def execute_model(args):
    variables, rounding, delete_after = args
    femm = Executor()

    femm.run(variables.output_file + '.lua')

    with open(variables.output_file + '.csv', 'r') as file:
        csvfile = next(csv.reader(file))
        if isinstance(rounding, int):
            torque = np.round(float(''.join(csvfile).replace('wTorque_0 = ', '')), rounding)
        elif rounding is None:
            torque = float(''.join(csvfile).replace('wTorque_0 = ', ''))
        else:
            raise Exception("x")

    if delete_after:
        try:
            Path(variables.output_file + '.lua').unlink()
            Path(variables.output_file + '.fem').unlink()
            Path(variables.output_file + '.ans').unlink()
            Path(variables.output_file + '.csv').unlink()

        except PermissionError:
            print(f'PermissionError')
            pass

    return torque


def max_torque_angle(variables: model.VariableParameters, resolution, start_position, end_position, rounding,
                     delete_after=True):

    all_variables = []
    mutable_variables = copy.deepcopy(variables)

    if not Path(variables.output_folder).exists():
        Path(variables.output_folder).mkdir(parents=True, exist_ok=True)

    for alpha in np.linspace(start_position, end_position, resolution):
        mutable_variables = copy.deepcopy(variables)
        mutable_variables.update_rotor_position(alpha)

        model.model_creation(mutable_variables)

        all_variables.append((mutable_variables, rounding, delete_after))

    with Pool(11) as pool:
        result = list(pool.map(execute_model, all_variables))

    torque_ang = start_position + result.index((max(result))) * ((end_position - start_position) / (resolution - 1))

    result.clear()
    all_variables.clear()

    return torque_ang
