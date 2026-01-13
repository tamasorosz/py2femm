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
# GEP PARAMETEREI (A CIKK ALAPJAN)
# ----------------------------------------------------------------------
ORIGIN = Node(0.0, 0.0)

# Geometriai allandok (mm-ben) az 1. tablazat alapjan
AXIAL_LENGTH = 50.0
ROTOR_INNER_DIAMETER = 22.8
ROTOR_OUTER_DIAMETER = 55.1
AIR_GAP_LENGTH = 0.7
STATOR_OUTER_DIAMETER = 100.0
TOOTH_ROOT_DIAMETER = 86.6
MAGNET_WIDTH = 15.9

# Horony/polus adatok
# A cikk szerint: "The motor has 24 slits"
STATOR_SLOTS = 24
SEGMENT_SIZE = 3 # Horonyszam a szegmensben (45 fok)

# A VIZSGALT SZEGMENS ANGULARIS HOSSZA (45 fok)
SEGMENT_ANGLE_DEG = 360 / STATOR_SLOTS * SEGMENT_SIZE # 45.0 deg

# Magnes adatok a 2. tablazat alapjan
MAGNET_HEIGHT = 3.577
MAGNET_HC = 724 * 1000        # (kA/m -> A/m)
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
    Kesziti az alloresz geometriajat. (Most uresen hagyva)
    """
    return Geometry()


def rotor_geometry():
    """
    Kesziti a rotor geometriajat (45 fok).
    A vasmag teteje a magnes alatt lapos, a szegmens szele fele
    egy LAPOSABB (nem meredek) lejtessel (chamfer) fut le.
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
    
    # Mágnes Lapolási Y magassága a Rr_o ivhez
    x_mag_side = half_mw
    y_rro = math.sqrt(R_mag_top**2 - x_mag_side**2) 
    
    # Mágnes Lapos Alja / Rotorvas Teteje (Y koordináta a mágnes alatt)
    Y_ROTOR_TOP_FLAT = y_rro - Mh 
    
    # ------------------------------------------------------------------
    # 1. ROTOR VASMAG KONSTRUKCIÓ (LAPOSABB LETÖRÉSSEL)
    # ------------------------------------------------------------------
    
    # A. Lapos tető pontjai (Csak a mágnes szélességében)
    # Ezek a lejtés (chamfer) KEZDŐPONTJAI a mágnes sarka alatt.
    p_iron_top_left_flat = Node(-half_mw, Y_ROTOR_TOP_FLAT)
    p_iron_top_right_flat = Node(half_mw, Y_ROTOR_TOP_FLAT)
    
    # B. Lejtés (Chamfer) VÉGPONTJAI a szegmens radiális határán
    # JAVITÁS: A mélység 0.8 mm, ami laposabb szöget ad.
    CHAMFER_DEPTH = 0.8 
    Y_CHAMFER_END = Y_ROTOR_TOP_FLAT - CHAMFER_DEPTH
    
    # Kiszámítjuk az X koordinátát a szegmens határvonalán (y = x / tan(angle))
    tan_angle_half = math.tan(math.radians(angle_half))
    X_chamfer_end = Y_CHAMFER_END * tan_angle_half
    
    p_iron_chamfer_left = Node(-X_chamfer_end, Y_CHAMFER_END)
    p_iron_chamfer_right = Node(X_chamfer_end, Y_CHAMFER_END)
    
    # C. Rotor belső ív pontjai
    p_in_left_yoke, p_in_right_yoke = create_arc_pair(Rr_i, angle_deg)
    
    # D. Vasmag kontúrjának rajzolása
    
    # 1. Bal oldali LAPOS lejtés
    rotor_geo.add_line(Line(p_iron_chamfer_left, p_iron_top_left_flat))

    # 2. Középső Lapos tető (a mágnes alatt)
    rotor_geo.add_line(Line(p_iron_top_left_flat, p_iron_top_right_flat)) 

    # 3. Jobb oldali LAPOS lejtés
    rotor_geo.add_line(Line(p_iron_top_right_flat, p_iron_chamfer_right))

    # 4. Jobb oldali radiális határ
    rotor_geo.add_line(Line(p_iron_chamfer_right, p_in_right_yoke)) 
    
    # 5. Belső ív
    rotor_geo.add_arc(CircleArc(p_in_right_yoke, ORIGIN, p_in_left_yoke)) 
    
    # 6. Bal oldali radiális határ
    rotor_geo.add_line(Line(p_in_left_yoke, p_iron_chamfer_left)) 
    
    # ------------------------------------------------------------------
    # 2. MÁGNES KONSTRUKCIÓ
    # ------------------------------------------------------------------

    p_mag_bottom_left = p_iron_top_left_flat
    p_mag_bottom_right = p_iron_top_right_flat

    p_out_mag_left = Node(-x_mag_side, y_rro)
    p_out_mag_right = Node(x_mag_side, y_rro)

    # MÁGNES KONTÚR
    rotor_geo.add_arc(CircleArc(p_out_mag_right, ORIGIN, p_out_mag_left))
    rotor_geo.add_line(Line(p_mag_bottom_left, p_mag_bottom_right)) 
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

    Rs_o_air = STATOR_OUTER_DIAMETER / 2
    R_air_mid = (Rs_o_air + Rr_o) / 2
    
    angle = 0.0 

    femm_problem.define_block_label(create_node(R_magnet_center, angle), magnet)
    femm_problem.define_block_label(create_node(R_rotor_yoke, angle), steel)
    femm_problem.define_block_label(create_node(R_shaft_air, angle), air)
    femm_problem.define_block_label(create_node(R_air_mid, angle), air)


def boundary_definitions(femm_problem: FemmProblem):
    # Peremfeltetelek
    a0 = MagneticDirichlet(name='a0', a_0=0, a_1=0, a_2=0, phi=0)
    femm_problem.add_boundary(a0)
    
    pb_radial = MagneticPeriodic("PB_Radial")
    femm_problem.add_boundary(pb_radial)

    Rr_i = ROTOR_INNER_DIAMETER / 2
    Rr_o = ROTOR_OUTER_DIAMETER / 2
    Rs_o_air = STATOR_OUTER_DIAMETER / 2
    angle_deg = SEGMENT_ANGLE_DEG
    
    femm_problem.set_boundary_definition_arc(create_node(Rs_o_air * 0.99, 0), a0) 
    femm_problem.set_boundary_definition_arc(create_node(Rr_i * 1.01, 0), a0) 
    
    R_mid = (Rs_o_air + Rr_i) / 2
    
    femm_problem.set_boundary_definition_segment(create_node(R_mid, angle_deg/2), pb_radial)
    femm_problem.set_boundary_definition_segment(create_node(R_mid, -angle_deg/2), pb_radial)


def run_bldc_analysis(output_file="BLDC_rotor_gentle_chamfer_corrected.csv"):
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
    problem.make_analysis('bldc_rotor_gentle_chamfer_corrected_analysis')
    problem.write("BLDC_rotor_gentle_chamfer_corrected.lua")

    femm = Executor()
    lua_file = os.path.join(os.getcwd(), "BLDC_rotor_gentle_chamfer_corrected.lua")
    print(f"FEM analizis futtatasa a {lua_file} fajllal...")
    # femm.run(lua_file)

    print("BLDC_rotor_gentle_chamfer_corrected.lua fajl generalva a rotor geometriahoz.")


if __name__ == '__main__':
    run_bldc_analysis()