import os
import dataclasses
import math
from math import sin, cos, asin, acos, pi
from copy import copy

# Feltetelezett importok az src fajlokbol
from src.magnetics import MagneticDirichlet, MagneticMaterial, MagneticAnti, MagneticAntiPeriodicAirgap, LamType, MagneticPeriodic
from src.femm_problem import FemmProblem
from src.general import LengthUnit
from src.geometry import Geometry, Line, Node, CircleArc
from src.executor import Executor


# ----------------------------------------------------------------------
# GEP PARAMETEREI
# ----------------------------------------------------------------------
ORIGIN = Node(0.0, 0.0)

# Geometriai allandok (mm-ben)
AXIAL_LENGTH = 50.0
ROTOR_INNER_DIAMETER = 22.8
ROTOR_OUTER_DIAMETER = 55.1
AIR_GAP_LENGTH = 0.7
STATOR_OUTER_DIAMETER = 100.0
TOOTH_ROOT_DIAMETER = 86.6 
MAGNET_WIDTH = 15.9 

# Horony/polus adatok
STATOR_SLOTS = 24
SEGMENT_SIZE = 3 # Horonyszam a szegmensben (45 fok)

# A VIZSGALT SZEGMENS ANGULARIS HOSSZA (45 fok)
SEGMENT_ANGLE_DEG = 360 / STATOR_SLOTS * SEGMENT_SIZE # 45.0 deg

# Magnes adatok
MAGNET_HEIGHT = 3.577 
MAGNET_HC = 724 * 1000
MAGNET_MUR = 1.11

# ----------------------------------------------------------------------
# GEOMETRIAI FUGGVENYEK
# ----------------------------------------------------------------------

def create_node(R, angle_deg):
    """Segedfuggveny a koordinatak letrehozasahoz fok alapjan"""
    angle_rad = math.radians(angle_deg)
    return Node(R * sin(angle_rad), R * cos(angle_rad))

def create_arc_pair(R, angle_deg):
    """Letrehozza a ket pontot egy R sugaru ivhez a szegmens hatarain"""
    p_left = create_node(R, -angle_deg / 2)
    p_right = create_node(R, angle_deg / 2)
    return p_left, p_right


def stator_geometry():
    """
    Kesziti az alloresz geometriajat. (Placeholder)
    """
    return Geometry()


def rotor_geometry():
    """
    Kesziti a rotor vasmag geometriajat (45 fok) lapos teteju trapezkent.
    """
    rotor_geo = Geometry()

    Rr_o = ROTOR_OUTER_DIAMETER / 2
    Rr_i = ROTOR_INNER_DIAMETER / 2
    
    angle_deg = SEGMENT_ANGLE_DEG
    angle_half = angle_deg / 2
    
    # ROTOR VASMAG KONSTRUKCIÓ
    
    # 1. Lapos Tetejének Magassága (Y_ROTOR_TOP_FLAT)
    
    # A legmagasabb pont a Rr_o sugár Y tengelyén (cos(0) * Rr_o)
    Y_CENTER_MAX = Rr_o 
    
    # Levonunk egy kis chamfer magasságot (pl. 2 mm, hogy látványos legyen a chamfer)
    H_chamfer = 2.0 
    Y_ROTOR_TOP_FLAT = Y_CENTER_MAX - H_chamfer 

    # 2. Lapos Tetejének Széle (X koordináták)
    X_chamfer_start = Rr_o * math.sin(math.radians(angle_half)) - 1.0 # 1mm-rel beljebb a széltől
    
    # Rotorvas Lapos Tetejének Széle
    p_top_left_flat = Node(-X_chamfer_start, Y_ROTOR_TOP_FLAT)
    p_top_right_flat = Node(X_chamfer_start, Y_ROTOR_TOP_FLAT)
    
    # Rotorvas Külső sarkai (Rr_o-n, 45 fokos szegmens határán)
    p_out_left, p_out_right = create_arc_pair(Rr_o, angle_deg)
    
    # Rotor belső ív pontjai
    p_in_left, p_in_right = create_arc_pair(Rr_i, angle_deg)

    # Vasmag kontúrjának rajzolása
    
    # 1. Lapos Teteje (Egyenes)
    rotor_geo.add_line(Line(p_top_left_flat, p_top_right_flat))

    # 2. Chamfer (Lapolás) vonalak
    # KORRIGÁLVA: A lapolásnak a külső sarkoktól a lapos tetőig kell indulnia.
    rotor_geo.add_line(Line(p_top_right_flat, p_out_right)) # Jobb chamfer
    rotor_geo.add_line(Line(p_out_left, p_top_left_flat)) # Bal chamfer
    
    # 3. Oldalvonalak (a szegmens radiális határán)
    rotor_geo.add_line(Line(p_out_right, p_in_right)) 
    rotor_geo.add_line(Line(p_out_left, p_in_left))
    
    # 4. Belső ív
    rotor_geo.add_arc(CircleArc(p_in_right, ORIGIN, p_in_left)) 

    return rotor_geo

