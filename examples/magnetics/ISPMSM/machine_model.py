# Importing the packages from py2femm and third party packages too
import math  # For trigonometric functions to define the rotor geometry easier in Cartesian coordinate system.

# The FemmProblem class defines the .lua file which is an input of the FEMM solver.
import numpy as np
import re

from pathlib import Path  # For specifying the current folder path.

from src.femm_problem import FemmProblem

from src.general import LengthUnit

from src.geometry import Geometry, Node, CircleArc, Line

from src.magnetics import MagneticMaterial, LamType, MagneticDirichlet, MagneticVolumeIntegral

# Creating static global variables
# Gets the current file's folder path to specify the path of the output FEMM model file with .lua extension
current_folder_path = str(Path(__file__).resolve().parent).replace("\\", "/")

# The zero node specifies the center point of the machine, discretising the coordinate system
N0 = Node(0, 0)


class VariableParameters:
    """Store all the variables to create the machine model."""

    def __init__(self, folder_name='test',
                 file_name='test',
                 current=30,
                 number_of_coil_turns=11,
                 initial_current_angle=0,
                 current_angle=0,
                 initial_rotor_position=0,
                 rotor_position=0,
                 rotor_diameter=44,
                 shaft_diameter=10,
                 magnet_width=1,
                 magnet_height=1,
                 pole_pairs=1,
                 stack_lenght=1,
                 winding_scheme='A|b|C|a|B|c|A|b|C|a|B|c|',
                 shortening=0
                 ):

        self.folder = folder_name
        self.filename = file_name

        self.number_of_coil_turns = number_of_coil_turns

        self.rotor_position = rotor_position
        self.initial_rotor_position = initial_rotor_position
        self.rotor_diameter = rotor_diameter
        self.shaft_diameter = shaft_diameter
        self.magnet_width = magnet_width
        self.magnet_height = magnet_height
        self.pole_pairs = pole_pairs
        self.shortening = shortening

        self.stack_lenght = stack_lenght
        self.current = current

        # Check the validity of the winding scheme as it can crash the simulation.
        if bool(re.fullmatch(r"^(?:[A-Ca-c]\|){12}$", winding_scheme)):
            self.winding_scheme = list(filter(lambda item: item != '|', winding_scheme))
            self.winding_layers = False
            self.winding_type = 'distributed'
            self.slot_cross_section_area = 113.895
            self.current_density = self.current * self.number_of_coil_turns / self.slot_cross_section_area
        elif bool(re.fullmatch(r"^(?:[A-Ca-c][A-Ca-c]\|){12}$", winding_scheme)):
            self.winding_scheme = list(filter(lambda item: item != '|', winding_scheme))
            self.winding_layers = True
            self.winding_type = 'distributed'
            self.slot_cross_section_area = 113.895 / 2
            self.current_density = self.current * self.number_of_coil_turns / self.slot_cross_section_area
        elif bool(re.fullmatch(r"^(?:[A-Ca-c]){12}$", winding_scheme)):
            self.winding_scheme = list(filter(lambda item: item != '|', winding_scheme))
            self.winding_layers = False
            self.winding_type = 'concentrated'
            self.slot_cross_section_area = 113.895 / 2
            self.current_density = self.current * self.number_of_coil_turns / self.slot_cross_section_area
        else:
            raise Exception('Invalid input for winding scheme!')

        self.current_angle = current_angle
        self.initial_current_angle = initial_current_angle
        self.JUp = self.current_density * math.cos(math.radians(self.current_angle + self.initial_current_angle))
        self.JUn = (-1) * self.JUp
        self.JVp = self.current_density * math.cos(math.radians(self.current_angle + self.initial_current_angle + 120))
        self.JVn = (-1) * self.JVp
        self.JWp = self.current_density * math.cos(math.radians(self.current_angle + self.initial_current_angle + 240))
        self.JWn = (-1) * self.JWp

        self.output_file = f"{current_folder_path}/{self.folder}/{self.filename}_{self.rotor_position}"
        self.output_folder = f"{current_folder_path}/{self.folder}"

    def update_current(self, new_current):
        """ Updates current dynamically whenever current changes. """
        self.current_density = new_current * self.number_of_coil_turns / self.slot_cross_section_area
        self.update_phases()

    def update_initial_rotor_position(self, new_initial_rotor_position):
        """ Update initial_rotor_position dynamically. """
        self.initial_rotor_position = new_initial_rotor_position

    def update_rotor_position(self, new_rotor_position):
        """ Update rotor_position and regenerate output_file and output_folder  dynamically. """
        self.rotor_position = new_rotor_position
        self.update_output_file()
        self.update_output_folder()

    def update_folder_name(self, new_folder_name):
        """ Update folder and regenerate output_file and output_folder  dynamically. """
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
        """ Update current_angle dynamically whenever current_angle changes. """
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


