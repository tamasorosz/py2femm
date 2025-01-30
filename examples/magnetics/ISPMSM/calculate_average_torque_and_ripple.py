import csv
import copy

from pathlib import Path
import numpy as np
import machine_model as model

from multiprocessing import Pool
from src.executor import Executor

import calculate_max_torque_angle


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


def average_torque_and_ripple(variables: model.VariableParameters, resolution_angle, start_position_angle,
                              end_position_angle, resolution_average_ripple, start_position_average_ripple,
                              end_position_average_ripple, rounding, initial_rotor_position=0, folder_name_angle='ang',
                              file_name_angle='ang', folder_name_average='avg', file_name_average='avg',
                              delete_after=True):

    if initial_rotor_position != 0:
        pass
    else:
        variables.update_folder_name(folder_name_angle)
        variables.update_file_name(file_name_angle)
        initial_rotor_position = calculate_max_torque_angle.max_torque_angle(variables, resolution_angle,
                                                                             start_position_angle,
                                                                             end_position_angle, rounding,
                                                                             delete_after)
    variables.update_folder_name(folder_name_average)
    variables.update_file_name(file_name_average)

    all_variables = []

    if not Path(variables.output_folder).exists():
        Path(variables.output_folder).mkdir(parents=True, exist_ok=True)

    for alpha, beta in zip(np.linspace(start_position_average_ripple, end_position_average_ripple,
                                       resolution_average_ripple),
                           np.linspace(start_position_average_ripple,
                                       variables.pole_pairs * end_position_average_ripple, resolution_average_ripple)):
        mutable_variables = copy.deepcopy(variables)
        mutable_variables.update_initial_rotor_position(initial_rotor_position)
        mutable_variables.update_rotor_position(alpha)
        mutable_variables.update_current_angle((-1) * beta)

        model.model_creation(mutable_variables)

        all_variables.append((mutable_variables, rounding, delete_after))

    with Pool(8) as pool:
        result = list(pool.map(execute_model, all_variables))

    torque_average = np.round(-1 * np.average(result), rounding)
    torque_ripple = np.round(-100 * (np.max(result) - np.min(result)) / torque_average, rounding)

    return torque_average, torque_ripple, result