def material_definitions(femm_problem: FemmProblem):
    # Anyagok
    air = MagneticMaterial(material_name='air', mesh_size=1)
    steel = MagneticMaterial(material_name='stator_steel', Sigma=1.9e6, lam_fill=0.98, Lam_d=0.34)
    steel.b = [0, 0.6708, 1.0189, 1.4156, 1.5773, 2.3883, 3.6682]
    steel.h = [0, 200, 700, 6773, 35206, 509252, 1527756]
    
    femm_problem.add_material(air)
    femm_problem.add_material(steel)
    
    # Placeholder anyagok
    magnet = MagneticMaterial(material_name='magnet', mu_x=MAGNET_MUR, mu_y=MAGNET_MUR, H_c=MAGNET_HC, Sigma=0.667e6)
    copper = MagneticMaterial(material_name='copper', J=0, Sigma=58e6, LamType=LamType.MAGNET_WIRE)
    air_gap = MagneticMaterial(material_name='air_gap', mesh_size=0.5)
    femm_problem.add_material(magnet)
    femm_problem.add_material(copper)
    femm_problem.add_material(air_gap)


    # Blokk cimke
    Rr_o = ROTOR_OUTER_DIAMETER / 2
    Rr_i = ROTOR_INNER_DIAMETER / 2
    
    R_rotor_center = (Rr_o + Rr_i) / 2
    R_shaft_air = Rr_i * 0.5
    
    angle = 0.0 

    # 1. Rotor vasmag
    femm_problem.define_block_label(create_node(R_rotor_center, angle), steel)
    
    # 2. Tengely/belso levego
    Rs_o_air = STATOR_OUTER_DIAMETER / 2
    R_air_mid = (Rs_o_air + Rr_o) / 2
    
    femm_problem.define_block_label(create_node(R_shaft_air, angle), air)
    # 3. Kulso levego (Légüreg és Stator helye)
    femm_problem.define_block_label(create_node(R_air_mid, angle), air)


def boundary_definitions(femm_problem: FemmProblem):
    # Dirichlet hatarfeltetel (A=0)
    a0 = MagneticDirichlet(name='a0', a_0=0, a_1=0, a_2=0, phi=0)
    femm_problem.add_boundary(a0)
    
    # Periodikus peremfeltetel 45 fokos szegmenshez
    pb_radial = MagneticPeriodic("PB_Radial")
    femm_problem.add_boundary(pb_radial)

    # Atmerok
    Rr_i = ROTOR_INNER_DIAMETER / 2
    Rr_o = ROTOR_OUTER_DIAMETER / 2
    Rs_o_air = STATOR_OUTER_DIAMETER / 2
    angle_deg = SEGMENT_ANGLE_DEG # 45 fok
    
    # Tangencialis hatarok (A=0 Dirichlet)
    femm_problem.set_boundary_definition_arc(create_node(Rs_o_air * 0.99, 0), a0) 
    femm_problem.set_boundary_definition_arc(create_node(Rr_i * 1.01, 0), a0) 
    
    # Radialis Periodikus hatarok
    R_mid = (Rs_o_air + Rr_i) / 2
    
    femm_problem.set_boundary_definition_segment(create_node(R_mid, angle_deg/2), pb_radial)
    femm_problem.set_boundary_definition_segment(create_node(R_mid, -angle_deg/2), pb_radial)


def run_bldc_analysis(output_file="BLDC_rotor_yoke.csv"):
    """Fo futtato funkcio a BLDC gep FEM analizisehez (csak rotor vasmag)."""

    # 1. Problema definialasa
    problem = FemmProblem(out_file=output_file)
    problem.magnetic_problem(0, LengthUnit.MILLIMETERS, "planar", depth=AXIAL_LENGTH)

    # 2. Geometria letrehozasa
    rotor_geo = rotor_geometry()
    stator_geo = stator_geometry() 
    
    problem.create_geometry(rotor_geo)
    problem.create_geometry(stator_geo) 

    # 3. Anyagok es gerjesztes definialasa
    material_definitions(problem)

    # 4. Peremfeltetelek beallitasa
    boundary_definitions(problem)

    # 5. Analizis es LUA fajl elkeszitese
    problem.make_analysis('bldc_rotor_yoke_analysis')
    problem.write("BLDC_rotor_yoke.lua")

    # 6. FEMM futtatasa (Kikommmentelve hagyom)
    femm = Executor()
    lua_file = os.path.join(os.getcwd(), "BLDC_rotor_yoke.lua")
    print(f"FEM analizis futtatasa a {lua_file} fajllal...")
    # femm.run(lua_file)

    print("BLDC_rotor_yoke.lua fajl generalva a rotor vasmag geometriahoz.")


if __name__ == '__main__':
    run_bldc_analysis()