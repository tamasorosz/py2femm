import math
import os
from dataclasses import dataclass

from src.executor import Executor
from src.femm_problem import FemmProblem
from src.general import LengthUnit
from src.geometry import Geometry, Node, Sector, CircleArc, Line
from src.magnetics import MagneticDirichlet, MagneticPeriodicAirgap, MagneticPeriodic, MagneticBoundaryModification, \
    MagneticMaterial, LamType

current_file_path = os.path.abspath(__file__)
folder_path = os.path.dirname(current_file_path)

n0 = Node(0, 0)


class VariableParameters:

    def __init__(self, fold, out, counter, JAp, JAn, JBp, JBn, JCp, JCn, ang_co, deg_co, bd, bw, bh, bg):
        self.fold = fold
        self.out = out
        self.counter = counter

        self.JAp = JAp
        self.JAn = JAn
        self.JBp = JBp
        self.JBn = JBn
        self.JCp = JCp
        self.JCn = JCn

        self.ang_co = ang_co
        self.deg_co = deg_co

        self.bd = bd
        self.bw = bw
        self.bh = bh
        self.bg = bg


def stator_geometry(femm_problem: FemmProblem):
    # stator geometry imported from a .dxf file with airgap sliding band: https://www.femm.info/wiki/SlidingBand
    stator_geo = Geometry()

    stator_geo.import_dxf("resources/stator.dxf")

    femm_problem.create_geometry(stator_geo)


