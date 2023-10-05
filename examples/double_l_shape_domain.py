from src.electrostatics import ElectrostaticMaterial, ElectrostaticSurfaceCharge, ElectrostaticFixedVoltage
from src.femm_problem import FemmProblem
from src.general import FemmFields, LengthUnit
from src.geometry import Geometry, Line, CircleArc, Node

import matplotlib.pyplot as plt


def double_l_shape_problem(h, l, delta, voltage=2500.0):
    # problem definition
    planar_problem = FemmProblem(out_file="electrostatic_data.csv")
    planar_problem.electrostatic_problem(LengthUnit.INCHES, "planar")

    # define the geometry
    geo = Geometry()

    r1 = Node(0.0, 0.0)
    r2 = Node(2.0 * h, 0.0)
    r3 = Node(2.0 * h, 2.0 * l)
    r4 = Node(2.0 * h, 2.0 * l + delta)
    r5 = Node(0.0, 2.0 * l + delta)
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
    planar_problem.define_block_label(Node((r1.x + r2.x) / 2, (r2.y + r4.y) / 2), air)

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

    planar_problem.analyze()
    planar_problem.get_point_values()
    planar_problem.write("planar.lua")


def plot_solutions():
    """
    The calculate
    :return:
    """

    # JSON adatok
    data = {
        "version": [4, 2],
        "axesColl": [
            {
                "name": "XY",
                "type": "XYAxes",
                "isLogX": False,
                "isLogY": False,
                "noRotation": True,
                "calibrationPoints": [
                    {"px": 81.83265582655827, "py": 452.48644986449864, "dx": "0", "dy": "0", "dz": None},
                    {"px": 465.55216802168025, "py": 453.8617886178862, "dx": "8", "dy": "0", "dz": None},
                    {"px": 81.83265582655827, "py": 452.48644986449864, "dx": "0", "dy": "0", "dz": None},
                    {"px": 82.52032520325203, "py": 26.131436314363146, "dx": "8", "dy": "9", "dz": None},
                ],
            }
        ],
        "datasetColl": [
            {
                "name": "Schwarz-Christoffel solution",
                "axesName": "XY",
                "colorRGB": [200, 0, 0, 255],
                "metadataKeys": [],
                "data": [
                    {"x": 126.53116531165313, "y": 41.94783197831978, "value": [0.9318996415770611, 8.666129032258064]},
                    {"x": 177.4186991869919, "y": 360.33875338753387, "value": [1.9928315412186384, 1.94516129032258]},
                    {"x": 224.18021680216802, "y": 433.91937669376694,
                     "value": [2.967741935483871, 0.39193548387096655]},
                ],
                "autoDetectionData": None,
            },
            {
                "name": "Experimental Data",
                "axesName": "XY",
                "colorRGB": [51, 51, 51, 255],
                "metadataKeys": [],
                "data": [
                    {"x": 151.28726287262873, "y": 89.3970189701897, "value": [1.4480286738351256, 7.664516129032258]},
                    {"x": 180.16937669376694, "y": 319.07859078590786,
                     "value": [2.0501792114695343, 2.816129032258064]},
                    {"x": 215.24051490514907, "y": 412.6016260162602,
                     "value": [2.7813620071684593, 0.8419354838709658]},
                    {"x": 270.9417344173442, "y": 449.7357723577236, "value": [3.942652329749105, 0.05806451612903096]},
                    {"x": 321.14159891598916, "y": 451.11111111111114,
                     "value": [4.989247311827957, 0.029032258064514593]},
                    {"x": 371.3414634146342, "y": 451.7987804878049,
                     "value": [6.035842293906811, 0.014516129032257297]},
                ],
                "autoDetectionData": None,
            },
        ],
        "measurementColl": [],
    }

    # Adatok kinyerése
    schwarz_data = data["datasetColl"][0]["data"]
    experimental_data = data["datasetColl"][1]["data"]

    # Schwarz-Christoffel Solution
    schwarz_x_values = [item["value"][0] for item in schwarz_data]
    schwarz_y_values = [item["value"][1] for item in schwarz_data]

    # Experimental Data
    experimental_x_values = [item["value"][0] for item in experimental_data]
    experimental_y_values = [item["value"][1] for item in experimental_data]

    # Diagram kirajzolása
    plt.plot(schwarz_x_values, schwarz_y_values, label="Schwarz-Christoffel solution", color="r")
    plt.plot(experimental_x_values, experimental_y_values, label="Experimental Data", color="b")

    plt.xlabel("L/H ")
    plt.ylabel("Tilting angle of E-field")
    plt.title("Schwarz-Christoffel vs. Experimental Data")
    plt.legend()
    plt.grid(True)

    # Diagram megjelenítése
    plt.show()


if __name__ == '__main__':
    H = 0.07112
    L = 0.3556
    delta = 0.2032

    double_l_shape_problem(H, L, delta)
