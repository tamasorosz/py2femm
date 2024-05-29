import os
import dataclasses
import math
from math import sin, cos, asin, acos, pi
from copy import copy

from src.magnetics import MagneticDirichlet, MagneticMaterial, MagneticAnti, MagneticAntiPeriodicAirgap, LamType
from src.femm_problem import FemmProblem
from src.general import LengthUnit
from src.geometry import Geometry, Line, Node, CircleArc
from src.executor import Executor

ORIGIN = Node(0.0, 0.0)

# Geometry parameters for stator
Ro = 17
Ri = 10
w1 = 0.5
w2 = 1
w3 = 2.5
w4 = 2
h1 = 0.2
h2 = 0.3
h3 = 4
h4 = 0.2
s3 = 1.8
ag_s = 0.2
ag_r = 0.2
ns = 24
np = 8
nsr = 6  # number of required slots
slot_deg = 360 / ns
slot_rad = 2 * pi / ns

# Geometry parameters for stator
mw = 6
r1 = 2
r2 = 8
r3 = 9
pole_deg = 360 / np
pole_rad = 2 * pi / np

gamma = 0  # current offset
Imax = 250
nturns = 9
coil_area = 1  # TODO: kérdéses
J0 = nturns * Imax / coil_area
JU = J0 * cos(gamma)
JV = J0 * cos(gamma + 2 * pi / 3)
JW = J0 * cos(gamma + 2 * pi / 3)


