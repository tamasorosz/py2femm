import math
import os

from src.executor import Executor
from src.femm_problem import FemmProblem
from src.general import LengthUnit
from src.geometry import Node, Geometry, Line, CircleArc
from dataclasses import dataclass


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

        geom.nodes = [self.v_0, self.v_1, self.v_2, self.h_0, self.h_1, self.h_2]
        geom.lines = [lv01, lv12, lh01, lh12]
        geom.circle_arcs = [a00, a11, a22]

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

        geom.nodes = [self.tlb1, self.tlb2, self.tlb3, self.tlb4, self.trb1, self.trb2, self.trb3, self.trb4, self.tcb1,
                      self.tcb2]
        geom.lines = [ltl1, ltl2, ltl3, ltr1, ltr2, ltr3, ltc1, ltc2]
        geom.circle_arcs = [at1, at2]

        return geom


if __name__ == '__main__':
    problem = FemmProblem(out_file="../machine.csv")
    problem.magnetic_problem(50, LengthUnit.MILLIMETERS, "planar")

    stator_enc = StatorEnclosingGeometry().create_geometry()
    stator_tooth_base = StatorToothGeometry().create_geometry()

    stator_tooth_base.rotate_about(Node(0.0, 0.0), math.radians(-15))

    geo = stator_tooth_base

    problem.create_geometry(geo)
    problem.write("machine.lua")

    femm = Executor()
    current_dir = os.getcwd()
    lua_file = current_dir + "/machine.lua"
    femm.run(lua_file)
