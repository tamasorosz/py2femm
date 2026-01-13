import os
import dataclasses
import math
from math import sin, cos, asin, acos, pi, radians, degrees, tan, sqrt
from copy import copy

# importok
from src.magnetics import MagneticDirichlet, MagneticMaterial, MagneticAnti, MagneticAntiPeriodicAirgap, LamType, MagneticPeriodic
from src.femm_problem import FemmProblem
from src.general import LengthUnit
from src.geometry import Geometry, Line, Node, CircleArc
from src.executor import Executor


# parameterek
ORIGIN = Node(0.0, 0.0)

AXIAL_LENGTH = 50.0
ROTOR_INNER_DIAMETER = 22.8
ROTOR_OUTER_DIAMETER = 55.1
AIR_GAP_LENGTH = 0.7
STATOR_OUTER_DIAMETER = 100.0
TOOTH_ROOT_DIAMETER = 86.6
MAGNET_WIDTH = 15.9
TOOTH_WIDTH = 4.0

STATOR_SLOTS = 24
SEGMENT_SIZE = 3
SEGMENT_ANGLE_DEG = 360 / STATOR_SLOTS * SEGMENT_SIZE # 45.0 deg

TOOTH_TIP_ANGLE_DEG = 11.9

MAGNET_HEIGHT = 3.577
MAGNET_HC = 724 * 1000
MAGNET_MUR = 1.11

# geometry_functions

def create_node(R, angle_deg):
    """Letrehoz egy pontot polaris koordinatakkal. +Szog = Jobbra."""
    angle_rad = radians(angle_deg)
    return Node(R * sin(angle_rad), R * cos(angle_rad))

def create_arc_pair(R, angle_deg):
    """Ket pont a szegmens szelen (+/- angle/2)"""
    p_left = create_node(R, -angle_deg / 2)
    p_right = create_node(R, angle_deg / 2)
    return p_left, p_right

def rotate_node(node, angle_deg):
    """Elforgat egy (x,y) pontot az origo korul."""
    rad = radians(angle_deg)
    x_new = node.x * cos(rad) + node.y * sin(rad)
    y_new = -node.x * sin(rad) + node.y * cos(rad)
    return Node(x_new, y_new)

# stator_geometry

def stator_geometry():
    """
    Kesziti az alloresz geometriajat.
    A 'whole_pacek.py' alapjan: JOBB -> BAL ivek.
    MODOSITAS: Szelso fogak levagva, valtozokeszlet javitva (NameError fix).
    """
    stator_geo = Geometry()

    # sugar
    Rs_o = STATOR_OUTER_DIAMETER / 2
    R_root = TOOTH_ROOT_DIAMETER / 2
    Rs_i = ROTOR_OUTER_DIAMETER / 2 + AIR_GAP_LENGTH
    
    # fog_definicio
    shoe_angle = TOOTH_TIP_ANGLE_DEG
    shoe_height = 1.0 
    
    # pontok
    base_shoe_L = create_node(Rs_i, -shoe_angle/2)
    base_shoe_R = create_node(Rs_i, shoe_angle/2)
    
    R_shoe_back = Rs_i + shoe_height
    x_body = TOOTH_WIDTH / 2
    y_body_start = sqrt(R_shoe_back**2 - x_body**2)
    y_body_end = sqrt(R_root**2 - x_body**2)
    
    base_neck_L = Node(-x_body, y_body_start)
    base_neck_R = Node(x_body, y_body_start)
    base_root_L = Node(-x_body, y_body_end)
    base_root_R = Node(x_body, y_body_end)

    # stator_side
    bound_R_in = create_node(Rs_i, 22.5)
    bound_R_root = create_node(R_root, 22.5)
    bound_R_out = create_node(Rs_o, 22.5)
    
    bound_L_in = create_node(Rs_i, -22.5)
    bound_L_root = create_node(R_root, -22.5)
    bound_L_out = create_node(Rs_o, -22.5)

    # fog_generalas
    tooth_angles = [-15, 0, 15]
    
    # valtozok
    tL_rR, tL_rL, tL_sR, tL_sL = None, None, None, None
    tM_rR, tM_rL, tM_sR, tM_sL = None, None, None, None
    tR_rR, tR_rL, tR_sR, tR_sL = None, None, None, None

    for angle in tooth_angles:
        sR = rotate_node(base_shoe_R, angle)
        sL = rotate_node(base_shoe_L, angle)
        nR = rotate_node(base_neck_R, angle)
        nL = rotate_node(base_neck_L, angle)
        rR = rotate_node(base_root_R, angle)
        rL = rotate_node(base_root_L, angle)
        
        # fog_levagas
        
        if angle == 15: # jobb_fog
            
            stator_geo.add_arc(CircleArc(bound_R_in, ORIGIN, sL))
            
            # Oldalak
            stator_geo.add_line(Line(bound_R_in, nR)) # Jobb_oldal
            stator_geo.add_line(Line(nL, sL))
            stator_geo.add_line(Line(nR, rR))
            stator_geo.add_line(Line(rL, nL))
            
            # adatok_csatlakozashoz
            tR_rR, tR_rL = rR, rL
            tR_sL = sL 
            
            
        elif angle == -15: # bal_fog
            stator_geo.add_arc(CircleArc(sR, ORIGIN, bound_L_in))
            
            # Oldalak
            stator_geo.add_line(Line(sR, nR))
            stator_geo.add_line(Line(nL, bound_L_in)) # Bal_oldal
            stator_geo.add_line(Line(nR, rR))
            stator_geo.add_line(Line(rL, nL))
            
            # adatok_csatlakozashoz
            tL_rR, tL_rL = rR, rL
            tL_sR = sR
            
            
        else: # KOZEPSO_fog
            stator_geo.add_arc(CircleArc(sR, ORIGIN, sL)) 
            stator_geo.add_line(Line(sR, nR))
            stator_geo.add_line(Line(nL, sL))
            stator_geo.add_line(Line(nR, rR))
            stator_geo.add_line(Line(rL, nL))
            
            tM_rR, tM_rL = rR, rL
            tM_sR, tM_sL = sR, sL

    # osszekotesek_jobbrol_balra
    
    # yoke
    stator_geo.add_arc(CircleArc(bound_R_out, ORIGIN, bound_L_out))
    

    stator_geo.add_line(Line(bound_R_out, bound_R_in))
    stator_geo.add_line(Line(bound_L_in, bound_L_out))
    
    # horony
    stator_geo.add_arc(CircleArc(bound_R_root, ORIGIN, tR_rR))
    
    stator_geo.add_arc(CircleArc(tR_rL, ORIGIN, tM_rR))
    
    stator_geo.add_arc(CircleArc(tM_rL, ORIGIN, tL_rR))
    
    stator_geo.add_arc(CircleArc(tL_rL, ORIGIN, bound_L_root))
    

    stator_geo.add_arc(CircleArc(tR_sL, ORIGIN, tM_sR))
    
    stator_geo.add_arc(CircleArc(tM_sL, ORIGIN, tL_sR))

    return stator_geo

