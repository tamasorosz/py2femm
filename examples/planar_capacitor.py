from src.electrostatics import ElectrostaticMaterial, ElectrostaticSurfaceCharge, ElectrostaticFixedVoltage
from src.writer import FemmWriter
from src.general import FemmFields, LengthUnit
from src.geometry import Geometry, Node, Line, CircleArc


def create_geometry(width, thickness, d):
    # problem definition
    planar_problem = FemmWriter()
    planar_problem.field = FemmFields.ELECTROSTATIC
    planar_problem.init_problem("electrostatic_data.csv")
    planar_problem.electrostatic_problem(LengthUnit.METERS, "planar")

    # geometry definition
    geo = Geometry()

    n1 = Node(x=-width / 2, y=d / 2)
    n2 = Node(x=-width / 2, y=d / 2 + thickness)
    n3 = Node(x=width / 2, y=d / 2 + thickness)
    n4 = Node(x=width / 2, y=d / 2)

    n5 = Node(x=-width / 2, y=-d / 2)
    n6 = Node(x=-width / 2, y=-d / 2 - thickness)
    n7 = Node(x=width / 2, y=-d / 2 - thickness)
    n8 = Node(x=width / 2, y=-d / 2)

    l1 = Line(n1, n2)
    l2 = Line(n2, n3)
    l3 = Line(n3, n4)
    l4 = Line(n4, n1)

    l5 = Line(n5, n6)
    l6 = Line(n6, n7)
    l7 = Line(n7, n8)
    l8 = Line(n8, n5)

    l9 = Line(n1, n5)
    l10 = Line(n8, n4)

    center = Node(x=0, y=0)
    out1 = Node(x=0.0, y=0.3)
    out2 = Node(x=-0.3, y=0.0)
    out3 = Node(x=0.0, y=-0.3)
    out4 = Node(x=0.3, y=0.0)

    arc1 = CircleArc(out1, center, out2)
    arc2 = CircleArc(out2, center, out3)
    arc3 = CircleArc(out3, center, out4)
    arc4 = CircleArc(out4, center, out1)

    geo.nodes = [n1, n2, n3, n4, n5, n6, n7, n8, out1, out2, out3, out4]
    geo.lines = [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10]
    geo.circle_arcs = [arc1, arc2, arc3, arc4]

    planar_problem.create_geometry(geo)

    # materials
    epoxy = ElectrostaticMaterial(material_name="epoxy", ex=3.7, ey=3.7, qv=0.0)
    air = ElectrostaticMaterial(material_name="air", ex=1.0, ey=1.0, qv=0.0)
    metal = ElectrostaticMaterial(material_name="metal", ex=1.0, ey=1.0, qv=0.0)

    planar_problem.add_material(epoxy)
    planar_problem.add_material(air)
    planar_problem.add_material(metal)

    planar_problem.define_block_label(0.0, 0.0, epoxy)
    planar_problem.define_block_label(0.0, 0.2, air)

    planar_problem.define_block_label(0.0, d / 2 + thickness / 2, metal)
    planar_problem.define_block_label(0.0, - d / 2 - thickness / 2, metal)

    # Boundary conditions
    v0 = ElectrostaticFixedVoltage("U0", 10.0)
    gnd = ElectrostaticFixedVoltage("GND", 0.0)
    neumann = ElectrostaticSurfaceCharge('outline', 0.0)
    planar_problem.add_boundary(neumann)
    planar_problem.add_boundary(gnd)
    planar_problem.add_boundary(v0)

    # voltage electrode
    planar_problem.set_boundary_definition(l1.selection_point(), v0)
    planar_problem.set_boundary_definition(l2.selection_point(), v0)
    planar_problem.set_boundary_definition(l3.selection_point(), v0)
    planar_problem.set_boundary_definition(l4.selection_point(), v0)

    # gnd electrode
    planar_problem.set_boundary_definition(l5.selection_point(), gnd)
    planar_problem.set_boundary_definition(l6.selection_point(), gnd)
    planar_problem.set_boundary_definition(l7.selection_point(), gnd)
    planar_problem.set_boundary_definition(l8.selection_point(), gnd)

    # outer surface of the geometry
    planar_problem.set_boundary_definition(arc1.selection_point(),  neumann)
    planar_problem.set_boundary_definition(arc2.selection_point(), neumann)
    planar_problem.set_boundary_definition(arc3.selection_point(), neumann)
    planar_problem.set_boundary_definition(arc4.selection_point(), neumann)

    planar_problem.write("planar.lua")


if __name__ == '__main__':
    # create geometry
    width = 0.2  # m
    thickness = 0.005  # m
    d = 0.01  # m

    create_geometry(width, thickness, d)
