import math
import os
from dataclasses import dataclass

from src.executor import Executor
from src.femm_problem import FemmProblem
from src.general import LengthUnit
from src.geometry import Geometry, Node, Sector, CircleArc, Line
from src.magnetics import MagneticDirichlet, MagneticPeriodicAirgap, MagneticPeriodic, MagneticBoundaryModification, \
    MagneticMaterial, LamType, MagneticVolumeIntegral

current_file_path = os.path.abspath(__file__)
folder_path = os.path.dirname(current_file_path)

n0 = Node(0, 0)


class VariableParameters:

    def __init__(self, fold, out, counter, JAp, JAn, JBp, JBn, JCp, JCn, ang_co, deg_co, bd, bw, bh, bg, ia, mh,
                 ang_m, ang_mp, deg_m, deg_mp):
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

        self.ia = ia

        self.ang_m = ang_m
        self.ang_mp = ang_mp
        self.deg_m = deg_m/2
        self.deg_mp = deg_mp/2

        self.mh = mh


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

    # rot_arc_l = CircleArc(co_e, n0, co_l)
    # rot_arc_r = CircleArc(co_r, n0, co_s)
    #
    # rotor_geo.add_arc(rot_arc_l)
    # rotor_geo.add_arc(rot_arc_r)

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

    rot_bound1_l = encl_l.selection_point()
    rot_bound1_r = encl_r.selection_point()
    rot_bound2_l = sbl_l.selection_point()
    rot_bound2_r = sbl_r.selection_point()
    rot_bound_arc1 = enc_arc_0.selection_point()
    rot_bound_arc2 = sb_arc.selection_point()

    # rotor_geo.add_node(rot_bound1_l)
    # rotor_geo.add_node(rot_bound1_r)
    # rotor_geo.add_node(rot_bound2_l)
    # rotor_geo.add_node(rot_bound2_r)
    # rotor_geo.add_node(rot_bound_arc1)
    # rotor_geo.add_node(rot_bound_arc2)

    # LEFT ROTOR MAGNET POCKET-----------------------------------------------------------------------------------------
    nmpbase_lo = Node(22, 0).rotate_about(n0, 67.5+var.deg_mp, True)
    nmpbase_lu = Node(22 - var.mh, 0).rotate_about(n0, 67.5+var.deg_mp, True)

    nmp_llo = nmpbase_lo.rotate_about(n0, var.ang_mp/2, True)
    nmp_rlo = nmpbase_lo.rotate_about(n0, -var.ang_mp/2, True)
    nmp_llu = nmpbase_lu.rotate_about(n0, var.ang_mp/2, True)
    nmp_rlu = nmpbase_lu.rotate_about(n0, -var.ang_mp/2, True)

    rotor_geo.add_node(nmp_llo)
    rotor_geo.add_node(nmp_rlo)
    rotor_geo.add_node(nmp_llu)
    rotor_geo.add_node(nmp_rlu)

    lm_ll = Line(nmp_llo, nmp_llu)
    lm_lr = Line(nmp_rlo, nmp_rlu)

    rotor_geo.add_line(lm_ll)
    rotor_geo.add_line(lm_lr)

    am_lu = CircleArc(nmp_rlu, n0, nmp_llu)

    rotor_geo.add_arc(am_lu)

    rot_arc_ll = CircleArc(nmp_llo, n0, co_l)
    rot_arc_lr = CircleArc(co_e, n0, nmp_rlo)
    rotor_geo.add_arc(rot_arc_ll)
    rotor_geo.add_arc(rot_arc_lr)

    # LEFT ROTOR MAGNET------------------------------------------------------------------------------------------------
    nmbase_lo = Node(22, 0).rotate_about(n0, 67.5+var.deg_m, True)
    nmbase_lu = Node(22 - var.mh, 0).rotate_about(n0, 67.5+var.deg_m, True)

    nm_llo = nmbase_lo.rotate_about(n0, var.ang_m/2, True)
    nm_rlo = nmbase_lo.rotate_about(n0, -var.ang_m/2, True)
    nm_llu = nmbase_lu.rotate_about(n0, var.ang_m/2, True)
    nm_rlu = nmbase_lu.rotate_about(n0, -var.ang_m/2, True)

    rotor_geo.add_node(nm_llo)
    rotor_geo.add_node(nm_rlo)
    rotor_geo.add_node(nm_llu)
    rotor_geo.add_node(nm_rlu)

    lm_ll = Line(nm_llo, nm_llu)
    lm_lr = Line(nm_rlo, nm_rlu)

    rotor_geo.add_line(lm_ll)
    rotor_geo.add_line(lm_lr)

    # am_lu = CircleArc(nm_rlu, n0, nm_llu)

    # rotor_geo.add_arc(am_lu)

    lab_mag_l = Line(lm_ll.selection_point(), lm_lr.selection_point()).selection_point()

    rot_arc_lc = CircleArc(nm_rlo, n0, nm_llo)

    rotor_geo.add_arc(rot_arc_lc)

    # RIGHT ROTOR MAGNET POCKET-----------------------------------------------------------------------------------------
    nmpbase_ro = Node(22, 0).rotate_about(n0, 22.5+var.deg_mp, True)
    nmpbase_ru = Node(22 - var.mh, 0).rotate_about(n0, 22.5+var.deg_mp, True)

    nmp_lro = nmpbase_ro.rotate_about(n0, var.ang_mp/2, True)
    nmp_rro = nmpbase_ro.rotate_about(n0, -var.ang_mp/2, True)
    nmp_lru = nmpbase_ru.rotate_about(n0, var.ang_mp/2, True)
    nmp_rru = nmpbase_ru.rotate_about(n0, -var.ang_mp/2, True)

    rotor_geo.add_node(nmp_lro)
    rotor_geo.add_node(nmp_rro)
    rotor_geo.add_node(nmp_lru)
    rotor_geo.add_node(nmp_rru)

    lm_rl = Line(nmp_lro, nmp_lru)
    lm_rr = Line(nmp_rro, nmp_rru)

    rotor_geo.add_line(lm_rl)
    rotor_geo.add_line(lm_rr)

    am_ru = CircleArc(nmp_rru, n0, nmp_lru)

    rotor_geo.add_arc(am_ru)

    rot_arc_rl = CircleArc(co_r, n0, nmp_rro)
    rot_arc_rr = CircleArc(nmp_lro, n0, co_s)
    rotor_geo.add_arc(rot_arc_rl)
    rotor_geo.add_arc(rot_arc_rr)

    # RIGHT ROTOR MAGNET------------------------------------------------------------------------------------------------
    nmbase_ro = Node(22, 0).rotate_about(n0, 22.5+var.deg_m, True)
    nmbase_ru = Node(22 - var.mh, 0).rotate_about(n0, 22.5+var.deg_m, True)

    nm_lro = nmbase_ro.rotate_about(n0, var.ang_m/2, True)
    nm_rro = nmbase_ro.rotate_about(n0, -var.ang_m/2, True)
    nm_lru = nmbase_ru.rotate_about(n0, var.ang_m/2, True)
    nm_rru = nmbase_ru.rotate_about(n0, -var.ang_m/2, True)

    rotor_geo.add_node(nm_lro)
    rotor_geo.add_node(nm_rro)
    rotor_geo.add_node(nm_lru)
    rotor_geo.add_node(nm_rru)

    lm_rl = Line(nm_lro, nm_lru)
    lm_rr = Line(nm_rro, nm_rru)

    rotor_geo.add_line(lm_rl)
    rotor_geo.add_line(lm_rr)

    rot_arc_rc = CircleArc(nm_rro, n0, nm_lro)

    rotor_geo.add_arc(rot_arc_rc)

    # am_ru = CircleArc(nm_rru, n0, nm_lru)
    #
    # rotor_geo.add_arc(am_ru)

    lab_mag_r = Line(lm_rl.selection_point(), lm_rr.selection_point()).selection_point()

    femm_problem.create_geometry(rotor_geo)

    return ib_mp1, ib_mp2, ib_mp3, ib_mp4, rot_bound1_l, rot_bound1_r, rot_bound2_l, rot_bound2_r, rot_bound_arc1, \
           rot_bound_arc2, lab_mag_l, lab_mag_r


