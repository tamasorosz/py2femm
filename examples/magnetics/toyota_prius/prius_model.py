import dataclasses
import math
import os
from copy import copy

from src.executor import Executor
from src.femm_problem import FemmProblem
from src.general import LengthUnit
from src.geometry import Node, Geometry, Line, CircleArc
from src.magnetics import MagneticMaterial, LamType, MagneticDirichlet, MagneticAnti, MagneticAntiPeriodicAirgap

ORIGIN = Node(0.0, 0.0)

# Geometry parameters - Constants
Dso = 269.0  # Stator outer diameter [mm]
Dsi = 161.93  # Stator inner diameter [mm]
Dro = 160.47  # Rotor outer diameter [mm]
airgap = (Dsi - Dro) / 2

Dso = 269.0  # Stator outer diameter [mm]
Dsi = 161.93  # Stator inner diameter [mm]

Dro = 160.47  # Rotor outer diameter [mm]
Dri = 111.0  # Rotor inner diameter [mm]
airgap = (Dsi - Dro) / 2

slheight = 7.7  # Slot height from rotor inner diameter apex point [mm]
mangle = 145.0  # Magnet angle [°]
mheight = 6.5  # Magnet height [mm]
mwidth = 18.9  # Magnet width [mm]

aslheight = 3.0  # Flux barrier geometry [mm]
earheight = 2.1  # Flux barrier geometry [mm]
earlenght1x = 2.1  # Flux barrier geometry [mm]
earlenght2x = 1.90  # Flux barrier geometry [mm]
earlenght2y = 2.35  # Flux barrier geometry [mm]
earlenght3y = 1.5  # Flux barrier geometry [mm]
earlenght4 = 2.2  # Flux barrier geometry [mm]

R3 = 145  # Magnet material point.
R6 = 70  # Magnet material point.

# Excitation parameters
I0 = 250.0  # Stator current of one phase [A]
alpha = 0.0  # Offset of the current [°]

coil_area = 0.000142795  # area of the slot [m^2]
Nturns = 9  # turns of the coil in one slot [u.]
J0 = Nturns * I0 / coil_area
JU = J0 * math.cos(math.radians(alpha))
JV = J0 * math.cos(math.radians(alpha + 120))
JW = J0 * math.cos(math.radians(alpha + 240))


@dataclasses.dataclass
class VariableParams:
    prob2x = 0.0
    prob2y = 0.0
    prob3x = 0.0
    prob3y = 0.0
    prob4x = 0.0
    prob4y = 0.0
    prob5x = 0.0
    prob5y = 0.0


def stator():
    # stator outline
    stator_geo = Geometry()

    dsil = Node(Dso / 2, 0.0).rotate(112.5, degrees=True)
    dsir = Node(Dso / 2, 0.0).rotate(67.5, degrees=True)

    stator_geo.add_arc(CircleArc(dsir, ORIGIN, dsil))

    dsol = Node(Dsi / 2, 0.0).rotate(112.5, degrees=True)
    dsor = Node(Dsi / 2, 0.0).rotate(67.5, degrees=True)

    stator_geo.add_arc(CircleArc(dsor, ORIGIN, dsol))

    stator_geo.add_line(Line(dsil, dsol))
    stator_geo.add_line(Line(dsir, dsor))

    agsl = Node(Dsi / 2 - airgap / 3, 0.0).rotate(112.5, degrees=True)
    agsr = Node(Dsi / 2 - airgap / 3, 0.0).rotate(67.5, degrees=True)

    stator_geo.add_arc(CircleArc(agsr, ORIGIN, agsl))

    stator_geo.add_line(Line(dsol, agsl))
    stator_geo.add_line(Line(dsor, agsr))

    # slot geometry
    slot = Geometry()
    slot.import_dxf("resources/prius_slot_pyleecan.dxf")

    stator_geo.merge_geometry(slot)

    return stator_geo


