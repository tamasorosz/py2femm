import os

from src.magnetics import MagneticMaterial, MagneticDirichlet, MagneticVolumeIntegral
from src.femm_problem import FemmProblem
from src.general import LengthUnit
from src.geometry import Geometry, Line, Node
from src.executor import Executor


def turn(radius, z0, w, h):
    a = Node(radius - w / 2, z0)
    b = Node(radius + w / 2, z0)
    c = Node(radius + w / 2, z0 + h)
    d = Node(radius - w / 2, z0 + h)

    l1 = Line(a, b)
    l2 = Line(b, c)
    l3 = Line(c, d)
    l4 = Line(d, a)

    return [a, b, c, d], [l1, l2, l3, l4]


def solenoid(n, w, h, radius, gap):
    """
    :param n:  number of the turns
    :param w:  width of a single turn
    :param h:  height of a turn
    :param radius: the mean radius of the turn
    :return: the inductance of the coil
    """

    problem = FemmProblem(out_file="../solenoid.csv")
    problem.magnetic_problem(0, LengthUnit.CENTIMETERS, "axi")

    geo = Geometry()

    z0 = -(h + gap) * n / 2
    for i in range(n):
        nodes, lines = turn(radius, z0, w, h)

        geo.nodes += nodes
        geo.lines += lines

        z0 += gap + h

    # set boundary
    z = (h + gap) * n
    a = Node(0, -z)
    b = Node(10 * radius, -z)
    c = Node(10 * radius, z)
    d = Node(0, z)

    l1 = Line(a, b)
    l2 = Line(b, c)
    l3 = Line(c, d)
    l4 = Line(d, a)

    geo.nodes += [a, b, c, d]
    geo.lines += [l1, l2, l3, l4]

    problem.create_geometry(geo)

    # Boundary conditions
    a0 = MagneticDirichlet(name="a0", a_0=0, a_1=0, a_2=0, phi=0)
    problem.add_boundary(a0)
    problem.set_boundary_definition_segment(l1.selection_point(), a0)
    problem.set_boundary_definition_segment(l2.selection_point(), a0)
    problem.set_boundary_definition_segment(l3.selection_point(), a0)
    problem.set_boundary_definition_segment(l4.selection_point(), a0)

    # Materials
    copper = MagneticMaterial(material_name="copper", J=1 / (w * h), Sigma=58.0)
    air = MagneticMaterial(material_name="air")

    problem.add_material(copper)
    problem.add_material(air)

    air_block = Node(radius / 4.0, 0.0)
    problem.define_block_label(air_block, air)

    # turns
    z0 = -(h + gap) * n / 2 + h / 2
    for i in range(n):
        problem.define_block_label(Node(radius, z0), copper)
        z0 += gap + h

    problem.make_analysis('solenoid')

    # the goal in this task is to calculate the point values of the inductance in a 5x5 cm squared region
    for i in range(11):
        for j in range(11):
            problem.get_point_values(Node(0.5 * i, 0.5 * j))

    z0 = -(h + gap) * n / 2

    problem.get_integral_values([Node(radius, z0)], save_image=True, variable_name=MagneticVolumeIntegral.A)

    # nem működik amíg nincs eredmény
    #problem.get_nr_nodes()
    #problem.get_nr_elements()
    #problem.get_nodal_coordinate(1)
    #problem.get_nodal_coordinate(2)
    #problem.get_element(3)

    # post-processing operations
    problem.get_back_fem_results()

    problem.write("solenoid.lua")

    return problem


if __name__ == '__main__':
    problem = solenoid(2, 2, 2, 6, 1)

    femm = Executor()
    current_dir = os.getcwd()
    lua_file = current_dir + "/solenoid.lua"
    femm.run(lua_file)

    problem.post_process_mesh_data()
    k_nn = problem.calc_stiffness_matrix()

    import matplotlib.pyplot as plt
    import numpy as np

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = np.arange(k_nn.shape[0])
    y = np.arange(k_nn.shape[1])
    x, y = np.meshgrid(x, y)
    z = k_nn[x, y]

    surface = ax.plot_surface(x, y, z, cmap='viridis')
    fig.colorbar(surface, ax=ax, shrink=0.5, aspect=5)
    ax.set_title('Surface Plot of Global Stiffness Matrix K_glb')
    ax.set_xlabel('Node Index')
    ax.set_ylabel('Node Index')
    ax.set_zlabel('Value')

    plt.show()