def rotor_geometry(femm_problem: FemmProblem, var: VariableParameters):
    rotor_geo = Geometry()

    # define the nodes and sectors of the cut-off barriers
    co_s = Node(22, 0).rotate_about(n0, 45 - var.ang_co / 2, degrees=True)
    co_e = Node(22, 0).rotate_about(n0, 45 + var.ang_co / 2, degrees=True)
    co_r = co_e.rotate_about(n0, -45, degrees=True)
    co_l = co_s.rotate_about(n0, 45, degrees=True)

    rotor_geo.add_node(co_s)
    rotor_geo.add_node(co_e)
    rotor_geo.add_node(co_r)
    rotor_geo.add_node(co_l)

    co_arc = Sector(co_e, co_s, var.deg_co)

    rotor_geo.add_sector(co_arc)

    co_arc_ep = co_arc.selection_point()
    co_arc_ep_r = co_arc_ep.rotate_about(n0, -45, degrees=True)
    co_arc_ep_l = co_arc_ep.rotate_about(n0, 45, degrees=True)

    rotor_geo.add_node(co_arc_ep_r)
    rotor_geo.add_node(co_arc_ep_l)

    co_arcr = Sector(co_r, co_arc_ep_r, var.deg_co / 2)
    co_arcl = Sector(co_arc_ep_l, co_l, var.deg_co / 2)

    rotor_geo.add_sector(co_arcr)
    rotor_geo.add_sector(co_arcl)

    rot_arc_l = CircleArc(co_e, n0, co_l)
    rot_arc_r = CircleArc(co_r, n0, co_s)

    rotor_geo.add_arc(rot_arc_l)
    rotor_geo.add_arc(rot_arc_r)

    # define sliding band nodes, lines and arc
    sb_l = Node(0.00, 22.10)
    sb_r = Node(22.10, 0.00)

    rotor_geo.add_node(sb_r)
    rotor_geo.add_node(sb_l)

    sbl_l = Line(sb_l, co_arc_ep_l)
    sbl_r = Line(sb_r, co_arc_ep_r)

    rotor_geo.add_line(sbl_l)
    rotor_geo.add_line(sbl_r)

    sb_arc = CircleArc(sb_r, n0, sb_l)

    rotor_geo.add_arc(sb_arc)

    # define the enclosing geometry
    h0 = Node(6.00, 0.00)
    v0 = h0.rotate_about(n0, 90, True)

    rotor_geo.add_node(h0)
    rotor_geo.add_node(v0)

    encl_r = Line(h0, co_arc_ep_r)
    encl_l = Line(v0, co_arc_ep_l)

    rotor_geo.add_line(encl_r)
    rotor_geo.add_line(encl_l)

    enc_arc_0 = CircleArc(h0, n0, v0)

    rotor_geo.add_arc(enc_arc_0)

    # define inner barriers
    co_arc_ep = co_arc.selection_point()  # Cut-off barrier arc point at 45 deg.
    co_arc_cp = co_arc.center_point()  # Cut-off barrier arc center point.

    # rotor_geo.add_node(co_arc_ep)

    d_ep_cp = co_arc_ep.distance_to(co_arc_cp)
    d_n0_ep = co_arc_ep.distance_to(n0)
    d_n0_cp = co_arc_cp.distance_to(n0)

    # define upper arc of inner barrier
    ib_base1 = Node(d_n0_ep - var.bd, 0.00).rotate_about(n0, 45, True)

    ib_1_ang = math.atan2(var.bw / 2, (d_ep_cp + var.bd))
    ib_1l = ib_base1.rotate_about(co_arc_cp, -ib_1_ang, False)
    ib_1r = ib_base1.rotate_about(co_arc_cp, ib_1_ang, False)

    ib_1l_r = ib_1l.rotate_about(n0, -45, True)
    ib_1r_l = ib_1r.rotate_about(n0, 45, True)

    # rotor_geo.add_node(ib_base1)
    rotor_geo.add_node(ib_1l)
    rotor_geo.add_node(ib_1r)
    rotor_geo.add_node(ib_1r_l)
    rotor_geo.add_node(ib_1l_r)

    A = d_ep_cp + var.bd
    B = d_n0_cp
    C = 22 - var.bg
    ib_3_ang = math.acos((A ** 2 + B ** 2 - C ** 2) / (2 * A * B))
    ib_3l = ib_base1.rotate_about(co_arc_cp, -ib_3_ang, False)
    ib_3r = ib_base1.rotate_about(co_arc_cp, ib_3_ang, False)

    ib_3l_r = ib_3l.rotate_about(n0, -45, True)
    ib_3r_l = ib_3r.rotate_about(n0, 45, True)

    rotor_geo.add_node(ib_3l)
    rotor_geo.add_node(ib_3r)
    rotor_geo.add_node(ib_3r_l)
    rotor_geo.add_node(ib_3l_r)

    # define under arc of inner barrier
    ib_base2 = Node(d_n0_ep - var.bd - var.bh, 0.00).rotate_about(n0, 45, True)

    ib_2_ang = math.atan2(var.bw / 2, (d_ep_cp + var.bd + var.bh))
    ib_2l = ib_base2.rotate_about(co_arc_cp, -ib_2_ang, False)
    ib_2r = ib_base2.rotate_about(co_arc_cp, ib_2_ang, False)

    ib_2l_r = ib_2l.rotate_about(n0, -45, True)
    ib_2r_l = ib_2r.rotate_about(n0, 45, True)

    # rotor_geo.add_node(ib_base)
    rotor_geo.add_node(ib_2l)
    rotor_geo.add_node(ib_2r)
    rotor_geo.add_node(ib_2r_l)
    rotor_geo.add_node(ib_2l_r)

    A = d_ep_cp + var.bd + var.bh
    B = d_n0_cp
    C = 22 - var.bg
    ib_4_ang = math.acos((A ** 2 + B ** 2 - C ** 2) / (2 * A * B))
    ib_4l = ib_base2.rotate_about(co_arc_cp, -ib_4_ang, False)
    ib_4r = ib_base2.rotate_about(co_arc_cp, ib_4_ang, False)

    ib_4l_r = ib_4l.rotate_about(n0, -45, True)
    ib_4r_l = ib_4r.rotate_about(n0, 45, True)

    rotor_geo.add_node(ib_4l)
    rotor_geo.add_node(ib_4r)
    rotor_geo.add_node(ib_4r_l)
    rotor_geo.add_node(ib_4l_r)

    # define line between upper and under barrier arcs

    ibl_1l = Line(ib_1l, ib_2l)
    ibl_1r = Line(ib_1r, ib_2r)
    ibl_2l = Line(ib_3l, ib_4l)
    ibl_2r = Line(ib_3r, ib_4r)

    ibl_1r_l = Line(ib_1r_l, ib_2r_l)
    ibl_1l_r = Line(ib_1l_r, ib_2l_r)
    ibl_2r_l = Line(ib_3r_l, ib_4r_l)
    ibl_2l_r = Line(ib_3l_r, ib_4l_r)

    rotor_geo.add_line(ibl_1l)
    rotor_geo.add_line(ibl_1r)
    rotor_geo.add_line(ibl_2l)
    rotor_geo.add_line(ibl_2r)

    rotor_geo.add_line(ibl_1l_r)
    rotor_geo.add_line(ibl_1r_l)
    rotor_geo.add_line(ibl_2l_r)
    rotor_geo.add_line(ibl_2r_l)

    iblu_arc = Sector(ib_3l, ib_1l, var.deg_co / 2)
    ibru_arc = Sector(ib_1r, ib_3r, var.deg_co / 2)
    iblo_arc = Sector(ib_4l, ib_2l, var.deg_co / 2)
    ibro_arc = Sector(ib_2r, ib_4r, var.deg_co / 2)

    iblu_arc_r = Sector(ib_3l_r, ib_1l_r, var.deg_co / 2)
    ibru_arc_l = Sector(ib_1r_l, ib_3r_l, var.deg_co / 2)
    iblo_arc_r = Sector(ib_4l_r, ib_2l_r, var.deg_co / 2)
    ibro_arc_l = Sector(ib_2r_l, ib_4r_l, var.deg_co / 2)

    rotor_geo.add_sector(iblu_arc)
    rotor_geo.add_sector(ibru_arc)
    rotor_geo.add_sector(iblo_arc)
    rotor_geo.add_sector(ibro_arc)
    rotor_geo.add_sector(iblu_arc_r)
    rotor_geo.add_sector(ibru_arc_l)
    rotor_geo.add_sector(iblo_arc_r)
    rotor_geo.add_sector(ibro_arc_l)

    # calculate the midpoint of every flux barrier to define material labels later on

    ib_mp1 = Line(iblu_arc_r.selection_point(), iblo_arc_r.selection_point()).selection_point()
    ib_mp2 = Line(ibru_arc.selection_point(), ibro_arc.selection_point()).selection_point()
    ib_mp3 = Line(iblu_arc.selection_point(), iblo_arc.selection_point()).selection_point()
    ib_mp4 = Line(ibru_arc_l.selection_point(), ibro_arc_l.selection_point()).selection_point()

    # rotor_geo.add_node(ib_mp1)
    # rotor_geo.add_node(ib_mp2)
    # rotor_geo.add_node(ib_mp3)
    # rotor_geo.add_node(ib_mp4)

    femm_problem.create_geometry(rotor_geo)

    return ib_mp1, ib_mp2, ib_mp3, ib_mp4


