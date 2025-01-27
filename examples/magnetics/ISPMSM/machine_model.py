# Importing the packages from py2femm and third party packages too -----------------------------------------------------
import math  # For trigonometric functions to define the rotor geometry easier in Cartesian coordinate system.
import os  # For specifying the current folder path.

# The FemmProblem class defines the .lua file which is an input of the FEMM solver.
import numpy as np

from src.femm_problem import FemmProblem

from src.general import LengthUnit

from src.geometry import Geometry, Node, CircleArc, Line

from src.magnetics import MagneticMaterial

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
    magnet_line_for_material_left = []
    magnet_line_for_material_right = []

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
        magnet_node_circumference_left = magnet_nocile.rotate_about(N0, poles + np.radians(variables.rotor_position))
        magnet_node_circumference_right = magnet_nociri.rotate_about(N0, poles + np.radians(variables.rotor_position))

        magnet_node_lower_left = magnet_nolole.rotate_about(N0, poles + np.radians(variables.rotor_position))
        magnet_node_lower_right = magnet_nolori.rotate_about(N0, poles + np.radians(variables.rotor_position))

        magnet_line_left = Line(magnet_node_circumference_left, magnet_node_lower_left)
        magnet_line_right = Line(magnet_node_circumference_right, magnet_node_lower_right)

        magnet_arc_lower = CircleArc(magnet_node_lower_left, N0, magnet_node_lower_right)

        rotor.add_line(magnet_line_left)
        rotor.add_line(magnet_line_right)

        magnet_line_for_material_left.append(magnet_line_left)
        magnet_line_for_material_right.append(magnet_line_right)

        rotor.add_arc(magnet_arc_lower)

    # Creating rotor circumference -------------------------------------------------------------------------------------
    horizontal_node_circumference_left = Node(-1 * variables.rotor_diameter / 2, 0.0)
    horizontal_node_circumference_right = Node(variables.rotor_diameter / 2, 0.0)

    arc_lower_circumference = CircleArc(horizontal_node_circumference_left, N0, horizontal_node_circumference_right)
    arc_upper_circumference = CircleArc(horizontal_node_circumference_right, N0, horizontal_node_circumference_left)

    rotor.add_arc(arc_lower_circumference)
    rotor.add_arc(arc_upper_circumference)

    femm_model.create_geometry(rotor)

    return magnet_line_for_material_left, magnet_line_for_material_right


# Creating and adding the material labels for the simulation -----------------------------------------------------------
def material_definition(femm_model: FemmProblem, variables: VariableParameters, rotor: rotor_geometry):

    # Adding N55 NdFeB magnet to the model from the material library ---------------------------------------------------
    for oscillation, (line_left, line_right) in enumerate(zip(rotor[0], rotor[1])):
        magnet_midpoint = Line(line_left.selection_point(), line_right.selection_point()).selection_point()

        magnet = MagneticMaterial(material_name=f"N55_{oscillation}", H_c=922850, Sigma=0.667)

        magnet.remanence_angle = (180 * (oscillation % 2)) + np.degrees(math.atan2(magnet_midpoint.y, magnet_midpoint.x))

        femm_model.add_material(magnet)

        femm_model.add_bh_curve(material_name=f"N55_{oscillation}",
                                data_b=[0.000000, 0.075300, 0.150600, 0.225900, 0.301200, 0.376500, 0.451800, 0.527100,
                                        0.602400, 1.506000],
                                data_h=[0.000000, 5371.000000, 12456.000000, 22657.000000, 39606.000000, 72533.000000,
                                        124321.000000, 180991.000000, 238036.000000, 922850.000000])

        femm_model.define_block_label(magnet_midpoint, magnet)


def model_creation(variables: VariableParameters):
    if not os.path.exists(variables.output_folder):
        os.makedirs(variables.output_folder)

    problem = FemmProblem(out_file=variables.output_file + ".csv")

    problem.magnetic_problem(0, LengthUnit.MILLIMETERS, "planar", depth=variables.stack_lenght)

    stator_geometry(problem)
    rotor = rotor_geometry(problem, variables)
    material_definition(problem, variables, rotor)

    problem.create_model(filename=variables.output_file)

    problem.write(file_name=variables.output_file + '.lua')