def stator():
    stator_geo = Geometry()

    ORIGIN = Node(0, 0, 'ORIGIN')

    p1 = Node((-w1 / 2), (Ri * cos(asin(w1 / 2 / Ri))), 'p1')
    p2 = Node((-w1 / 2), ((Ri + h1) * cos(asin(w1 / 2 / (Ri + h1)))), 'p2')
    p3 = Node((-w2 / 2), ((Ri + h1 + h2) * cos(asin(w2 / 2 / (Ri + h1 + h2)))), 'p3')
    p4 = Node((-w3 / 2), ((Ri + h1 + h2 + h3) * cos(asin(w3 / 2 / (Ri + h1 + h2 + h3)))), 'p4')
    p6 = Node((-w4 / 2), ((Ri + h1 + h2 + h3 + h4) * cos(asin(w4 / 2 / (Ri + h1 + h2 + h3 + h4)))), 'p6')
    p7 = Node((w4 / 2), ((Ri + h1 + h2 + h3 + h4) * cos(asin(w4 / 2 / (Ri + h1 + h2 + h3 + h4)))), 'p7')
    p9 = Node((w3 / 2), ((Ri + h1 + h2 + h3) * cos(asin(w3 / 2 / (Ri + h1 + h2 + h3)))), 'p9')
    p10 = Node((w2 / 2), ((Ri + h1 + h2) * cos(asin(w2 / 2 / (Ri + h1 + h2)))), 'p10')
    p11 = Node((w1 / 2), ((Ri + h1) * cos(asin(w1 / 2 / (Ri + h1)))), 'p11')
    p12 = Node((w1 / 2), (Ri * cos(asin(w1 / 2 / Ri))), 'p12')

    l1 = Line(p1, p2)
    l2 = Line(p2, p3)
    l3 = Line(p3, p4)
    l4 = Line(p6, p7)
    l5 = Line(p9, p10)
    l6 = Line(p10, p11)
    l7 = Line(p11, p12)
    l8 = Line(p12, p1)

    stator_geo.nodes = [ORIGIN, p1, p2, p3, p4, p6, p7, p9, p10, p11, p12]
    stator_geo.lines = [l1, l2, l3, l4, l5, l6, l7, l8]

    # Emlékeztető: majd később megírni if-fel, hogy működjön 24-re is, most csak így
    # A horony pontjainak távolsága az origótól
    rp1 = p1.distance_to(ORIGIN)
    rp2 = p2.distance_to(ORIGIN)
    rp3 = p3.distance_to(ORIGIN)
    rp4 = p4.distance_to(ORIGIN)
    rp6 = p6.distance_to(ORIGIN)
    rp7 = p7.distance_to(ORIGIN)
    rp9 = p9.distance_to(ORIGIN)
    rp10 = p10.distance_to(ORIGIN)
    rp11 = p11.distance_to(ORIGIN)
    rp12 = p2.distance_to(ORIGIN)
    # A pontok függőlegessel bezárt szöge (origó csúccsal) // nem biztos, hogy jó valamire, de egyelőre itthagyom
    rotpar1 = -asin(p1.x / rp1)
    rotpar2 = -asin(p2.x / rp2)
    rotpar3 = -asin(p3.x / rp3)
    rotpar4 = -asin(p4.x / rp4)
    rotpar6 = -asin(p6.x / rp6)
    rotpar7 = -asin(p7.x / rp7)
    rotpar9 = -asin(p9.x / rp9)
    rotpar10 = -asin(p10.x / rp10)
    rotpar11 = -asin(p11.x / rp11)
    rotpar12 = -asin(p12.x / rp12)

    # Calculations for the slot fillet
    radius = s3
    const1 = p4.x ** 2 + p4.y ** 2 - p6.x ** 2 - p6.y ** 2
    a = 1 + ((2 * (p6.x - p4.x) + const1) / (2 * (p6.y - p4.y))) ** 2
    b = -2 * p4.x - p4.y * ((2 * (p6.x - p4.x) + const1) / (p6.y - p4.y))
    c = p4.y ** 2 - radius ** 2
    x_solv = ((-1 * b + math.sqrt(b ** 2 - 4 * a * c)) / (2 * a))
    y_solv = (-2 * x_solv * (p6.x - p4.x) - const1) / (2 * (p6.y - p4.y))

    p_aux1 = Node(x_solv, y_solv, 'aux1')
    p_aux2 = Node(-x_solv, y_solv, 'aux2')

    stator_geo.nodes += [p_aux1, p_aux2]
    corner_1 = CircleArc(p6, p_aux1, p4)
    corner_2 = CircleArc(p9, p_aux2, p7)
    stator_geo.circle_arcs = [corner_1, corner_2]
    # -

    i = 1
    while i < nsr:
        q1 = p1.rotate_about(ORIGIN, -i * slot_rad)
        q1.id = 'p' + str(i * 12 + 1)
        q2 = p2.rotate_about(ORIGIN, -i * slot_rad)
        q2.id = 'p' + str(i * 12 + 2)
        q3 = p3.rotate_about(ORIGIN, -i * slot_rad)
        q3.id = 'p' + str(i * 12 + 3)
        q4 = p4.rotate_about(ORIGIN, -i * slot_rad)
        q4.id = 'p' + str(i * 12 + 4)
        q6 = p6.rotate_about(ORIGIN, -i * slot_rad)
        q6.id = 'p' + str(i * 12 + 6)
        q7 = p7.rotate_about(ORIGIN, -i * slot_rad)
        q7.id = 'p' + str(i * 12 + 7)
        q9 = p9.rotate_about(ORIGIN, -i * slot_rad)
        q9.id = 'p' + str(i * 12 + 9)
        q10 = p10.rotate_about(ORIGIN, -i * slot_rad)
        q10.id = 'p' + str(i * 12 + 10)
        q11 = p11.rotate_about(ORIGIN, -i * slot_rad)
        q11.id = 'p' + str(i * 12 + 11)
        q12 = p12.rotate_about(ORIGIN, -i * slot_rad)
        q12.id = 'p' + str(i * 12 + 12)
        q_aux1 = p_aux1.rotate_about(ORIGIN, -i * slot_rad)
        q_aux1.id = 'p_aux' + str(i * 2 + 1)
        q_aux2 = p_aux2.rotate_about(ORIGIN, -i * slot_rad)
        q_aux2.id = 'p_aux' + str(i * 2 + 2)
        qnodes = [q1, q2, q3, q4, q6, q7, q9, q10, q11, q12, q_aux1, q_aux2]
        stator_geo.nodes += qnodes
        m1 = Line(q1, q2)
        m2 = Line(q2, q3)
        m3 = Line(q3, q4)
        m4 = Line(q6, q7)
        m6 = Line(q9, q10)
        m7 = Line(q10, q11)
        m9 = Line(q11, q12)
        m10 = Line(q12, q1)
        mlines = [m1, m2, m3, m4, m6, m7, m9, m10]
        stator_geo.lines += mlines
        fillet_1 = CircleArc(q6, q_aux1, q4)
        fillet_2 = CircleArc(q9, q_aux2, q7)
        fillets = [fillet_1, fillet_2]
        stator_geo.circle_arcs += fillets
        i += 1
    j = 1
    yokearcs = []
    while j < nsr:
        start = j * 12 + 1
        end = j * 12 - 2
        yokearc = CircleArc(stator_geo.nodes[start], ORIGIN, stator_geo.nodes[end])
        yokearcs += [yokearc]
        j += 1
    stator_geo.circle_arcs += yokearcs

    yp1 = Node(Ri * sin(-slot_rad / 2), Ri * cos(slot_rad / 2))
    yp2 = Node(Ro * sin(-slot_rad / 2), Ro * cos(slot_rad / 2))
    yp3 = Node(Ro * sin(-slot_rad / 2 + slot_rad * nsr), Ro * cos(slot_rad / 2 - slot_rad * nsr))
    yp4 = Node(Ri * sin(-slot_rad / 2 + slot_rad * nsr), Ri * cos(slot_rad / 2 - slot_rad * nsr))
    yl1 = Line(yp1, yp2)
    yl2 = Line(yp3, yp4)
    yl3 = CircleArc(yp3, ORIGIN, yp2)
    yl4 = CircleArc(stator_geo.nodes[1], ORIGIN, yp1)
    yl5 = CircleArc(yp4, ORIGIN, stator_geo.nodes[len(stator_geo.nodes) - 3])
    stator_geo.nodes += [yp1, yp2, yp3, yp4]
    stator_geo.lines += [yl1, yl2]
    stator_geo.circle_arcs += [yl3, yl4, yl5]

    agp1 = Node((Ri - ag_s) * sin(-slot_rad / 2), (Ri - ag_s) * cos(slot_rad / 2))
    agp2 = Node((Ri - ag_s) * sin(-slot_rad / 2 + slot_rad * nsr), (Ri - ag_s) * cos(slot_rad / 2 - slot_rad * nsr))
    stator_geo.nodes += [agp1, agp2]
    agl1 = Line(agp1, yp1)
    agl2 = Line(agp2, yp4)
    sagarc = CircleArc(agp2, ORIGIN, agp1)  # stator airgap arc
    stator_geo.lines += [agl1, agl2]
    stator_geo.circle_arcs += [sagarc]

    return stator_geo


