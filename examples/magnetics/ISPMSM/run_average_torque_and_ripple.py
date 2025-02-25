import re
import subprocess
import sys

import numpy as np
from matplotlib import pyplot as plt
import tkinter as tk
import calculate_average_torque_and_ripple as average
import machine_model as model

# The following code is necessary for the parallel computation. Without it the algorithm freezes.
if __name__ == '__main__':

    # List of labels for each input field.
    # The type hint in parentheses is used for input and type conversion.
    # For detailed description of each parameter check: user_guide.md.
    labels = [
        'current (int/float/pos)',  # 0 – convert to float
        'initial_current_angle (int/float)',  # 1 – convert to float
        'initial_rotor_position (int/float)',  # 2 – convert to float
        'rotor_diameter (int/float/pos)',  # 3 – convert to float
        'shaft_diameter (int/float/pos)',  # 4 – convert to float
        'magnet_width (int/float/pos)',  # 5 – convert to float
        'magnet_height (int/float/pos)',  # 6 – convert to float
        'pole_pairs (int/pos)',  # 7 – convert to int
        'stack_length (int/float/pos)',  # 8 – convert to float
        'winding_scheme (str)',  # 9 – string
        'number_of_coil_turns (int/pos)',  # 10 - convert to int
        'shortening (int/float)',  # 11 – convert to float
        'resolution_angle (int/pos)',  # 12 - convert to int
        'start_position_angle (int/float)',  # 13 - convert to float
        'end_position_angle (int/float)',  # 14 - convert to float
        'resolution_average_ripple (int/pos)',  # 15 – convert to int
        'start_position_average_ripple (int/float)',  # 16 – convert to float
        'end_position_average_ripple (int/float)',  # 17 – convert to float
        'rounding (int/pos)',  # 18 – convert to int
        'delete_after (bool)',  # 19 – convert to bool
        'number_of_cores (int/pos)'  # 20 - convert to int
    ]


    def go_back():
        """Closes the simulation GUI and reopens the selector."""
        root.destroy()
        subprocess.run([sys.executable, "run_selector.py"])


    def process_entries(dict_of_entries):
        """Uses the submitted inputs of the GUI to perform the average torque and torque ripple calculation and plot
         the results."""

        # Print all the input values submitted to double-check.
        for key, value in dict_of_entries.items():
            print(f"{key}: {value}")
        print('--------------------------------------------------------------------------------')

        # Create the variable parameters from the dictionary of entries for the machine model.
        variables = model.VariableParameters(folder_name='avg',
                                             file_name='avg',
                                             current=dict_of_entries[labels[0]],
                                             initial_current_angle=dict_of_entries[labels[1]],
                                             current_angle=0,
                                             initial_rotor_position=dict_of_entries[labels[2]],
                                             rotor_position=0,
                                             rotor_diameter=dict_of_entries[labels[3]],
                                             shaft_diameter=dict_of_entries[labels[4]],
                                             magnet_width=dict_of_entries[labels[5]],
                                             magnet_height=dict_of_entries[labels[6]],
                                             pole_pairs=dict_of_entries[labels[7]],
                                             stack_lenght=dict_of_entries[labels[8]],
                                             winding_scheme=dict_of_entries[labels[9]],
                                             number_of_coil_turns=dict_of_entries[labels[10]],
                                             shortening=dict_of_entries[labels[11]]
                                             )

        # Run the average torque and torque ripple calculation.
        average_torque, torque_ripple, result, initial_rotor_position, result_angle = average.average_torque_and_ripple(
            variables,
            resolution_angle=dict_of_entries[labels[12]],
            start_position_angle=dict_of_entries[labels[13]],
            end_position_angle=dict_of_entries[labels[14]],
            resolution_average_ripple=dict_of_entries[labels[15]],
            start_position_average_ripple=dict_of_entries[labels[16]],
            end_position_average_ripple=dict_of_entries[labels[17]],
            rounding=dict_of_entries[labels[18]],
            delete_after=dict_of_entries[labels[19]],
            cores=dict_of_entries[labels[20]])

        # Print the results of the calculation.
        print(f'The rotor position where the torque is maximal is {initial_rotor_position} degrees')
        print(f'The list of torque values: {result_angle} for the torque angle calculation' )
        print(f'The average torque is {average_torque} Nm')
        print(f'The torque ripple is {torque_ripple} %')
        print(f'The list of torque values: {result} for average torque calculation' )

        if result_angle is not None:
            # Plot the results of the calculation.
            plt.figure(figsize=(8, 6))
            plt.plot(np.linspace(dict_of_entries[labels[13]], dict_of_entries[labels[14]], dict_of_entries[labels[12]]),
                     result_angle,
                     color='blue', linestyle='-', marker='o')
            plt.title('Static Torque')
            plt.xlabel('Rotor position [deg]')
            plt.ylabel('Torque [Nm]')
            plt.grid(True)
            plt.show()

        # Plot the results of the calculation.
        plt.figure(figsize=(8, 6))
        plt.plot(np.linspace(dict_of_entries[labels[16]], dict_of_entries[labels[17]], dict_of_entries[labels[15]]),
                 result,
                 color='blue', linestyle='-', marker='o')
        plt.title('Dynamic Torque')
        plt.xlabel('Rotor position [deg]')
        plt.ylabel('Torque [Nm]')
        plt.grid(True)
        plt.show()


    def submit():
        """
        Retrieves inputs from all entry widgets, converts the values according to their type hints,
        and, if all conversions succeed, passes the dictionary of entries to process_entries(). If not, it raises
        exceptions.
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

        elif valid_inputs[labels[5]] > (constraint := 360 / (valid_inputs[labels[7]] * 2)):
            print(f"Error: {labels[5]} must be lower than {constraint} degrees.")
            return

        elif valid_inputs[labels[6]] > (constraint := (valid_inputs[labels[3]] - valid_inputs[labels[4]]) / 2 - 1.5):
            print(f"Error: {labels[6]} must be lower than {constraint} millimeters.")
            return

        elif valid_inputs[labels[13]] >= valid_inputs[labels[14]]:
            print(f"Error: {labels[14]} must be larger than {labels[13]}.")
            return

        elif valid_inputs[labels[16]] >= valid_inputs[labels[17]]:
            print(f"Error: {labels[17]} must be larger than {labels[16]}.")
            return

        elif valid_inputs[labels[18]] > 10:
            print(f"Error: {labels[18]} must be lower than 10.")
            return

        # If all inputs are valid, proceed with processing
        process_entries(valid_inputs)


    # Create the main application window with tkinter.
    root = tk.Tk()
    root.title("CALCULATING AVERAGE TORQUE AND TORQUE RIPPLE")

    # List to hold the widget or variable associated with each input.
    # For Entry fields, we store the tk.Entry widget.
    entries = []
    num_columns = 3  # Two input pairs per row (each pair occupies 2 grid columns).

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

    # Determine the row index for the submit and back buttons.
    submit_row = (len(labels) - 1) // num_columns + 1
    back_row = (len(labels) - 1) // num_columns + 2

    # Create the back and submit buttons and position it to the middle.
    submit_button = tk.Button(root, text="RUN SIMULATION", command=submit)
    submit_button.grid(row=submit_row, column=0, columnspan=num_columns * 2, pady=5)

    back_button = tk.Button(root, text="BACK", command=go_back)
    back_button.grid(row=back_row, column=0, columnspan=num_columns * 2, pady=5)

    # Start the GUI event loop.
    root.mainloop()
