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
MAGNET_WIDTH = 15.9 # Table 1: Magnes szelesseg

# Horony/polus adatok
STATOR_SLOTS = 24
SEGMENT_SIZE = 3 # Horonyszam a szegmensben (45 fok)

# A VIZSGALT SZEGMENS ANGULARIS HOSSZA (45 fok)
SEGMENT_ANGLE_DEG = 360 / STATOR_SLOTS * SEGMENT_SIZE # 45.0 deg

# Magnes adatok
MAGNET_HEIGHT = 3.577 # Table 2
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
    Kesziti az alloresz geometriajat. (Most uresen hagyva, csak a rotorhoz)
    """
    return Geometry()


def rotor_geometry():
    """
    Kesziti a rotor geometriajat (45 fok) a magnesekkel es a vasmaggal.
    A vasmag teteje lapos (trapez).
    """
    rotor_geo = Geometry()

    Rr_o = ROTOR_OUTER_DIAMETER / 2
    Rr_i = ROTOR_INNER_DIAMETER / 2
    Mh = MAGNET_HEIGHT
    
    angle_deg = SEGMENT_ANGLE_DEG
    angle_half = angle_deg / 2
    
    # MÁGNES KONSTRUKCIÓ
    
    half_mw = MAGNET_WIDTH / 2 
    R_mag_top = Rr_o 
    
    # Mágnes Lapolási Y magassága a Rr_o ivhez (a mágnes a Rr_o ivet követi)
    x_mag_side = half_mw
    y_rro = math.sqrt(R_mag_top**2 - x_mag_side**2) 
    
    # Mágnes Lapos Alja / Rotorvas Teteje (Y koordináta)
    Y_ROTOR_TOP_FLAT = y_rro - Mh 
    
    # ------------------------------------------------------------------
    # 1. ROTOR VASMAG KONSTRUKCIÓ (Lapostetejű trapezoid a 45 fokos szegmensben)
    # ------------------------------------------------------------------
    
    # Rotorvas Lapos Tetejének Pontjai (45 fokos szegmens)
    x_seg_half = Rr_o * math.sin(math.radians(angle_half)) # X koordinata 22.5 foknál
    
    p_iron_top_left_flat = Node(-x_seg_half, Y_ROTOR_TOP_FLAT)
    p_iron_top_right_flat = Node(x_seg_half, Y_ROTOR_TOP_FLAT)
    
    # Rotor belső ív pontjai
    p_in_left_yoke, p_in_right_yoke = create_arc_pair(Rr_i, angle_deg)
    
    # Vasmag kontúrjának rajzolása (Lapostetejű trapezoid)
    rotor_geo.add_line(Line(p_iron_top_left_flat, p_iron_top_right_flat)) # Lapos tető
    rotor_geo.add_line(Line(p_iron_top_right_flat, p_in_right_yoke)) # Jobb oldal
    rotor_geo.add_arc(CircleArc(p_in_right_yoke, ORIGIN, p_in_left_yoke)) # Belső ív
    rotor_geo.add_line(Line(p_in_left_yoke, p_iron_top_left_flat)) # Bal oldal
    
    # ------------------------------------------------------------------
    # 2. MÁGNES KONSTRUKCIÓ (Független elem a vasmag felett)
    # ------------------------------------------------------------------

    # Mágnes Lapos Aljának Pontjai (megegyeznek a vasmag tetejével)
    p_mag_bottom_left = Node(-half_mw, Y_ROTOR_TOP_FLAT) 
    p_mag_bottom_right = Node(half_mw, Y_ROTOR_TOP_FLAT)

    # Mágnes Íves Tetejének Pontjai
    p_out_mag_left = Node(-x_mag_side, y_rro)
    p_out_mag_right = Node(x_mag_side, y_rro)

    # MÁGNES KONTÚR RAJZOLÁSA
    
    # 1. Mágnes külső ÍV (Rr_o sugarú) -> Zölddel jelölt ives tető
    rotor_geo.add_arc(CircleArc(p_out_mag_right, ORIGIN, p_out_mag_left))

    # 2. Mágnes belső EGYENES lapolása (Magnes alja)
    rotor_geo.add_line(Line(p_mag_bottom_left, p_mag_bottom_right)) 
    
    # 3. Mágnes oldalai (Függőleges/Radiális)
    rotor_geo.add_line(Line(p_out_mag_left, p_mag_bottom_left)) 
    rotor_geo.add_line(Line(p_out_mag_right, p_mag_bottom_right)) 
    
    return rotor_geo

def material_definitions(femm_problem: FemmProblem):
    # Anyagok
    air = MagneticMaterial(material_name='air', mesh_size=1)
    steel = MagneticMaterial(material_name='stator_steel', Sigma=1.9e6, lam_fill=0.98, Lam_d=0.34)
    steel.b = [0, 0.6708, 1.0189, 1.4156, 1.5773, 2.3883, 3.6682]
    steel.h = [0, 200, 700, 6773, 35206, 509252, 1527756]
    magnet = MagneticMaterial(material_name='magnet', mu_x=MAGNET_MUR, mu_y=MAGNET_MUR, H_c=MAGNET_HC, Sigma=0.667e6)
    magnet.mesh_size = 1
    magnet.remanence_angle = 90 
    copper = MagneticMaterial(material_name='copper', J=0, Sigma=58e6, LamType=LamType.MAGNET_WIRE)
    air_gap = MagneticMaterial(material_name='air_gap', mesh_size=0.5)

    femm_problem.add_material(air)
    femm_problem.add_material(steel)
    femm_problem.add_material(magnet)
    femm_problem.add_material(copper)
    femm_problem.add_material(air_gap)


    # Blokk cimkek
    Rr_o = ROTOR_OUTER_DIAMETER / 2
    Rr_i = ROTOR_INNER_DIAMETER / 2
    Mh = MAGNET_HEIGHT
    
    # Sugarak
    R_mag_top = Rr_o
    R_mag_bottom = Rr_o - Mh
    
    R_magnet_center = R_mag_top - Mh / 2
    R_rotor_yoke = (R_mag_bottom + Rr_i) / 2
    R_shaft_air = Rr_i * 0.5
    
    # Angularis pontok (szegmens kozepe)
    angle = 0.0 

    # 1. Magnes (kek satorozas)
    femm_problem.define_block_label(create_node(R_magnet_center, angle), magnet)

    # 2. Rotor vas (sarga satorozas)
    femm_problem.define_block_label(create_node(R_rotor_yoke, angle), steel)
    
    # 3. Tengely/belso levego (Air)
    Rs_o_air = STATOR_OUTER_DIAMETER / 2
    R_air_mid = (Rs_o_air + Rr_o) / 2
    
    femm_problem.define_block_label(create_node(R_shaft_air, angle), air)
    # 4. Kulso levego (Kulso levego cimke)
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
    # A legkulso iv (Rs_o_air) es a belso iv (Rr_i)
    femm_problem.set_boundary_definition_arc(create_node(Rs_o_air * 0.99, 0), a0) 
    femm_problem.set_boundary_definition_arc(create_node(Rr_i * 1.01, 0), a0) 
    
    # Radialis Periodikus hatarok
    R_mid = (Rs_o_air + Rr_i) / 2
    
    # Rotor oldalai
    femm_problem.set_boundary_definition_segment(create_node(R_mid, angle_deg/2), pb_radial)
    femm_problem.set_boundary_definition_segment(create_node(R_mid, -angle_deg/2), pb_radial)


def run_bldc_analysis(output_file="BLDC_rotor_only.csv"):
    """Fo futtato funkcio a BLDC gep FEM analizisehez (csak rotor)."""

    # 1. Problema definialasa
    problem = FemmProblem(out_file=output_file)
    problem.magnetic_problem(0, LengthUnit.MILLIMETERS, "planar", depth=AXIAL_LENGTH)

    # 2. Geometria letrehozasa
    rotor_geo = rotor_geometry()
    
    problem.create_geometry(rotor_geo)

    # 3. Anyagok es gerjesztes definialasa
    material_definitions(problem)

    # 4. Peremfeltetelek beallitasa
    boundary_definitions(problem)

    # 5. Analizis es LUA fajl elkeszitese
    problem.make_analysis('bldc_rotor_analysis')
    problem.write("BLDC_rotor_only.lua")

    # 6. FEMM futtatasa (Kikommmentelve hagyom)
    femm = Executor()
    lua_file = os.path.join(os.getcwd(), "BLDC_rotor_only.lua")
    print(f"FEM analizis futtatasa a {lua_file} fajllal...")
    # femm.run(lua_file)

    print("BLDC_rotor_only.lua fajl generalva a rotor geometriahoz.")


if __name__ == '__main__':
    run_bldc_analysis()