def rotor():
    rotor_geo = Geometry()

    rotang1 = asin(mw / (2 * r2))
    rotang2 = asin(mw / (2 * r3))
    p01 = Node(r1 * sin(-slot_rad / 2), r1 * cos(slot_rad / 2), 'pr01')
    p02 = Node(r1 * sin(-slot_rad / 2 + nsr / 3 * pole_rad), r1 * cos(-slot_rad / 2 + nsr / 3 * pole_rad), 'pr02')
    p1 = Node(r2 * sin(-slot_rad / 2), r2 * cos(slot_rad / 2), 'pr1')
    p2 = Node(r2 * sin(-slot_rad / 2 + pole_rad), r2 * cos(-slot_rad / 2 + pole_rad), 'pr2')
    p3 = Node(r2 * sin(-slot_rad / 2 + pole_rad / 2 - rotang1 / 2),
              r2 * cos(-slot_rad / 2 + pole_rad / 2 - rotang1 / 2), 'pr3')
    p4 = Node(r2 * sin(-slot_rad / 2 + pole_rad / 2 + rotang1 / 2),
              r2 * cos(-slot_rad / 2 + pole_rad / 2 + rotang1 / 2), 'pr4')
    p5 = Node(r3 * sin(-slot_rad / 2 + pole_rad / 2 - rotang2 / 2),
              r3 * cos(-slot_rad / 2 + pole_rad / 2 - rotang2 / 2), 'pr5')
    p6 = Node(r3 * sin(-slot_rad / 2 + pole_rad / 2 + rotang2 / 2),
              r3 * cos(-slot_rad / 2 + pole_rad / 2 + rotang2 / 2), 'pr6')
    rotornodes = [p1, p2, p3, p4, p5, p6]

    rotor_geo.nodes += rotornodes
    l1 = Line(p1, p01)
    l3 = Line(p3, p4)
    l4 = Line(p3, p5)
    l5 = Line(p4, p6)
    rotor_geo.lines += [l1, l3, l4, l5]
    c0 = CircleArc(p02, ORIGIN, p01)
    c1 = CircleArc(p3, ORIGIN, p1)
    c2 = CircleArc(p2, ORIGIN, p4)
    c3 = CircleArc(p6, ORIGIN, p5)
    rotor_geo.circle_arcs += [c0, c1, c2, c3]

    i = 1
    while i < nsr / 3:
        q1 = p1.rotate_about(ORIGIN, -i * pole_rad)
        q1.id = 'pr' + str(i * 6 + 1)
        q2 = p2.rotate_about(ORIGIN, -i * pole_rad)
        q2.id = 'pr' + str(i * 6 + 2)
        q3 = p3.rotate_about(ORIGIN, -i * pole_rad)
        q3.id = 'pr' + str(i * 6 + 3)
        q4 = p4.rotate_about(ORIGIN, -i * pole_rad)
        q4.id = 'pr' + str(i * 6 + 4)
        q5 = p5.rotate_about(ORIGIN, -i * pole_rad)
        q5.id = 'pr' + str(i * 6 + 5)
        q6 = p6.rotate_about(ORIGIN, -i * pole_rad)
        q6.id = 'pr' + str(i * 6 + 6)
        qnodes = [q1, q2, q3, q4, q5, q6]
        rotor_geo.nodes += qnodes
        m1 = Line(q3, q5)
        m2 = Line(q4, q6)
        m3 = Line(q3, q4)
        mlines = [m1, m2, m3]
        rotor_geo.lines += mlines
        v1 = CircleArc(q3, ORIGIN, q1)
        v2 = CircleArc(q2, ORIGIN, q4)
        v3 = CircleArc(q6, ORIGIN, q5)
        varcs = [v1, v2, v3]
        rotor_geo.circle_arcs += varcs
        i += 1

    l = Line(rotor_geo.nodes[len(rotor_geo.nodes) - 5], p02)
    rotor_geo.lines += [l]

    agp1 = Node((r3 + ag_r) * sin(-slot_rad / 2), (r3 + ag_r) * cos(slot_rad / 2))
    agp2 = Node((r3 + ag_r) * sin(-slot_rad / 2 + slot_rad * nsr), (r3 + ag_r) * cos(slot_rad / 2 - slot_rad * nsr))
    rotor_geo.nodes += [agp1, agp2]
    agl1 = Line(agp1, p1)
    agl2 = Line(agp2, q2)
    ragarc = CircleArc(agp2, ORIGIN, agp1)  # rotor airgap arc
    rotor_geo.lines += [agl1, agl2]
    rotor_geo.circle_arcs += [ragarc]

    return rotor_geo


