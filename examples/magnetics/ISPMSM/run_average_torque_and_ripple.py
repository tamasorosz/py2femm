from matplotlib import pyplot as plt
import tkinter as tk
import calculate_average_torque_and_ripple as average
import machine_model as model

if __name__ == '__main__':

    # List of labels for each input field.
    # The type hint in parentheses is used for input.
    labels = [
        'current_density (int/float)',  # 0 – convert to float
        'initial_current_angle (int/float)',  # 1 – convert to float
        'initial_rotor_position (int/float)',  # 2 – convert to float
        'rotor_diameter (int/float)',  # 3 – convert to float
        'shaft_diameter (int/float)',  # 4 – convert to float
        'magnet_width (int/float)',  # 5 – convert to float
        'magnet_height (int/float)',  # 6 – convert to float
        'pole_pairs (int)',  # 7 – convert to int
        'stack_length (int/float)',  # 8 – convert to float
        'winding_scheme (str)',  # 9 – string
        'shortening (int/float)',  # 10 – convert to float
        'resolution_angle (int)',  # 11 - convert to int
        'start_position_angle (int/float)',  # 12 - convert to float
        'end_position_angle (int/float)',  # 13 - convert to float
        'resolution_average_ripple (int)',  # 14 – convert to int
        'start_position_average_ripple (int/float)',  # 15 – convert to float
        'end_position_average_ripple (int/float)',  # 16 – convert to float
        'rounding (int)',  # 17 – convert to int
        'delete_after (bool)'  # 18 – convert to bool
    ]


    def process_entries(dict_of_entries):
        """Uses the submitted input to perform the simulation and plot the results."""
        # Print all the input values
        for key, value in dict_of_entries.items():
            print(f"{key}: {value}")
        print('--------------------------------------------------------------------------------')

        # Create the variable parameters from the dictionary
        variables = model.VariableParameters(folder_name='avg',
                                             file_name='avg',
                                             current_density=dict_of_entries[labels[0]],
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
                                             shortening=dict_of_entries[labels[10]]
                                             )

        # Run the simulation
        average_torque, torque_ripple, result = average.average_torque_and_ripple(
            variables,
            resolution_angle=dict_of_entries[labels[11]],
            start_position_angle=dict_of_entries[labels[12]],
            end_position_angle=dict_of_entries[labels[13]],
            resolution_average_ripple=dict_of_entries[labels[14]],
            start_position_average_ripple=dict_of_entries[labels[15]],
            end_position_average_ripple=dict_of_entries[labels[16]],
            rounding=dict_of_entries[labels[17]],
            delete_after=dict_of_entries[labels[18]])

        print(f'The average torque is {average_torque} Nm')
        print(f'The torque ripple is {torque_ripple} Nm')
        print(f'The list of torque values: {result}')

        # Plot the results
        plt.figure(figsize=(8, 6))
        plt.plot(result, color='blue', linestyle='-', marker='o')
        plt.title('Dynamic Torque')
        plt.xlabel('Rotor position [deg]')
        plt.ylabel('Torque [Nm]')
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
    root.title("CALCULATING AVERAGE TORQUE AND TORQUE RIPPLE")

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
