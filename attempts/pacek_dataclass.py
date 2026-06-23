import os
import dataclasses
import math
from math import sin, cos, asin, acos, pi, radians, degrees, tan, sqrt
from copy import copy
from dataclasses import dataclass

# importok
from src.magnetics import MagneticDirichlet, MagneticMaterial, MagneticAnti, MagneticAntiPeriodicAirgap, LamType, MagneticPeriodic
from src.femm_problem import FemmProblem
from src.general import LengthUnit
from src.geometry import Geometry, Line, Node, CircleArc
from src.executor import Executor


# parameterek
ORIGIN = Node(0.0, 0.0)
@dataclass
class MotorParameters:
    #BLDC motor geometriai es fizikat parametereit tartalmazo osztaly
    #geometriai meretek:

    axial_length: float = 50.0
    rotor_inner_diameter: float = 22.8
    rotor_outer_diameter: float = 55.1
    air_gap_length: float = 0.7
    stator_outer_diameter: float = 100.0
    tooth_root_diameter: float = 86.6
    

    #alloresz es fogazas

    stator_slots: int = 24
    segment_size: int = 3

    #magneses tulajdosagok

    magnet_height: float = 3.577
    magnet_hc: float = 724 * 1000
    magnet_mur: float = 1.11
    @property
    def segment_angle_deg(self) -> float:
        #automatikusan szamolt szegmens szog fokban
        return 360. / self.stator_slots * self.segment_size
    @property
    def slot_pitch_deg(self) -> float:
        """Két szomszédos horony közötti szög."""
        return 360.0 / self.stator_slots

    @property
    def tooth_width(self) -> float:
        """Dinamikus fogszélesség: a horonyosztás ívhosszának ~54%-a."""
        rs_i = self.rotor_outer_diameter / 2 + self.air_gap_length
        # Egy teljes horonyosztásra jutó ívhossz az állórész belső átmérőjén
        pitch_arc_length = (2 * math.pi * rs_i) / self.stator_slots
        return pitch_arc_length * 0.54

    @property
    def magnet_width(self) -> float:
        """Dinamikus mágnesszélesség, ami a horonyszámmal fordítottan arányosan skálázódik."""
        # 24 slot esetén az eredeti 15.9 mm-ből indulunk ki
        return 15.9 * (24 / self.stator_slots) * (self.segment_size / 3)
    @property
    def tooth_tip_angle_deg(self) -> float:
        """Dinamikus fogvég szög (a horonynyílás mérete)."""
        # A 24 hornyos alapérték (11.9 fok) arányosítása a tényleges horonyszámhoz
        return 11.9 * (24 / self.stator_slots)

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

def stator_geometry(params: MotorParameters) -> Geometry:
    stator_geo = Geometry()

    Rs_o = params.stator_outer_diameter / 2
    R_root = params.tooth_root_diameter / 2
    Rs_i = params.rotor_outer_diameter / 2 + params.air_gap_length
    
    shoe_angle = params.tooth_tip_angle_deg
    shoe_height = 1.0 
    
    base_shoe_L = create_node(Rs_i, -shoe_angle/2)
    base_shoe_R = create_node(Rs_i, shoe_angle/2)
    
    R_shoe_back = Rs_i + shoe_height
    x_body = params.tooth_width / 2
    y_body_start = sqrt(R_shoe_back**2 - x_body**2)
    y_body_end = sqrt(R_root**2 - x_body**2)
    
    base_neck_L = Node(-x_body, y_body_start)
    base_neck_R = Node(x_body, y_body_start)
    base_root_L = Node(-x_body, y_body_end)
    base_root_R = Node(x_body, y_body_end)

    bound_angle = params.segment_angle_deg / 2
    
    bound_R_in = create_node(Rs_i, bound_angle)
    bound_R_root = create_node(R_root, bound_angle)
    bound_R_out = create_node(Rs_o, bound_angle)
    
    bound_L_in = create_node(Rs_i, -bound_angle)
    bound_L_root = create_node(R_root, -bound_angle)
    bound_L_out = create_node(Rs_o, -bound_angle)

    slot_pitch = params.slot_pitch_deg
    tooth_angles = [-slot_pitch, 0, slot_pitch]
    
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
        
        # FIGYELEM! Most már MINDEN fogat egyformán, teljesen megrajzolunk!
        stator_geo.add_arc(CircleArc(sR, ORIGIN, sL)) 
        stator_geo.add_line(Line(sR, nR))
        stator_geo.add_line(Line(nL, sL))
        stator_geo.add_line(Line(nR, rR))
        stator_geo.add_line(Line(rL, nL))
        
        if angle > 0.1: # jobb_fog
            # Csak a maradék légrés ívet kötjük hozzá a jobb határvonalhoz
            stator_geo.add_arc(CircleArc(bound_R_in, ORIGIN, sR))
            tR_rR, tR_rL, tR_sR, tR_sL = rR, rL, sR, sL 
            
        elif angle < -0.1: # bal_fog
            # Csak a maradék légrés ív a bal határvonalhoz
            stator_geo.add_arc(CircleArc(sL, ORIGIN, bound_L_in))
            tL_rR, tL_rL, tL_sR, tL_sL = rR, rL, sR, sL
            
        else: # KOZEPSO_fog
            tM_rR, tM_rL, tM_sR, tM_sL = rR, rL, sR, sL
    
    # Yoke külső ív és a keret oldalai
    stator_geo.add_arc(CircleArc(bound_R_out, ORIGIN, bound_L_out))
    stator_geo.add_line(Line(bound_R_out, bound_R_in))
    stator_geo.add_line(Line(bound_L_in, bound_L_out))
    
    # Horony aljak összekötése (yoke belső ív)
    stator_geo.add_arc(CircleArc(bound_R_root, ORIGIN, tR_rR))
    stator_geo.add_arc(CircleArc(tR_rL, ORIGIN, tM_rR))
    stator_geo.add_arc(CircleArc(tM_rL, ORIGIN, tL_rR))
    stator_geo.add_arc(CircleArc(tL_rL, ORIGIN, bound_L_root))
    
    # A két teljes horony légrésének összekötése a fogak között
    stator_geo.add_arc(CircleArc(tR_sL, ORIGIN, tM_sR))
    stator_geo.add_arc(CircleArc(tM_sL, ORIGIN, tL_sR))

    return stator_geo