def add_boundaries(femm_problem: FemmProblem, var: VariableParameters, rot: rotor_geometry):
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
    pbca = MagneticBoundaryModification(pbca.name, pbca.boundary_format, propnum=10, value=var.ia)

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

    # Add boundary conditions to rotor segments
    femm_problem.set_boundary_definition_segment(rot[4], pbc1)
    femm_problem.set_boundary_definition_segment(rot[5], pbc1)
    femm_problem.set_boundary_definition_segment(rot[6], pbc2)
    femm_problem.set_boundary_definition_segment(rot[7], pbc2)

    # Add boundary conditions to rotor arcs
    femm_problem.set_boundary_definition_arc(rot[8], a0)
    femm_problem.set_boundary_definition_arc(rot[9], pbca)


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
    FeSi65 = MagneticMaterial(material_name="FeSi65", Sigma=5.8, Lam_d=0, lam_fill=1)

    # Add wire material, air and steel material.
    femm_problem.add_material(copper_Ap)
    femm_problem.add_material(copper_An)
    femm_problem.add_material(copper_Bp)
    femm_problem.add_material(copper_Bn)
    femm_problem.add_material(copper_Cp)
    femm_problem.add_material(copper_Cn)
    femm_problem.add_material(air)
    femm_problem.add_material(steel)
    femm_problem.add_material(FeSi65)

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

    femm_problem.add_bh_curve(material_name="FeSi65",
                              data_b=[0, 0.358294627, 0.478028092, 0.563148872, 0.629244556, 0.683285138, 0.728997037,
                                      0.768607936, 0.803556282, 0.834825031, 0.863115728, 0.888946635, 0.912711487,
                                      0.934716448, 0.955204299, 1.030452669, 1.086202243, 1.130688402, 1.167706237,
                                      1.199406524, 1.227126836, 1.251755988, 1.273914738, 1.294053804, 1.3125108,
                                      1.329545176, 1.34536063, 1.360120017, 1.373955589, 1.402248493, 1.425268547,
                                      1.443943891, 1.459657021, 1.473220258, 1.485151723, 1.495802219, 1.505420324,
                                      1.514188618, 1.522245155, 1.529696862, 1.536628245, 1.54310725, 1.549189325,
                                      1.554920311, 1.560338538, 1.565476384, 1.570361444, 1.575017432, 1.579464871,
                                      1.583721646, 1.587803435, 1.591724059, 1.595495761, 1.599129443, 1.60263485,
                                      1.606020731, 1.609294969, 1.612464692],
                              data_h=[0, 235.7142857, 371.4285714, 507.1428571, 642.8571429, 778.5714286, 914.2857143,
                                      1050, 1185.714286, 1321.428571, 1457.142857, 1592.857143, 1728.571429,
                                      1864.285714, 2000, 2571.428571, 3142.857143, 3714.285714, 4285.714286,
                                      4857.142857, 5428.571429, 6000, 6571.428571, 7142.857143, 7714.285714,
                                      8285.714286, 8857.142857, 9428.57429, 10000, 11379.31034, 12758.62069,
                                      14137.93103, 15517.24138, 16896.55172, 18275.86207, 19655.17241, 21034.48276,
                                      22413.7931, 23793.10345, 25172.41379, 26551.72414, 27931.03448, 29310.34483,
                                      30689.65517, 32068.96552, 33448.27586, 34827.58621, 6206.89655, 37586.2069,
                                      38965.51724, 40344.82759, 41724.13793, 43103.44828, 44482.75862, 45862.06897,
                                      47241.37931, 48620.68966, 50000])

    ferrite_left = MagneticMaterial(material_name="ml", H_c=200106)
    ferrite_right = MagneticMaterial(material_name="mr", H_c=200106)

    ferrite_left.remanence_angle = 247.5 + var.deg_m
    ferrite_right.remanence_angle = 22.5 + var.deg_m

    femm_problem.add_material(ferrite_left)
    femm_problem.add_material(ferrite_right)

    femm_problem.add_bh_curve(material_name="ml",
                              data_b=[0.000000, 0.066000, 0.131390, 0.144000, 0.153280, 0.162400, 0.171530,
                                      0.211680, 0.273720, 0.386860],
                              data_h=[0.000000, 1160.000000, 2323.660000, 3490.000000, 6000.000000, 11630.000000,
                                      18613.200000, 51192.200000, 102376.000000, 200106.000000])

    femm_problem.add_bh_curve(material_name="mr",
                              data_b=[0.000000, 0.066000, 0.131390, 0.144000, 0.153280, 0.162400, 0.171530,
                                      0.211680, 0.273720, 0.386860],
                              data_h=[0.000000, 1160.000000, 2323.660000, 3490.000000, 6000.000000, 11630.000000,
                                      18613.200000, 51192.200000, 102376.000000, 200106.000000])

    # Add block labels to the stator
    femm_problem.define_block_label(Node(17, 17), air)

    femm_problem.define_block_label(Node(28.00, 28.00), steel)

    femm_problem.define_block_label(Node(31, 0).rotate_about(n0, 80, True), copper_An)
    femm_problem.define_block_label(Node(31, 0).rotate_about(n0, 70, True), copper_Bp)
    femm_problem.define_block_label(Node(31, 0).rotate_about(n0, 50, True), copper_Bn)
    femm_problem.define_block_label(Node(31, 0).rotate_about(n0, 40, True), copper_Cp)
    femm_problem.define_block_label(Node(31, 0).rotate_about(n0, 20, True), copper_Cn)
    femm_problem.define_block_label(Node(31, 0).rotate_about(n0, 10, True), copper_Ap)

    # Add block labels to the rotor
    femm_problem.define_block_label(rot[0], air)
    femm_problem.define_block_label(rot[1], air)
    femm_problem.define_block_label(rot[2], air)
    femm_problem.define_block_label(rot[3], air)

    femm_problem.define_block_label(Node(22.05, 0.00).rotate_about(n0, 45, True), air)
    femm_problem.define_block_label(Node(7, 0.00).rotate_about(n0, 45, True), FeSi65)

    femm_problem.define_block_label(rot[10], ferrite_left)
    femm_problem.define_block_label(rot[11], ferrite_right)


