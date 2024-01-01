import os

from src.electrostatics import ElectrostaticMaterial, ElectrostaticFixedVoltage
from src.femm_problem import FemmProblem
from src.general import LengthUnit
from src.geometry import Geometry, Line, Node
from src.executor import Executor


def double_l_shape_problem(h, l, delta, voltage=2500.0):
    # problem definition
    planar_problem = FemmProblem(out_file="electrostatic_data.csv")
    planar_problem.electrostatic_problem(LengthUnit.INCHES, "planar")

    # define the geometry
    geo = Geometry()

    r1 = Node(0.0, 0.0)
    r2 = Node(2.0 * h, 0.0)
    r3 = Node(2.0 * h, 2.0 * l + delta)
    r4 = Node(2.0 * h, 2.0 * l + 2.0 * delta)
    r5 = Node(0.0, 2.0 * l + 2.0 * delta)
    r6 = Node(0.0, delta)

    l1 = Line(r1, r2)
    l2 = Line(r2, r3)
    l3 = Line(r3, r4)
    l4 = Line(r4, r5)
    l5 = Line(r5, r6)
    l6 = Line(r6, r1)

    geo.nodes = [r1, r2, r3, r4, r5, r6]
    geo.lines = [l1, l2, l3, l4, l5, l6]

    planar_problem.create_geometry(geo)

    # Material definition
    air = ElectrostaticMaterial(material_name="air", ex=1.0, ey=1.0, qv=0.0)
    planar_problem.add_material(air)

    middle_point = Node((r1.x + r2.x) / 2, (r2.y + r4.y) / 2)
    planar_problem.define_block_label(middle_point, air)

    # boundary definition
    v0 = ElectrostaticFixedVoltage("U0", voltage)
    gnd = ElectrostaticFixedVoltage("GND", 0.0)
    planar_problem.add_boundary(gnd)
    planar_problem.add_boundary(v0)

    # gnd
    planar_problem.set_boundary_definition(l1.selection_point(), gnd)
    planar_problem.set_boundary_definition(l2.selection_point(), gnd)

    # voltage
    planar_problem.set_boundary_definition(l4.selection_point(), v0)
    planar_problem.set_boundary_definition(l5.selection_point(), v0)

    # planar_problem.analyze()
    planar_problem.make_analysis('double_l_shape')
    planar_problem.get_point_values(middle_point)
    planar_problem.write("double_l_shape.lua")

    femm = Executor()
    current_dir = os.getcwd()
    lua_file = current_dir + "/double_l_shape.lua"
    femm.run(lua_file)


if __name__ == '__main__':
    L = 0.280 / 2.
    H = 0.056 / 2.
    delta = 0.08

    H = 0.056 / 2.
    L = 0.084 / 2.

    # L = 0.168 / 2.
    delta = 0.08

    print('Gamma:', L / H)

    double_l_shape_problem(H, L, delta)
    # plot_solutions()