# rotor_geometria

def rotor_geometry():
    """Rotor geometria (Laposabb chamferrel)."""
    rotor_geo = Geometry()

    Rr_o = ROTOR_OUTER_DIAMETER / 2
    Rr_i = ROTOR_INNER_DIAMETER / 2
    Mh = MAGNET_HEIGHT
    
    angle_deg = SEGMENT_ANGLE_DEG
    angle_half = angle_deg / 2
    
    half_mw = MAGNET_WIDTH / 2 
    R_mag_top = Rr_o 
    x_mag_side = half_mw
    y_rro = math.sqrt(R_mag_top**2 - x_mag_side**2) 
    Y_ROTOR_TOP_FLAT = y_rro - Mh 
    
    p_iron_top_L = Node(-half_mw, Y_ROTOR_TOP_FLAT)
    p_iron_top_R = Node(half_mw, Y_ROTOR_TOP_FLAT)
    
    CHAMFER_DEPTH = 0.8 
    Y_CHAMFER_END = Y_ROTOR_TOP_FLAT - CHAMFER_DEPTH
    tan_angle = math.tan(radians(angle_half))
    X_chamfer = Y_CHAMFER_END * tan_angle
    
    p_chamfer_L = Node(-X_chamfer, Y_CHAMFER_END)
    p_chamfer_R = Node(X_chamfer, Y_CHAMFER_END)
    
    p_in_L = create_node(Rr_i, -angle_half)
    p_in_R = create_node(Rr_i, angle_half)
    
    # rotor_vas
    rotor_geo.add_line(Line(p_chamfer_L, p_iron_top_L))
    rotor_geo.add_line(Line(p_iron_top_L, p_iron_top_R))
    rotor_geo.add_line(Line(p_iron_top_R, p_chamfer_R))
    rotor_geo.add_line(Line(p_chamfer_R, p_in_R))
    rotor_geo.add_arc(CircleArc(p_in_R, ORIGIN, p_in_L)) 
    rotor_geo.add_line(Line(p_in_L, p_chamfer_L))
    
    # magnes
    p_mag_out_L = Node(-x_mag_side, y_rro)
    p_mag_out_R = Node(x_mag_side, y_rro)

    rotor_geo.add_arc(CircleArc(p_mag_out_R, ORIGIN, p_mag_out_L))
    rotor_geo.add_line(Line(p_iron_top_L, p_iron_top_R)) 
    rotor_geo.add_line(Line(p_mag_out_L, p_iron_top_L))
    rotor_geo.add_line(Line(p_mag_out_R, p_iron_top_R))
    
    return rotor_geo

# anyagok_labels