def add_boundaries(femm_problem: FemmProblem):
    # Define all boundary conditions
    a0 = MagneticDirichlet(name="a0", a_0=0, a_1=0, a_2=0, phi=0)  # A0 Boundary Condition

    pbca = MagneticPeriodicAirgap(name="pbca")  # Periodic Air Gap Boundary Condition

    pbc1 = MagneticPeriodic(name="pbc1")  # Periodic Boundary Condition
    pbc2 = MagneticPeriodic(name="pbc2")  # Periodic Boundary Condition
    pbc3 = MagneticPeriodic(name="pbc3")  # Periodic Boundary Condition
    pbc4 = MagneticPeriodic(name="pbc4")  # Periodic Boundary Condition

    # Add all boundary conditions
    femm_problem.add_boundary(a0)
    femm_problem.add_boundary(pbca)
    femm_problem.add_boundary(pbc1)
    femm_problem.add_boundary(pbc2)
    femm_problem.add_boundary(pbc3)
    femm_problem.add_boundary(pbc4)

    # Modify Periodic Air Gap Boundary Condition Inner Angle to imitate rotation
    # modify_boundary added, because there is a FEMM bug with add_boundary, that ia is set by oa and oa is not possible
    # to set. If you need to set oa, you need modify_boundary.
    pbca = MagneticBoundaryModification(pbca.name, pbca.boundary_format, propnum=10, value=1)

    # Add modified Periodic Air Gap Boundary Condition
    femm_problem.modify_boundary(pbca)

    # Add boundary conditions to stator segments
    femm_problem.set_boundary_definition_segment(Node(0, 22.4), pbc3)
    femm_problem.set_boundary_definition_segment(Node(22.4, 0), pbc3)
    femm_problem.set_boundary_definition_segment(Node(0, 34), pbc4)
    femm_problem.set_boundary_definition_segment(Node(34, 0), pbc4)

    # Define and add boundary conditions to stator circle arcs
    a02 = Node(22.30, 0).rotate_about(n0, 45, degrees=True)
    a03 = Node(43.25, 0).rotate_about(n0, 45, degrees=True)

    femm_problem.set_boundary_definition_arc(a02, pbca)
    femm_problem.set_boundary_definition_arc(a03, a0)


