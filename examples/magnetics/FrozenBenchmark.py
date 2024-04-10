from src.femm_problem import FemmProblem
from src.general import LengthUnit
import os
from src.executor import Executor
from src.magnetics import MagneticMaterial,MagneticDirichlet,MagneticVolumeIntegral,BHCurve, LamType
from src.femm_problem import FemmProblem
from src.general import LengthUnit
from src.geometry import Geometry,Line,Node,CircleArc
from src.executor import Executor
import matplotlib.pyplot as plt
import math

def calcChord(r,s):
    """
    Get chord length of known arc
    r : radius
    s : arc length
    """
    c = 2 * r * math.sin(s / 2 / r)
    return c


def calcChordHeight(r,s):
    """
        Get chord distance from center of a known arc
        r : radius
        s : arc length
        """
    rm = math.sqrt(r ** 2 - (s / 2) ** 2)
    return rm


def calcArc(r,c):
    s = 2 * r * math.asin(c / 2 / r)
    return s


def dependentArc_Width(r,Z,B):
    """
    With one fixed width (parallel teeth width, for example) get the dependent arc length (like slot width
    at a given radius)
    r : radius
    Z : number of teeth/slots
    B : fixed width
    """
    s = calcArc(r,B)
    c = (2 * r * math.pi - Z * s) / Z
    return c

def dependentArc_Angle(r,Z,s):
    """
    With one fixed arc length get the dependent arc length
    r : radius
    Z : number of teeth/slots
    B : fixed arc angle in radians
    """
    c = (2 * r * math.pi - Z * s * r) / Z
    return c