def material_definitions(femm_problem: FemmProblem):
    air = MagneticMaterial(material_name='air', mesh_size=1)
    stator_steel = MagneticMaterial(material_name='stator_steel', Sigma=1.9e6, lam_fill=0.98, Lam_d=0.34)
    stator_steel.b = [0, 0.6708, 1.0189, 1.4156, 1.5773, 2.3883, 3.6682]
    stator_steel.h = [0, 200, 700, 6773, 35206, 509252, 1527756]
    
    rotor_steel = MagneticMaterial(material_name='rotor_steel', Sigma=5.8e6)
    rotor_steel.b = [0, 0.8, 1.2, 1.5, 1.8, 2.0, 2.2]
    rotor_steel.h = [0, 400, 1000, 2500, 8000, 20000, 50000]

    magnet = MagneticMaterial(material_name='magnet', mu_x=MAGNET_MUR, mu_y=MAGNET_MUR, H_c=MAGNET_HC, Sigma=0.667e6)
    magnet.mesh_size = 1
    magnet.remanence_angle = 90 
    
    copper = MagneticMaterial(material_name='copper', J=0, Sigma=58e6, LamType=LamType.MAGNET_WIRE)
    air_gap = MagneticMaterial(material_name='air_gap', mesh_size=0.5)

    femm_problem.add_material(air)
    femm_problem.add_material(stator_steel)
    femm_problem.add_material(rotor_steel)
    femm_problem.add_material(magnet)
    femm_problem.add_material(copper)
    femm_problem.add_material(air_gap)

    
    Rr_o = ROTOR_OUTER_DIAMETER / 2
    Rr_i = ROTOR_INNER_DIAMETER / 2
    Rs_o = STATOR_OUTER_DIAMETER / 2
    R_root = TOOTH_ROOT_DIAMETER / 2
    Rs_i = Rr_o + AIR_GAP_LENGTH
    Mh = MAGNET_HEIGHT
    
    # rotorvas
    R_rotor_yoke = (Rr_i + (Rr_o - Mh)) / 2
    femm_problem.define_block_label(create_node(R_rotor_yoke, 0), rotor_steel)
    
    # magnes
    R_magnet_center = Rr_o - Mh / 2
    femm_problem.define_block_label(create_node(R_magnet_center, 0), magnet)
    
    # legres
    R_air_mid = (Rs_i + Rr_o) / 2
    femm_problem.define_block_label(create_node(R_air_mid, 0), air_gap)
    
    # tengely
    femm_problem.define_block_label(create_node(Rr_i * 0.5, 0), air)
    
    # statorvas
    R_stator_yoke = (R_root + Rs_o) / 2
    femm_problem.define_block_label(create_node(R_stator_yoke, 0), stator_steel)
    
    # hornyok
    R_slot_mid = (Rs_i + R_root) / 2
    
    femm_problem.define_block_label(create_node(R_slot_mid, 7.5), copper)
    femm_problem.define_block_label(create_node(R_slot_mid, -7.5), copper)
    
    
    femm_problem.define_block_label(create_node(R_slot_mid, 21.0), copper)
    femm_problem.define_block_label(create_node(R_slot_mid, -21.0), copper)

    
    # rotor_zsebek
    R_pocket = Rr_o - 1.0 
    femm_problem.define_block_label(create_node(R_pocket, 20.0), air)
    femm_problem.define_block_label(create_node(R_pocket, -20.0), air)


def boundary_definitions(femm_problem: FemmProblem):
    a0 = MagneticDirichlet(name='a0', a_0=0, a_1=0, a_2=0, phi=0)
    femm_problem.add_boundary(a0)
    pb_radial = MagneticPeriodic("PB_Radial")
    femm_problem.add_boundary(pb_radial)

    Rr_i = ROTOR_INNER_DIAMETER / 2
    Rs_o = STATOR_OUTER_DIAMETER / 2
    angle_deg = SEGMENT_ANGLE_DEG
    
    femm_problem.set_boundary_definition_arc(create_node(Rs_o * 0.99, 0), a0) 
    femm_problem.set_boundary_definition_arc(create_node(Rr_i * 1.01, 0), a0) 
    
    R_mid = (Rs_o + Rr_i) / 2
    femm_problem.set_boundary_definition_segment(create_node(R_mid, angle_deg/2), pb_radial)
    femm_problem.set_boundary_definition_segment(create_node(R_mid, -angle_deg/2), pb_radial)


def run_bldc_analysis(output_file="BLDC_whole_v2.csv"):
    problem = FemmProblem(out_file=output_file)
    problem.magnetic_problem(0, LengthUnit.MILLIMETERS, "planar", depth=AXIAL_LENGTH)

    rotor_geo = rotor_geometry()
    stator_geo = stator_geometry()
    
    problem.create_geometry(rotor_geo)
    problem.create_geometry(stator_geo)

    material_definitions(problem)
    boundary_definitions(problem)

    problem.make_analysis('bldc_whole_v2_analysis')
    problem.write("BLDC_whole_v2.lua")

    femm = Executor()
    lua_file = os.path.join(os.getcwd(), "BLDC_whole_v2.lua")
    print(f"FEM analizis futtatasa: {lua_file}")
    femm.run(lua_file)

    print("BLDC_whole_v2.lua generalva.")


if __name__ == '__main__':
    run_bldc_analysis()