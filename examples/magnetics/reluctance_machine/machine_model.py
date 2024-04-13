import math
import os

from src.executor import Executor
from src.femm_problem import FemmProblem
from src.general import LengthUnit
from src.geometry import Node, Geometry, Line, CircleArc
from dataclasses import dataclass


def pol2cart(rho, phi):
    """Convert polar coordinates to cartesian."""
    x = rho * math.cos(math.radians(phi))
    y = rho * math.sin(math.radians(phi))
    result = Node(round(x, 4), round(y, 4))
    return result


@dataclass
class MachineModel:
    z: float = 1.0  # some parameter
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
    #
    # cutoff = Geometry()
    #
    # # Outer cutoff parameters, check rotor_notes.pdf
    # acol = CircleArc2(self.col_s, self.col_e, self.deg_coo)
    # acor = CircleArc2(self.cor_e, self.cor_s, self.deg_coo)
    #
    # # Inner cutoff parameters, check rotor_notes.pdf
    # coi_m = self.coi_m.rotate_about(self.n0, math.radians(-45))
    #
    # acoil = CircleArc2(self.coi_s, coi_m, self.deg_coi)
    # acoir = CircleArc2(coi_m, self.coi_e, self.deg_coi)
    #
    # cutoff.nodes += [self.col_e, self.cor_e, self.coi_s, self.coi_e, coi_m]
    #
    # cutoff.circle_arcs2 += [acol, acor, acoil, acoir]

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
