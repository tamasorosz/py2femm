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
TOOTH_WIDTH = 4.0
TOOTH_ROOT_DIAMETER = 86.6 

# Horony/polus adatok
STATOR_SLOTS = 24
SEGMENT_SIZE = 3 # Horonyszam a szegmensben (3 horony = 45 fok)

# A VIZSGALT SZEGMENS ANGULARIS HOSSZA (45 fok)
SEGMENT_ANGLE_DEG = 360 / STATOR_SLOTS * SEGMENT_SIZE # 45.0 deg

# Szög adatok
ANGLE_SLOT_PITCH = 360 / STATOR_SLOTS # 15 fok
ANGLE_SPANNED_BY_TOOTH = 11.9 # fok (Foghegy iv hossza)
ANGLE_SLOT_OPENING = ANGLE_SLOT_PITCH - ANGLE_SPANNED_BY_TOOTH # 3.1 fok

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
    Kesziti az alloresz geometriajat (45 fok) retges szerkezettel.
    """
    stator_geo = Geometry()
    Rs_o = STATOR_OUTER_DIAMETER / 2 # 50.0 mm
    Rr_o = ROTOR_OUTER_DIAMETER / 2 # 27.55 mm
    Rs_i = Rr_o + AIR_GAP_LENGTH # 28.25 mm (Legres feletti belso atmero)
    Rs_root = TOOTH_ROOT_DIAMETER / 2 # 43.3 mm (Foggyoker atmero)
    
    angle_deg = SEGMENT_ANGLE_DEG
    angle_half = angle_deg / 2
    
    # KULSO VASMAG (YOKE) KONTUR
    p_out_left, p_out_right = create_arc_pair(Rs_o, angle_deg)
    p_yoke_left, p_yoke_right = create_arc_pair(Rs_root, angle_deg)
    
    # Kulso ív
    stator_geo.add_arc(CircleArc(p_out_right, ORIGIN, p_out_left))
    # Radiális határok
    stator_geo.add_line(Line(p_out_left, p_yoke_left))
    stator_geo.add_line(Line(p_out_right, p_yoke_right))
    
    # 3. Belső kontur (Fogak, hornyok)
    
    # Horony/Fog ciklus (a hegyesszögek forrása)
    
    # Kezdeti szög
    current_angle = -angle_half
    p_prev_root = p_yoke_left
    
    num_teeth = SEGMENT_SIZE + 1 # 4 fog
    
    for i in range(num_teeth):
        
        # FOG GEOMETRIA (11.9 fok)
        angle_tooth_center = current_angle + ANGLE_SLOT_OPENING / 2 + ANGLE_SPANNED_BY_TOOTH / 2
        
        angle_tooth_start = angle_tooth_center - ANGLE_SPANNED_BY_TOOTH / 2
        angle_tooth_end = angle_tooth_center + ANGLE_SPANNED_BY_TOOTH / 2
        
        p_tip_start = create_node(Rs_i, angle_tooth_start)
        p_tip_end = create_node(Rs_i, angle_tooth_end)
        
        # Trapéz imitáció: Kiszamoljuk a fog szélét Rs_root-nál (egyszerűsítve)
        R_tooth_angle_at_root = ANGLE_SLOT_PITCH * 0.9 
        p_root_start = create_node(Rs_root, angle_tooth_center - R_tooth_angle_at_root / 2)
        p_root_end = create_node(Rs_root, angle_tooth_center + R_tooth_angle_at_root / 2)
        
        # 1. Rajzoljuk a fogat, ha nem a szegmens határon van (bonyolult, elkerüljük)
        # MOST CSAK AZ ÁLLÓVAS KONTRÚRT RAJZOLJUK, A FOGAK KÜLÖN RÉGIÓK LESZNEK
        
        # FOGHEGY IV (Rs_i-nel)
        stator_geo.add_arc(CircleArc(p_tip_start, ORIGIN, p_tip_end))
        
        # Fog oldalak
        stator_geo.add_line(Line(p_tip_start, p_root_start))
        stator_geo.add_line(Line(p_tip_end, p_root_end))
        
        # 2. HORONY NYILAS (3.1 fok)
        if i < SEGMENT_SIZE:
            angle_slot_end = angle_tooth_end + ANGLE_SLOT_OPENING
            
            p_slot_tip_end = create_node(Rs_i, angle_slot_end)
            p_slot_root_end = create_node(Rs_root, angle_slot_end)
            
            # Horony nyílás (Rs_i ív)
            stator_geo.add_arc(CircleArc(p_tip_end, ORIGIN, p_slot_tip_end)) 
            
            # Horony oldal (külső)
            stator_geo.add_line(Line(p_slot_tip_end, p_slot_root_end))
            
            # Horony alja (Rs_root ív)
            stator_geo.add_arc(CircleArc(p_slot_root_end, ORIGIN, p_root_end))
            
            # Következő iteráció előkészítése
            current_angle = angle_slot_end 
    
    # Foggyökér íve (a kontúr lezárása)
    stator_geo.add_arc(CircleArc(p_yoke_right, ORIGIN, p_yoke_left))
    
    return stator_geo

def rotor_geometry():
    """
    Kesziti a rotor geometriajat (45 fok) a magnesekkel.
    """
    rotor_geo = Geometry()

    Rr_o = ROTOR_OUTER_DIAMETER / 2
    Rr_i = ROTOR_INNER_DIAMETER / 2
    Mh = MAGNET_HEIGHT

    angle_deg = SEGMENT_ANGLE_DEG
    
    # 1. Rotor kulso iv (legres fele)
    p_out_left, p_out_right = create_arc_pair(Rr_o, angle_deg)
    rotor_geo.add_arc(CircleArc(p_out_right, ORIGIN, p_out_left))

    # 2. Magnes / Vas mag határ
    R_magnet_inner = Rr_o - Mh
    p_mag_left, p_mag_right = create_arc_pair(R_magnet_inner, angle_deg)

    # Magnes belso hatara (iv)
    rotor_geo.add_arc(CircleArc(p_mag_right, ORIGIN, p_mag_left))
    
    # 3. Rotor belso iv (tengely)
    p_in_left, p_in_right = create_arc_pair(Rr_i, angle_deg)
    rotor_geo.add_arc(CircleArc(p_in_right, ORIGIN, p_in_left)) # KIFELÉ MUTATÓ ÍV

    # 4. Radiális határok (felosztva)
    rotor_geo.add_line(Line(p_out_left, p_mag_left)) 
    rotor_geo.add_line(Line(p_mag_left, p_in_left)) 

    rotor_geo.add_line(Line(p_out_right, p_mag_right)) 
    rotor_geo.add_line(Line(p_mag_right, p_in_right)) 

    return rotor_geo

def material_definitions(femm_problem: FemmProblem):
    # Anyagok
    air = MagneticMaterial(material_name='air', mesh_size=1)
    air_gap = MagneticMaterial(material_name='air_gap', mesh_size=0.5)
    steel = MagneticMaterial(material_name='stator_steel', Sigma=1.9e6, lam_fill=0.98, Lam_d=0.34)
    steel.b = [0.000000, 0.047002, 0.094002, 0.141002, 0.338404, 0.507605,
               0.611006, 0.930612, 1.128024, 1.203236, 1.250248, 1.278460,
               1.353720, 1.429040, 1.485560, 1.532680, 1.570400, 1.693200,
               1.788400, 1.888400, 1.988400, 2.188400, 2.388397, 2.452391,
               3.668287]
    steel.h = [0.000000, 22.28000, 25.46000, 31.83000, 47.74000, 63.66000,
               79.57000, 159.1500, 318.3000, 477.4600, 636.6100, 795.7700,
               1591.500, 3183.000, 4774.600, 6366.100, 7957.700, 15915.00,
               31830.00, 111407.0, 190984.0, 350135.0, 509252.0, 560177.2,
               1527756.0]
    magnet = MagneticMaterial(material_name='magnet', mu_x=MAGNET_MUR, mu_y=MAGNET_MUR, H_c=MAGNET_HC, Sigma=0.667e6)
    magnet.mesh_size = 1
    magnet.remanence_angle = 90
    copper = MagneticMaterial(material_name='copper', J=0, Sigma=58e6, LamType=LamType.MAGNET_WIRE)

    femm_problem.add_material(air)
    femm_problem.add_material(air_gap)
    femm_problem.add_material(steel)
    femm_problem.add_material(magnet)
    femm_problem.add_material(copper)

    # Blokk cimkek
    Rs_o = STATOR_OUTER_DIAMETER / 2
    Rr_o = ROTOR_OUTER_DIAMETER / 2
    Rr_i = ROTOR_INNER_DIAMETER / 2
    Rs_i = Rr_o + AIR_GAP_LENGTH
    Rs_root = TOOTH_ROOT_DIAMETER / 2
    Mh = MAGNET_HEIGHT

    # Sugarak
    R_stator_yoke = (Rs_o + Rs_root) / 2
    R_air_gap = (Rr_o + Rs_i) / 2
    R_magnet = Rr_o - Mh / 2
    R_rotor_yoke = (Rr_i + (Rr_o - Mh)) / 2
    R_shaft_air = Rr_i * 0.5
    
    # Angularis pontok
    angles = [0.0, 7.5, -7.5, 15.0, -15.0, 22.5, -22.5]
    R_coil = (Rs_i + Rs_root) / 2
    
    for angle in angles:
        # Alloresz/Fog (0, 15 fokon van fog kozep)
        if abs(angle) % 15 < 3.0:
             # Fog/Allóvas
             femm_problem.define_block_label(create_node(R_stator_yoke, angle), steel)
             femm_problem.define_block_label(create_node(R_coil, angle), steel)
        else:
             # Horony (7.5, 22.5, -7.5, -22.5 fok)
             femm_problem.define_block_label(create_node(R_coil, angle), copper)

        # Legres
        femm_problem.define_block_label(create_node(R_air_gap, angle), air_gap)

        # Magnes
        femm_problem.define_block_label(create_node(R_magnet, angle), magnet)

        # Rotor vas
        femm_problem.define_block_label(create_node(R_rotor_yoke, angle), steel)
    
    # Tengely/belso levego (Air)
    femm_problem.define_block_label(create_node(R_shaft_air, 0), air)
    # Kulso levego (Air)
    femm_problem.define_block_label(create_node(Rs_o * 1.05, 0), air)


def boundary_definitions(femm_problem: FemmProblem):
    # Dirichlet hatarfeltetel (A=0) a kulso es belso hatarokon
    a0 = MagneticDirichlet(name='a0', a_0=0, a_1=0, a_2=0, phi=0)
    femm_problem.add_boundary(a0)

    # Anti-periodikus hatarfeltetelek a radialis hatarokon
    apbc = MagneticAntiPeriodicAirgap('APairgap')
    femm_problem.add_boundary(apbc)
    
    # Periodikus peremfeltétel 45 fokos szegmenshez
    pb_radial = MagneticPeriodic("PB_Radial")
    femm_problem.add_boundary(pb_radial)

    # Atmerok
    Rs_o = STATOR_OUTER_DIAMETER / 2
    Rr_i = ROTOR_INNER_DIAMETER / 2
    Rr_o = ROTOR_OUTER_DIAMETER / 2
    Rs_i = Rr_o + AIR_GAP_LENGTH
    angle_deg = SEGMENT_ANGLE_DEG # 45 fok
    
    # Tangencialis hatarok (A=0 Dirichlet)
    femm_problem.set_boundary_definition_arc(create_node(Rs_o * 0.99, 0), a0)
    femm_problem.set_boundary_definition_arc(create_node(Rr_i * 1.01, 0), a0)

    # Radialis Periodikus hatarok
    R_mid = (Rs_o + Rr_i) / 2
    
    # 1. Alloresz oldalai
    femm_problem.set_boundary_definition_segment(create_node(R_mid, angle_deg/2), pb_radial)
    femm_problem.set_boundary_definition_segment(create_node(R_mid, -angle_deg/2), pb_radial)

    # Legres iveihez Anti-Periodic Airgap
    femm_problem.set_boundary_definition_arc(create_node(Rr_o + AIR_GAP_LENGTH / 3, 0), apbc)
    femm_problem.set_boundary_definition_arc(create_node(Rs_i - AIR_GAP_LENGTH / 3, 0), apbc)


def run_bldc_analysis(output_file="BLDC_cogging_torque.csv"):
    """Fo futtato funkcio a BLDC gep FEM analizisehez."""

    # 1. Problema definialasa
    problem = FemmProblem(out_file=output_file)
    # Planar problema mm-ben, melyseg az axialis hossz
    problem.magnetic_problem(0, LengthUnit.MILLIMETERS, "planar", depth=AXIAL_LENGTH)

    # 2. Geometria letrehozasa
    stator_geo = stator_geometry()
    rotor_geo = rotor_geometry()
    stator_geo.merge_geometry(rotor_geo)
    problem.create_geometry(stator_geo)

    # 3. Anyagok es gerjesztes definialasa
    material_definitions(problem)

    # 4. Peremfeltetelek beallitasa
    boundary_definitions(problem)

    # 5. Analizis es LUA fajl elkeszitese
    problem.make_analysis('bldc_fem_analysis')
    problem.write("BLDC_motor.lua")

    # 6. FEMM futtatasa
    femm = Executor()
    lua_file = os.path.join(os.getcwd(), "BLDC_motor.lua")
    print(f"FEM analizis futtatasa a {lua_file} fajllal...")
    # femm.run(lua_file)

    print("BLDC_motor.lua fajl generalva a FEMM analizishez.")


if __name__ == '__main__':
    run_bldc_analysis()