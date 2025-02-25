import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import tkinter as tk

from matplotlib import pyplot as plt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.termination import get_termination
from pymoo.optimize import minimize
from torch.nn.init import constant
from torchgen.executorch.api.et_cpp import return_names

import calculate_average_torque_and_ripple as objective_function
import machine_model as model

if __name__ == '__main__':

    # List of labels for each input field.
    # The type hint in parentheses is used for input.
    labels = [
        'current (int/float)',  # 0 – convert to float
        'initial_current_angle (int/float)',  # 1 – convert to float
        'initial_rotor_position (int/float)',  # 2 – convert to float
        'rotor_diameter (int/float)',  # 3 – convert to float
        'shaft_diameter (int/float)',  # 4 – convert to float
        'pole_pairs (int)',  # 5 – convert to int
        'stack_length (int/float)',  # 6 – convert to float
        'winding_scheme (str)',  # 7 – string
        'number_of_coil_turns (int/pos)',  # 8 - convert to int
        'shortening (int/float)',  # 9 – convert to float
        'resolution_angle (int)',  # 10 - convert to int
        'start_position_angle (int/float)',  # 11 - convert to float
        'end_position_angle (int/float)',  # 12 - convert to float
        'resolution_average_ripple (int)',  # 13 – convert to int
        'start_position_average_ripple (int/float)',  # 14 – convert to float
        'end_position_average_ripple (int/float)',  # 15 – convert to float
        'rounding (int)',  # 16 – convert to int
        'lower_boundaries (list)',  # 17 – convert to list
        'upper_boundaries (list)',  # 18 – convert to list
        'population_size (int)',  # 19 – convert to int
        'number_of_offsprings (int)',  # 20 – convert to int
        'number_of_generations (int)',  # 21 – convert to int
        'delete_after (bool)',  # 22 – convert to bool
        'number_of_cores (int/pos)'  # 23 - convert to int
    ]

    def go_back():
        """Closes the simulation GUI and reopens the selector."""
        root.destroy()
        subprocess.run([sys.executable, "run_selector.py"])

    # Define paths
    folder_path = Path(__file__).resolve().parent
    results_path = folder_path / 'results'
    results_path.mkdir(exist_ok=True)  # Ensure the 'results' directory exists

   # Generate NSGA-II result file path
    date_str = datetime.today().strftime('%Y%m%d')
    file_path_res = results_path / f'nsga2_result_{date_str}.csv'

    # Generate a filepath for a .csv that contains all the calculated models.
    date_str = datetime.today().strftime('%Y%m%d')
    file_path_all = results_path / f'nsga2_all_{date_str}.csv'

    if file_path_res.exists():
        file_path_res.unlink()
    if file_path_all.exists():
        file_path_all.unlink()

    def process_entries(dict_of_entries):
        """Uses the submitted input to perform the simulation and plot the results."""
        # Print all the input values
        for key, value in dict_of_entries.items():
            print(f"{key}: {value}")
        print('--------------------------------------------------------------------------------')

        class MyProblem(ElementwiseProblem):
            def __init__(self):
                super().__init__(n_var=3,
                                 n_obj=2,
                                 xl=np.array(dict_of_entries[labels[17]]),
                                 xu=np.array(dict_of_entries[labels[18]]),
                                 vtype=int)

            def _evaluate(self, x, out, *args, **kwargs):
                variables = model.VariableParameters(current=dict_of_entries[labels[0]],
                                                     initial_current_angle=dict_of_entries[labels[1]],
                                                     initial_rotor_position=dict_of_entries[labels[2]],
                                                     rotor_diameter=dict_of_entries[labels[3]] + x[0] / 10,
                                                     shaft_diameter=dict_of_entries[labels[4]],
                                                     magnet_width=x[1],
                                                     magnet_height=x[2],
                                                     pole_pairs=dict_of_entries[labels[5]],
                                                     stack_lenght=dict_of_entries[labels[6]],
                                                     winding_scheme=dict_of_entries[labels[7]],
                                                     number_of_coil_turns=dict_of_entries[labels[8]],
                                                     shortening=dict_of_entries[labels[9]]
                                                     )
                print(f'X1: {x[0] / 10}, X2: {x[1]}, X3: {x[2]}')
                f1, f2, _, _, _ = objective_function.average_torque_and_ripple(
                    variables,
                    resolution_angle=dict_of_entries[labels[10]],
                    start_position_angle=dict_of_entries[labels[11]],
                    end_position_angle=dict_of_entries[labels[12]],
                    resolution_average_ripple=dict_of_entries[labels[13]],
                    start_position_average_ripple=dict_of_entries[labels[14]],
                    end_position_average_ripple=dict_of_entries[labels[15]],
                    rounding=dict_of_entries[labels[16]],
                    delete_after=dict_of_entries[labels[22]],
                    optimisation=True,
                    cores=dict_of_entries[labels[23]],
                    file_path=file_path_all)

                out['F'] = [-f1, f2]

        problem = MyProblem()

        algorithm = NSGA2(
            pop_size=dict_of_entries[labels[19]],
            n_offsprings=dict_of_entries[labels[20]],
            sampling=IntegerRandomSampling(),
            crossover=SBX(prob=0.9, eta=15, vtype=float, repair=RoundingRepair()),
            mutation=PM(prob=1, eta=20, vtype=float, repair=RoundingRepair()),
            eliminate_duplicates=True
        )

        termination = get_termination("n_gen", dict_of_entries[labels[21]])

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
                           'AVG': -F[:, 0], 'RIP': F[:, 1]})

        df.to_csv(results_path / f'nsga2_result_{date_str}.csv', index=False)

        folder_path = ['ang', 'avg']

        for i in folder_path:
            if os.path.exists(i) and dict_of_entries[labels[22]]:
                shutil.rmtree(i)

        with open(file_path_all, 'r') as f:
            df1 = pd.read_csv(f)
        with open(file_path_res, 'r') as f:
            df2 = pd.read_csv(f)

        # Plot the results
        plt.figure(figsize=(8, 6))
        plt.scatter(df1.iloc[:, -2], df1.iloc[:, -1], color='blue', label='dominated')
        plt.scatter(df2.iloc[:, -2], df2.iloc[:, -1], color='red', label='non-dominated')
        plt.title('Pareto Front')
        plt.xlabel('Average Torque [Nm]')
        plt.ylabel('Torque Ripple [Nm]')
        plt.grid(True)
        plt.legend()
        plt.show()


    def submit():
        """
        Retrieves inputs from all entry widgets, converts the values according to their type hints,
        and, if all conversions succeed, passes the dictionary of entries to process_entries().
        """
        # Gather the content from each widget in the entries list.
        input_values = [entry.get() for entry in entries]
        valid_inputs = {}

        # Makes the type conversion based on their type hints and handles exceptions.
        try:
            for i, input_value in enumerate(input_values):
                label_text = labels[i]

                if not input_value.strip():  # Check for empty input
                    print(f"Error: {label_text} cannot be empty.")
                    return

                elif "(int/float)" in label_text:
                    valid_inputs[label_text] = float(input_value)

                elif "(int/float/pos)" in label_text:
                    value = float(input_value)
                    if value > 0:
                        valid_inputs[label_text] = value
                    else:
                        print(f"Error: {label_text} must be greater than 0.")
                        return

                elif "(int)" in label_text:
                    valid_inputs[label_text] = int(input_value)

                elif "(int/pos)" in label_text:
                    value = int(input_value)
                    if value > 0:
                        valid_inputs[label_text] = value
                    else:
                        print(f"Error: {label_text} must be greater than 0.")
                        return

                elif "(bool)" in label_text:
                    if input_value.lower() in ["true", "false"]:
                        valid_inputs[label_text] = input_value.lower() == "true"
                    else:
                        print(f"Error: {label_text} must be 'True' or 'False'.")
                        return

                elif "(list)" in label_text:
                    if bool(re.fullmatch(r"^(\d+),(\d+),(\d+)$", input_value)):
                        valid_inputs[label_text] = [float(i) for i in input_value.split(",")]
                    else:
                        print(f"Error: {label_text} must be in the format i,j,k where i,j and k are integers.")
                        return

                else:
                    if bool(re.fullmatch(r"^(?:[A-Ca-c]\|){12}$", input_value)):
                        valid_inputs[label_text] = input_value
                    elif bool(re.fullmatch(r"^(?:[A-Ca-c][A-Ca-c]\|){12}$", input_value)):
                        valid_inputs[label_text] = input_value
                    elif bool(re.fullmatch(r"^(?:[A-Ca-c]){12}$", input_value)):
                        valid_inputs[label_text] = input_value
                    else:
                        print(f"Error: {label_text} must be a valid winding topology."
                              f"Check the user guide for more information.")
                        return

        except (ValueError, TypeError) as e:
            print(f"Error processing {label_text}: {e}. Please enter a valid type as specified!")
            return

        if valid_inputs[labels[4]] >= valid_inputs[labels[3]]:
            print(f"Error: {labels[3]} must be larger than {labels[4]}.")
            return

        elif valid_inputs[labels[3]] >= 45:
            print(f"Error: {labels[3]} must be lower than 45 millimeters.")
            return

        elif valid_inputs[labels[11]] >= valid_inputs[labels[12]]:
            print(f"Error: {labels[12]} must be larger than {labels[11]}.")
            return

        elif valid_inputs[labels[14]] >= valid_inputs[labels[15]]:
            print(f"Error: {labels[15]} must be larger than {labels[14]}.")
            return

        elif valid_inputs[labels[16]] > 10:
            print(f"Error: {labels[16]} must be lower than 10.")
            return

        elif any(i > j for i, j in zip(valid_inputs[labels[17]], valid_inputs[labels[18]])):
            print(f"Error: All values of {labels[17]} must be lower than {labels[18]}.")
            return

        elif valid_inputs[labels[3]] + valid_inputs[labels[18]][0]/10 >= 45:
            print(f"Error: {labels[3]} + the first element (X1) of {labels[18]}/10 must be lower than 45 millimeters.")
            return

        elif valid_inputs[labels[17]][1] <= 0:
            print(f"Error: the second element (X2) of {labels[17]} must be greater than 0.")
            return

        elif valid_inputs[labels[18]][1] > (constraint:=360 / (valid_inputs[labels[5]] * 2)):
            print(f"Error: the second element (X2) of {labels[18]} must be lower than {constraint} degrees.")
            return

        elif valid_inputs[labels[17]][2] <= 0:
            print(f"Error:the third element (X3) of {labels[17]} must be greater than 0.")
            return

        elif valid_inputs[labels[18]][2] > (constraint := (valid_inputs[labels[3]] - valid_inputs[labels[4]]) / 2 - 1.5):
            print(f"Error: the third element (X2) of {labels[18]} must be lower than {constraint} millimeters.")
            return

        # If all inputs are valid, proceed with processing
        process_entries(valid_inputs)


    # Create the main application window.
    root = tk.Tk()
    root.title("NSGA-II OPTIMISATION")

    # List to hold the widget or variable associated with each input.
    # For Entry fields, we store the tk.Entry widget.
    entries = []
    num_columns = 4  # Two input pairs per row (each pair occupies 2 grid columns).

    # Loop through each label and create a label widget and its corresponding input widget.
    for i, label_text in enumerate(labels):
        row = i // num_columns  # Determine the current row.
        col_group = i % num_columns  # Determine the current column group.

        # Create and position the label.
        label = tk.Label(root, text=f"{label_text}:")
        label.grid(row=row, column=col_group * 2, padx=5, pady=5, sticky="e")

        # For boolean fields, use an OptionMenu; otherwise, use a regular Entry widget.
        if '(bool)' in label_text:
            var = tk.StringVar(root)
            var.set("True")  # Default value.
            option_menu = tk.OptionMenu(root, var, "True", "False")
            option_menu.config(width=10)
            option_menu.grid(row=row, column=col_group * 2 + 1, padx=5, pady=5, sticky="w")
            entries.append(var)
        elif 'number_of_cores (int/pos)' in label_text:
            var = tk.StringVar(root)
            var.set("1")  # Default value.
            option_menu = tk.OptionMenu(root, var, "2", "3", "4", "5", "6", "7", "8")
            option_menu.config(width=10)
            option_menu.grid(row=row, column=col_group * 2 + 1, padx=5, pady=5, sticky="w")
            entries.append(var)
        else:
            entry = tk.Entry(root, width=20)
            entry.grid(row=row, column=col_group * 2 + 1, padx=5, pady=5, sticky="w")
            entries.append(entry)

    # Determine the row index for the submit button (just after the last row of inputs).
    submit_row = (len(labels) - 1) // num_columns + 1
    back_row = (len(labels) - 1) // num_columns + 2

    # Create the submit button and position it to span across all input columns.
    submit_button = tk.Button(root, text="RUN SIMULATION", command=submit)
    submit_button.grid(row=submit_row, column=0, columnspan=num_columns * 2, pady=10)

    back_button = tk.Button(root, text="BACK", command=go_back)
    back_button.grid(row=back_row, column=0, columnspan=num_columns * 2, pady=5)

    # Start the GUI event loop.
    root.mainloop()