def material_definitions(femm_problem: FemmProblem):
    air = MagneticMaterial(material_name='air')
    air.mesh_size = 1
    air.material_positions = [Node(0, Ri + (Ro - Ri) / 2)]
    i = 1
    while i < nsr:
        p = Node(0, Ri + (Ro - Ri) / 2).rotate_about(ORIGIN, -i * slot_rad)
        air.material_positions += [p]
        i += 1
    femm_problem.add_material(air)

    # airgap material, different mesh size
    rotang2 = asin(mw / (2 * r3))
    air_gap = MagneticMaterial(material_name='air_gap')
    air_gap.material_positions = [Node(0, Ri - ag_s / 2)]
    air_gap.mesh_size = 0.5
    femm_problem.add_material(air_gap)

    air_rotor = MagneticMaterial(material_name='air_gap')
    air_rotor.material_positions = [Node(r3 * 0.95 * sin(-slot_rad / 2 + pole_rad / 2 + rotang2 / 2),
                                         r3 * 0.95 * cos(-slot_rad / 2 + pole_rad / 2 + rotang2 / 2))]
    air_rotor.mesh_size = 1
    femm_problem.add_material(air_rotor)

    # wire
    wire = MagneticMaterial(material_name='19 AMG', LamType=LamType.MAGNET_WIRE, WireD=0.912, Sigma=58e6)

    # magnetic steel
    steel = MagneticMaterial(material_name='M19_29GSF094', Sigma=1.9e6, lam_fill=0.94, Lam_d=0.34)
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
    steel.mesh_size = 1
    steel.material_positions = [Node(0, r2 * 0.95), Node(0, Ro * 0.95)]
    femm_problem.add_material(steel)

    # magnet
    magnet = MagneticMaterial(material_name='N36Z_50', mu_x=1.03, mu_y=1.03, H_c=782000, Sigma=0.667e6)
    magnet.mesh_size = 1

    '''# Coils
    # Phase U
    phase_U_pos = copy(wire)
    phase_U_pos.material_name='U+'
    phase_U_pos.Je = JU

    phase_U_pos.material_positions = [Node(0, )]'''  # Todo: a tekercseléséről semmit sem tudok


