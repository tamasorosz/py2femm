import os
from dataclasses import dataclass

from src.executor import Executor
from src.femm_problem import FemmProblem
from src.general import LengthUnit
from src.geometry import Geometry, Node
from src.magnetics import MagneticDirichlet, MagneticPeriodicAirgap, MagneticPeriodic, MagneticBoundaryModification, \
    MagneticMaterial, LamType

current_file_path = os.path.abspath(__file__)
folder_path = os.path.dirname(current_file_path)

n0 = Node(0, 0)


class VariableParameters:

    def __init__(self, fold, out, counter, JAp, JAn, JBp, JBn, JCp, JCn):
        self.fold = fold
        self.out = out
        self.counter = counter

        self.JAp = JAp
        self.JAn = JAn
        self.JBp = JBp
        self.JBn = JBn
        self.JCp = JCp
        self.JCn = JCn


def stator_geometry(femm_problem: FemmProblem):
    # stator geometry imported from a .dxf file with airgap sliding band: https://www.femm.info/wiki/SlidingBand
    stator_geo = Geometry()

    stator_geo.import_dxf("resources/stator.dxf")

    femm_problem.create_geometry(stator_geo)


def rotor_geometry(femm_problem: FemmProblem):
    pass


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


def add_materials(femm_problem: FemmProblem, var: VariableParameters):
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


def problem_definition(var: VariableParameters):
    problem = FemmProblem(out_file=os.path.join(folder_path, f'temp_{var.fold}/{var.out}{var.counter}.csv'))
    variables = VariableParameters(var.fold, var.out, var.counter, var.JAp, var.JAn, var.JBp, var.JBn, var.JCp, var.JCn)

    problem.magnetic_problem(0, LengthUnit.MILLIMETERS, "planar", depth=40)

    stator_geometry(problem)
    add_boundaries(problem)
    add_materials(problem, variables)

    problem.make_analysis(os.path.join(folder_path, f'temp_{var.fold}/{var.out}{var.counter}'))

    problem.write(os.path.join(folder_path, f'temp_{var.fold}/{var.out}{var.counter}.lua'))


def run_model(var: VariableParameters):
    problem_definition(var)

    femm = Executor()
    lua_file = os.path.join(folder_path, f'temp_{var.fold}/{var.out}{var.counter}.lua')
    femm.run(lua_file)


if __name__ == '__main__':
     run_model()
