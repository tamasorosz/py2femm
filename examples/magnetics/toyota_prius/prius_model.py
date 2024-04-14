import dataclasses
import math
import os
from copy import copy

from src.executor import Executor
from src.femm_problem import FemmProblem
from src.general import LengthUnit
from src.geometry import Node, Geometry, Line, CircleArc, Sector

ORIGIN = Node(0.0, 0.0)

# Geometry parameters - Constants
Dso = 269.0  # Stator outer diameter [mm]
Dsi = 161.93  # Stator inner diameter [mm]
Dro = 160.47  # Rotor outer diameter [mm]
airgap = (Dsi - Dro) / 2

Dso = 269.0  # Stator outer diameter [mm]
Dsi = 161.93  # Stator inner diameter [mm]

Dro = 160.47  # Rotor outer diameter [mm]
Dri = 111.0  # Rotor inner diameter [mm]
airgap = (Dsi - Dro) / 2

slheight = 7.7  # Slot height from rotor inner diameter apex point [mm]
mangle = 145.0  # Magnet angle [°]
mheight = 6.5  # Magnet height [mm]
mwidth = 18.9  # Magnet width [mm]

aslheight = 3.0  # Flux barrier geometry [mm]
earheight = 2.1  # Flux barrier geometry [mm]
earlenght1x = 2.1  # Flux barrier geometry [mm]
earlenght2x = 1.90  # Flux barrier geometry [mm]
earlenght2y = 2.35  # Flux barrier geometry [mm]
earlenght3y = 1.5  # Flux barrier geometry [mm]
earlenght4 = 2.2  # Flux barrier geometry [mm]


@dataclasses.dataclass
class VariableParams:
    prob2x = 0.0
    prob2y = 0.0
    prob3x = 0.0
    prob3y = 0.0
    prob4x = 0.0
    prob4y = 0.0
    prob5x = 0.0
    prob5y = 0.0

def stator():
    # stator outline
    stator_geo = Geometry()

    dsil = Node(Dso / 2, 0.0).rotate(112.5, degrees=True)
    dsir = Node(Dso / 2, 0.0).rotate(67.5, degrees=True)

    stator_geo.add_arc(CircleArc(dsir, ORIGIN, dsil))

    dsol = Node(Dsi / 2, 0.0).rotate(112.5, degrees=True)
    dsor = Node(Dsi / 2, 0.0).rotate(67.5, degrees=True)

    stator_geo.add_arc(CircleArc(dsor, ORIGIN, dsol))

    stator_geo.add_line(Line(dsil, dsol))
    stator_geo.add_line(Line(dsir, dsor))

    agsl = Node(Dsi / 2 - airgap / 3, 0.0).rotate(112.5, degrees=True)
    agsr = Node(Dsi / 2 - airgap / 3, 0.0).rotate(67.5, degrees=True)

    stator_geo.add_arc(CircleArc(agsr, ORIGIN, agsl))

    stator_geo.add_line(Line(dsol, agsl))
    stator_geo.add_line(Line(dsor, agsr))

    # slot geometry
    slot = Geometry()
    slot.import_dxf("resources/prius_slot_pyleecan.dxf")

    stator_geo.merge_geometry(slot)

    return stator_geo


def rotor_geometry(var_params:VariableParams):


    rotor_geo = Geometry()

    dril = Node(Dri / 2, 0.0).rotate(112.5, degrees=True)
    drir = Node(Dri / 2, 0.0).rotate(67.5, degrees=True)

    rotor_geo.add_arc(CircleArc(drir, ORIGIN, dril))

    drol = Node(Dro / 2, 0.0).rotate(112.5, degrees=True)
    dror = Node(Dro / 2, 0.0).rotate(67.5, degrees=True)

    rotor_geo.add_arc(CircleArc(dror, ORIGIN, drol))

    rotor_geo.add_line(Line(dril, drol))
    rotor_geo.add_line(Line(drir, dror))

    agrl = Node(Dro / 2 + airgap / 3, 0.0).rotate(112.5, degrees=True)
    agrr = Node(Dro / 2 + airgap / 3, 0.0).rotate(67.5, degrees=True)

    rotor_geo.add_arc(CircleArc(agrr, ORIGIN, agrl))

    rotor_geo.add_line(Line(drol, agrl))
    rotor_geo.add_line(Line(dror, agrr))

    # Rotor slot
    rotor_slot = Geometry()
    temp1 = math.cos(math.radians((180 - mangle) / 2)) * mheight

    sorigin = Node(0.0, Dri / 2 + slheight + temp1)

    pmb1 = Node(0.0, sorigin.y - mheight)
    pmb2 = Node(-mwidth, pmb1.y)
    pmb3 = Node(-mwidth, sorigin.y)

    rotor_slot.add_line(Line(sorigin, pmb1))
    rotor_slot.add_line(Line(pmb2, pmb1))
    rotor_slot.add_line(Line(pmb2, pmb3))
    rotor_slot.add_line(Line(sorigin, pmb3))

    temp2 = math.tan(math.radians((180 - mangle) / 2)) * (mheight - aslheight)

    apmb1 = Node(0.0, sorigin.y - mheight + aslheight)
    apmb2 = Node(temp2, apmb1.y)

    rotor_slot.add_line(Line(apmb1, apmb2))

    ear1 = Node(pmb2.x, pmb2.y + earheight)
    ear2 = Node(ear1.x - earlenght1x, ear1.y)
    ear3 = Node(ear2.x - earlenght2x, ear2.y + earlenght2y)
    ear4 = Node(ear3.x, ear3.y + earlenght3y)
    remy = mheight - earheight - earlenght2y - earlenght3y
    remx = math.sqrt((earlenght4 ** 2) - (remy ** 2))
    ear5 = Node(ear4.x + remx, ear4.y + remy)

    ear2.x = ear2.x + var_params.prob2x
    ear2.y = ear2.y + var_params.prob2y
    ear3.x = ear3.x + var_params.prob3x
    ear3.y = ear3.y + var_params.prob3y
    ear4.x = ear4.x + var_params.prob4x
    ear4.y = ear4.y + var_params.prob4y
    ear5.x = ear5.x + var_params.prob5x
    ear5.y = ear5.y + var_params.prob5y

    rotor_slot.add_line(Line(ear1, ear2))
    rotor_slot.add_line(Line(ear3, ear2))
    rotor_slot.add_line(Line(ear3, ear4))
    rotor_slot.add_line(Line(ear5, ear4))
    rotor_slot.add_line(Line(ear5, pmb3))

    rotor_slot.rotate_about(Node(sorigin.x, sorigin.y), -(180 - mangle) / 2, degrees=True)

    second_magnet = rotor_slot.duplicate()
    second_magnet.mirror(0)
    rotor_geo.merge_geometry(rotor_slot)
    rotor_geo.merge_geometry(second_magnet)
    return rotor_geo


if __name__ == '__main__':
    problem = FemmProblem(out_file="../prius.csv")
    problem.magnetic_problem(50, LengthUnit.MILLIMETERS, "planar")

    variables = VariableParams()

    geo = stator()
    rotor = rotor_geometry(variables)
    geo.merge_geometry(rotor)

    problem.create_geometry(geo)
    problem.write("prius.lua")

    femm = Executor()
    current_dir = os.getcwd()
    lua_file = current_dir + "/prius.lua"
    femm.run(lua_file)
