# Importing the packages from py2femm and third party packages too
import math  # For trigonometric functions to define the rotor geometry easier in Cartesian coordinate system.

# The FemmProblem class defines the .lua file which is an input of the FEMM solver.
import numpy as np
import re

from pathlib import Path  # For specifying the current folder path.

from src.femm_problem import FemmProblem

from src.general import LengthUnit

from src.geometry import Geometry, Node, CircleArc, Line, Sector

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
             current=0,
             number_of_coil_turns=0,
             initial_current_angle=0,
             current_angle=0,
             initial_rotor_position=0,
             rotor_position=0,
             shaft_diameter=0,
             rotor_diameter=0,
             cut_off_barrier_angle=0,
             cut_off_barrier_curve_degree=0,
             barrier_distance=0,
             barrier_width=0,
             barrier_height=0,
             barrier_gap=0,
             magnet_height=0,
             magnet_width=0,
             magnet_pocket_width=0,
             magnet_shift=0,
             magnet_pocket_shift=0,
             pole_pairs=1,
             stack_length=1,
             winding_scheme='A|b|C|a|B|c|A|b|C|a|B|c|',
             shortening=0
             ):

        self.folder = folder_name
        self.filename = file_name

        self.current = current
        self.number_of_coil_turns = number_of_coil_turns
        self.initial_current_angle = initial_current_angle
        self.current_angle = current_angle

        self.rotor_position = rotor_position
        self.initial_rotor_position = initial_rotor_position

        self.rotor_diameter = rotor_diameter
        self.shaft_diameter = shaft_diameter
        self.ang_co = cut_off_barrier_angle
        self.deg_co = cut_off_barrier_curve_degree
        self.bd = barrier_distance
        self.bw = barrier_width
        self.bh = barrier_height
        self.bg = barrier_gap

        self.mh = magnet_height
        self.ang_m = magnet_width
        self.ang_mp = magnet_pocket_width
        self.deg_m = magnet_shift
        self.deg_mp = magnet_pocket_shift

        self.pole_pairs = pole_pairs
        self.shortening = shortening
        self.stack_length = stack_length

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

        self.JUp = self.current_density * math.cos(math.radians(self.current_angle + self.initial_current_angle))
        self.JUn = (-1) * self.JUp
        self.JVp = self.current_density * math.cos(math.radians(self.current_angle + self.initial_current_angle + 120))
        self.JVn = (-1) * self.JVp
        self.JWp = self.current_density * math.cos(math.radians(self.current_angle + self.initial_current_angle + 240))
        self.JWn = (-1) * self.JWp

        self.output_file = f"{current_folder_path}/{self.folder}/{self.filename}_{self.rotor_position}"
        self.output_folder = f"{current_folder_path}/{self.folder}"

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
    barrier_arc_for_material_upper = []
    barrier_arc_for_material_lower = []

    # Creating the shaft
    shaft_node_left = Node((-1) * variables.shaft_diameter / 2, 0.0)
    shaft_node_right = Node(1 * variables.shaft_diameter / 2, 0.0)

    shaft_arc_lower = CircleArc(shaft_node_left, N0, shaft_node_right)
    shaft_arc_upper = CircleArc(shaft_node_right, N0, shaft_node_left)

    rotor.add_arc(shaft_arc_lower)
    rotor.add_arc(shaft_arc_upper)

    # Creating the cut-off barrier around the vertical line through zero and copy-rotate
    cut_off_barrier_left = Node(0, variables.rotor_diameter / 2).rotate_about(N0, - variables.ang_co / 2, degrees=True)
    cut_off_barrier_right = Node(0, variables.rotor_diameter / 2).rotate_about(N0, variables.ang_co / 2, degrees=True)

    for poles in [i * (2 * np.pi / (variables.pole_pairs * 2)) for i in range(variables.pole_pairs * 2)]:
        cut_off_barrier_arc = Sector(cut_off_barrier_right, cut_off_barrier_left, variables.deg_co)

    rotor.add_sector(cut_off_barrier_arc)

    # Creating the magnets by creating the first magnet around the vertical line through the zero and copy-rotate
    # vertical_node_circumference = Node(0.0, variables.rotor_diameter / 2)
    # vertical_node_lower = Node(0.0, variables.rotor_diameter / 2 - variables.magnet_height)
    #
    # magnet_nocile = vertical_node_circumference.rotate_about(N0, (-1) * np.radians(variables.magnet_width / 2))
    # magnet_nociri = vertical_node_circumference.rotate_about(N0, np.radians(variables.magnet_width / 2))
    #
    # magnet_nolole = vertical_node_lower.rotate_about(N0, (-1) * np.radians(variables.magnet_width / 2))
    # magnet_nolori = vertical_node_lower.rotate_about(N0, np.radians(variables.magnet_width / 2))
    #
    # for poles in [i * (2 * np.pi / (variables.pole_pairs * 2)) for i in range(variables.pole_pairs * 2)]:
    #     magnet_node_circumference_left = magnet_nocile.rotate_about(N0, poles +
    #                                                                 np.radians(variables.initial_rotor_position +
    #                                                                            variables.rotor_position))
    #     magnet_node_circumference_right = magnet_nociri.rotate_about(N0, poles +
    #                                                                  np.radians(variables.initial_rotor_position +
    #                                                                             variables.rotor_position))
    #
    #     magnet_node_lower_left = magnet_nolole.rotate_about(N0, poles +
    #                                                         np.radians(variables.initial_rotor_position +
    #                                                                    variables.rotor_position))
    #     magnet_node_lower_right = magnet_nolori.rotate_about(N0, poles +
    #                                                          np.radians(variables.initial_rotor_position +
    #                                                                     variables.rotor_position))
    #
    #     magnet_line_left = Line(magnet_node_circumference_left, magnet_node_lower_left)
    #     magnet_line_right = Line(magnet_node_circumference_right, magnet_node_lower_right)
    #
    #     magnet_arc_lower = CircleArc(magnet_node_lower_left, N0, magnet_node_lower_right)
    #     magnet_arc_upper = CircleArc(magnet_node_circumference_left, N0, magnet_node_circumference_right)
    #
    #     rotor.add_line(magnet_line_left)
    #     rotor.add_line(magnet_line_right)
    #
    #     magnet_arc_for_material_lower.append(magnet_arc_lower)
    #     magnet_arc_for_material_upper.append(magnet_arc_upper)
    #
    #     rotor.add_arc(magnet_arc_lower)
    #
    # # Creating rotor circumference
    # horizontal_node_circumference_left = Node((-1) * variables.rotor_diameter / 2, 0.0)
    # horizontal_node_circumference_right = Node(variables.rotor_diameter / 2, 0.0)
    #
    # arc_lower_circumference = CircleArc(horizontal_node_circumference_left, N0, horizontal_node_circumference_right)
    # arc_upper_circumference = CircleArc(horizontal_node_circumference_right, N0, horizontal_node_circumference_left)
    #
    # rotor.add_arc(arc_lower_circumference)
    # rotor.add_arc(arc_upper_circumference)

    femm_model.create_geometry(rotor)

    return (magnet_arc_for_material_lower, magnet_arc_for_material_upper,
            barrier_arc_for_material_lower, barrier_arc_for_material_upper)


