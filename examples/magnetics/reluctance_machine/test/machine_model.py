import math
import os

from src.executor import Executor
from src.femm_problem import FemmProblem
from src.general import LengthUnit
from src.geometry import Node, Geometry, Line, CircleArc, Sector
from dataclasses import dataclass


def pol2cart(rho, phi):
    """Convert polar coordinates to cartesian."""
    x = rho * math.cos(math.radians(phi))
    y = rho * math.sin(math.radians(phi))
    result = Node(round(x, 4), round(y, 4))
    return result


@dataclass
class MachineModel:
    z: float = .5  # some parameter
    J0 = 20.0
    v1y = 21.0
    h1x = 21.0
    ang_coo = 18.0
    deg_coo = 45.0
    h_coi = 21.0
    ang_coi = 18.0
    deg_coi = 45.0
    ang_mpl = 22.0
    deg_mpl = 67.5
    mphl = z
    ang_mpr = 22.0
    deg_mpr = 22.5
    mphr = z
    ang_ml = 20.0
    deg_ml = 67.5
    ang_mr = 20.0
    deg_mr = 22.5
    mhl = z
    mhr = z
    bhu = 19.0
    bdu = 3.0
    bwu = 2.0
    bho = 13.0
    bdo = 10.0
    bwo = 2.0
    deg_bu = 45.0
    deg_bo = 45.0


@dataclass
class StatorEnclosingGeometry:
    # Dataset to describe the stator ring
    n_0 = Node(0.0, 0.0)
    v_0 = Node(0.0, 22.30)
    v_1 = Node(0.0, 22.50)
    v_2 = Node(0.0, 43.25)
    h_0 = Node(22.30, 0.0)
    h_1 = Node(22.50, 0.0)
    h_2 = Node(43.25, 0.0)

    def create_geometry(self):
        geom = Geometry()

        lv01 = Line(self.v_0, self.v_1)
        lv12 = Line(self.v_1, self.v_2)
        lh01 = Line(self.h_0, self.h_1)
        lh12 = Line(self.h_1, self.h_2)

        a00 = CircleArc(self.h_0, self.n_0, self.v_0)
        a11 = CircleArc(self.h_1, self.n_0, self.v_1)
        a22 = CircleArc(self.h_2, self.n_0, self.v_2)

        geom.add_line(lv01)
        geom.add_line(lv12)
        geom.add_line(lh01)
        geom.add_line(lh12)

        geom.add_arc(a00)
        geom.add_arc(a11)
        geom.add_arc(a22)

        return geom


@dataclass
class StatorToothGeometry:
    n_0 = Node(0.0, 0.0)
    # Tooth Dimensions
    tlb1 = Node(-0.45, 22.4955)
    tlb2 = Node(-0.45, 23.05)
    tlb3 = Node(-3.04, 25.02)
    tlb4 = Node(-5.93, 36.53)

    trb1 = Node(0.4, 22.4955)
    trb2 = Node(0.45, 23.05)
    trb3 = Node(3.04, 25.02)
    trb4 = Node(5.93, 36.53)

    tcb1 = Node(0.00, 25.02)
    tcb2 = Node(0.00, 37.05)

    def create_geometry(self):
        geom = Geometry()

        ltl1 = Line(self.tlb1, self.tlb2)
        ltl2 = Line(self.tlb2, self.tlb3)
        ltl3 = Line(self.tlb3, self.tlb4)
        ltr1 = Line(self.trb1, self.trb2)
        ltr2 = Line(self.trb2, self.trb3)
        ltr3 = Line(self.trb3, self.trb4)

        ltc1 = Line(self.tlb3, self.trb3)
        ltc2 = Line(self.tcb1, self.tcb2)

        at1 = CircleArc(self.trb4, self.n_0, self.tcb2)
        at2 = CircleArc(self.tcb2, self.n_0, self.tlb4)

        geom.add_line(ltl1)
        geom.add_line(ltl2)
        geom.add_line(ltl3)
        geom.add_line(ltr1)
        geom.add_line(ltr2)
        geom.add_line(ltr3)

        geom.add_line(ltc1)
        geom.add_line(ltc2)

        geom.add_arc(at1)
        geom.add_arc(at2)

        return geom


