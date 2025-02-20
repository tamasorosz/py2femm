import csv
import copy

from pathlib import Path
import numpy as np

import machine_model as model

from multiprocessing import Pool
from src.executor import Executor


def execute_model(args):
    """
    Executes the previously generated .lua file and read the calculated torque values from the generated .csv file.
    """
    variables, rounding, delete_after = args
    femm = Executor()

    # Execute the .lua file.
    femm.run(variables.output_file + '.lua')

    # Open .csv and read the calculated torque value.
    with open(variables.output_file + '.csv', 'r') as file:
        csvfile = next(csv.reader(file))
        if isinstance(rounding, int):
            torque = np.round(float(''.join(csvfile).replace('wTorque_0 = ', '')), rounding)
        else:
            torque = float(''.join(csvfile).replace('wTorque_0 = ', ''))

    # Delete temporary files.
    if delete_after:
        try:
            Path(variables.output_file + '.lua').unlink()
            Path(variables.output_file + '.fem').unlink()
            Path(variables.output_file + '.ans').unlink()
            Path(variables.output_file + '.csv').unlink()

        except PermissionError as e:
            print(f'{e}')
            pass

    return torque


def max_torque_angle(variables: model.VariableParameters,
                     resolution=91,
                     start_position=0,
                     end_position=180,
                     rounding=3,
                     folder_name='ang',
                     file_name='ang',
                     delete_after=True,
                     cores=1):
    """
    Create .lua files to calculate the torque angle based on the input parameters and executes them in a parallel
    simulation process.
    """

    variables.update_folder_name(folder_name)
    variables.update_file_name(file_name)

    all_variables = []

    if not Path(variables.output_folder).exists():
        Path(variables.output_folder).mkdir(parents=True, exist_ok=True)

    # Create .lua files.
    for alpha in np.linspace(start_position, end_position, resolution):
        mutable_variables = copy.deepcopy(variables)
        mutable_variables.update_initial_rotor_position(variables.initial_rotor_position)
        mutable_variables.update_rotor_position(alpha)

        model.model_creation(mutable_variables)

        all_variables.append((mutable_variables, rounding, delete_after))

    # Parallel execution.
    with Pool(cores) as pool:
        result = list(pool.map(execute_model, all_variables))

    torque_ang = start_position + result.index((max(result))) * ((end_position - start_position) / (resolution - 1))

    return torque_ang, result
