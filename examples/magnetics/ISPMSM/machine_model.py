# Importing the packages from py2femm and third party packages too -----------------------------------------------------
import math  # For trigonometric functions to define the rotor geometry easier in Cartesian coordinate system.
import os  # For specifying the current folder path.

# The FemmProblem class defines the .lua file which is an input of the FEMM solver.
import numpy as np

from src.executor import Executor
from src.femm_problem import FemmProblem
from src.general import LengthUnit

from src.geometry import Geometry, Node, CircleArc, Line

# Creating static global variables -------------------------------------------------------------------------------------

# Gets the current file's folder path to specify the path of the output FEMM model file with .lua extension ------------
current_folder_path = os.path.dirname(os.path.abspath(__file__))

# The zero node specifies the center point of the machine, discretising the coordinate system --------------------------
N0 = Node(0, 0)

# Creating the variables of the machine to simplify the functions later on ---------------------------------------------
class VariableParameters:

    def __init__(self, folder, filename, current_density, current_angle, rotor_position, rotor_diameter, shaft_diameter,
                 magnet_width, magnet_height, pole_pairs, stack_lenght):
        self.folder = folder
        self.filename = filename

        self.JUp = current_density * math.cos(math.radians(current_angle))
        self.JUn = -1 * self.JUp
        self.JVp = current_density * math.cos(math.radians(current_angle + 120))
        self.JVn = -1 * self.JVp
        self.JWp = current_density * math.cos(math.radians(current_angle + 240))
        self.JWn = -1 * self.JWp

        self.rotor_position = rotor_position
        self.rotor_diameter = rotor_diameter
        self.shaft_diameter = shaft_diameter
        self.magnet_width = magnet_width
        self.magnet_height = magnet_height
        self.pole_pairs = pole_pairs

        self.stack_lenght = stack_lenght

        self.output_file = f"{current_folder_path}/{folder}/{filename}_{rotor_position}"
        self.output_folder = f"{current_folder_path}/{folder}"

# Importing stator geometry from a dxf file instead of manually defining the nodes, lines and arc ----------------------
def stator_geometry(femm_model: FemmProblem):
    """Creating stator geometry."""
    stator = Geometry()

    stator.import_dxf("stator.dxf")

    femm_model.create_geometry(stator)

# Creating the parametric rotor geometry manually to make it possible to optimise --------------------------------------
def rotor_geometry(femm_model: FemmProblem, variables: VariableParameters):
    """Creating rotor geometry."""
    rotor = Geometry()

    # Creating the shaft -----------------------------------------------------------------------------------------------

    shaft_node_left = Node(-1 * variables.shaft_diameter / 2, 0.0)
    shaft_node_right = Node(1 * variables.shaft_diameter / 2, 0.0)

    shaft_arc_lower = CircleArc(shaft_node_left, N0, shaft_node_right)
    shaft_arc_upper = CircleArc(shaft_node_right, N0, shaft_node_left)

    rotor.add_arc(shaft_arc_lower)
    rotor.add_arc(shaft_arc_upper)

    # Creating the magnets by creating the first magnet around the vertical line through the zero and copy-rotate ------

    vertical_node_circumference = Node(0.0, variables.rotor_diameter / 2)
    vertical_node_lower = Node(0.0, variables.rotor_diameter / 2 - variables.magnet_height)

    magnet_nocile = vertical_node_circumference.rotate_about(N0, -1 * np.radians(variables.magnet_width / 2))
    magnet_nociri = vertical_node_circumference.rotate_about(N0, np.radians(variables.magnet_width / 2))

    magnet_nolole = vertical_node_lower.rotate_about(N0, -1 * np.radians(variables.magnet_width / 2))
    magnet_nolori = vertical_node_lower.rotate_about(N0, np.radians(variables.magnet_width / 2))

    for poles in [i * (2 * np.pi / (variables.pole_pairs * 2)) for i in range(variables.pole_pairs * 2 + 1)]:

        magnet_node_circumference_left = magnet_nocile.rotate_about(N0, poles)
        magnet_node_circumference_right = magnet_nociri.rotate_about(N0, poles)

        magnet_node_lower_left = magnet_nolole.rotate_about(N0, poles)
        magnet_node_lower_right = magnet_nolori.rotate_about(N0, poles)

        magnet_line_left = Line(magnet_node_circumference_left, magnet_node_lower_left)
        magnet_line_right = Line(magnet_node_circumference_right, magnet_node_lower_right)

        magnet_arc_lower = CircleArc(magnet_node_lower_left, N0, magnet_node_lower_right)

        rotor.add_line(magnet_line_left)
        rotor.add_line(magnet_line_right)

        rotor.add_arc(magnet_arc_lower)

    # Creating rotor circumference -------------------------------------------------------------------------------------
    horizontal_node_circumference_left = Node(-1 * variables.rotor_diameter / 2, 0.0)
    horizontal_node_circumference_right = Node(variables.rotor_diameter / 2, 0.0)

    arc_lower_circumference = CircleArc(horizontal_node_circumference_left, N0, horizontal_node_circumference_right)
    arc_upper_circumference = CircleArc(horizontal_node_circumference_right, N0, horizontal_node_circumference_left)

    rotor.add_arc(arc_lower_circumference)
    rotor.add_arc(arc_upper_circumference)

    femm_model.create_geometry(rotor)

def model_creation(variables: VariableParameters):

    if not os.path.exists(variables.output_folder):
        os.makedirs(variables.output_folder)

    problem = FemmProblem(out_file=variables.output_file + ".csv")

    problem.magnetic_problem(0, LengthUnit.MILLIMETERS, "planar", depth=variables.stack_lenght)

    stator_geometry(problem)
    rotor_geometry(problem, variables)

    problem.create_model(filename=variables.output_file)

    problem.write(file_name=variables.output_file + '.lua')
