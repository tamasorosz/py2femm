# Inset Surface Permanent Magnet Synchronous Machine Torque Calculation

## A fully functional EXAMPLE project written in Python, automating FEMM solver to calculate the EXAMPLE machines torque angle, average torque, torque ripple and NSGA-II optimisation with a GUI

This project is an example to calculate the different torque values of an example electric machine, aiming to help
students and anyone who is interested to learn about how electric machines work. The calculations are initialised
with a GUI eliminating deep Python coding knowledge prerequisite and helps focusing on the physics backround and the 
behaviour of the electric machine. **For some examples and limitations check tests_and_examples.md file.**

* Select torque angle, average torque and torque ripple, cogging torque or NSGA-II. optimisation via a GUI.
* Create the topology of the electric machine by defining the main parameters through a separate GUI for each function.
* Parameterise the simulation to calculate the torque component with the same GUI where the motor topology is defined.
* Possible parallelisation from 1 to 8 cores.
* Save all calculated optimisation models, calculating and plotting the Pareto Front.

** INSERT A FLOW CHART AND A VIDEO EXPLAINING HOW IT WORKS **

## How to install and run this example project

1. Download an IDE (PyCharm Community Edition recommended: https://www.jetbrains.com/pycharm/download/?section=windows)
2. Download Python 3.9< from https://www.python.org/downloads/
3. Configure IDE (help: https://www.jetbrains.com/help/pycharm/getting-started.html)
4. Clone this project from https://github.com/tamasorosz/py2femm
5. Install packages (list below)
6. Locate examples>magnetics>ISPMSM>run_selector.py
7. Enjoy!

        Third Party Packages*
        - math:                    for trigonometric functions
        - numpy:                   arrays and radians from/to conversion
        - re:                      exception handling for strings
        - pathlib:                 folder and file path handling
        - ezdxf:                   reading dxf files
        - csv:                     reading and writing .csv files
        - copy:                    creating copies of the model objects
        - multiprocessing:         parallel processing of working points
        - pandas:                  handling numerous data points
        - subprocess:              calling FEMM solver
        - sys:                     handling interconnectivity of the GUIs
        - matplotlib:              plotting results
        - tkinter:                 handling GUI
        - os:                      path handling
        - shutil:                  removal of temporary files
        - datetime:                getting the date of start
        - pymoo:                   NSGA-II optimisation framework
        
        *Third party packages directly used by this example.
         Some more packages are used by py2FEMM which are not necessarraly used
         by this example but listed below. If necessarry the IDE will warn you on run.

       Third Party Packages for py2FEMM (no duplicates)
       - dataclasses
       - string
       - enum
       - threading
       - typing
       - json
       - uvicorn
       - fastapi
       - pydantic
       - abc
       - uuid
       - itertools

## What each parameter in the simulations represents

### [machine_model.py](../machine_model.py)

This file contains the machine model. Its stator is built from a .dxf file directly, while its winding, rotor, materials
boundary conditions are parameterised with the p2FEMM functions to communicate with FEMM which accepts .lua commands.

The **VariableParameters** class contains all the variables needed to build the machine model. There are some parameters
necessary for the file handling, some for the geometry and some for the simulations.

#### File handling parameters of VariableParameters class:

* **folder_name**: It specifies a folder where the temporary simulation files are stored separately for each type of
torque calculation function. It can be any kind of character which is valid for a folder name. For cogging torque
calculation "cog", for torque angle calculation "ang", for average torque and torque ripple calculation "avg" is
recommended.


* **file_name**: It specifies the name of the temporary simulation files separately for each type of
torque calculation function stored in the according folders. It can be any kind of character which is valid for a file
name. For cogging torque calculation "cog", for torque angle calculation "ang", for average torque and torque ripple
calculation "avg" is recommended. Each file is unique as all ends with a number corresponding to the rotor position.

#### Geometry and physics parameters of VariableParameters class:
\*some parameters not covered here, please check [tests_and_examples.md](tests_and_examples.md)


* **current_angle [electrical degrees]**: It specifies the resulting magnetic field and rotates the magnetic field in
each simulation step.


* **rotor_position [mechanical degrees]:** It specifies the rotor position and rotates it in every simulation step.



## How to tweak this project to your own uses

### Functions and building blocks 

## Find a bug or want to contribute?
- open issue
- fill pull request template

**Many thanks for the contribution!**

## Like this project?
If you are feeling generous buy me a coffee:

**Many thanks for the support!**