def stator_geometry(femm_model: FemmProblem, variables: VariableParameters):
    """Importing stator geometry from a dxf file instead of manually defining the nodes, lines and arcs."""
    stator = Geometry()

    if not variables.winding_layers and variables.winding_type == 'distributed':
        stator.import_dxf("resources/stator_distributed_1layer.dxf")
    elif variables.winding_layers and variables.winding_type == 'distributed':
        stator.import_dxf("resources/stator_distributed_2layers.dxf")
    elif not variables.winding_layers and variables.winding_type == 'concentrated':
        stator.import_dxf("resources/stator_concentrated.dxf")
    else:
        pass

    femm_model.create_geometry(stator)


def rotor_geometry(femm_model: FemmProblem, variables: VariableParameters):
    """Create rotor geometry."""
    rotor = Geometry()
    magnet_arc_for_material_upper = []
    magnet_arc_for_material_lower = []

    # Creating the shaft
    shaft_node_left = Node((-1) * variables.shaft_diameter / 2, 0.0)
    shaft_node_right = Node(1 * variables.shaft_diameter / 2, 0.0)

    shaft_arc_lower = CircleArc(shaft_node_left, N0, shaft_node_right)
    shaft_arc_upper = CircleArc(shaft_node_right, N0, shaft_node_left)

    rotor.add_arc(shaft_arc_lower)
    rotor.add_arc(shaft_arc_upper)

    # Creating the magnets by creating the first magnet around the vertical line through the zero and copy-rotate
    vertical_node_circumference = Node(0.0, variables.rotor_diameter / 2)
    vertical_node_lower = Node(0.0, variables.rotor_diameter / 2 - variables.magnet_height)

    magnet_nocile = vertical_node_circumference.rotate_about(N0, (-1) * np.radians(variables.magnet_width / 2))
    magnet_nociri = vertical_node_circumference.rotate_about(N0, np.radians(variables.magnet_width / 2))

    magnet_nolole = vertical_node_lower.rotate_about(N0, (-1) * np.radians(variables.magnet_width / 2))
    magnet_nolori = vertical_node_lower.rotate_about(N0, np.radians(variables.magnet_width / 2))

    for poles in [i * (2 * np.pi / (variables.pole_pairs * 2)) for i in range(variables.pole_pairs * 2)]:
        magnet_node_circumference_left = magnet_nocile.rotate_about(N0, poles +
                                                                    np.radians(variables.initial_rotor_position +
                                                                               variables.rotor_position))
        magnet_node_circumference_right = magnet_nociri.rotate_about(N0, poles +
                                                                     np.radians(variables.initial_rotor_position +
                                                                                variables.rotor_position))

        magnet_node_lower_left = magnet_nolole.rotate_about(N0, poles +
                                                            np.radians(variables.initial_rotor_position +
                                                                       variables.rotor_position))
        magnet_node_lower_right = magnet_nolori.rotate_about(N0, poles +
                                                             np.radians(variables.initial_rotor_position +
                                                                        variables.rotor_position))

        magnet_line_left = Line(magnet_node_circumference_left, magnet_node_lower_left)
        magnet_line_right = Line(magnet_node_circumference_right, magnet_node_lower_right)

        magnet_arc_lower = CircleArc(magnet_node_lower_left, N0, magnet_node_lower_right)
        magnet_arc_upper = CircleArc(magnet_node_circumference_left, N0, magnet_node_circumference_right)

        rotor.add_line(magnet_line_left)
        rotor.add_line(magnet_line_right)

        magnet_arc_for_material_lower.append(magnet_arc_lower)
        magnet_arc_for_material_upper.append(magnet_arc_upper)

        rotor.add_arc(magnet_arc_lower)

    # Creating rotor circumference
    horizontal_node_circumference_left = Node((-1) * variables.rotor_diameter / 2, 0.0)
    horizontal_node_circumference_right = Node(variables.rotor_diameter / 2, 0.0)

    arc_lower_circumference = CircleArc(horizontal_node_circumference_left, N0, horizontal_node_circumference_right)
    arc_upper_circumference = CircleArc(horizontal_node_circumference_right, N0, horizontal_node_circumference_left)

    rotor.add_arc(arc_lower_circumference)
    rotor.add_arc(arc_upper_circumference)

    femm_model.create_geometry(rotor)

    return magnet_arc_for_material_lower, magnet_arc_for_material_upper


