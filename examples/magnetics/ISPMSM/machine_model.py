# Importing the packages from py2femm and third party packages too -----------------------------------------------------
import math  # For trigonometric functions to define the rotor geometry easier in Cartesian coordinate system.
import os  # For specifying the current folder path.

# The FemmProblem class defines the .lua file which is an input of the FEMM solver.
from src.executor import Executor
from src.femm_problem import FemmProblem
from src.general import LengthUnit

from src.geometry import Geometry, Node

# Creating static global variables -------------------------------------------------------------------------------------

# Gets the current file's folder path to specify the path of the output FEMM model file with .lua extension.
current_folder_path = os.path.dirname(os.path.abspath(__file__))

# The zero node specifies the center point of the machine, discretising the coordinate system.
N0 = Node(0, 0)

# Creating the variables of the machine to simplify the functions later on ---------------------------------------------
class VariableParameters:

    def __init__(self, folder, filename, current_density, current_angle, rotor_position, rotor_diameter, magnet_width,
                 magnet_height, stack_lenght):
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
        self.magnet_width = magnet_width
        self.magnet_height = magnet_height

        self.stack_lenght = stack_lenght

        self.output_file = f"{current_folder_path}/{folder}/{filename}_{rotor_position}"
        self.output_folder = f"{current_folder_path}/{folder}"


def stator_geometry(femm_model: FemmProblem):
    stator = Geometry()

    stator.import_dxf("stator.dxf")

    femm_model.create_geometry(stator)


def model_creation(variables: VariableParameters):

    if not os.path.exists(variables.output_folder):
        os.makedirs(variables.output_folder)

    problem = FemmProblem(out_file=variables.output_file + ".csv")

    problem.magnetic_problem(0, LengthUnit.MILLIMETERS, "planar", depth=variables.stack_lenght)

    stator_geometry(problem)

    problem.create_model(filename=variables.output_file)

    problem.write(file_name=variables.output_file + '.lua')