def problem_definition(var: VariableParameters):
    problem = FemmProblem(out_file=os.path.join(folder_path, f'temp_{var.fold}/{var.out}{var.counter}.csv'))
    variables = VariableParameters(var.fold, var.out, var.counter, var.JAp, var.JAn, var.JBp, var.JBn, var.JCp, var.JCn,
                                   var.ang_co, var.deg_co, var.bd, var.bw, var.bh, var.bg, var.ia, var.mh, var.ang_m,
                                   var.ang_mp, var.deg_m, var.deg_mp)

    problem.magnetic_problem(0, LengthUnit.MILLIMETERS, "planar", depth=40)

    stator_geometry(problem)
    rot = rotor_geometry(problem, variables)
    add_boundaries(problem, variables, rot)
    add_materials(problem, variables, rot)

    problem.make_analysis(os.path.join(folder_path, f'temp_{var.fold}/{var.out}{var.counter}'))

    problem.get_integral_values(label_list=[list(rot)[0], list(rot)[1], list(rot)[2], list(rot)[3], list(rot)[10],
                                            list(rot)[11], Node(5, 5)],
                                save_image=False,
                                variable_name=MagneticVolumeIntegral.wTorque)

    problem.write(os.path.join(folder_path, f'temp_{var.fold}/{var.out}{var.counter}.lua'))


def run_model(var: VariableParameters):
    problem_definition(var)

    femm = Executor()
    lua_file = os.path.join(folder_path, f'temp_{var.fold}/{var.out}{var.counter}.lua')
    femm.run(lua_file)