def material_definition(femm_model: FemmProblem, variables: VariableParameters, rotor: rotor_geometry):
    """Create and add materials to the simulation."""

    magnet_midpoints = []

    # Adding N55 NdFeB magnet to the model from the material library
    if variables.pole_pairs == 1:
        for oscillation, (arc_low, arc_high) in enumerate(zip(rotor[0], rotor[1])):
            magnet_midpoint = Line(arc_low.selection_point(), arc_high.selection_point()).selection_point()

            magnet = MagneticMaterial(material_name=f"N55_{oscillation}", H_c=922850, Sigma=0.667)

            magnet.remanence_angle = np.degrees(math.atan2(magnet_midpoint.y, magnet_midpoint.x))

            femm_model.add_material(magnet)

            femm_model.add_bh_curve(material_name=f"N55_{oscillation}",
                                    data_b=[0.000000, 0.075300, 0.150600, 0.225900, 0.301200, 0.376500, 0.451800,
                                            0.527100, 0.602400, 1.506000],
                                    data_h=[0.000000, 5371.000000, 12456.000000, 22657.000000, 39606.000000,
                                            72533.000000, 124321.000000, 180991.000000, 238036.000000, 922850.000000])

            femm_model.define_block_label(magnet_midpoint, magnet)

            magnet_midpoints.append(magnet_midpoint)

    else:
        for oscillation, (arc_low, arc_high) in enumerate(zip(rotor[0], rotor[1])):
            magnet_midpoint = Line(arc_low.selection_point(), arc_high.selection_point()).selection_point()

            magnet = MagneticMaterial(material_name=f"N55_{oscillation}", H_c=922850, Sigma=0.667)

            magnet.remanence_angle = (-180 * (oscillation % 2)) + np.degrees(
                math.atan2(magnet_midpoint.y, magnet_midpoint.x))

            femm_model.add_material(magnet)

            femm_model.add_bh_curve(material_name=f"N55_{oscillation}",
                                    data_b=[0.000000, 0.075300, 0.150600, 0.225900, 0.301200, 0.376500, 0.451800,
                                            0.527100, 0.602400, 1.506000],
                                    data_h=[0.000000, 5371.000000, 12456.000000, 22657.000000, 39606.000000,
                                            72533.000000, 124321.000000, 180991.000000, 238036.000000, 922850.000000])

            femm_model.define_block_label(magnet_midpoint, magnet)

            magnet_midpoints.append(magnet_midpoint)

    # Adding 1018 steel to the model from the material library.
    steel = MagneticMaterial(material_name="1018 steel", Phi_hmax=20, Sigma=5.8, Lam_d=0.5, lam_fill=0.98)

    femm_model.add_material(steel)

    femm_model.add_bh_curve(material_name=f"1018 steel",
                            data_b=[0.000000, 0.250300, 0.925000, 1.250000, 1.390000, 1.525000, 1.710000, 1.870000,
                                    1.955000, 2.020000, 2.110000, 2.225000, 2.430000],
                            data_h=[0.000000, 238.732500, 795.775000, 1591.550000, 2387.325000, 3978.875000,
                                    7957.750000, 15915.500000, 23873.250000, 39788.750000, 79577.500000,
                                    159155.000000, 318310.000000])

    femm_model.define_block_label(steel_label_node := Node(0, variables.shaft_diameter / 2 + 1), steel)

    femm_model.define_block_label(Node(0, 40), steel)

    # Adding air to the model from material library.
    air = MagneticMaterial(material_name="air")

    femm_model.add_material(air)

    femm_model.define_block_label(Node(0, 22.85), air)
    femm_model.define_block_label(N0, air)

    return steel_label_node, magnet_midpoints


