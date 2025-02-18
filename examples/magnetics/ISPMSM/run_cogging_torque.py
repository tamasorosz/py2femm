import re
import subprocess
import sys

from matplotlib import pyplot as plt
import tkinter as tk
import calculate_cogging_torque as cogging
import machine_model as model

# The following code is necessary for the parallel computation. Without it the algorithm freezes.
if __name__ == '__main__':

    # List of labels for each input field.
    # The type hint in parentheses is used for input and type conversion.
    # For detailed description of each parameter check: user_guide.md.
    labels = [
        'initial_rotor_position (int/float)',  # 0 - convert to float
        'rotor_diameter (int/float/pos)',  # 1 – convert to float
        'shaft_diameter (int/float/pos)',  # 2 – convert to float
        'magnet_width (int/float/pos)',  # 3 – convert to float
        'magnet_height (int/float/pos)',  # 4 – convert to float
        'pole_pairs (int/pos)',  # 5 – convert to int
        'stack_length (int/float/pos)',  # 6 – convert to float
        'winding_scheme (str)',  # 7 – string
        'shortening (int/float)',  # 8 – convert to float
        'resolution_cogging (int/pos)',  # 9 – convert to int
        'start_position_cogging (int/float)',  # 10 – convert to float
        'end_position_cogging (int/float)',  # 11 – convert to float
        'rounding (int/pos)',  # 12 – convert to int
        'delete_after (bool)',  # 13 – convert to bool
        'number_of_cores (int/pos)'  # 14 - convert to int
    ]


    def go_back():
        """Closes the simulation GUI and reopens the selector."""
        root.destroy()
        subprocess.run([sys.executable, "run_selector.py"])


    def process_entries(dict_of_entries):
        """Uses the submitted inputs of the GUI to perform the cogging torque calculation and plot the results."""

        # Print all the input values submitted to double-check.
        for key, value in dict_of_entries.items():
            print(f"{key}: {value}")
        print('--------------------------------------------------------------------------------')

        # Create the variable parameters from the dictionary of entries for the machine model.
        variables = model.VariableParameters(folder_name='cog',
                                             file_name='cog',
                                             current_density=0,
                                             initial_current_angle=0,
                                             current_angle=0,
                                             initial_rotor_position=dict_of_entries[labels[0]],
                                             rotor_position=0,
                                             rotor_diameter=dict_of_entries[labels[1]],
                                             shaft_diameter=dict_of_entries[labels[2]],
                                             magnet_width=dict_of_entries[labels[3]],
                                             magnet_height=dict_of_entries[labels[4]],
                                             pole_pairs=dict_of_entries[labels[5]],
                                             stack_lenght=dict_of_entries[labels[6]],
                                             winding_scheme=dict_of_entries[labels[7]],
                                             shortening=dict_of_entries[labels[8]]
                                             )

        # Run the cogging torque calculation.
        cogging_torque, result = cogging.cogging(variables=variables,
                                                 resolution=dict_of_entries[labels[9]],
                                                 start_position=dict_of_entries[labels[10]],
                                                 end_position=dict_of_entries[labels[11]],
                                                 rounding=dict_of_entries[labels[12]],
                                                 delete_after=dict_of_entries[labels[13]],
                                                 cores=dict_of_entries[labels[14]])

        # Print the results of the calculation.
        print(f'The cogging torque is {cogging_torque} Nm')
        print(f'The list of torque values: {result}')

        # Plot the results of the calculation.
        plt.figure(figsize=(8, 6))
        plt.plot(result, color='blue', linestyle='-', marker='o')
        plt.title('Cogging Torque')
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

                if "resolution" in label_text:
                    value = int(input_value)
                    if value > 1:
                        valid_inputs[label_text] = value
                    else:
                        print(f"Error: {label_text} must be greater than 1.")
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

                elif input_values[10] >= input_values[11]:
                    print(f"Error: {labels[11]} must be larger than {labels[10]}.")
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

        # If all inputs are valid, proceed with processing
        process_entries(valid_inputs)

    # Create the main application window with tkinter.
    root = tk.Tk()
    root.title("CALCULATING COGGING TORQUE")

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