# rotor_geometria

def rotor_geometry(params: MotorParameters) -> Geometry:
    """Rotor geometria (Laposabb chamferrel)."""
    rotor_geo = Geometry()

    Rr_o = params.rotor_outer_diameter / 2
    Rr_i = params.rotor_inner_diameter / 2
    Mh = params.magnet_height
    
    angle_deg = params.segment_angle_deg
    angle_half = angle_deg / 2
    
    half_mw = params.magnet_width / 2 
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

def material_definitions(femm_problem: FemmProblem, params: MotorParameters):
    air = MagneticMaterial(material_name='air', mesh_size=1)
    stator_steel = MagneticMaterial(material_name='stator_steel', Sigma=1.9e6, lam_fill=0.98, Lam_d=0.34)
    stator_steel.b = [0, 0.6708, 1.0189, 1.4156, 1.5773, 2.3883, 3.6682]
    stator_steel.h = [0, 200, 700, 6773, 35206, 509252, 1527756]
    
    rotor_steel = MagneticMaterial(material_name='rotor_steel', Sigma=5.8e6)
    rotor_steel.b = [0, 0.8, 1.2, 1.5, 1.8, 2.0, 2.2]
    rotor_steel.h = [0, 400, 1000, 2500, 8000, 20000, 50000]

    magnet = MagneticMaterial(material_name='magnet', mu_x=params.magnet_mur, mu_y=params.magnet_mur, H_c=params.magnet_hc, Sigma=0.667e6)
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

    
    Rr_o = params.rotor_outer_diameter / 2
    Rr_i = params.rotor_inner_diameter / 2
    Rs_o = params.stator_outer_diameter / 2
    R_root = params.tooth_root_diameter / 2
    Rs_i = Rr_o + params.air_gap_length
    Mh = params.magnet_height
    
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
    
    # hornyok (Dinamikusan számolva a horonyszámhoz)
    R_slot_mid = (Rs_i + R_root) / 2
    
    # A belső hornyok pozíciója (a középső fog mellett)
    slot_inner = params.slot_pitch_deg / 2
    # A külső hornyok pozíciója (a szélső fogak és a határvonal között)
    slot_outer = params.slot_pitch_deg + (params.slot_pitch_deg / 4)
    
    femm_problem.define_block_label(create_node(R_slot_mid, slot_inner), copper)
    femm_problem.define_block_label(create_node(R_slot_mid, -slot_inner), copper)
    
    femm_problem.define_block_label(create_node(R_slot_mid, slot_outer), copper)
    femm_problem.define_block_label(create_node(R_slot_mid, -slot_outer), copper)

    
    # rotor_zsebek
    R_pocket = Rr_o - 1.0 
    bound_angle = params.segment_angle_deg / 2
    pocket_angle = bound_angle * 0.85

    femm_problem.define_block_label(create_node(R_pocket, 20.0), air)
    femm_problem.define_block_label(create_node(R_pocket, -20.0), air)


def boundary_definitions(femm_problem: FemmProblem, params: MotorParameters):
    a0 = MagneticDirichlet(name='a0', a_0=0, a_1=0, a_2=0, phi=0)
    femm_problem.add_boundary(a0)
    pb_radial = MagneticPeriodic("PB_Radial")
    femm_problem.add_boundary(pb_radial)

    Rr_i = params.rotor_inner_diameter / 2
    Rs_o = params.stator_outer_diameter / 2
    angle_deg = params.segment_angle_deg
    
    femm_problem.set_boundary_definition_arc(create_node(Rs_o * 0.99, 0), a0) 
    femm_problem.set_boundary_definition_arc(create_node(Rr_i * 1.01, 0), a0) 
    
    R_mid = (Rs_o + Rr_i) / 2
    femm_problem.set_boundary_definition_segment(create_node(R_mid, angle_deg/2), pb_radial)
    femm_problem.set_boundary_definition_segment(create_node(R_mid, -angle_deg/2), pb_radial)


def run_bldc_analysis(motor_params: MotorParameters = None, output_file="BLDC_whole_v2.csv"):
    my_motor = motor_params if motor_params is not None else MotorParameters()

    problem = FemmProblem(out_file=output_file)
    problem.magnetic_problem(0, LengthUnit.MILLIMETERS, "planar", depth=my_motor.axial_length)

    rotor_geo = rotor_geometry(my_motor)
    stator_geo = stator_geometry(my_motor)
    
    problem.create_geometry(rotor_geo)
    problem.create_geometry(stator_geo)

    material_definitions(problem, my_motor)
    boundary_definitions(problem, my_motor)

    problem.make_analysis('bldc_whole_v2_analysis')
    problem.write("BLDC_whole_v2.lua")

    femm = Executor()
    lua_file = os.path.join(os.getcwd(), "BLDC_whole_v2.lua")
    print(f"FEM analizis futtatasa: {lua_file}")
    femm.run(lua_file)

    print("BLDC_whole_v2.lua generalva.")


if __name__ == '__main__':
    run_bldc_analysis()