def winding_definition(femm_model: FemmProblem, variables: VariableParameters):
    """Create and add the winding scheme."""

    phases = ['A', 'B', 'C', 'a', 'b', 'c']

    excitation_map = {'A': variables.JUp,
                      'a': variables.JUn,
                      'B': variables.JVp,
                      'b': variables.JVn,
                      'C': variables.JWp,
                      'c': variables.JWn}

    # Initialise the phases for the FEMM model.
    phase_map = {f'{i}': MagneticMaterial(material_name=f"{i}", J=excitation_map[i], Sigma=58,
                                          LamType=LamType.MAGNET_WIRE, WireD=1) for i in phases}

    # Add phases to the FEMM model.
    for phase in phases:
        femm_model.add_material(phase_map[phase])

    # Create distributed, one layer winding scheme.
    if not variables.winding_layers and variables.winding_type == 'distributed':
        for slot, phase in enumerate(variables.winding_scheme):
            femm_model.define_block_label(Node(0, 30.5).rotate_about(N0, (-1) * 30 * slot, degrees=True),
                                          phase_map[phase])

    # Create distributed, two layer winding scheme.
    elif variables.winding_layers and variables.winding_type == 'distributed':
        for slot, phase in enumerate(variables.winding_scheme[0::2]):
            femm_model.define_block_label(Node(0, 33.5).rotate_about(N0, (-1) * 30 * slot, degrees=True),
                                          phase_map[phase])
        for slot, phase in enumerate(variables.winding_scheme[1::2]):
            femm_model.define_block_label(Node(0, 27.5).rotate_about(N0, (-1) * 30 * (slot + variables.shortening),
                                                                     degrees=True), phase_map[phase])

    # Create concentrated winding scheme.
    elif not variables.winding_layers and variables.winding_type == 'concentrated':
        for slot, phase in enumerate(variables.winding_scheme):
            femm_model.define_block_label(Node(2, 30.5).rotate_about(N0, (-1) * 30 * slot, degrees=True),
                                          phase_map[phase])
            femm_model.define_block_label(Node(13.5, 27.5).rotate_about(N0, (-1) * 30 * slot, degrees=True),
                                          phase_map[phase.swapcase()])


def boundary_definition(femm_model: FemmProblem, variables: VariableParameters):
    """Create and add the boundaries to the model."""

    # Create A0 boundary condition.
    A0 = MagneticDirichlet(name="a0", a_0=0, a_1=0, a_2=0, phi=0)

    # Add A0 boundary condition to the FEMM model.
    femm_model.add_boundary(A0)

    # Add the boundary condition to specified elements of the geometry.
    femm_model.set_boundary_definition_arc(Node(0, 43.25), A0)
    femm_model.set_boundary_definition_arc(Node(0, (-1) * 43.25), A0)

    femm_model.set_boundary_definition_arc(Node(0, variables.shaft_diameter / 2), A0)
    femm_model.set_boundary_definition_arc(Node(0, (-1) * variables.shaft_diameter / 2), A0)


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

    # Initialise the intended output values to calculate. In this case the torque.
    problem.get_integral_values(label_list=[materials[0]] + materials[1], save_image=False,
                                variable_name=MagneticVolumeIntegral.wTorque)

    # Create .lua file.
    problem.write(file_name=variables.output_file + '.lua')
