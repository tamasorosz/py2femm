# Inset Surface Permanent Magnet Synchronous Machine Torque Calculation

## A fully functional EXAMPLE project written in Python, automating FEMM solver to calculate an EXAMPLE machine's torque angle, average torque, torque ripple and NSGA-II optimisation with a GUI

This project is an example of calculating the different torque values of an example electric machine, aiming to help
students and anyone interested in learning about how electric machines work. The calculations are initialised
with a GUI, eliminating the deep Python coding knowledge prerequisite and helping to focus on the physics background and the 
behaviour of the electric machine. **For some examples, rules, tips and limitations check the tests_and_examples.md file.**

* Select torque angle, average torque and torque ripple, cogging torque or NSGA-II optimisation via a GUI.
* Create the topology of the electric machine by defining the main parameters through a separate GUI for each function.
* Parameterise the simulation to calculate the torque component with the same GUI where the motor topology is defined.
* Possible parallelisation from 1 to 8 cores.
* Save all calculated optimisation models, calculating and plotting the Pareto Front.

## How to install and run this example project

1. Download FEMM https://www.femm.info/wiki/HomePage and install to
   - On Windows:
   ```C:\femm42\bin\femm.exe```
   - On Linux/macOS (using Wine):
   ```~/Downloads/femm42bin_x64.exe```