def add_materials(femm_problem: FemmProblem, var: VariableParameters, rot: rotor_geometry):
    # Define wire material, air and steel material.
    # There is an interesting bug in FEMM, that you can't add source current density to magnet wire, but it is possible
    # using .lua code
    # To get the correct winding scheme, check: https://bavaria-direct.co.za/scheme/calculator/
    copper_Ap = MagneticMaterial(material_name="U+", J=var.JAp, Sigma=58, LamType=LamType.MAGNET_WIRE, WireD=1)
    copper_An = MagneticMaterial(material_name="U-", J=var.JAn, Sigma=58, LamType=LamType.MAGNET_WIRE, WireD=1)
    copper_Bp = MagneticMaterial(material_name="V+", J=var.JBp, Sigma=58, LamType=LamType.MAGNET_WIRE, WireD=1)
    copper_Bn = MagneticMaterial(material_name="V-", J=var.JBn, Sigma=58, LamType=LamType.MAGNET_WIRE, WireD=1)
    copper_Cp = MagneticMaterial(material_name="W+", J=var.JCp, Sigma=58, LamType=LamType.MAGNET_WIRE, WireD=1)
    copper_Cn = MagneticMaterial(material_name="W-", J=var.JCn, Sigma=58, LamType=LamType.MAGNET_WIRE, WireD=1)

    air = MagneticMaterial(material_name="air")

    steel = MagneticMaterial(material_name="steel", Sigma=5.8, Lam_d=0.5, lam_fill=0.98)

    # Add wire material, air and steel material.
    femm_problem.add_material(copper_Ap)
    femm_problem.add_material(copper_An)
    femm_problem.add_material(copper_Bp)
    femm_problem.add_material(copper_Bn)
    femm_problem.add_material(copper_Cp)
    femm_problem.add_material(copper_Cn)
    femm_problem.add_material(air)
    femm_problem.add_material(steel)

    # Add BH curve for stator steel material.
    # There is an interesting bug in FEMM, that you can add any number of BH point, but it will only plot it manually
    # to B~10.000. If you check the BH list, all the points are there.
    femm_problem.add_bh_curve(material_name="steel",
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

    # Add block labels to the stator
    femm_problem.define_block_label(Node(15.85, 15.85), air)

    femm_problem.define_block_label(Node(28.00, 28.00), steel)

    femm_problem.define_block_label(Node(31, 0).rotate_about(n0, 80, True), copper_An)
    femm_problem.define_block_label(Node(31, 0).rotate_about(n0, 70, True), copper_Bp)
    femm_problem.define_block_label(Node(31, 0).rotate_about(n0, 50, True), copper_Bn)
    femm_problem.define_block_label(Node(31, 0).rotate_about(n0, 40, True), copper_Cp)
    femm_problem.define_block_label(Node(31, 0).rotate_about(n0, 20, True), copper_Cn)
    femm_problem.define_block_label(Node(31, 0).rotate_about(n0, 10, True), copper_Ap)

    # Add block labels to the rotor
    femm_problem.define_block_label(rot[0], air)


def problem_definition(var: VariableParameters):
    problem = FemmProblem(out_file=os.path.join(folder_path, f'temp_{var.fold}/{var.out}{var.counter}.csv'))
    variables = VariableParameters(var.fold, var.out, var.counter, var.JAp, var.JAn, var.JBp, var.JBn, var.JCp, var.JCn,
                                   var.ang_co, var.deg_co, var.bd, var.bw, var.bh, var.bg)

    problem.magnetic_problem(0, LengthUnit.MILLIMETERS, "planar", depth=40)

    stator_geometry(problem)
    rot = rotor_geometry(problem, variables)
    add_boundaries(problem)
    add_materials(problem, variables, rot)

    problem.make_analysis(os.path.join(folder_path, f'temp_{var.fold}/{var.out}{var.counter}'))

    problem.write(os.path.join(folder_path, f'temp_{var.fold}/{var.out}{var.counter}.lua'))


def run_model(var: VariableParameters):
    problem_definition(var)

    femm = Executor()
    lua_file = os.path.join(folder_path, f'temp_{var.fold}/{var.out}{var.counter}.lua')
    femm.run(lua_file)

# if __name__ == '__main__':
#     run_model()
