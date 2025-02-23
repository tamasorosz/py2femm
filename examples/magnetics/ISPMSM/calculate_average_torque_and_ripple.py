import csv
import copy

from pathlib import Path
import numpy as np
import pandas as pd

import machine_model as model

from multiprocessing import Pool
from src.executor import Executor

import calculate_max_torque_angle
import run_nsga2


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


def average_torque_and_ripple(variables: model.VariableParameters,
                              resolution_average_ripple=16,
                              start_position_average_ripple=0,
                              end_position_average_ripple=15,
                              rounding=3,
                              folder_name_angle='ang',
                              file_name_angle='ang',
                              folder_name_average='avg',
                              file_name_average='avg',
                              delete_after=True,
                              resolution_angle=91,
                              start_position_angle=0,
                              end_position_angle=180,
                              cores=1,
                              optimisation=False):
    """
        Create .lua files to calculate the torque angle then average torque and torque ripple based on the input
        parameters and executes them in a parallel simulation process.
        """

    if variables.initial_rotor_position != 0:
        initial_rotor_position = variables.initial_rotor_position
    else:
        variables.update_folder_name(folder_name_angle)
        variables.update_file_name(file_name_angle)
        initial_rotor_position, _ = calculate_max_torque_angle.max_torque_angle(variables,
                                                                                resolution_angle,
                                                                                start_position_angle,
                                                                                end_position_angle,
                                                                                rounding,
                                                                                delete_after)

    variables.update_folder_name(folder_name_average)
    variables.update_file_name(file_name_average)

    all_variables = []

    if not Path(variables.output_folder).exists():
        Path(variables.output_folder).mkdir(parents=True, exist_ok=True)

    # Create .lua files.
    for alpha, beta in zip(np.linspace(start_position_average_ripple, end_position_average_ripple,
                                       resolution_average_ripple),
                           np.linspace(start_position_average_ripple,
                                       variables.pole_pairs * end_position_average_ripple, resolution_average_ripple)):
        mutable_variables = copy.deepcopy(variables)
        mutable_variables.update_initial_rotor_position(initial_rotor_position)
        mutable_variables.update_rotor_position(alpha)
        mutable_variables.update_current_angle(beta)

        model.model_creation(mutable_variables)

        all_variables.append((mutable_variables, rounding, delete_after))

    # Parallel execution.
    with Pool(cores) as pool:
        result = list(pool.map(execute_model, all_variables))

    torque_average = np.round(np.average(result), rounding)
    torque_ripple = np.round((-100) * (np.max(result) - np.min(result)) / torque_average, rounding)

    # Print out interim results to keep track of the process.
    if optimisation:
        with open(run_nsga2.file_path_all, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header row
            row_count = sum(1 for row in reader)  # Count remaining rows

        print(f'ANGLE: {initial_rotor_position}, AVERAGE: {(-1) * torque_average}, RIPPLE: {torque_ripple}\n'
              f'INDEX: {row_count}')
        print('-------------------------------------')

        labels = [
            'current',  # 0
            'rotor_diameter',  # 1
            'shaft_diameter',  # 2
            'magnet_width',  # 3
            'magnet_height',  # 4
            'pole_pairs',  # 5
            'stack_length',  # 6
            'winding_scheme',  # 7
            'shortening',  # 8
        ]

        df = pd.DataFrame({labels[0]: mutable_variables.current,
                           labels[1]: mutable_variables.rotor_diameter,
                           labels[2]: mutable_variables.shaft_diameter,
                           labels[3]: mutable_variables.magnet_width,
                           labels[4]: mutable_variables.magnet_height,
                           labels[5]: mutable_variables.pole_pairs,
                           labels[6]: mutable_variables.stack_lenght,
                           labels[7]: [mutable_variables.winding_scheme],
                           labels[8]: mutable_variables.shortening,
                           'ANG': initial_rotor_position,
                           'AVG': torque_average,
                           'RIP': torque_ripple})

        # Append to CSV, writing header only if the file doesn't exist
        df.to_csv(run_nsga2.file_path_all, mode='a', index=False, header=not run_nsga2.file_path_all.exists())

    return torque_average, torque_ripple, result