def rotor_geometry(var_params: VariableParams):
    rotor_geo = Geometry()

    dril = Node(Dri / 2, 0.0).rotate(112.5, degrees=True)
    drir = Node(Dri / 2, 0.0).rotate(67.5, degrees=True)

    rotor_geo.add_arc(CircleArc(drir, ORIGIN, dril))

    drol = Node(Dro / 2, 0.0).rotate(112.5, degrees=True)
    dror = Node(Dro / 2, 0.0).rotate(67.5, degrees=True)

    rotor_geo.add_arc(CircleArc(dror, ORIGIN, drol))

    rotor_geo.add_line(Line(dril, drol))
    rotor_geo.add_line(Line(drir, dror))

    agrl = Node(Dro / 2 + airgap / 3, 0.0).rotate(112.5, degrees=True)
    agrr = Node(Dro / 2 + airgap / 3, 0.0).rotate(67.5, degrees=True)

    rotor_geo.add_arc(CircleArc(agrr, ORIGIN, agrl))

    rotor_geo.add_line(Line(drol, agrl))
    rotor_geo.add_line(Line(dror, agrr))

    # Rotor slot
    rotor_slot = Geometry()
    temp1 = math.cos(math.radians((180 - mangle) / 2)) * mheight

    sorigin = Node(0.0, Dri / 2 + slheight + temp1)

    pmb1 = Node(0.0, sorigin.y - mheight)
    pmb2 = Node(-mwidth, pmb1.y)
    pmb3 = Node(-mwidth, sorigin.y)

    rotor_slot.add_line(Line(sorigin, pmb1))
    rotor_slot.add_line(Line(pmb2, pmb1))
    rotor_slot.add_line(Line(pmb2, pmb3))
    rotor_slot.add_line(Line(sorigin, pmb3))

    temp2 = math.tan(math.radians((180 - mangle) / 2)) * (mheight - aslheight)

    apmb1 = Node(0.0, sorigin.y - mheight + aslheight)
    apmb2 = Node(temp2, apmb1.y)

    rotor_slot.add_line(Line(apmb1, apmb2))

    ear1 = Node(pmb2.x, pmb2.y + earheight)
    ear2 = Node(ear1.x - earlenght1x, ear1.y)
    ear3 = Node(ear2.x - earlenght2x, ear2.y + earlenght2y)
    ear4 = Node(ear3.x, ear3.y + earlenght3y)
    remy = mheight - earheight - earlenght2y - earlenght3y
    remx = math.sqrt((earlenght4 ** 2) - (remy ** 2))
    ear5 = Node(ear4.x + remx, ear4.y + remy)

    ear2.x = ear2.x + var_params.prob2x
    ear2.y = ear2.y + var_params.prob2y
    ear3.x = ear3.x + var_params.prob3x
    ear3.y = ear3.y + var_params.prob3y
    ear4.x = ear4.x + var_params.prob4x
    ear4.y = ear4.y + var_params.prob4y
    ear5.x = ear5.x + var_params.prob5x
    ear5.y = ear5.y + var_params.prob5y

    rotor_slot.add_line(Line(ear1, ear2))
    rotor_slot.add_line(Line(ear3, ear2))
    rotor_slot.add_line(Line(ear3, ear4))
    rotor_slot.add_line(Line(ear5, ear4))
    rotor_slot.add_line(Line(ear5, pmb3))

    rotor_slot.rotate_about(Node(sorigin.x, sorigin.y), -(180 - mangle) / 2, degrees=True)

    second_magnet = rotor_slot.duplicate()
    second_magnet.mirror(0)
    rotor_geo.merge_geometry(rotor_slot)
    rotor_geo.merge_geometry(second_magnet)
    return rotor_geo


def material_definitions(femm_problem: FemmProblem):
    # define default materials
    # air
    air = MagneticMaterial(material_name="air")
    air.mesh_size = 1.0
    air.material_positions = [Node(81.5, 0.0).rotate(108.75, degrees=True),
                              Node(81.5, 0.0).rotate(101.25, degrees=True),
                              Node(81.5, 0.0).rotate(93.75, degrees=True),
                              Node(81.5, 0.0).rotate(86.25, degrees=True),
                              Node(81.5, 0.0).rotate(78.75, degrees=True),
                              Node(81.5, 0.0).rotate(71.25, degrees=True),
                              Node(0.0, 67.5)]
    femm_problem.add_material(air)

    # airgap material, to define different mesh size
    air_gap = MagneticMaterial(material_name="air_gap")
    air_gap.material_positions = [Node(0, 80.35), Node(0, 80.85)]
    air_gap.mesh_size = 0.5
    femm_problem.add_material(air_gap)

    air_rotor = MagneticMaterial(material_name="air_rotor")
    air_rotor.material_positions = [Node(-19.5, 73.5), Node(19.5, 73.5)]
    air_rotor.mesh_size = 1.0
    femm_problem.add_material(air_rotor)

    # wire
    wire = MagneticMaterial(material_name="19 AWG", LamType=LamType.MAGNET_WIRE, WireD=0.912, Sigma=58e6)

    # magnetic steel
    steel = MagneticMaterial(material_name="M19_29GSF094", Sigma=1.9e6, lam_fill=0.94, Lam_d=0.34)
    steel.b = [0.000000, 0.047002, 0.094002, 0.141002, 0.338404, 0.507605,
               0.611006, 0.930612, 1.128024, 1.203236, 1.250248, 1.278460,
               1.353720, 1.429040, 1.485560, 1.532680, 1.570400, 1.693200,
               1.788400, 1.888400, 1.988400, 2.188400, 2.388397, 2.452391,
               3.668287]

    steel.h = [0.000000, 22.28000, 25.46000, 31.83000, 47.74000, 63.66000,
               79.57000, 159.1500, 318.3000, 477.4600, 636.6100, 795.7700,
               1591.500, 3183.000, 4774.600, 6366.100, 7957.700, 15915.00,
               31830.00, 111407.0, 190984.0, 350135.0, 509252.0, 560177.2,
               1527756.0]
    steel.mesh_size = 1.0
    steel.material_positions = [Node(0.0, 79.0), Node(0.0, 120.0)]
    femm_problem.add_material(steel)

    magnet = MagneticMaterial(material_name="N36Z_50", mu_x=1.03, mu_y=1.03, H_c=782000, Sigma=0.667e6)
    magnet.mesh_size = 1.0

    # Coils
    # PHASE U
    phase_U_positive = copy(wire)
    phase_U_positive.material_name = "U+"
    phase_U_positive.Je = JU
    phase_U_positive.material_positions = [Node(100.0, 0.0).rotate(109.0, degrees=True)]

    phase_W_negative = copy(wire)
    phase_W_negative.material_name = "W-"
    phase_W_negative.Je = -JW
    phase_W_negative.material_positions = [Node(100.0, 0.0).rotate(101.5, degrees=True),
                                           Node(100.0, 0.0).rotate(94.0, degrees=True)]

    # PHASE V
    phase_V_positive = copy(wire)
    phase_V_positive.material_name = "V+"
    phase_V_positive.Je = JV
    phase_V_positive.material_positions = [Node(100.0, 0.0).rotate(86.5, degrees=True),
                                           Node(100.0, 0.0).rotate(79.0, degrees=True)]

    phase_U_negative = copy(wire)
    phase_U_negative.material_name = "U-"
    phase_U_negative.Je = -JU
    phase_U_negative.material_positions = [Node(100.0, 0.0).rotate(71.5, degrees=True)]

    # Magnet right
    magnet_right = copy(magnet)
    magnet_right.material_name = 'magnet_right'
    magnet_right.remanence_angle = -90 + 90 - R3 / 2.0
    magnet_right.material_positions = [Node(-10, R6)]

    # Magnet left
    magnet_left = copy(magnet)
    magnet_left.material_name = 'magnet_left'
    magnet_left.remanence_angle = -magnet_right.remanence_angle + 180
    magnet_left.material_positions = [Node(10, R6)]

    # adding these materials to the femm problem
    femm_problem.add_material(phase_U_positive)
    femm_problem.add_material(phase_U_negative)
    femm_problem.add_material(phase_V_positive)
    femm_problem.add_material(phase_W_negative)
    femm_problem.add_material(magnet_right)
    femm_problem.add_material(magnet_left)

    femm_problem.make_analysis(filename="prius")