def machineGeom(machine,precision):

    # Let's draw
    geo = Geometry()
    # -------------------------- Stator
    # define nodes
    geo.nodes += [Node(0,0,0,label="center",precision=precision)]
    geo.nodes += [Node(0 - machine['geom']['ToothWidth'] / 2 - machine['geom']['radiusOfSlotCorners'],
                       machine['geom']['statorOuterDiameter'] / 2 - machine['geom']['BackIronThickness'],
                       1,label="Stator",precision=precision)]
    geo.nodes += [Node(0 - machine['geom']['ToothWidth'] / 2,
                       machine['geom']['statorOuterDiameter'] / 2 - machine['geom']['BackIronThickness'] -
                       machine['geom']['radiusOfSlotCorners'],
                       2,label="Stator",precision=precision)]
    geo.nodes += [Node(0 - machine['geom']['ToothWidth'] / 2,
                       calcChordHeight(r=machine['geom']['RadAtBaseToothTip'],
                                       s=calcArc(r=machine['geom']['RadAtBaseToothTip'],
                                                 c=machine['geom']['ToothWidth'])),
                       3,label="Stator",precision=precision)]
    geo.nodes += [Node(0 - calcChord(machine['geom']['statorInnerDiameter'] / 2 + machine['geom']['SlotOpDepth'],
                                     dependentArc_Width(
                                         machine['geom']['statorInnerDiameter'] / 2 + machine['geom']['SlotOpDepth'],
                                         machine['geom']['numberOfSlots'],
                                         machine['geom']['SlotOpWidth'])) / 2,
                       calcChordHeight(r=machine['geom']['statorInnerDiameter'] / 2 + machine['geom']['SlotOpDepth'],
                                       s=dependentArc_Width(
                                           machine['geom']['statorInnerDiameter'] / 2 + machine['geom']['SlotOpDepth'],
                                           machine['geom']['numberOfSlots'],
                                           machine['geom']['SlotOpWidth'])),
                       4,label="Stator",precision=precision)]
    geo.nodes += [Node(0 - calcChord(machine['geom']['statorInnerDiameter'] / 2,
                                     dependentArc_Width(machine['geom']['statorInnerDiameter'] / 2,
                                                        machine['geom']['numberOfSlots'],
                                                        machine['geom']['SlotOpWidth'])) / 2,
                       calcChordHeight(r=machine['geom']['statorInnerDiameter'] / 2,
                                       s=dependentArc_Width(machine['geom']['statorInnerDiameter'] / 2,
                                                            machine['geom']['numberOfSlots'],
                                                            machine['geom']['SlotOpWidth'])),
                       5,label="Stator",precision=precision)]

    geo.nodes += [Node(-geo.nodes[5].x,geo.nodes[5].y,6,"Stator",precision=precision)]
    geo.nodes += [Node(-geo.nodes[4].x,geo.nodes[4].y,7,"Stator",precision=precision)]
    geo.nodes += [Node(-geo.nodes[3].x,geo.nodes[3].y,8,"Stator",precision=precision)]
    geo.nodes += [Node(-geo.nodes[2].x,geo.nodes[2].y,9,"Stator",precision=precision)]
    geo.nodes += [Node(-geo.nodes[1].x,geo.nodes[1].y,10,"Stator",precision=precision)]
    ArcMidPoint1 = [Node(geo.nodes[2].x,geo.nodes[1].y)]
    ArcMidPoint2 = [Node(-geo.nodes[2].x,geo.nodes[1].y)]
    sttrPr = len(geo.nodes)-1  # Number of stator primitive points
    boundaryIdx = [] # which line is boundary
    for ii in range(machine['geom']['numberOfSlots'] - 1):  # 0-ról indul az indexelés és nem akarom duplázni az elsőt
        geo.nodes += [geo.nodes[1].rotate(-(ii + 1) * 2 * math.pi / machine['geom']['numberOfSlots'])]
        geo.nodes += [geo.nodes[2].rotate(-(ii + 1) * 2 * math.pi / machine['geom']['numberOfSlots'])]
        geo.nodes += [geo.nodes[3].rotate(-(ii + 1) * 2 * math.pi / machine['geom']['numberOfSlots'])]
        geo.nodes += [geo.nodes[4].rotate(-(ii + 1) * 2 * math.pi / machine['geom']['numberOfSlots'])]
        geo.nodes += [geo.nodes[5].rotate(-(ii + 1) * 2 * math.pi / machine['geom']['numberOfSlots'])]
        geo.nodes += [geo.nodes[6].rotate(-(ii + 1) * 2 * math.pi / machine['geom']['numberOfSlots'])]
        geo.nodes += [geo.nodes[7].rotate(-(ii + 1) * 2 * math.pi / machine['geom']['numberOfSlots'])]
        geo.nodes += [geo.nodes[8].rotate(-(ii + 1) * 2 * math.pi / machine['geom']['numberOfSlots'])]
        geo.nodes += [geo.nodes[9].rotate(-(ii + 1) * 2 * math.pi / machine['geom']['numberOfSlots'])]
        geo.nodes += [geo.nodes[10].rotate(-(ii + 1) * 2 * math.pi / machine['geom']['numberOfSlots'])]
        ArcMidPoint1 += [ArcMidPoint1[0].rotate(-(ii + 1) * 2 * math.pi / machine['geom']['numberOfSlots'])]
        ArcMidPoint2 += [ArcMidPoint2[0].rotate(-(ii + 1) * 2 * math.pi / machine['geom']['numberOfSlots'])]

    geo.nodes += [Node(0,machine['geom']['statorOuterDiameter'] / 2,0,label="Stator",precision=precision)]
    geo.nodes += [Node(0,-machine['geom']['statorOuterDiameter'] / 2,0,label="Stator",precision=precision)]

    # Define lines

    for ii in range(machine['geom']['numberOfSlots']):
        geo.circle_arcs += [CircleArc(geo.nodes[2 + ii*sttrPr],ArcMidPoint1[0 + ii],geo.nodes[1 + ii*sttrPr])]
        geo.lines += [Line(geo.nodes[2 + ii*sttrPr],geo.nodes[3 + ii*sttrPr])]
        geo.lines += [Line(geo.nodes[3 + ii*sttrPr],geo.nodes[4 + ii*sttrPr])]
        geo.lines += [Line(geo.nodes[4 + ii*sttrPr],geo.nodes[5 + ii*sttrPr])]
        geo.circle_arcs += [CircleArc(geo.nodes[6 + ii*sttrPr],geo.nodes[0],geo.nodes[5 + ii*sttrPr])]
        geo.lines += [Line(geo.nodes[6 + ii*sttrPr],geo.nodes[7 + ii*sttrPr])]
        geo.lines += [Line(geo.nodes[7 + ii*sttrPr],geo.nodes[8 + ii*sttrPr])]
        geo.lines += [Line(geo.nodes[8 + ii*sttrPr],geo.nodes[9 + ii*sttrPr])]
        geo.circle_arcs += [CircleArc(geo.nodes[10 + ii*sttrPr],ArcMidPoint2[0 + ii],geo.nodes[9 + ii*sttrPr])]
        geo.circle_arcs += [
            CircleArc(geo.nodes[1 + ((ii+1)*sttrPr % (sttrPr*machine['geom']['numberOfSlots']))],geo.nodes[0],geo.nodes[10 + ii*sttrPr])]
        geo.circle_arcs += [
            CircleArc(geo.nodes[3 + ((ii + 1) * sttrPr % (sttrPr * machine['geom']['numberOfSlots']))],geo.nodes[0],
                      geo.nodes[8 + ii * sttrPr])]
        # geo.lines += [Line(geo.nodes[8 + ii*sttrPr],geo.nodes[3 +((ii+1)*sttrPr % (sttrPr*machine['geom']['numberOfSlots']))])]

    geo.circle_arcs += [CircleArc(geo.nodes[-1],geo.nodes[0],geo.nodes[-2])]
    boundaryIdx += [len(geo.circle_arcs)]
    geo.circle_arcs += [CircleArc(geo.nodes[-2],geo.nodes[0],geo.nodes[-1])]
    boundaryIdx += [len(geo.circle_arcs)]

    noOfStatorNodes = len(geo.nodes)
    noOfStatorArcs = len(geo.circle_arcs)
    noOfStatorLines = len(geo.lines)

    # -------------------------- Rotor

    ROR = machine['geom']['statorInnerDiameter'] / 2 - machine['geom']['airgapLength']

    geo.nodes += [Node(0 - calcChord(ROR,
                                     dependentArc_Angle(ROR,
                                                        machine['geom']['numberOfPoles'],
                                                        math.pi / 180 * machine['geom']['bAngle'])) / 2,
                       calcChordHeight(r=ROR,
                                       s=dependentArc_Angle(ROR,
                                                            machine['geom']['numberOfPoles'],
                                                            math.pi / 180 * machine['geom']['bAngle'])),
                       11,label="Rotor",precision=precision)]

    geo.nodes += [Node(0 - calcChord(ROR - machine['geom']['bMag'],
                                     dependentArc_Angle(ROR - machine['geom']['bMag'],
                                                        machine['geom']['numberOfPoles'],
                                                        math.pi / 180 * machine['geom']['bAngle'])) / 2,
                       calcChordHeight(r=ROR - machine['geom']['bMag'],
                                       s=dependentArc_Angle(ROR - machine['geom']['bMag'],
                                                            machine['geom']['numberOfPoles'],
                                                            math.pi / 180 * machine['geom']['bAngle'])),
                       12,label="Rotor",precision=precision)]
    geo.nodes += [Node(-geo.nodes[noOfStatorNodes].x,geo.nodes[noOfStatorNodes].y,13,"Rotor",precision=precision)]
    geo.nodes += [
        Node(-geo.nodes[noOfStatorNodes + 1].x,geo.nodes[noOfStatorNodes + 1].y,14,"Rotor",precision=precision)]
    rtrPr = len(geo.nodes) - noOfStatorNodes
    for ii in range(machine['geom']['numberOfPoles'] - 1):  # 0-ról indul az indexelés és nem akarom duplázni az elsőt
        geo.nodes += [geo.nodes[noOfStatorNodes].rotate(-(ii + 1) * 2 * math.pi / machine['geom']['numberOfPoles'])]
        geo.nodes += [geo.nodes[noOfStatorNodes + 1].rotate(-(ii + 1) * 2 * math.pi / machine['geom']['numberOfPoles'])]
        geo.nodes += [geo.nodes[noOfStatorNodes + 2].rotate(-(ii + 1) * 2 * math.pi / machine['geom']['numberOfPoles'])]
        geo.nodes += [geo.nodes[noOfStatorNodes + 3].rotate(-(ii + 1) * 2 * math.pi / machine['geom']['numberOfPoles'])]

    geo.nodes += [Node(0,machine['geom']['rotorInnerDiameter'] / 2,0,label="Rotor",precision=precision)]
    geo.nodes += [Node(0,-machine['geom']['rotorInnerDiameter'] / 2,0,label="Rotor",precision=precision)]

    for ii in range(machine['geom']['numberOfPoles']):
        geo.circle_arcs += [CircleArc(geo.nodes[noOfStatorNodes + 2 + ii*rtrPr],geo.nodes[0],
                                      geo.nodes[noOfStatorNodes + 0 + ii*rtrPr])]
        # geo.circle_arcs += [CircleArc(geo.nodes[noOfStatorNodes + 3 + ii*rtrPr],geo.nodes[0],
        #                               geo.nodes[noOfStatorNodes + 1 + ii*rtrPr])]
        geo.circle_arcs += [CircleArc(geo.nodes[noOfStatorNodes + 0 + (((ii+1)%machine['geom']['numberOfPoles'])*rtrPr)],geo.nodes[0],
                                      geo.nodes[noOfStatorNodes + 2 + ii*rtrPr])]
        geo.circle_arcs += [CircleArc(geo.nodes[noOfStatorNodes + 1 + (((ii + 1)%machine['geom']['numberOfPoles']) * rtrPr)],geo.nodes[0],
                                      geo.nodes[noOfStatorNodes + 3 + ii * rtrPr])]

        geo.lines += [Line(geo.nodes[noOfStatorNodes + 0 + ii*rtrPr],geo.nodes[noOfStatorNodes + 1 + ii*rtrPr])]
        geo.lines += [Line(geo.nodes[noOfStatorNodes + 2 + ii*rtrPr],geo.nodes[noOfStatorNodes + 3 + ii*rtrPr])]

    geo.circle_arcs += [CircleArc(geo.nodes[-1],geo.nodes[0],geo.nodes[-2])]
    boundaryIdx += [len(geo.circle_arcs)]
    geo.circle_arcs += [CircleArc(geo.nodes[-2],geo.nodes[0],geo.nodes[-1])]
    boundaryIdx += [len(geo.circle_arcs)]

    # x_coord = [nodes.x for nodes in geo.nodes]
    # y_coord = [nodes.y for nodes in geo.nodes]
    # x_coord += [element.x for element in ArcMidPoint2]
    # x_coord += [element.x for element in ArcMidPoint1]
    # y_coord += [element.y for element in ArcMidPoint2]
    # y_coord += [element.y for element in ArcMidPoint1]
    #
    # plt.scatter(x_coord,y_coord)
    # plt.xlabel('X')
    # plt.ylabel('Y')
    # plt.grid(True)
    # plt.axis('equal')
    # plt.show()
    return [geo,boundaryIdx]