def rotor_geometry(machine: MachineModel):
    # Enclosing dimension of the stator, check stator_nodes.pdf.---------------
    n0 = Node(0.00, 0.00)  # Origin point.
    v0 = Node(0.00, 6.00)
    v1 = Node(0.00, machine.v1y)  # Left airgap node on stator side.
    v2 = Node(0.00, 22.20)  # Optimisation parameter, check rotor_notes.pdf
    h0 = Node(6.00, 0.00)
    h1 = Node(machine.h1x, 0.00)  # Right airgap node on stator side.
    h2 = Node(22.20, 0.00)  # Optimisation parameter, check rotor_notes.pdf

    # outer cutoff parameters
    col_s = v1
    col_e = pol2cart(22.00, 90 - machine.ang_coo / 2.0)

    cor_s = h1
    cor_e = pol2cart(22.00, machine.ang_coo / 2)
    deg_coo = machine.deg_coo

    # Inner cutoff parameters, check rotor_notes.pdf
    coi_m = Node(0.00, machine.h_coi)
    ang_coi = machine.ang_coi
    deg_coi = machine.deg_coi
    coi_s = pol2cart(22.00, 45 + ang_coi / 2)
    coi_e = pol2cart(22.00, 45 - ang_coi / 2)

    # Magnet pocket, check rotor_notes.pdf
    # Left pocket
    ang_mpl = machine.ang_mpl
    deg_mpl = machine.deg_mpl
    mphl = machine.mphl

    mpl2s = pol2cart(22.00, deg_mpl - ang_mpl / 2)
    mpl2e = pol2cart(22.00, deg_mpl + ang_mpl / 2)

    # Right pocket
    ang_mpr = machine.ang_mpr
    deg_mpr = machine.deg_mpr
    mphr = machine.mphr

    mpr2s = pol2cart(22.00, deg_mpr - ang_mpr / 2)
    mpr2e = pol2cart(22.00, deg_mpr + ang_mpr / 2)

    # Magnets, check rotor_notes.pdf
    # Left magnet
    ang_ml = machine.ang_ml
    deg_ml = machine.deg_ml
    mbl = machine.mphl
    mhl = machine.mhl

    ml3s = pol2cart(22.00, deg_ml - ang_ml / 2)
    ml3e = pol2cart(22.00, deg_ml + ang_ml / 2)

    # Right magnet
    ang_mr = machine.ang_mr
    deg_mr = machine.deg_mr
    mbr = machine.mphr
    mhr = machine.mhr

    mr3s = pol2cart(22.00, deg_mr - ang_mr / 2)
    mr3e = pol2cart(22.00, deg_mr + ang_mr / 2)

    # Barrier, check rotor_notes.pdf
    # Top line
    bhu = machine.bhu
    bdu = machine.bdu
    bwu = machine.bwu

    # Bottom line
    bho = machine.bho
    bdo = machine.bdo
    bwo = machine.bwo

    # Arc degree
    deg_bu = machine.deg_bu
    deg_bo = machine.deg_bo

    ####
    # Rotor enclosing
    ###
    rotorenc = Geometry()

    lv01 = Line(v0, v1)
    lv12 = Line(v1, v2)
    lh01 = Line(h0, h1)
    lh12 = Line(h1, h2)

    a00 = CircleArc(h0, n0, v0)
    a22 = CircleArc(h2, n0, v2)

    rotorenc.add_line(lv01)
    rotorenc.add_line(lv12)
    rotorenc.add_line(lh01)
    rotorenc.add_line(lh12)

    rotorenc.add_arc(a00)
    rotorenc.add_arc(a22)

    ###
    # Cutoff geometry
    ###
    cutoff = Geometry()

    # Outer cutoff parameters, check rotor_notes.pdf
    acol = Sector(col_s, col_e, deg_coo)
    acor = Sector(cor_e, cor_s, deg_coo)

    cutoff.add_sector(acol)
    cutoff.add_sector(acor)

    # Inner cutoff parameters, check rotor_notes.pdf
    coi_m = coi_m.rotate_about(n0, math.radians(-45))

    acoil = Sector(coi_s, coi_m, deg_coi)
    acoir = Sector(coi_m, coi_e, deg_coi)

    cutoff.add_sector(acoil)
    cutoff.add_sector(acoir)

    rotorenc.merge_geometry(cutoff)

    ### Magnet
    magnet = Geometry()

    # Left magnet pocket
    mpl1s = pol2cart(22.00 - mphl, deg_mpl - ang_mpl / 2)
    mpl1e = pol2cart(22.00 - mphl, deg_mpl + ang_mpl / 2)

    lmpl1 = Line(mpl1s, mpl2s)
    lmpl2 = Line(mpl1e, mpl2e)

    magnet.add_line(lmpl1)
    magnet.add_line(lmpl2)

    # Right magnet pocket
    mpr1s = pol2cart(22.00 - mphr, deg_mpr - ang_mpr / 2)
    mpr1e = pol2cart(22.00 - mphr, deg_mpr + ang_mpr / 2)

    lmpr1 = Line(mpr1s, mpr2s)
    lmpr2 = Line(mpr1e, mpr2e)

    magnet.add_line(lmpr1)
    magnet.add_line(lmpr2)

    # Left magnet
    ml1s = pol2cart(22.00 - mbl, deg_ml - ang_ml / 2)
    ml1e = pol2cart(22.00 - mbl, deg_ml + ang_ml / 2)
    #
    ml2s = pol2cart(22.00 - mbl + mhl, deg_ml - ang_ml / 2)
    ml2e = pol2cart(22.00 - mbl + mhl, deg_ml + ang_ml / 2)
    #
    lml1 = Line(ml1s, ml2s)
    lml2 = Line(ml1e, ml2e)

    magnet.add_line(lml1)
    magnet.add_line(lml2)

    aml1 = CircleArc(mpl1s, n0, ml1s)
    aml2 = CircleArc(ml1s, n0, ml1e)
    aml3 = CircleArc(ml1e, n0, mpl1e)
    aml4 = CircleArc(ml2s, n0, ml2e)

    magnet.add_line(aml1)
    magnet.add_line(aml2)
    magnet.add_line(aml3)
    magnet.add_line(aml4)

    # Right magnet
    mr1s = pol2cart(22.00 - mbr, deg_mr - ang_mr / 2)
    mr1e = pol2cart(22.00 - mbr, deg_mr + ang_mr / 2)

    mr2s = pol2cart(22.00 - mbr + mhr, deg_mr - ang_mr / 2)
    mr2e = pol2cart(22.00 - mbr + mhr, deg_mr + ang_mr / 2)

    lmr1 = Line(mr1s, mr2s)
    lmr2 = Line(mr1e, mr2e)

    magnet.add_line(lmr1)
    magnet.add_line(lmr2)

    amr1 = CircleArc(mpr1s, n0, mr1s)
    amr2 = CircleArc(mr1s, n0, mr1e)
    amr3 = CircleArc(mr1e, n0, mpr1e)
    amr4 = CircleArc(mr2s, n0, mr2e)

    magnet.add_line(amr1)
    magnet.add_line(amr2)
    magnet.add_line(amr3)
    magnet.add_line(amr4)

    rotorenc.merge_geometry(magnet)

    # barrier

    # BASE
    barrier = Geometry()

    # Top line
    bul1 = Node(-bdu / 2, bhu)
    bul2 = Node(-bdu / 2 - bwu, bhu)

    bur1 = Node(bdu / 2, bhu)
    bur2 = Node(bdu / 2 + bwu, bhu)

    # Bottom line
    bol1 = Node(-bdo / 2, bho)
    bol2 = Node((-bdo / 2) - (math.tan(math.radians(225)) * bwo), bho + bwo)

    bor1 = Node(bdo / 2, bho)
    bor2 = Node((bdo / 2) + (math.tan(math.radians(225)) * bwo), bho + bwo)

    # First rotation
    a = math.radians(-22.5)

    # Top line
    bul1 = bul1.rotate_about(n0, a)
    bul2 = bul2.rotate_about(n0, a)

    bur1 = bur1.rotate_about(n0, a)
    bur2 = bur2.rotate_about(n0, a)

    lul = Line(bul1, bul2)
    lur = Line(bur1, bur2)

    # Bottom line
    bol1 = bol1.rotate_about(n0, a)
    bol2 = bol2.rotate_about(n0, a)

    bor1 = bor1.rotate_about(n0, a)
    bor2 = bor2.rotate_about(n0, a)

    lol = Line(bol1, bol2)
    lor = Line(bor1, bor2)

    abul = Sector(bol2, bul2, deg_bu)
    abur = Sector(bur2, bor2, deg_bu)
    abol = Sector(bol1, bul1, deg_bo)
    abor = Sector(bur1, bor1, deg_bo)

    barrier.add_line(lul)
    barrier.add_line(lur)
    barrier.add_line(lol)
    barrier.add_line(lor)

    barrier.add_sector(abul)
    barrier.add_sector(abur)
    barrier.add_sector(abol)
    barrier.add_sector(abor)

    # Second rotation
    a = math.radians(-45)

    # Top line
    bul1 = bul1.rotate_about(n0, a)
    bul2 = bul2.rotate_about(n0, a)

    bur1 = bur1.rotate_about(n0, a)
    bur2 = bur2.rotate_about(n0, a)

    lul = Line(bul1, bul2)
    lur = Line(bur1, bur2)

    # Bottom line
    bol1 = bol1.rotate_about(n0, a)
    bol2 = bol2.rotate_about(n0, a)

    bor1 = bor1.rotate_about(n0, a)
    bor2 = bor2.rotate_about(n0, a)

    lol = Line(bol1, bol2)
    lor = Line(bor1, bor2)

    barrier.add_line(lul)
    barrier.add_line(lur)
    barrier.add_line(lol)
    barrier.add_line(lor)

    # Arc
    abul = Sector(bol2, bul2, deg_bu)
    abur = Sector(bur2, bor2, deg_bu)
    abol = Sector(bol1, bul1, deg_bo)
    abor = Sector(bur1, bor1, deg_bo)

    barrier.add_sector(abul)
    barrier.add_sector(abur)
    barrier.add_sector(abol)
    barrier.add_sector(abor)

    rotorenc.merge_geometry(barrier)

    ###  supplementary

    supplementary = Geometry()

    aml_gapl = CircleArc(mpl2e, n0, col_e)
    amr_gapr = CircleArc(cor_e, n0, mpr2s)

    aml_gapr = CircleArc(coi_s, n0, mpl2s)
    amr_gapl = CircleArc(mpr2e, n0, coi_e)

    supplementary.add_arc(aml_gapl)
    supplementary.add_arc(amr_gapr)
    supplementary.add_arc(amr_gapr)
    supplementary.add_arc(amr_gapl)

    rotorenc.merge_geometry(supplementary)

    return rotorenc


if __name__ == '__main__':
    problem = FemmProblem(out_file="../machine.csv")
    problem.magnetic_problem(50, LengthUnit.MILLIMETERS, "planar")

    machine = MachineModel()

    rotor = rotor_geometry(machine)

    stator_enc = StatorEnclosingGeometry().create_geometry()
    stator_tooth_base = StatorToothGeometry().create_geometry()

    stator_tooth_base.rotate_about(Node(0.0, 0.0), math.radians(-75))

    geo = stator_tooth_base
    geo.merge_geometry(stator_enc)
    geo.merge_geometry(rotor)

    problem.create_geometry(geo)
    problem.write("machine.lua")

    femm = Executor()
    current_dir = os.getcwd()
    lua_file = current_dir + "/machine.lua"
    femm.run(lua_file)
