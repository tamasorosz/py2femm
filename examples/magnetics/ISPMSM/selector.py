import subprocess
import sys

import tkinter as tk

def option_1():
    """ Opens the cogging torque calculation from the selector. """
    open_second_gui('run_cogging_torque.py')

def option_2():
    """ Opens the torque angle calculation from the selector. """
    open_second_gui('run_max_torque_angle.py')

def option_3():
    """ Opens the average torque and torque ripple calculation from the selector. """
    open_second_gui('run_average_torque_and_ripple.py')

def option_4():
    """ Opens the NSGA-II optimisation from the selector. """
    open_second_gui('run_nsga2.py.py')

def open_second_gui(filepath):
    """Closes the first GUI and opens another script. """
    root.destroy()
    subprocess.run([sys.executable, f'{filepath}'])

# Create main GUI window.
root = tk.Tk()
root.title("SELECT SIMULATION")
root.geometry("300x300")

# Create buttons.
btn1 = tk.Button(root, text="COGGING", command=option_1, width=20, height=2)
btn2 = tk.Button(root, text="TORQUE ANGLE", command=option_2, width=20, height=2)
btn3 = tk.Button(root, text="AVERAGE TORQUE", command=option_3, width=20, height=2)
btn4 = tk.Button(root, text="OPTIMISATION", command=option_4, width=20, height=2)

# Arrange buttons in grid layout.
btn1.pack(pady=10)
btn2.pack(pady=10)
btn3.pack(pady=10)
btn4.pack(pady=10)

# Run GUI loop.
root.mainloop()