2. Download Python 3.9< from https://www.python.org/downloads/
3. Download an IDE (PyCharm Community Edition recommended: https://www.jetbrains.com/pycharm/download/?section=windows)
   
   **Note: There is no need for an IDE, you can use the command line too.**
4. Configure IDE (help: https://www.jetbrains.com/help/pycharm/getting-started.html) if needed.
5. Clone this project from https://github.com/tamasorosz/py2femm
   - ```git clone https://github.com/tamasorosz/py2femm```
6. Install packages from
   ```pip install -r D:\Respositories\py2femm\examples\magnetics\ISPMSM\requirements.txt```
7. Locate run_selector.py
   - ```cd D:\Respositories\py2femm\examples\magnetics\ISPMSM```
   - Makes sure /src/ is pointed in your PYTHONPATH if necessary
   - ```python run_selector.py```
8. Enjoy!

Some more packages are used by py2FEMM, which are not necessarily used
in this example. If necessary, the IDE will warn you on the run. To solve

```pip install -r D:\Respositories\py2femm\requirements.txt```

## How to tweak the code for your unique project

### [machine_model.py](../machine_model.py)

This file contains the machine model. Its stator is built from a .dxf file directly, while its winding, rotor, materials
boundary conditions are parameterised with the p2FEMM functions to communicate with FEMM, which accepts .lua commands.

The **VariableParameters** class contains all the variables needed to build the machine model. There are some parameters
necessary for the file handling, some for the geometry and some for the simulations.

#### File handling parameters of VariableParameters class:

* **folder_name**: It specifies a folder where the temporary simulation files are stored separately for each type of
torque calculation function. It can be any kind of character valid for a folder name. For cogging torque
calculation, "cog", for torque angle calculation "ang", for average torque and torque ripple calculation "avg" is
recommended.


* **file_name**: It specifies the name of the temporary simulation files separately for each type of
torque calculation function stored in the according folders. It can be any kind of character valid for a file
name. For cogging torque calculation "cog", for torque angle calculation "ang", for average torque and torque ripple
calculation "avg" is recommended. Each file is unique as all ends with a number corresponding to the rotor position.

* **output_folder**: It specifies the output folder for the .fem, .lua, .csv and other files for the simulation. It is 
generated automatically from **folder_name** and **file_name**. The resulting folder is created in the ISPMSM root folder,
where all the .py files for the algoritm are.

* **output_file**: It specifies the output file path and the algorithm generates the .fem, .lua, .csv and other files
for the simulation.

#### Geometry and physics parameters of VariableParameters class:
\*some parameters not covered here, please check [tests_and_examples.md](tests_and_examples.md)

* **current_density**: The algorithm asks for an input of the maximal value of the sinusoidal excitation current but the
machine_model.py converts it to current density. It is more versatile to use current density while using f=0Hz static
simulations. Be aware that at f!=0Hz, it does not produce the same excitation as generating a circuit. The stator's 
generated magnetic field depends on the total current in one slot, meaning _**current** * **number_of_coil_turn**_. 
Technically, to define one phase, you should only define a material label in the slot, and if you define the current density
which is [A/mm2] in dimensions the conversion from maximal current is _**current** / **slot_area**_ where the slot area
is a static parameter easily obtained from the stator dxf with a CAD program.

#### Functions:

The following functions are defined for the VariableParameters class because the following algorithms calculate the
torque values dynamically and change these parameters. What these functions do is highlighted in each function.

    def update_current(self, new_current):
        """ Update current dynamically whenever the current parameter changes and the definition of the phases. """
        self.current_density = new_current * self.number_of_coil_turns / self.slot_cross_section_area
        self.update_phases()

    def update_initial_rotor_position(self, new_initial_rotor_position):
        """ Update initial_rotor_position dynamically whenever the rotor is rotated to its initial position. """
        self.initial_rotor_position = new_initial_rotor_position

    def update_rotor_position(self, new_rotor_position):
        """ Update rotor_position and regenerate output_file and output_folder dynamically whenever the rotor is rotated. """
        self.rotor_position = new_rotor_position
        self.update_output_file()
        self.update_output_folder()

    def update_folder_name(self, new_folder_name):
        """ Update folder and regenerate output_file and output_folder dynamically. """
        self.folder = new_folder_name
        self.update_output_file()
        self.update_output_folder()

    def update_file_name(self, new_file_name):
        """ Update folder and regenerate output_file and output_folder dynamically. """
        self.filename = new_file_name
        self.update_output_file()
        self.update_output_folder()

    def update_output_file(self):
        """ Update output_file dynamically whenever it changes. """
        self.output_file = f"{current_folder_path}/{self.folder}/{self.filename}_{self.rotor_position}"

    def update_output_folder(self):
        """ Update output_folder dynamically whenever it changes. """
        self.output_folder = f"{current_folder_path}/{self.folder}"

    def update_current_angle(self, new_current_angle):
        """ Update current_angle dynamically whenever current_angle changes, so the stator magnetic field is rotated. """
        self.current_angle = new_current_angle
        self.update_phases()

    def update_phases(self):
        """ Update phases dynamically whenever current_angle or current or number_of_coil_turns changes. """
        self.JUp = self.current_density * math.cos(math.radians(self.current_angle))
        self.JUn = (-1) * self.JUp
        self.JVp = self.current_density * math.cos(math.radians(self.current_angle + 120))
        self.JVn = (-1) * self.JVp
        self.JWp = self.current_density * math.cos(math.radians(self.current_angle + 240))
        self.JWn = (-1) * self.JWp

## How to tweak this project to your own use and create a unique geometry

The geometry is defined in [machine_model.py](../machine_model.py). First, the machine should be designed according to
parameters. Here are a few questions which should help you decide:

* Which parts should be parameterised? --> Define variables and code the geometry.
* Which parts should be static? --> Create the geometry in a .dxf and import.
* What is the goal of the calculation? --> Check FEMM for its capabilities: https://www.femm.info/wiki/Documentation/
* The py2FEMM package follows the original documentation in terms of calculations but makes the geometry definition 
easier. Dwell into the code of the py2FEMM package to create unique simulations.
* Keep the variable parameters at the minimum necessary number!

### How to import a .dxf geometry

      def stator_geometry(femm_model: FemmProblem):
       """Importing stator geometry from a dxf file instead of manually defining the nodes, lines and arcs."""

          stator = Geometry()

          stator.import_dxf("resources/stator_distributed_1layer.dxf")

          femm_model.create_geometry(stator)

First, create a function in the machine_model.py file representing the part intended to be defined. In this
case, it is the stator imported from a .dxf file. One necessary argument is the FemmProblem class, which initiates
the .lua file generation and is unique to the py2FEMM package. The second step is creating a geometry object that tells
the FemmProblem that the input is geometry. Use the _import_dxf_ function of the Geometry() class to import the .dxf
geometry. Lastly, create the geometry. The last function tells the FemmProblem that it should write the geometry in the
.lua file, which is the input of the FEMM solver.

### How to create a parametric rotor geometry

\*The following code snippet contains examples, not a working code.

      def rotor_geometry(femm_model: FemmProblem, variables: VariableParameters):
          """Create rotor geometry."""

         rotor = Geometry()

         shaft_node_left = Node((-1) * variables.shaft_diameter / 2, 0.0)

         shaft_arc_lower = CircleArc(shaft_node_left, N0, shaft_node_right)

         rotor.add_arc(shaft_arc_lower)

         magnet_nociri = vertical_node_circumference.rotate_about(N0, np.radians(variables.magnet_width / 2))
         
         magnet_line_left = Line(magnet_node_circumference_left, magnet_node_lower_left)

         rotor.add_line(magnet_line_left)

         femm_model.create_geometry(rotor)

         return magnet_arc_for_material_lower, magnet_arc_for_material_upper

First, create a function in the machine_model.py file representing the part intended to be defined. In this
case, the rotor is uniquely defined and parameterised. There are two necessary arguments the FemmProblem class which initiates
the .lua file generation and is unique to the py2FEMM package and the VariableParameters for parametrisation.
The second step is creating a geometry object that tells the FemmProblem that the input is geometry. The following
features are available to create a geometry. Be aware that not all possibilities are covered here, so please look into the code
of py2FEMM for further information.


* **Node()**: The FEMM works with nodes, lines and arcs, which are enough to define any geometry. A line and an arc can
only be defined between two nodes. FEMM also works in cartesian coordinates so that a node can be defined with _x_ and _y_ coordinates.
Nodes can also be added separately to the simulation file with _Gemotery().add_node(Node())_ but the FEMM cannot interpret
a free node, so it is not recommended.


* **Node().rotate_about()**: A node can be rotated around a point with _alpha_ radians, so Node().rotate_about(Node(), alpha).
The Node() object is not mutable so every rotation should result in a new node definition and be added to the Geometry().


* **Line()**: A line can only be defined between two nodes, so Line(Node(), Node()) and be added by Geometry().add_line(Line()).


* **CircleArc()**: An arc is defined between two points and a centre point of the arc, so CircleArc(Node(), Node(), Node())
and added by Gometry()add_arc(CircleArc()).


* **.selection_point()**: For lines and arcs it is important to select that object later to associate boundary conditions
with it for example. The selection point is the middle point of a line or arc.

Be aware not to forget to add the defined object to the FemmProblem with .create_gemotery() and if you want to reuse a variable
calculated in the rotor then _return_ it.

### How to define materials

\*The following code snippet contains examples, not a working code.

      def material_definition(femm_model: FemmProblem, variables: VariableParameters, rotor: rotor_geometry):
          """Create and add materials to the simulation."""
      
         magnet = MagneticMaterial(material_name=f"N55_{oscillation}", H_c=922850, Sigma=0.667)

         magnet.remanence_angle = np.degrees(math.atan2(magnet_midpoint.y, magnet_midpoint.x))

         femm_model.add_material(magnet)

         femm_model.add_bh_curve(material_name=f"N55_{oscillation}",
                                    data_b=[0.000000, 0.075300, 0.150600, 0.225900, 0.301200, 0.376500, 0.451800,
                                            0.527100, 0.602400, 1.506000],
                                    data_h=[0.000000, 5371.000000, 12456.000000, 22657.000000, 39606.000000,
                                            72533.000000, 124321.000000, 180991.000000, 238036.000000, 922850.000000])

         femm_model.define_block_label(magnet_midpoint, magnet)
      
The material definition requires three different objects as input. The FemmProblem, as before, uses the VariableParameters
and the rotor_geometry to define the position of the material labels. To understand how FEMM defines materials, please
check the FEMM page for examples and tutorials. In this algorithm, the MagneticMaterial object and its parameters define a
material, such as magnets, magnetic steel, conductor and air needed for this simulation. A magnet, for example, is 
defined by its name, H_c, Sigma remanence angle and BH curve. To understand these parameters, check:
https://www.femm.info/wiki/Documentation/.

In this case, the _magnet.remanence_angle_sets the magnetisation angle of the magnet. It is important as it should be 
in a radial direction, and the neighbouring poles should have an opposite direction. Only after defining the magnet it is
possible to add a BH curve by _FemmProblem().add_bh_curve()_ by specifying the material name and then the B and H parameters. 

The _FemmProblem().define_block_label(Node(), MagneticMaterial())_ adds the material to the specified point.

Defining the winding topology follows the same method. You can set it manually by adding 
_FemmProblem().define_block_label(Node(), MagneticMaterial())_. In this algorithm, the
_def winding_definition(femm_model: FemmProblem, variables: VariableParameters):_ sets the winding topology automatically
for different topologies, but the core idea is the same as defining any other material.

### How to define the boundary conditions

\*The following code snippet contains examples, not a working code.

      def boundary_definition(femm_model: FemmProblem, variables: VariableParameters):
          """Create and add the boundaries to the model."""
      
          # Create A0 boundary condition.
          A0 = MagneticDirichlet(name="a0", a_0=0, a_1=0, a_2=0, phi=0)
      
          # Add A0 boundary condition to the FEMM model.
          femm_model.add_boundary(A0)
      
          # Add the boundary condition to specified elements of the geometry.
          femm_model.set_boundary_definition_arc(Node(0, 43.25), A0)

There are many ways to reduce the computational burden of the simulation, such as by using the symmetry of the 
machine. The whole machine model is defined in this algorithm, so no periodic or antiperiodic boundary conditions are used.
For examples, please check the FEMM examples page. Because no simplification is used, only the MagneticDirichlet() object
is necessary. The core idea is the same as defining a material, you should add the boundary object to the FemmProblem() first
then define it on the arcs or lines one by one with _FemmProblem().set_boundary_definition_arc(Node(), Boundary())_ or with
_FemmProblem().set_boundary_definition_line(Node(), Boundary())_.

The Dirichlet boundary condition specifies a boundary which the flux cannot cross, which means it should only be defined for
the arc of the stator outer circle. Be aware that FEMM cannot interpret a circle; it is built by two arcs representing half
of the circle, so the boundaries should be added to each arc.

### How to create the model and specify the output values to be calculated

      def model_creation(variables: VariableParameters):
          """Put all the block together to create the machine model."""
      
          if not Path(variables.output_folder).exists():
              Path(variables.output_folder).mkdir(parents=True, exist_ok=True)
      
          # Call the FEMM class.
          problem = FemmProblem(out_file=variables.output_file + ".csv", )
      
          # Initialise the FEMM class.
          problem.magnetic_problem(0, LengthUnit.MILLIMETERS, "planar", depth=variables.stack_lenght)
      
          # Initialise the machine model blocks.
          stator_geometry(problem, variables)
          rotor = rotor_geometry(problem, variables)
          materials = material_definition(problem, variables, rotor)
          winding_definition(problem, variables)
          boundary_definition(problem, variables)
      
          # Create the .lua file's content as txt.
          problem.make_analysis(filename=variables.output_file)
      
          # Initialise the intended output values to calculate. In this case, the torque.
          problem.get_integral_values(label_list=[materials[0]] + materials[1], save_image=False,
                                      variable_name=MagneticVolumeIntegral.wTorque)
      
          # Create .lua file.
          problem.write(file_name=variables.output_file + '.lua')

First of all, the FemmProblem() object is called, and the output file is specified as a .csv, which will contain the value
of the calculated objective of the machine. In this case, it is the torque. Then the FemmProblem().magnetic_problem() 
specifies that we are dealing with a magnetic field calculation. FEMM is also capable of calculating thermal problems.
The first parameter specifies the frequency. It should always be 0 for this kind of static calculation. Using a higher 
frequency will tamper with the excitation of the machine, making it more complex. The second parameter specifies the unit
used for the model, in this case, millimetres. The third defines this as a planar problem used for radial flux machines,
and the last sets the stack length.

In the next step, the previously defined building blocks of the machine are called and added to the FemmProblem(). The 
_FemmProblem().make_analysis()_ adds the command line to the FemmProblem() that makes the analysis possible, it is a technical
solution.

The most important is to decide what to calculate. In this case, we are dealing only with torque values, so the
_FemmProblem().get_integral_values([Node(), Node()...], MagneticVolumeIntegral.wTorque)_ tells the FEMM solver to calculate
torque where the nodes specify all the different nodes inside a geometry of the rotor, meaning the shaft, the magnets, the
rotor core and the flux barriers. If any geometry is left out, then the FEMM throws an exception.

Last but not least _FemmProblem().write()_ creates the .lua file which will be used by the FEMM solver.

## How to [calculate_average_torque_and_ripple.py](../calculate_average_torque_and_ripple.py), [calculate_max_torque_angle.py](../calculate_max_torque_angle.py) and [calculate_cogging_torque.py](../calculate_cogging_torque.py)

All the different calculations are based on the same code structure. How do those work and why, please check
[tests_and_examples.md](tests_and_examples.md). The two parts are always the model execution and the model creation as physics dictates.

#### The model execution:

* **Executor()**: This object initiates the FEMM solver, which is an independent third-party solver, but it can communicate 
with the Python algorithm by wrapping the Python code in a .lua format.

* **Executor().run(lua_file)**: It runs the specified .lua file with FEMM.

The following code reads the .csv file as it has a specific format in py2FEMM.

       with open(variables.output_file + '.csv', 'r') as file:
              csvfile = next(csv.reader(file))
              if isinstance(rounding, int):
                  torque = np.round(float(''.join(csvfile).replace('wTorque_0 = ', '')), rounding)
              else:
                  torque = float(''.join(csvfile).replace('wTorque_0 = ', ''))

#### The model creation:

The model creation creates every .lua file for every different electric machine state. For example, the cogging torque is
the simplest, as only the rotor position should be changed. If a whole rotation is investigated with one degree of 
resolution, then the model creation creates 360 different models and executes them in parallel. 

    for alpha in np.linspace(start_position, end_position, resolution):
        mutable_variables = copy.deepcopy(variables)
        mutable_variables.update_initial_rotor_position(variables.initial_rotor_position)
        mutable_variables.update_rotor_position(alpha)

        model.model_creation(mutable_variables)

        all_variables.append((mutable_variables, rounding, delete_after))

Always create a mutable_variables object with deepcopy() to ensure that there is no unintended miss definitions of the models.
Then, only the rotor position should be updated for every different model, which can be created with a simple _for cycle_.
Then, in every cycle, the .lua file is created in the corresponding folder by calling _model_creation_ from the
_machine_model.py_ and all models are added to a list, which will be an input for the execution.

    with Pool(cores) as pool:
        result = list(pool.map(execute_model, all_variables))

    # Calculate cogging torque.
    cogging_torque = np.round((-1) * (np.max(result) - np.min(result)), rounding)

    return cogging_torque, [float(i) for i in result]

The multiprocessing package is used to run the models in parallel and returns the corresponding torque value. The average
torque and torque angle calculation follow the same idea but with different physics behind them.

## Whats with [run_average_torque_and_ripple.py](../run_average_torque_and_ripple.py), [run_cogging_torque.py](../run_cogging_torque.py), [run_max_torque_angle.py](../run_max_torque_angle.py), [run_nsga2.py](../run_nsga2.py) and [run_selector.py](../run_selector.py)?

The sole purpose of these files is to make a GUI for users who are not well-versed in Python programming. These are not necessary
files to make the calculations, but they help with the user experience. These files contain the GUI with the Tkinter package and 
handle the exceptions for the inputs, but they also limit the code's capability. These files also plot the
results in one specific way, but there are many other possibilities. Be brave to experiment with the code!

## Find a bug or want to contribute?
- open an issue
- create a pull request with a detailed explanation

### Ideas for contribution

- Creating a button which only creates the model in a .fem file but does not calculate it.
- Creating a better GUI.
- Calculating back EMF.

...

**Many thanks for the contribution!**