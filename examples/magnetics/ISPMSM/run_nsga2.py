import os
import shutil
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
        'shortening (int/float)',  # 8 – convert to float
        'resolution_angle (int)',  # 9 - convert to int
        'start_position_angle (int/float)',  # 10 - convert to float
        'end_position_angle (int/float)',  # 11 - convert to float
        'resolution_average_ripple (int)',  # 12 – convert to int
        'start_position_average_ripple (int/float)',  # 13 – convert to float
        'end_position_average_ripple (int/float)',  # 14 – convert to float
        'rounding (int)',  # 15 – convert to int
        'lower_boundaries (list)',  # 16 – convert to list
        'upper_boundaries (list)',  # 17 – convert to list
        'population_size (int)',  # 18 – convert to int
        'number_of_offsprings (int)',  # 19 – convert to int
        'number_of_generations (int)',  # 20 – convert to int
        'delete_after (bool)'  # 21 – convert to bool
    ]

    # Define paths
    folder_path = Path(__file__).resolve().parent
    results_path = folder_path / 'results'
    results_path.mkdir(exist_ok=True)  # Ensure the 'results' directory exists

    # Generate filename with date
    date_str = datetime.today().strftime('%Y%m%d')
    file_path_all = results_path / f'nsga2_all_{date_str}.csv'

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
                                 xl=np.array(dict_of_entries[labels[16]]),
                                 xu=np.array(dict_of_entries[labels[17]]),
                                 vtype=int)

            def _evaluate(self, x, out, *args, **kwargs):
                variables = model.VariableParameters(current=dict_of_entries[labels[0]],
                                                     initial_current_angle=dict_of_entries[labels[1]],
                                                     initial_rotor_position=dict_of_entries[labels[2]],
                                                     rotor_diameter=dict_of_entries[labels[3]] - x[0] / 10,
                                                     shaft_diameter=dict_of_entries[labels[4]],
                                                     magnet_width=x[1],
                                                     magnet_height=x[2],
                                                     pole_pairs=dict_of_entries[labels[5]],
                                                     stack_lenght=dict_of_entries[labels[6]],
                                                     winding_scheme=dict_of_entries[labels[7]],
                                                     shortening=dict_of_entries[labels[8]]
                                                     )
                print(f'X1: {x[0] / 10}, X2: {x[1]}, X3: {x[2]}')
                f1, f2, _ = objective_function.average_torque_and_ripple(
                    variables,
                    resolution_angle=dict_of_entries[labels[9]],
                    start_position_angle=dict_of_entries[labels[10]],
                    end_position_angle=dict_of_entries[labels[11]],
                    resolution_average_ripple=dict_of_entries[labels[12]],
                    start_position_average_ripple=dict_of_entries[labels[13]],
                    end_position_average_ripple=dict_of_entries[labels[14]],
                    rounding=dict_of_entries[labels[15]],
                    delete_after=dict_of_entries[labels[21]],
                    optimisation=True)

                out['F'] = [f1, f2]

        problem = MyProblem()

        algorithm = NSGA2(
            pop_size=dict_of_entries[labels[18]],
            n_offsprings=dict_of_entries[labels[19]],
            sampling=IntegerRandomSampling(),
            crossover=SBX(prob=0.9, eta=15, vtype=float, repair=RoundingRepair()),
            mutation=PM(prob=1, eta=20, vtype=float, repair=RoundingRepair()),
            eliminate_duplicates=True
        )

        termination = get_termination("n_gen", dict_of_entries[labels[20]])

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

        with open(file_path_all, 'r') as f:
            df = pd.read_csv(f)

        # Plot the results
        plt.figure(figsize=(8, 6))
        plt.scatter(df.iloc[:, -2], df.iloc[:, -1], color='blue')
        plt.title('Pareto Front')
        plt.xlabel('Average Torque [Nm]')
        plt.ylabel('Torque Ripple [Nm]')
        plt.grid(True)
        plt.show()


    def submit():
        """
        Retrieves inputs from all entry widgets, converts the values according to their type hints,
        and, if all conversions succeed, passes the dictionary of entries to process_entries().
        """
        # Gather the content from each widget in the entries list.
        input_values = [entry.get() for entry in entries]
        flow_checker = True

        try:
            for i, input_value in enumerate(input_values):
                label_text = labels[i]
                # Process numeric fields: check for the (int/float) type hint.
                if "(int/float)" in label_text:
                    input_values[i] = float(input_value)
                elif "(int)" in label_text:
                    input_values[i] = int(input_value)
                elif "(list)" in label_text:
                    input_values[i] = [int(x) for x in input_value.strip("[]").split(",")]
                elif "(bool)" in label_text:
                    if input_value == 'True':
                        input_values[i] = True
                    elif input_value == 'False':
                        input_values[i] = False
                else:
                    input_values[i] = input_value

        except ValueError as e:
            print(f"Error converting {labels[i]}: {e}. Please enter a valid type as specified!")
            print('--------------------------------------------------------------------------------')
            flow_checker = False

        if flow_checker:
            dict_of_entries = {key: value for key, value in zip(labels, input_values)}
            process_entries(dict_of_entries)


    # Create the main application window.
    root = tk.Tk()
    root.title("NSGA-II OPTIMISATION")

    # List to hold the widget or variable associated with each input.
    # For Entry fields, we store the tk.Entry widget.
    entries = []
    num_columns = 2  # Two input pairs per row (each pair occupies 2 grid columns).

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
        else:
            entry = tk.Entry(root, width=20)
            entry.grid(row=row, column=col_group * 2 + 1, padx=5, pady=5, sticky="w")
            entries.append(entry)

    # Determine the row index for the submit button (just after the last row of inputs).
    submit_row = (len(labels) - 1) // num_columns + 1

    # Create the submit button and position it to span across all input columns.
    submit_button = tk.Button(root, text="RUN SIMULATION", command=submit)
    submit_button.grid(row=submit_row, column=0, columnspan=num_columns * 2, pady=10)

    # Start the GUI event loop.
    root.mainloop()