def material_definition(femm_model: FemmProblem, variables: VariableParameters, rotor: rotor_geometry):
    """Create and add materials to the simulation."""

    magnet_midpoints = []
    barrier_midpoints = []

    # Adding Y30 ferrite magnet to the model from the material library

    for oscillation, (arc_low, arc_high) in enumerate(zip(rotor[0], rotor[1])):
        magnet_midpoint = Line(arc_low.selection_point(), arc_high.selection_point()).selection_point()

        magnet = MagneticMaterial(material_name=f"magnet_{oscillation}", H_c=200106)

        if variables.pole_pairs == 1:
            magnet.remanence_angle = np.degrees(math.atan2(magnet_midpoint.y, magnet_midpoint.x))
        else:
            magnet.remanence_angle = (-180 * (oscillation % 2)) + np.degrees(
                math.atan2(magnet_midpoint.y, magnet_midpoint.x))

        femm_model.add_material(magnet)

        femm_model.add_bh_curve(material_name=f"magnet_{oscillation}",
                                data_b=[0.000000, 0.066000, 0.131390, 0.144000, 0.153280, 0.162400, 0.171530,
                                        0.211680, 0.273720, 0.386860],
                                data_h=[0.000000, 1160.000000, 2323.660000, 3490.000000, 6000.000000, 11630.000000,
                                        18613.200000, 51192.200000, 102376.000000, 200106.000000])

        femm_model.define_block_label(magnet_midpoint, magnet)

        magnet_midpoints.append(magnet_midpoint)

    # Adding 1018 steel to the model from the material library.
    steel = MagneticMaterial(material_name="steel", Sigma=5.8, Lam_d=0.5, lam_fill=0.98)

    femm_model.add_material(steel)

    femm_model.add_bh_curve(material_name=f"steel",
                            data_b=[0, 0.670856255, 0.791524678, 0.871414555, 0.931231537, 0.979063683, 1.0189211,
                                    1.053086796, 1.082985065, 1.109564545, 1.126953298, 1.20365399, 1.250426447,
                                    1.284175967, 1.31059707, 1.332311427, 1.350745115, 1.366760558, 1.380919281,
                                    1.393607415, 1.405101905, 1.41560815, 1.42528271, 1.434247653, 1.442600004,
                                    1.450418152, 1.457766344, 1.464697889, 1.47125751, 1.477483095, 1.476550438,
                                    1.488764478, 1.498939108, 1.507658923, 1.515288382, 1.52207011, 1.528173797,
                                    1.533722786, 1.538809552, 1.543505214, 1.547865643, 1.551935531, 1.555751191,
                                    1.559342524, 1.56273445, 1.565947951, 1.569000866, 1.571908482, 1.574684004,
                                    1.577338915, 1.579883262, 1.582325887, 1.584674612, 1.586936389, 1.589117427,
                                    1.591223293, 1.593258995, 1.595229059, 1.597137587, 1.598988305],
                            data_h=[0, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1615.789474,
                                    2131.578947, 2647.368421, 3163.157895, 3678.947368, 4194.736842, 4710.526316,
                                    5226.315789, 5742.105263, 6257.894737, 6773.684211, 7289.473684, 7805.263158,
                                    8321.052632, 8836.842105, 9352.631579, 9868.421053, 10384.21053, 10900, 11000,
                                    12344.82759, 13689.65517, 15034.48276, 16379.31034, 17724.13793, 19068.96552,
                                    20413.7931, 21758.62069, 23103.44828, 24448.27586, 25793.10345, 27137.93103,
                                    28482.75862, 29827.58621, 31172.41379, 32517.24138, 33862.06897, 35206.89655,
                                    36551.72414, 37896.55172, 39241.37931, 40586.2069, 41931.03448, 43275.86207,
                                    44620.68966, 45965.51724, 47310.34483, 48655.17241, 50000])

    femm_model.define_block_label(steel_label_node := Node(0, variables.shaft_diameter / 2 + 1), steel)

    femm_model.define_block_label(Node(0, 40), steel)

    # Adding air to the model from material library.
    air = MagneticMaterial(material_name="air")

    femm_model.add_material(air)

    femm_model.define_block_label(Node(0, 22.85), air)
    femm_model.define_block_label(N0, air)

    return steel_label_node, magnet_midpoints ,barrier_midpoints


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
            femm_model.define_block_label(Node(2, 30.5).rotate_about(N0, 30 * slot, degrees=True),
                                          phase_map[phase])
            femm_model.define_block_label(Node(13.5, 27.5).rotate_about(N0, 30 * slot, degrees=True),
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
    problem.magnetic_problem(0, LengthUnit.MILLIMETERS, "planar", depth=variables.stack_length)

    # Initialise the machine model blocks.
    stator_geometry(problem, variables)
    rotor = rotor_geometry(problem, variables)
    # materials = material_definition(problem, variables, rotor)
    winding_definition(problem, variables)
    # boundary_definition(problem, variables)

    # Create the .lua file's content as txt.
    problem.make_analysis(filename=variables.output_file)

    # Initialise the intended output values to calculate. In this case the torque.
    # problem.get_integral_values(label_list=[materials[0]] + materials[1], save_image=False,
    #                             variable_name=MagneticVolumeIntegral.wTorque)

    # Create .lua file.
    problem.write(file_name=variables.output_file + '.lua')