if __name__ == '__main__':
    precision = 6
    problem = FemmProblem(out_file="FrozenBenchmark.csv")
    problem.magnetic_problem(0,LengthUnit.MILLIMETERS,"axi",precision=precision)
    machine = {
        'geom':{
            'bMag':3.25,  # mm
            'bAngle':41.6,  # degrees
            'rotorInnerDiameter':24.7,  # mm
            'SlotOpWidth':2.3,  # mm
            'SlotOpDepth':1,  # mm
            'ToothWidth':5,  # mm
            'RadAtBaseToothTip':33.1,  # mm
            'BackIronThickness':6.75,  # mm
            'statorOuterDiameter':106,  # mm
            'statorInnerDiameter':62,  # mm
            'airgapLength':0.75,  # mm
            'axialLength':30,  # mm
            'numberOfSlots':18,
            'numberOfPoles':6,
            'turnsPerSlot':152,
            'radiusOfSlotCorners':2,  # mm
            'laminationStackingFactor':0.98,
            'wireSize':"AWG 22",
            'wireD':0.64380801773901497,
            'ironDlam':0.635,

            },
        'elec':{
            'magBr': 1.17,  # Tesla
            'magHc': 891000,  # A/m
            'magMu': 1.04496,
            'ratedCurrent': 4,  # Apk
            'statorMaterial':"24 gauge M-19",
            'ironMu':4416,
            'ironSig':1.8999,
            'ironBvec':[0,0.050,0.1,0.15,0.20,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1,
                        1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.45,1.5,1.55,1.6,1.65,1.7,1.75,1.8,1.85,1.7,1.95,2,2.05,
                        2.1,2.15,2.2,2.25,2.3],
            'ironHvec':[0,15.120714,22.718292000000002,27.842732999999999,31.871434000000001,35.365043999999997,
                        38.600588000,41.73620199,44.8739789999,48.087806999,51.43723599,54.97522099,
                        58.752992999,62.82364400,67.245284999,72.0844060,77.4201000,83.35002099,89.9996119999,
                        97.53735299,106.20140600,116.34846400,128.54732899,143.76543100000001,163.75416899999999,
                        191.86815799999999,234.833507,306.50976900000001,435.255202,674.911968,1108.3255690000001,
                        1813.085468,2801.2174209999998,4053.6531169999998,5591.10689,7448.318413,
                        9708.81567,12486.931615,16041.483644,21249.420623999998,31313.495878000002,
                        53589.446877000002,88477.484601000004,124329.41054,159968.5693,197751.604272,
                        234024.75134700001],
        }
    }

    ## Geometry
    [geo,boundaryIdx] = machineGeom(machine,precision)
    problem.create_geometry(geo)
    ## Boundary conditions

    a0 = MagneticDirichlet(name="a0",a_0=0,a_1=0,a_2=0,phi=0)
    problem.add_boundary(a0)
    for ii in range(len(boundaryIdx)):
        problem.set_boundary_definition(geo.circle_arcs[boundaryIdx[ii]-1].selection_point(),a0)

    # Materials
    Winding = MagneticMaterial(material_name="Winding",
                               Sigma=58.0,
                               WireD=machine['geom']['wireD'],
                               LamType=LamType(3))
    air = MagneticMaterial(material_name="air")
    M19 = MagneticMaterial(material_name="M19",
                           mu_x=machine['elec']['ironMu'],
                           mu_y=machine['elec']['ironMu'],
                           Lam_d=machine['geom']['ironDlam'],
                           lam_fill=machine['geom']['laminationStackingFactor'],
                           Sigma=machine['elec']['ironSig'])
    ironCurve = BHCurve(M='M19',B=machine['elec']['ironBvec'],
                        H=machine['elec']['ironHvec'])

    NdFeB = MagneticMaterial(material_name="NdFeB",
                             H_c=machine['elec']['magHc'],
                             mu_x=machine['elec']['magMu'],
                             mu_y=machine['elec']['magMu'])

    problem.add_material(Winding)
    problem.add_material(M19)
    problem.add_BHCurve(ironCurve)
    problem.add_material(air)
    problem.add_material(NdFeB)

    ## Circuits
    problem.add_circuit_property(circuit_name='A',i=4,circuit_type=1)
    problem.add_circuit_property(circuit_name='B',i=-2,circuit_type=1)
    problem.add_circuit_property(circuit_name='C',i=-2,circuit_type=1)

    ## Block properties
    air_block = Node(machine['geom']['statorInnerDiameter']-machine['geom']['airgapLength']/2,0.0)
    problem.define_block_label(air_block,air)

    ## Gimme LUA
    problem.write("FrozenBenchmark.lua")
    ## Execute
    # femm = Executor()
    # current_dir = os.getcwd()
    # lua_file = current_dir + "/solenoid.lua"
    # femm.run(lua_file)