def boundary_definitions(femm_problem: FemmProblem):
    # conditions
    a0 = MagneticDirichlet(name='a0', a_0=0, a_1=0, a_2=0, phi=0)
    femm_problem.add_boundary(a0)

    apb1 = MagneticAnti("APB1")
    apb2 = MagneticAnti("APB2")
    apb3 = MagneticAnti("APB3")
    apb4 = MagneticAnti("APB4")
    apb = MagneticAntiPeriodicAirgap('APAirgap')

    femm_problem.add_boundary(apb1)
    femm_problem.add_boundary(apb2)
    femm_problem.add_boundary(apb3)
    femm_problem.add_boundary(apb4)
    femm_problem.add_boundary(apb)

    # Add boundary conditions to stator segments
    femm_problem.set_boundary_definition_segment(Node(Ro * 0.99 * sin(-slot_rad / 2), Ro * 0.99 * cos(slot_rad / 2)),
                                                 apb1)
    femm_problem.set_boundary_definition_segment(
        Node(Ro * 0.99 * sin(-slot_rad / 2), Ro * 0.99 * cos(slot_rad / 2)).rotate_about(ORIGIN, -nsr * slot_rad), apb1)

    femm_problem.set_boundary_definition_segment(
        Node((r3 + ag_r) * sin(-slot_rad / 2), (r3 + ag_r) * cos(slot_rad / 2)), apb2)
    femm_problem.set_boundary_definition_segment(
        Node((r3 + ag_r) * sin(-slot_rad / 2), (r3 + ag_r) * cos(slot_rad / 2)).rotate_about(ORIGIN, -nsr * slot_rad),
        apb2)

    femm_problem.set_boundary_definition_segment(
        Node((r3 + ag_r) * sin(-slot_rad / 2), (r3 + ag_r) * cos(slot_rad / 2)), apb3)
    femm_problem.set_boundary_definition_segment(
        Node((r3 + ag_r) * sin(-slot_rad / 2 + slot_rad * nsr), (r3 + ag_r) * cos(slot_rad / 2 - slot_rad * nsr)), apb3)

    femm_problem.set_boundary_definition_segment(Node(r1 * sin(-slot_rad / 2), r1 * cos(slot_rad / 2)), apb4)
    femm_problem.set_boundary_definition_segment(
        Node(r1 * sin(-slot_rad / 2 + nsr / 3 * pole_rad), r1 * cos(-slot_rad / 2 + nsr / 3 * pole_rad)), apb4)

    femm_problem.set_boundary_definition_arc(Node(0, r2 + ag_r), apb)
    femm_problem.set_boundary_definition_arc(Node(0, Ri - ag_s), apb)
    femm_problem.set_boundary_definition_arc(Node(0, r1), a0)
    femm_problem.set_boundary_definition_arc(Node(0, Ro), a0)


if __name__ == '__main__':
    problem = FemmProblem(out_file="PMDC.csv")
    problem.magnetic_problem(0, LengthUnit.CENTIMETERS, 'axi')
    s = stator()
    r = rotor()
    s.merge_geometry(r)
    problem.create_geometry(s)
    material_definitions(problem)
    boundary_definitions(problem)
    problem.make_analysis()
    problem.write('PMDC.lua')

    femm = Executor()
    current_dir = os.getcwd()
    lua_file = current_dir + "/PMDC.lua"
    femm.run(lua_file)
