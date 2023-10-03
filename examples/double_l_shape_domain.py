from src.electrostatics import ElectrostaticMaterial, ElectrostaticSurfaceCharge, ElectrostaticFixedVoltage
from src.femm_problem import FemmProblem
from src.general import FemmFields, LengthUnit
from src.geometry import Geometry, Line, CircleArc, Node


def double_l_shape_problem(h, l, eta_1, eta_2):
    planar_problem = FemmProblem(out_file="electrostatic_data.csv")
    planar_problem.electrostatic_problem(LengthUnit.CENTIMETERS, "planar")

    geo = Geometry()

    p_1 = Node(0.0, 0.0)
    p_2 = Node(2.0 * h, 0.0)
    p_3 = Node(2.0 * h, 2.0 * l + eta_1)

    q_1 = Node(0.0, eta_2)
    q_2 = Node(0.0, eta_2 + 2.0 * l + eta_1)
    q_3 = Node(2.0 * h, eta_2 + 2.0 * l + eta_1)



    l1 = Line(q_1, q_2)
    l2 = Line(q_2, q_3)

    l3 = Line(p_1, p_2)
    l4 = Line(p_2, p_3)

    l5 = Line(p_1, q_1)
    l6 = Line(p_3, q_3)

    geo.nodes = [p_1, p_2, p_3, q_1, q_2, q_3]
    geo.lines = [l1, l2, l3, l4, l5, l6]

    planar_problem.create_geometry(geo)

    planar_problem.write("planar.lua")


if __name__ == '__main__':
    H = 0.07112
    L = 0.3556
    eta_1 = 0.2032
    eta_2 = 0.2032

    double_l_shape_problem(H, L, eta_1, eta_2)