def boundary_definitions(femm_problem: FemmProblem):
    # Boundary conditions
    a0 = MagneticDirichlet(name="a0", a_0=0, a_1=0, a_2=0, phi=0)
    femm_problem.add_boundary(a0)

    pb1 = MagneticAnti("PB1")
    pb2 = MagneticAnti("PB2")
    pb3 = MagneticAnti("PB3")
    pb4 = MagneticAnti("PB4")
    apb = MagneticAntiPeriodicAirgap("APairgap")

    femm_problem.add_boundary(pb1)
    femm_problem.add_boundary(pb2)
    femm_problem.add_boundary(pb3)
    femm_problem.add_boundary(pb4)
    femm_problem.add_boundary(apb)

    # Add boundary conditions to stator segments
    femm_problem.set_boundary_definition_segment(Node(70.0, 0.0).rotate(67.5, degrees=True), pb1)
    femm_problem.set_boundary_definition_segment(Node(70.0, 0.0).rotate(112.5, degrees=True), pb1)

    femm_problem.set_boundary_definition_segment(Node(80.25, 0.0).rotate(67.5, degrees=True), pb2)
    femm_problem.set_boundary_definition_segment(Node(80.25, 0.0).rotate(112.5, degrees=True), pb2)

    femm_problem.set_boundary_definition_segment(Node(80.8, 0.0).rotate(67.5, degrees=True), pb3)
    femm_problem.set_boundary_definition_segment(Node(80.8, 0.0).rotate(112.5, degrees=True), pb3)

    femm_problem.set_boundary_definition_segment(Node(110.0, 0.0).rotate(67.5, degrees=True), pb4)
    femm_problem.set_boundary_definition_segment(Node(110.0, 0.0).rotate(112.5, degrees=True), pb4)

    femm_problem.set_boundary_definition_arc(Node(0.0, 80.4494), apb)
    femm_problem.set_boundary_definition_arc(Node(0.0, 80.7), apb)

    femm_problem.set_boundary_definition_arc(Node(0.0, 134.62), a0)
    femm_problem.set_boundary_definition_arc(Node(0.0, 55.319), a0)


if __name__ == '__main__':
    problem = FemmProblem(out_file="prius.csv")
    problem.magnetic_problem(0, LengthUnit.MILLIMETERS, "planar")

    variables = VariableParams()

    geo = stator()
    rotor = rotor_geometry(variables)
    geo.merge_geometry(rotor)

    problem.create_geometry(geo)
    material_definitions(problem)
    boundary_definitions(problem)

    problem.write("prius.lua")

    femm = Executor()
    current_dir = os.getcwd()
    lua_file = current_dir + "/prius.lua"
    femm.run(lua_file)
