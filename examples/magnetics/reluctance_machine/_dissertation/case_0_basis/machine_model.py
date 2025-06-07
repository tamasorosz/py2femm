import math
import os
from pathlib import Path

import numpy as np

from src.femm_problem import FemmProblem
from src.general import LengthUnit
from src.geometry import Geometry, Node, Sector, CircleArc, Line
from src.magnetics import (MagneticDirichlet,
                           MagneticPeriodicAirgap,
                           MagneticPeriodic,
                           MagneticBoundaryModification,
                           MagneticMaterial,
                           LamType,
                           MagneticVolumeIntegral)

# Current folder path to designate temporary folders for the .lua files ------------------------------------------------
current_folder_path = str(Path(__file__).resolve().parent).replace("\\", "/")

# Global variable, the 0,0 point of the coordinate system --------------------------------------------------------------
n0 = Node(0, 0)


# Variable parameters class contains all the variables for the machine model -------------------------------------------
class VariableParameters:
    """Store all the variables to create the machine model."""

    def __init__(self,
                 output_folder_name,  # --> To specify the name of the temporary folders containing simulation files ---
                 output_file_name,  # --> To specify the name of the temporary simulation files ------------------------
                 output_file_counter,  # --> To differ between the temporary files -------------------------------------
                 current_density,  # --> To specify the current density in the slot ------------------------------------
                 initial_current_angle,  # --> To specify the initial current angle from which the simulation starts ---
                 current_angle,  # --> To specify the current angle of the simulation ----------------------------------
                 rotor_position,  # --> To specify the rotor position --------------------------------------------------
                 X1_cut_off_barrier_opening_angle,  # --> To specify the opening angle of the cut-off barrier (X1) -----
                 X2_cut_off_barrier_curve_angle,  # --> To specify the depth of the cut-off barrier (X2)
                 X3_cut_off_barrier_internal_barrier_distance,
                 # --> To specify the distance between the cut-off barrier and internal barrier (X3)
                 X4_rib_width_upper,  # --> To specify the rib with between internal barriers (X4) ---------------------
                 X5_internal_barrier_height_upper,  # --> To specify the height of the internal barrier (X5) -----------
                 X6_internal_barrier_lower_barrier_distance,
                 # --> To specify the distance between the upper and lower internal barrier (X6)
                 X7_rib_width_lower,  # --> To specify the rib with between internal barriers (X7) ---------------------
                 X8_internal_barrier_height_lower,  # --> To specify the height of the internal barrier (X8) -----------
                 X9_magnet_pocket_width,  # --> To specify the width of the magnet pocket (X9) -------------------------
                 X10_magnet_pocket_height,  # --> To specify the height of the magnet pocket (X10) ---------------------
                 X11_magnet_pocket_shift,  # --> To specify the magnet pocket shift (X11) ------------------------------
                 X12_distance_magnet_pocket_internal_barrier,  # --> To specify the distance between the magnet pocket and the internal barrier (X12)
                 X13_distance_internal_barriers,  # --> To specify the distance between the internal barriers (X13)
                 X14_magnet_width,  # --> To specify the width of the magnet (X14) -------------------------------------
                 X15_magnet_height,  # --> To specify the height of the magnet (X15) -----------------------------------
                 X16_magnet_shift,  # --> To specify the shift of the magnet (X16) -------------------------------------

                 ):
        # Define the output file path which is the name of the temporary simulation file -------------------------------
        # --> update_output_folder_name
        # --> update_output_file_name
        # --> update_output_file_counter
        # --> update_output_folder_path
        # --> update_output_file_path

        self.output_folder_name = output_folder_name
        self.output_file_name = output_file_name
        self.output_file_counter = output_file_counter

        self.output_folder_path = f"{current_folder_path}/{self.output_folder_name}"
        self.output_file_path = f"{current_folder_path}/{self.output_folder_name}/{self.output_file_name}_{self.output_file_counter}"

        # Calculates the positive and negative phases in the slot as symmetric three-phase sinusoidal excitation -------
        # --> update_current_density
        # --> update_initial_current_angle
        # --> update_current_angle
        # --> update_phases

        # slot_area = 53.5104  # Area of the slot [mm^2]
        # coil_turns = 11      # Turns of the coil in one slot [u.]

        self.current_density = current_density
        self.initial_current_angle = initial_current_angle
        self.current_angle = current_angle

        self.JAp = self.current_density * math.cos(math.radians(self.initial_current_angle + self.current_angle)),
        self.JAn = (-1) * self.JAp
        self.JBp = self.current_density * math.cos(math.radians(self.initial_current_angle + self.current_angle + 120)),
        self.JBn = (-1) * self.JBp
        self.JCp = self.current_density * math.cos(math.radians(self.initial_current_angle + self.current_angle + 240)),
        self.JCn = (-1) * self.JCp

        # Defines the design variables for the rotor -------------------------------------------------------------------
        self.X1_cut_off_barrier_opening_angle = X1_cut_off_barrier_opening_angle
        self.X2_cut_off_barrier_curve_angle = X2_cut_off_barrier_curve_angle
        self.X3_cut_off_barrier_internal_barrier_distance = X3_cut_off_barrier_internal_barrier_distance
        self.X4_rib_width_upper = X4_rib_width_upper
        self.X5_internal_barrier_height_upper = X5_internal_barrier_height_upper
        self.X6_internal_barrier_lower_barrier_distance = X6_internal_barrier_lower_barrier_distance
        self.X7_rib_width_lower = X7_rib_width_lower
        self.X8_internal_barrier_height_lower = X8_internal_barrier_height_lower
        self.X9_magnet_pocket_width = X9_magnet_pocket_width
        self.X10_magnet_pocket_height = X10_magnet_pocket_height
        self.X11_magnet_pocket_shift = X11_magnet_pocket_shift
        self.X12_distance_magnet_pocket_internal_barrier = X12_distance_magnet_pocket_internal_barrier
        self.X13_distance_internal_barriers = X13_distance_internal_barriers
        self.X14_magnet_width = X14_magnet_width
        self.X15_magnet_height = X15_magnet_height
        self.X16_magnet_shift = X16_magnet_shift

        # Defines the rotor position -----------------------------------------------------------------------------------
        # --> update_rotor_position
        self.rotor_position = rotor_position

    def update_output_folder_name(self, new_output_folder_name):
        """ Update folder and regenerate output_file and output_folder dynamically. """

        self.output_folder_name = new_output_folder_name
        self.update_output_file_path()
        self.update_output_folder_path()

    def update_output_file_name(self, new_output_file_name):
        """ Update file and regenerate output_file and output_folder dynamically. """

        self.output_file_name = new_output_file_name
        self.update_output_file_path()
        self.update_output_folder_path()

    def update_output_file_counter(self, new_output_file_counter):
        """ Update file counter and regenerate output_file and output_folder dynamically. """

        self.output_file_counter = new_output_file_counter
        self.update_output_file_path()
        self.update_output_folder_path()

    def update_output_folder_path(self):
        """ Update output_folder dynamically whenever it changes. """

        self.output_folder_path = f"{current_folder_path}/{self.output_folder_name}"

    def update_output_file_path(self):
        """ Update output_file dynamically whenever it changes. """

        self.output_file_path = f"{current_folder_path}/{self.output_folder_name}/{self.output_file_name}_{self.output_file_counter}"

    def update_current_density(self, new_current_density):
        """ Update current_density dynamically whenever the current density changes. Plus update phases. """

        self.current_density = new_current_density
        self.update_phases()

    def update_initial_current_angle(self, new_initial_current_angle):
        """ Update initial_current_angle dynamically whenever the initial current angle changes,
         so the simulation starts from that state. Plus update phases. """

        self.initial_current_angle = new_initial_current_angle
        self.update_phases()

    def update_current_angle(self, new_current_angle):
        """ Update current_angle dynamically whenever the current angle changes,
         so the stator magnetic field is rotated. Plus update phases. """

        self.current_angle = new_current_angle
        self.update_phases()

    def update_phases(self):
        """ Update phases dynamically whenever the current density, the initial current angle
         or the current angle changes. """

        self.JAp = self.current_density * math.cos(math.radians(self.initial_current_angle + self.current_angle)),
        self.JAn = (-1) * self.JAp
        self.JBp = self.current_density * math.cos(math.radians(self.initial_current_angle + self.current_angle + 120)),
        self.JBn = (-1) * self.JBp
        self.JCp = self.current_density * math.cos(math.radians(self.initial_current_angle + self.current_angle + 240)),
        self.JCn = (-1) * self.JCp

    def update_rotor_position(self, new_rotor_position):
        """ Update rotor_position """

        self.rotor_position = new_rotor_position


def define_stator_geometry(model: FemmProblem):
    """ Import stator geometry from a .dxf file with airgap sliding band: https://www.femm.info/wiki/SlidingBand """

    try:
        stator_geometry = Geometry()
        stator_geometry.import_dxf("resources/stator.dxf")
        model.create_geometry(stator_geometry)
        return True
    except ImportError:
        raise Exception("Can't import dxf geometry!")


def define_rotor_geometry(model: FemmProblem, var: VariableParameters):
    """ Define the parametric rotor geometry with 1/4 geometry and symmetric boundary condition """

    try:
        rotor_geometry = Geometry()

        rotor_geometry.add_node(n0)  # <<-- FOR DEBUGGING!==============================================================

        # Define the shaft geometry ------------------------------------------------------------------------------------
        shaft_horizontal_node = Node(6.00, 0.00)
        shaft_vertical_node = shaft_horizontal_node.rotate_about(n0, 90, True)

        rotor_geometry.add_node(shaft_horizontal_node)
        rotor_geometry.add_node(shaft_vertical_node)

        shaft_arc = CircleArc(shaft_horizontal_node, n0, shaft_vertical_node)

        rotor_geometry.add_arc(shaft_arc)

        # Define air gap arc and sliding band arc ----------------------------------------------------------------------
        sliding_band_left = Node(0.00, 22.10)
        sliding_band_right = Node(22.10, 0.00)

        rotor_geometry.add_node(sliding_band_left)
        rotor_geometry.add_node(sliding_band_right)

        sliding_band_arc = CircleArc(sliding_band_right, n0, sliding_band_left)

        rotor_geometry.add_arc(sliding_band_arc)

        # Define cut-off barrier arcs ----------------------------------------------------------------------------------
        # Cut-off barrier in the middle --------------------------------------------------------------------------------
        cut_off_barrier_middle_left = Node(22, 0).rotate_about(n0, 45 + var.X1_cut_off_barrier_opening_angle / 2,
                                                               degrees=True)
        cut_off_barrier_middle_right = Node(22, 0).rotate_about(n0, 45 - var.X1_cut_off_barrier_opening_angle / 2,
                                                                degrees=True)

        rotor_geometry.add_node(cut_off_barrier_middle_left)
        rotor_geometry.add_node(cut_off_barrier_middle_right)

        cut_off_barrier_middle_arc = Sector(cut_off_barrier_middle_left, cut_off_barrier_middle_right,
                                            var.X2_cut_off_barrier_curve_angle)

        rotor_geometry.add_sector(cut_off_barrier_middle_arc)

        rotor_geometry.add_node(cut_off_barrier_middle_arc.center_point())  # <<-- FOR DEBUGGING!=======================
        rotor_geometry.add_node(cut_off_barrier_middle_arc.selection_point())  # <<-- FOR DEBUGGING!====================

        # Left cut-off barrier right half ------------------------------------------------------------------------------
        cut_off_barrier_left_half_upper = cut_off_barrier_middle_right.rotate_about(n0, 45, degrees=True)
        rotor_geometry.add_node(cut_off_barrier_left_half_upper)

        cut_off_barrier_middle_selection_point = cut_off_barrier_middle_arc.selection_point()

        cut_off_barrier_left_half_lower = cut_off_barrier_middle_selection_point.rotate_about(n0, 45, degrees=True)
        rotor_geometry.add_node(cut_off_barrier_left_half_lower)

        cut_off_barrier_left_half_arc = Sector(cut_off_barrier_left_half_lower, cut_off_barrier_left_half_upper,
                                               var.X2_cut_off_barrier_curve_angle / 2)
        rotor_geometry.add_sector(cut_off_barrier_left_half_arc)

        rotor_geometry.add_node(cut_off_barrier_left_half_arc.center_point())  # <<-- FOR DEBUGGING!====================
        rotor_geometry.add_node(cut_off_barrier_left_half_arc.selection_point())  # <<-- FOR DEBUGGING!=================

        # Right cut-off barrier left half ------------------------------------------------------------------------------
        cut_off_barrier_right_half_upper = cut_off_barrier_middle_left.rotate_about(n0, -45, degrees=True)
        rotor_geometry.add_node(cut_off_barrier_right_half_upper)

        cut_off_barrier_right_half_lower = cut_off_barrier_middle_selection_point.rotate_about(n0, -45, degrees=True)
        rotor_geometry.add_node(cut_off_barrier_right_half_lower)

        cut_off_barrier_right_half_arc = Sector(cut_off_barrier_right_half_upper, cut_off_barrier_right_half_lower,
                                                var.X2_cut_off_barrier_curve_angle / 2)
        rotor_geometry.add_sector(cut_off_barrier_right_half_arc)

        rotor_geometry.add_node(
            cut_off_barrier_right_half_arc.center_point())  # <<-- FOR DEBUGGING!====================
        rotor_geometry.add_node(
            cut_off_barrier_right_half_arc.selection_point())  # <<-- FOR DEBUGGING!=================

        # Lines of the symmetric boundary conditions -------------------------------------------------------------------
        # Left side ----------------------------------------------------------------------------------------------------
        boundary_line_left_1 = Line(shaft_vertical_node, cut_off_barrier_left_half_lower)
        boundary_line_left_2 = Line(cut_off_barrier_left_half_lower, sliding_band_left)

        rotor_geometry.add_line(boundary_line_left_1)
        rotor_geometry.add_line(boundary_line_left_2)

        # Right side ---------------------------------------------------------------------------------------------------
        boundary_line_right_1 = Line(shaft_horizontal_node, cut_off_barrier_right_half_lower)
        boundary_line_right_2 = Line(cut_off_barrier_right_half_lower, sliding_band_right)

        rotor_geometry.add_line(boundary_line_right_1)
        rotor_geometry.add_line(boundary_line_right_2)

        # Definition of the rib between the internal barriers ----------------------------------------------------------
        # Upper internal barrier ---------------------------------------------------------------------------------------
        # Upper nodes --------------------------------------------------------------------------------------------------
        upper_rib_base_node_distance_from_cut_off_barrier_center_point_upper = cut_off_barrier_middle_arc.selection_point().distance_to(
            cut_off_barrier_middle_arc.center_point()) + var.X3_cut_off_barrier_internal_barrier_distance
        upper_rib_base_node_distance_from_zero_upper = cut_off_barrier_middle_arc.selection_point().distance_to(
            n0) - var.X3_cut_off_barrier_internal_barrier_distance
        upper_rib_base_node_upper = Node(upper_rib_base_node_distance_from_zero_upper, 0).rotate_about(n0, 45,
                                                                                                       degrees=True)

        rotor_geometry.add_node(
            upper_rib_base_node_upper)  # <<-- FOR DEBUGGING!========================================

        upper_rib_upper_rotation_angle = math.asin(
            (var.X4_rib_width_upper / 2) / upper_rib_base_node_distance_from_cut_off_barrier_center_point_upper)

        upper_rib_upper_node_left = upper_rib_base_node_upper.rotate_about(cut_off_barrier_middle_arc.center_point(),
                                                                           - upper_rib_upper_rotation_angle,
                                                                           degrees=False)
        upper_rib_upper_node_right = upper_rib_base_node_upper.rotate_about(cut_off_barrier_middle_arc.center_point(),
                                                                            upper_rib_upper_rotation_angle,
                                                                            degrees=False)

        rotor_geometry.add_node(upper_rib_upper_node_left)
        rotor_geometry.add_node(upper_rib_upper_node_right)

        # Lower nodes --------------------------------------------------------------------------------------------------
        upper_rib_base_node_distance_from_cut_off_barrier_center_point_lower = cut_off_barrier_middle_arc.selection_point().distance_to(
            cut_off_barrier_middle_arc.center_point()) + var.X5_internal_barrier_height_upper + var.X3_cut_off_barrier_internal_barrier_distance
        upper_rib_base_node_distance_from_zero_lower = cut_off_barrier_middle_arc.selection_point().distance_to(
            n0) - var.X5_internal_barrier_height_upper - var.X3_cut_off_barrier_internal_barrier_distance
        upper_rib_base_node_lower = Node(upper_rib_base_node_distance_from_zero_lower, 0).rotate_about(n0, 45,
                                                                                                       degrees=True)

        rotor_geometry.add_node(upper_rib_base_node_lower)  # <<-- FOR DEBUGGING!=======================================

        upper_rib_lower_rotation_angle = math.asin(
            (var.X4_rib_width_upper / 2) / upper_rib_base_node_distance_from_cut_off_barrier_center_point_lower)

        upper_rib_lower_node_left = upper_rib_base_node_lower.rotate_about(cut_off_barrier_middle_arc.center_point(),
                                                                           - upper_rib_lower_rotation_angle,
                                                                           degrees=False)
        upper_rib_lower_node_right = upper_rib_base_node_lower.rotate_about(cut_off_barrier_middle_arc.center_point(),
                                                                            upper_rib_lower_rotation_angle,
                                                                            degrees=False)

        rotor_geometry.add_node(upper_rib_lower_node_left)
        rotor_geometry.add_node(upper_rib_lower_node_right)

        rotor_geometry.add_line(Line(upper_rib_lower_node_left, upper_rib_upper_node_left))
        rotor_geometry.add_line(Line(upper_rib_lower_node_right, upper_rib_upper_node_right))

        # Lower internal barrier ---------------------------------------------------------------------------------------
        # Upper nodes --------------------------------------------------------------------------------------------------
        lower_rib_base_node_distance_from_cut_off_barrier_center_point_upper = upper_rib_base_node_lower.distance_to(
            cut_off_barrier_middle_arc.center_point()) + var.X6_internal_barrier_lower_barrier_distance
        lower_rib_base_node_distance_from_zero_upper = upper_rib_base_node_lower.distance_to(
            n0) - var.X6_internal_barrier_lower_barrier_distance
        lower_rib_base_node_upper = Node(lower_rib_base_node_distance_from_zero_upper, 0).rotate_about(n0, 45,
                                                                                                       degrees=True)

        rotor_geometry.add_node(lower_rib_base_node_upper)  # <<-- FOR DEBUGGING!=======================================

        lower_rib_upper_rotation_angle = math.asin(
            (var.X7_rib_width_lower / 2) / lower_rib_base_node_distance_from_cut_off_barrier_center_point_upper)

        lower_rib_upper_node_left = lower_rib_base_node_upper.rotate_about(cut_off_barrier_middle_arc.center_point(),
                                                                           - lower_rib_upper_rotation_angle,
                                                                           degrees=False)
        lower_rib_upper_node_right = lower_rib_base_node_upper.rotate_about(cut_off_barrier_middle_arc.center_point(),
                                                                            lower_rib_upper_rotation_angle,
                                                                            degrees=False)

        rotor_geometry.add_node(lower_rib_upper_node_left)
        rotor_geometry.add_node(lower_rib_upper_node_right)

        # Lower nodes --------------------------------------------------------------------------------------------------
        lower_rib_base_node_distance_from_cut_off_barrier_center_point_lower = upper_rib_base_node_lower.distance_to(
            cut_off_barrier_middle_arc.center_point()) + var.X8_internal_barrier_height_lower + var.X6_internal_barrier_lower_barrier_distance
        lower_rib_base_node_distance_from_zero_lower = upper_rib_base_node_lower.distance_to(
            n0) - var.X8_internal_barrier_height_lower - var.X6_internal_barrier_lower_barrier_distance
        lower_rib_base_node_lower = Node(lower_rib_base_node_distance_from_zero_lower, 0).rotate_about(n0, 45,
                                                                                                       degrees=True)

        rotor_geometry.add_node(lower_rib_base_node_lower)  # <<-- FOR DEBUGGING!======================================

        lower_rib_lower_rotation_angle = math.asin(
            (var.X7_rib_width_lower / 2) / lower_rib_base_node_distance_from_cut_off_barrier_center_point_lower)

        lower_rib_lower_node_left = lower_rib_base_node_lower.rotate_about(cut_off_barrier_middle_arc.center_point(),
                                                                           - lower_rib_lower_rotation_angle,
                                                                           degrees=False)
        lower_rib_lower_node_right = lower_rib_base_node_lower.rotate_about(cut_off_barrier_middle_arc.center_point(),
                                                                            lower_rib_lower_rotation_angle,
                                                                            degrees=False)

        rotor_geometry.add_node(lower_rib_lower_node_left)
        rotor_geometry.add_node(lower_rib_lower_node_right)

        rotor_geometry.add_line(Line(lower_rib_lower_node_left, lower_rib_upper_node_left))
        rotor_geometry.add_line(Line(lower_rib_lower_node_right, lower_rib_upper_node_right))

        # Magnet pocket definition -------------------------------------------------------------------------------------
        # Magnet pocket left upper nodes--------------------------------------------------------------------------------
        # Left----------------------------------------------------------------------------------------------------------
        magnet_pocket_left_base_node_upper = Line(cut_off_barrier_middle_left,
                                                  cut_off_barrier_left_half_upper).selection_point()

        # rotor_geometry.add_node(magnet_pocket_left_base_node_upper)  # <<-- FOR DEBUGGING================================

        width_magnet_pocket_left_upperleft = math.tan(
            np.radians(var.X9_magnet_pocket_width / 2)) * magnet_pocket_left_base_node_upper.distance_to(n0)
        # print(width_magnet_pocket_left_upperleft)  # <<-- FOR DEBUGGING=================================================

        magnet_pocket_left_upperleft_x_no_shift = magnet_pocket_left_base_node_upper.x - math.sin(
            np.radians(67.5)) * width_magnet_pocket_left_upperleft
        magnet_pocket_left_upperleft_y_no_shift = magnet_pocket_left_base_node_upper.y + math.cos(
            np.radians(67.5)) * width_magnet_pocket_left_upperleft
        magnet_pocket_left_upperleft_no_shift = Node(magnet_pocket_left_upperleft_x_no_shift,
                                                     magnet_pocket_left_upperleft_y_no_shift)

        # rotor_geometry.add_node(magnet_pocket_left_upperleft_no_shift)  # <<-- FOR DEBUGGING============================

        if var.X11_magnet_pocket_shift == 0:
            magnet_pocket_left_upperleft = magnet_pocket_left_upperleft_no_shift
        else:
            magnet_pocket_left_upperleft_distance_shift = magnet_pocket_left_upperleft_no_shift.distance_to(
                n0) * math.sin(np.radians(var.X11_magnet_pocket_shift)) / math.sin(
                np.radians(90 - var.X11_magnet_pocket_shift - var.X9_magnet_pocket_width / 2))
            # print(magnet_pocket_left_upperleft_distance_shift)  # <<-- FOR DEBUGGING====================================

            magnet_pocket_left_upperleft_x = magnet_pocket_left_upperleft_x_no_shift - math.sin(
                np.radians(67.5)) * magnet_pocket_left_upperleft_distance_shift
            magnet_pocket_left_upperleft_y = magnet_pocket_left_upperleft_y_no_shift + math.cos(
                np.radians(67.5)) * magnet_pocket_left_upperleft_distance_shift
            magnet_pocket_left_upperleft = Node(magnet_pocket_left_upperleft_x, magnet_pocket_left_upperleft_y)

        a = magnet_pocket_left_upperleft.distance_to(n0)
        b = 22
        B = np.radians(
            180 - np.degrees(math.atan2(magnet_pocket_left_upperleft.y, magnet_pocket_left_upperleft.x)) + 67.5)
        A = math.asin((a * math.sin(B)) / b)
        C = math.pi - A - B
        c = math.sqrt(a ** 2 + b ** 2 - 2 * a * b * math.cos(C))

        magnet_pocket_left_upperleft_on_radius_x = magnet_pocket_left_upperleft.x + math.sin(np.radians(90 - 67.5)) * c
        magnet_pocket_left_upperleft_on_radius_y = magnet_pocket_left_upperleft.y + math.cos(np.radians(90 - 67.5)) * c
        magnet_pocket_left_upperleft_on_radius = Node(magnet_pocket_left_upperleft_on_radius_x,
                                                      magnet_pocket_left_upperleft_on_radius_y)

        rotor_geometry.add_node(magnet_pocket_left_upperleft_on_radius)

        # Right----------------------------------------------------------------------------------------------------------
        width_magnet_pocket_left_upperright = math.tan(
            np.radians(var.X9_magnet_pocket_width / 2)) * magnet_pocket_left_base_node_upper.distance_to(n0)
        # print(width_magnet_pocket_left_upperright)  # <<-- FOR DEBUGGING================================================

        magnet_pocket_left_upperright_x_no_shift = magnet_pocket_left_base_node_upper.x + math.sin(
            np.radians(67.5)) * width_magnet_pocket_left_upperright
        magnet_pocket_left_upperright_y_no_shift = magnet_pocket_left_base_node_upper.y - math.cos(
            np.radians(67.5)) * width_magnet_pocket_left_upperright
        magnet_pocket_left_upperright_no_shift = Node(magnet_pocket_left_upperright_x_no_shift,
                                                      magnet_pocket_left_upperright_y_no_shift)

        # rotor_geometry.add_node(magnet_pocket_left_upperright_no_shift)  # <<-- FOR DEBUGGING===========================

        if var.X11_magnet_pocket_shift == 0:
            magnet_pocket_left_upperright = magnet_pocket_left_upperright_no_shift
        else:
            magnet_pocket_left_upperright_distance_shift = magnet_pocket_left_upperright_no_shift.distance_to(
                n0) * math.sin(np.radians(var.X11_magnet_pocket_shift)) / math.sin(
                np.radians(90 - var.X11_magnet_pocket_shift - var.X9_magnet_pocket_width / 2))
            # print(magnet_pocket_left_upperright_distance_shift)  # <<-- FOR DEBUGGING===================================

            magnet_pocket_left_upperright_x = magnet_pocket_left_upperright_x_no_shift - math.sin(
                np.radians(67.5)) * magnet_pocket_left_upperright_distance_shift
            magnet_pocket_left_upperright_y = magnet_pocket_left_upperright_y_no_shift + math.cos(
                np.radians(67.5)) * magnet_pocket_left_upperright_distance_shift
            magnet_pocket_left_upperright = Node(magnet_pocket_left_upperright_x, magnet_pocket_left_upperright_y)

        a = magnet_pocket_left_upperright.distance_to(n0)
        b = 22
        B = np.radians(
            180 - np.degrees(math.atan2(magnet_pocket_left_upperright.y, magnet_pocket_left_upperright.x)) + 67.5)
        A = math.asin((a * math.sin(B)) / b)
        C = math.pi - A - B
        c = math.sqrt(a ** 2 + b ** 2 - 2 * a * b * math.cos(C))

        magnet_pocket_left_upperright_on_radius_x = magnet_pocket_left_upperright.x + math.sin(
            np.radians(90 - 67.5)) * c
        magnet_pocket_left_upperright_on_radius_y = magnet_pocket_left_upperright.y + math.cos(
            np.radians(90 - 67.5)) * c
        magnet_pocket_left_upperright_on_radius = Node(magnet_pocket_left_upperright_on_radius_x,
                                                       magnet_pocket_left_upperright_on_radius_y)

        rotor_geometry.add_node(magnet_pocket_left_upperright_on_radius)

        # Magnet pocket left bottom nodes-------------------------------------------------------------------------------
        # Left----------------------------------------------------------------------------------------------------------
        magnet_pocket_left_lowerleft_x_no_shift = magnet_pocket_left_upperleft_no_shift.x - math.sin(
            np.radians(90 - 67.5)) * var.X10_magnet_pocket_height
        magnet_pocket_left_lowerleft_y_no_shift = magnet_pocket_left_upperleft_no_shift.y - math.cos(
            np.radians(90 - 67.5)) * var.X10_magnet_pocket_height
        magnet_pocket_left_lowerleft_no_shift = Node(magnet_pocket_left_lowerleft_x_no_shift,
                                                     magnet_pocket_left_lowerleft_y_no_shift)

        # rotor_geometry.add_node(magnet_pocket_left_lowerleft_no_shift)  # <<-- FOR DEBUGGING============================

        if var.X11_magnet_pocket_shift == 0:
            magnet_pocket_left_lowerleft = magnet_pocket_left_lowerleft_no_shift
        else:
            magnet_pocket_left_lowerleft_x = magnet_pocket_left_upperleft_x - math.sin(
                np.radians(90 - 67.5)) * var.X10_magnet_pocket_height
            magnet_pocket_left_lowerleft_y = magnet_pocket_left_upperleft_y - math.cos(
                np.radians(90 - 67.5)) * var.X10_magnet_pocket_height
            magnet_pocket_left_lowerleft = Node(magnet_pocket_left_lowerleft_x, magnet_pocket_left_lowerleft_y)

        correction = magnet_pocket_left_lowerleft.distance_to(
            magnet_pocket_left_upperleft_on_radius) - var.X10_magnet_pocket_height
        magnet_pocket_left_lowerleft_x_corrected = magnet_pocket_left_lowerleft.x + math.sin(
            np.radians(90 - 67.5)) * correction
        magnet_pocket_left_lowerleft_y_corrected = magnet_pocket_left_lowerleft.y + math.cos(
            np.radians(90 - 67.5)) * correction
        magnet_pocket_left_lowerleft_corrected = Node(magnet_pocket_left_lowerleft_x_corrected,
                                                      magnet_pocket_left_lowerleft_y_corrected)

        magnet_pocket_left_lowerleft = magnet_pocket_left_lowerleft_corrected

        rotor_geometry.add_node(magnet_pocket_left_lowerleft)

        # Right---------------------------------------------------------------------------------------------------------
        magnet_pocket_left_lowerright_x_no_shift = magnet_pocket_left_upperright_no_shift.x - math.sin(
            np.radians(90 - 67.5)) * var.X10_magnet_pocket_height
        magnet_pocket_left_lowerright_y_no_shift = magnet_pocket_left_upperright_no_shift.y - math.cos(
            np.radians(90 - 67.5)) * var.X10_magnet_pocket_height
        magnet_pocket_left_lowerright_no_shift = Node(magnet_pocket_left_lowerright_x_no_shift,
                                                      magnet_pocket_left_lowerright_y_no_shift)

        # rotor_geometry.add_node(magnet_pocket_left_lowerright_no_shift)  # <<-- FOR DEBUGGING============================

        if var.X11_magnet_pocket_shift == 0:
            magnet_pocket_left_lowerright = magnet_pocket_left_lowerright_no_shift
        else:
            magnet_pocket_left_lowerright_x = magnet_pocket_left_upperright_x - math.sin(
                np.radians(90 - 67.5)) * var.X10_magnet_pocket_height
            magnet_pocket_left_lowerright_y = magnet_pocket_left_upperright_y - math.cos(
                np.radians(90 - 67.5)) * var.X10_magnet_pocket_height
            magnet_pocket_left_lowerright = Node(magnet_pocket_left_lowerright_x, magnet_pocket_left_lowerright_y)

        magnet_pocket_left_lowerright_x_corrected = magnet_pocket_left_lowerright.x + math.sin(
            np.radians(90 - 67.5)) * correction
        magnet_pocket_left_lowerright_y_corrected = magnet_pocket_left_lowerright.y + math.cos(
            np.radians(90 - 67.5)) * correction
        magnet_pocket_left_lowerright_corrected = Node(magnet_pocket_left_lowerright_x_corrected,
                                                       magnet_pocket_left_lowerright_y_corrected)

        magnet_pocket_left_lowerright = magnet_pocket_left_lowerright_corrected

        rotor_geometry.add_node(magnet_pocket_left_lowerright)

        # Lines and arcs for magnet pocket left-------------------------------------------------------------------------
        rotor_geometry.add_line(Line(magnet_pocket_left_upperleft_on_radius, magnet_pocket_left_lowerleft))
        rotor_geometry.add_line(Line(magnet_pocket_left_upperright_on_radius, magnet_pocket_left_lowerright))

        magnet_pocket_baseline = Line(magnet_pocket_left_lowerleft, magnet_pocket_left_lowerright)
        rotor_geometry.add_line(magnet_pocket_baseline)

        rotor_geometry.add_arc(CircleArc(magnet_pocket_left_upperleft_on_radius, n0, cut_off_barrier_left_half_upper))
        rotor_geometry.add_arc(CircleArc(cut_off_barrier_middle_left, n0, magnet_pocket_left_upperright_on_radius))

        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # Magnet pocket right upper nodes--------------------------------------------------------------------------------
        # Left----------------------------------------------------------------------------------------------------------
        magnet_pocket_right_base_node_upper = Line(cut_off_barrier_middle_right,
                                                   cut_off_barrier_right_half_upper).selection_point()

        # rotor_geometry.add_node(magnet_pocket_right_base_node_upper)  # <<-- FOR DEBUGGING================================

        width_magnet_pocket_right_upperleft = math.tan(
            np.radians(var.X9_magnet_pocket_width / 2)) * magnet_pocket_right_base_node_upper.distance_to(n0)
        # print(width_magnet_pocket_right_upperleft)  # <<-- FOR DEBUGGING=================================================

        magnet_pocket_right_upperleft_x_no_shift = magnet_pocket_right_base_node_upper.x - math.sin(
            np.radians(22.5)) * width_magnet_pocket_right_upperleft
        magnet_pocket_right_upperleft_y_no_shift = magnet_pocket_right_base_node_upper.y + math.cos(
            np.radians(22.5)) * width_magnet_pocket_right_upperleft
        magnet_pocket_right_upperleft_no_shift = Node(magnet_pocket_right_upperleft_x_no_shift,
                                                      magnet_pocket_right_upperleft_y_no_shift)

        # rotor_geometry.add_node(magnet_pocket_right_upperleft_no_shift)  # <<-- FOR DEBUGGING============================

        if var.X11_magnet_pocket_shift == 0:
            magnet_pocket_right_upperleft = magnet_pocket_right_upperleft_no_shift
        else:
            magnet_pocket_right_upperleft_distance_shift = magnet_pocket_right_upperleft_no_shift.distance_to(
                n0) * math.sin(np.radians(var.X11_magnet_pocket_shift)) / math.sin(
                np.radians(90 - var.X11_magnet_pocket_shift - var.X9_magnet_pocket_width / 2))
            # print(magnet_pocket_right_upperleft_distance_shift)  # <<-- FOR DEBUGGING====================================

            magnet_pocket_right_upperleft_x = magnet_pocket_right_upperleft_x_no_shift - math.sin(
                np.radians(22.5)) * magnet_pocket_right_upperleft_distance_shift
            magnet_pocket_right_upperleft_y = magnet_pocket_right_upperleft_y_no_shift + math.cos(
                np.radians(22.5)) * magnet_pocket_right_upperleft_distance_shift
            magnet_pocket_right_upperleft = Node(magnet_pocket_right_upperleft_x, magnet_pocket_right_upperleft_y)

        a = magnet_pocket_right_upperleft.distance_to(n0)
        b = 22
        B = np.radians(
            180 - np.degrees(math.atan2(magnet_pocket_right_upperleft.y, magnet_pocket_right_upperleft.x)) + 22.5)
        A = math.asin((a * math.sin(B)) / b)
        C = math.pi - A - B
        c = math.sqrt(a ** 2 + b ** 2 - 2 * a * b * math.cos(C))

        magnet_pocket_right_upperleft_on_radius_x = magnet_pocket_right_upperleft.x + math.sin(
            np.radians(90 - 22.5)) * c
        magnet_pocket_right_upperleft_on_radius_y = magnet_pocket_right_upperleft.y + math.cos(
            np.radians(90 - 22.5)) * c
        magnet_pocket_right_upperleft_on_radius = Node(magnet_pocket_right_upperleft_on_radius_x,
                                                       magnet_pocket_right_upperleft_on_radius_y)

        rotor_geometry.add_node(magnet_pocket_right_upperleft_on_radius)

        # Right----------------------------------------------------------------------------------------------------------
        width_magnet_pocket_right_upperright = math.tan(
            np.radians(var.X9_magnet_pocket_width / 2)) * magnet_pocket_right_base_node_upper.distance_to(n0)
        # print(width_magnet_pocket_right_upperright)  # <<-- FOR DEBUGGING================================================

        magnet_pocket_right_upperright_x_no_shift = magnet_pocket_right_base_node_upper.x + math.sin(
            np.radians(22.5)) * width_magnet_pocket_right_upperright
        magnet_pocket_right_upperright_y_no_shift = magnet_pocket_right_base_node_upper.y - math.cos(
            np.radians(22.5)) * width_magnet_pocket_right_upperright
        magnet_pocket_right_upperright_no_shift = Node(magnet_pocket_right_upperright_x_no_shift,
                                                       magnet_pocket_right_upperright_y_no_shift)

        # rotor_geometry.add_node(magnet_pocket_right_upperright_no_shift)  # <<-- FOR DEBUGGING===========================

        if var.X11_magnet_pocket_shift == 0:
            magnet_pocket_right_upperright = magnet_pocket_right_upperright_no_shift
        else:
            magnet_pocket_right_upperright_distance_shift = magnet_pocket_right_upperright_no_shift.distance_to(
                n0) * math.sin(np.radians(var.X11_magnet_pocket_shift)) / math.sin(
                np.radians(90 - var.X11_magnet_pocket_shift - var.X9_magnet_pocket_width / 2))
            # print(magnet_pocket_right_upperright_distance_shift)  # <<-- FOR DEBUGGING===================================

            magnet_pocket_right_upperright_x = magnet_pocket_right_upperright_x_no_shift - math.sin(
                np.radians(22.5)) * magnet_pocket_right_upperright_distance_shift
            magnet_pocket_right_upperright_y = magnet_pocket_right_upperright_y_no_shift + math.cos(
                np.radians(22.5)) * magnet_pocket_right_upperright_distance_shift
            magnet_pocket_right_upperright = Node(magnet_pocket_right_upperright_x, magnet_pocket_right_upperright_y)

        a = magnet_pocket_right_upperright.distance_to(n0)
        b = 22
        B = np.radians(
            180 - np.degrees(math.atan2(magnet_pocket_right_upperright.y, magnet_pocket_right_upperright.x)) + 22.5)
        A = math.asin((a * math.sin(B)) / b)
        C = math.pi - A - B
        c = math.sqrt(a ** 2 + b ** 2 - 2 * a * b * math.cos(C))

        magnet_pocket_right_upperright_on_radius_x = magnet_pocket_right_upperright.x + math.sin(
            np.radians(90 - 22.5)) * c
        magnet_pocket_right_upperright_on_radius_y = magnet_pocket_right_upperright.y + math.cos(
            np.radians(90 - 22.5)) * c
        magnet_pocket_right_upperright_on_radius = Node(magnet_pocket_right_upperright_on_radius_x,
                                                        magnet_pocket_right_upperright_on_radius_y)

        rotor_geometry.add_node(magnet_pocket_right_upperright_on_radius)

        # Magnet pocket right bottom nodes-------------------------------------------------------------------------------
        # Left----------------------------------------------------------------------------------------------------------
        magnet_pocket_right_lowerleft_x_no_shift = magnet_pocket_right_upperleft_no_shift.x - math.sin(
            np.radians(90 - 22.5)) * var.X10_magnet_pocket_height
        magnet_pocket_right_lowerleft_y_no_shift = magnet_pocket_right_upperleft_no_shift.y - math.cos(
            np.radians(90 - 22.5)) * var.X10_magnet_pocket_height
        magnet_pocket_right_lowerleft_no_shift = Node(magnet_pocket_right_lowerleft_x_no_shift,
                                                      magnet_pocket_right_lowerleft_y_no_shift)

        # rotor_geometry.add_node(magnet_pocket_right_lowerleft_no_shift)  # <<-- FOR DEBUGGING============================

        if var.X11_magnet_pocket_shift == 0:
            magnet_pocket_right_lowerleft = magnet_pocket_right_lowerleft_no_shift
        else:
            magnet_pocket_right_lowerleft_x = magnet_pocket_right_upperleft_x - math.sin(
                np.radians(90 - 22.5)) * var.X10_magnet_pocket_height
            magnet_pocket_right_lowerleft_y = magnet_pocket_right_upperleft_y - math.cos(
                np.radians(90 - 22.5)) * var.X10_magnet_pocket_height
            magnet_pocket_right_lowerleft = Node(magnet_pocket_right_lowerleft_x, magnet_pocket_right_lowerleft_y)

        correction = magnet_pocket_right_lowerleft.distance_to(
            magnet_pocket_right_upperleft_on_radius) - var.X10_magnet_pocket_height
        magnet_pocket_right_lowerleft_x_corrected = magnet_pocket_right_lowerleft.x + math.sin(
            np.radians(90 - 22.5)) * correction
        magnet_pocket_right_lowerleft_y_corrected = magnet_pocket_right_lowerleft.y + math.cos(
            np.radians(90 - 22.5)) * correction
        magnet_pocket_right_lowerleft_corrected = Node(magnet_pocket_right_lowerleft_x_corrected,
                                                       magnet_pocket_right_lowerleft_y_corrected)

        magnet_pocket_right_lowerleft = magnet_pocket_right_lowerleft_corrected

        rotor_geometry.add_node(magnet_pocket_right_lowerleft)

        # Right---------------------------------------------------------------------------------------------------------
        magnet_pocket_right_lowerright_x_no_shift = magnet_pocket_right_upperright_no_shift.x - math.sin(
            np.radians(90 - 22.5)) * var.X10_magnet_pocket_height
        magnet_pocket_right_lowerright_y_no_shift = magnet_pocket_right_upperright_no_shift.y - math.cos(
            np.radians(90 - 22.5)) * var.X10_magnet_pocket_height
        magnet_pocket_right_lowerright_no_shift = Node(magnet_pocket_right_lowerright_x_no_shift,
                                                       magnet_pocket_right_lowerright_y_no_shift)

        # rotor_geometry.add_node(magnet_pocket_right_lowerright_no_shift)  # <<-- FOR DEBUGGING============================

        if var.X11_magnet_pocket_shift == 0:
            magnet_pocket_right_lowerright = magnet_pocket_right_lowerright_no_shift
        else:
            magnet_pocket_right_lowerright_x = magnet_pocket_right_upperright_x - math.sin(
                np.radians(90 - 22.5)) * var.X10_magnet_pocket_height
            magnet_pocket_right_lowerright_y = magnet_pocket_right_upperright_y - math.cos(
                np.radians(90 - 22.5)) * var.X10_magnet_pocket_height
            magnet_pocket_right_lowerright = Node(magnet_pocket_right_lowerright_x, magnet_pocket_right_lowerright_y)

        magnet_pocket_right_lowerright_x_corrected = magnet_pocket_right_lowerright.x + math.sin(
            np.radians(90 - 22.5)) * correction
        magnet_pocket_right_lowerright_y_corrected = magnet_pocket_right_lowerright.y + math.cos(
            np.radians(90 - 22.5)) * correction
        magnet_pocket_right_lowerright_corrected = Node(magnet_pocket_right_lowerright_x_corrected,
                                                        magnet_pocket_right_lowerright_y_corrected)

        magnet_pocket_right_lowerright = magnet_pocket_right_lowerright_corrected

        rotor_geometry.add_node(magnet_pocket_right_lowerright)

        # Lines and arcs for magnet pocket right------------------------------------------------------------------------
        rotor_geometry.add_line(Line(magnet_pocket_right_upperleft_on_radius, magnet_pocket_right_lowerleft))
        rotor_geometry.add_line(Line(magnet_pocket_right_upperright_on_radius, magnet_pocket_right_lowerright))

        magnet_pocket_baseline = Line(magnet_pocket_right_lowerleft, magnet_pocket_right_lowerright)
        rotor_geometry.add_line(magnet_pocket_baseline)

        rotor_geometry.add_arc(
            CircleArc(cut_off_barrier_right_half_upper, n0, magnet_pocket_right_upperright_on_radius))
        rotor_geometry.add_arc(CircleArc(magnet_pocket_right_upperleft_on_radius, n0, cut_off_barrier_middle_right))

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # TOP FLUX BARRIER %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # Left upper node ----------------------------------------------------------------------------------------------

        top_internal_barrier_distance_left_x = magnet_pocket_left_lowerright.x - math.sin(
            np.radians(90 - 67.5)) * var.X12_distance_magnet_pocket_internal_barrier
        top_internal_barrier_distance_left_y = magnet_pocket_left_lowerright.y - math.cos(
            np.radians(90 - 67.5)) * var.X12_distance_magnet_pocket_internal_barrier
        top_internal_barrier_distance_left = Node(top_internal_barrier_distance_left_x,
                                                  top_internal_barrier_distance_left_y)

        # rotor_geometry.add_node(
        #     top_internal_barrier_distance_left)  # <<-- FOR DEBUGGING================================

        a = top_internal_barrier_distance_left.distance_to(cut_off_barrier_middle_arc.center_point())
        b = top_internal_barrier_distance_left.distance_to(upper_rib_base_node_upper)
        c = upper_rib_base_node_upper.distance_to(cut_off_barrier_middle_arc.center_point())

        B = math.acos((a**2 + c**2 - b**2) / (2*a*c))

        top_internal_barrier_upper_left = upper_rib_base_node_upper.rotate_about(
            cut_off_barrier_middle_arc.center_point(), (-1) * B, degrees=False)

        # rotor_geometry.add_node(top_internal_barrier_upper_left)  # <<-- FOR DEBUGGING================================

        n = upper_rib_base_node_upper.distance_to(cut_off_barrier_middle_arc.center_point())
        m = top_internal_barrier_distance_left.distance_to(cut_off_barrier_middle_arc.center_point())
        N = np.radians(90-67.5) + math.atan2(
            cut_off_barrier_middle_arc.center_point().y - top_internal_barrier_distance_left.y,
            cut_off_barrier_middle_arc.center_point().x - top_internal_barrier_distance_left.x)
        M = math.pi - math.asin(math.sin(N) * m / n)
        L = math.pi - N - M
        # l = np.sqrt(n**2+m**2-2*n*m*math.cos(L))

        top_internal_barrier_upper_left_corrected = top_internal_barrier_upper_left.rotate_about(
            cut_off_barrier_middle_arc.center_point(), L, degrees=False)

        rotor_geometry.add_node(top_internal_barrier_upper_left_corrected)

        # Left lowe node ----------------------------------------------------------------------------------------------

        a = top_internal_barrier_distance_left.distance_to(cut_off_barrier_middle_arc.center_point())
        b = top_internal_barrier_distance_left.distance_to(upper_rib_base_node_lower)
        c = upper_rib_base_node_lower.distance_to(cut_off_barrier_middle_arc.center_point())

        B = math.acos((a ** 2 + c ** 2 - b ** 2) / (2 * a * c))

        top_internal_barrier_lower_left = upper_rib_base_node_lower.rotate_about(
            cut_off_barrier_middle_arc.center_point(), (-1) * B, degrees=False)

        # rotor_geometry.add_node(top_internal_barrier_lower_left)  # <<-- FOR DEBUGGING================================

        n = upper_rib_base_node_lower.distance_to(cut_off_barrier_middle_arc.center_point())
        m = top_internal_barrier_distance_left.distance_to(cut_off_barrier_middle_arc.center_point())
        N = np.radians(90 - 67.5) + math.atan2(
            cut_off_barrier_middle_arc.center_point().y - top_internal_barrier_distance_left.y,
            cut_off_barrier_middle_arc.center_point().x - top_internal_barrier_distance_left.x)
        M = math.pi - math.asin(math.sin(N) * m / n)
        L = math.pi - N - M
        l = np.sqrt(n ** 2 + m ** 2 - 2 * n * m * math.cos(L))

        top_internal_barrier_lower_left_corrected = top_internal_barrier_lower_left.rotate_about(
            cut_off_barrier_middle_arc.center_point(), L, degrees=False)

        rotor_geometry.add_node(top_internal_barrier_lower_left_corrected)

        top_internal_barrier_left_upper_arc = CircleArc(top_internal_barrier_upper_left_corrected,
                                                        cut_off_barrier_middle_arc.center_point(),
                                                        upper_rib_upper_node_left)

        top_internal_barrier_left_lower_arc = CircleArc(top_internal_barrier_lower_left_corrected,
                                                       cut_off_barrier_middle_arc.center_point(),
                                                       upper_rib_lower_node_left)

        rotor_geometry.add_arc(top_internal_barrier_left_upper_arc)
        rotor_geometry.add_arc(top_internal_barrier_left_lower_arc)

        rotor_geometry.add_line(Line(top_internal_barrier_upper_left_corrected, top_internal_barrier_lower_left_corrected))

        model.create_geometry(rotor_geometry)

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # BOTTOM FLUX BARRIER %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # Left upper node ----------------------------------------------------------------------------------------------

        bottom_internal_barrier_upper_left = lower_rib_base_node_upper.rotate_about()



        return True

    except ArithmeticError as e:
        raise Exception('{e}')


#     # define the nodes and sectors of the cut-off barriers
#     co_s = Node(22, 0).rotate_about(n0, 45 - var.ang_co / 2, degrees=True)
#     co_e = Node(22, 0).rotate_about(n0, 45 + var.ang_co / 2, degrees=True)
#     co_r = co_e.rotate_about(n0, -45, degrees=True)
#     co_l = co_s.rotate_about(n0, 45, degrees=True)
#
#     rotor_geo.add_node(co_s)
#     rotor_geo.add_node(co_e)
#     rotor_geo.add_node(co_r)
#     rotor_geo.add_node(co_l)
#
#     co_arc = Sector(co_e, co_s, var.deg_co)
#
#     rotor_geo.add_sector(co_arc)
#
#     co_arc_ep = co_arc.selection_point()
#     co_arc_ep_r = co_arc_ep.rotate_about(n0, -45, degrees=True)
#     co_arc_ep_l = co_arc_ep.rotate_about(n0, 45, degrees=True)
#
#     rotor_geo.add_node(co_arc_ep_r)
#     rotor_geo.add_node(co_arc_ep_l)
#
#     co_arcr = Sector(co_r, co_arc_ep_r, var.deg_co / 2)
#     co_arcl = Sector(co_arc_ep_l, co_l, var.deg_co / 2)
#
#     rotor_geo.add_sector(co_arcr)
#     rotor_geo.add_sector(co_arcl)
#
#     # define sliding band nodes, lines and arc
#     sb_l = Node(0.00, 22.10)
#     sb_r = Node(22.10, 0.00)
#
#     rotor_geo.add_node(sb_r)
#     rotor_geo.add_node(sb_l)
#
#     sbl_l = Line(sb_l, co_arc_ep_l)
#     sbl_r = Line(sb_r, co_arc_ep_r)
#
#     rotor_geo.add_line(sbl_l)
#     rotor_geo.add_line(sbl_r)
#
#     sb_arc = CircleArc(sb_r, n0, sb_l)
#
#     rotor_geo.add_arc(sb_arc)
#
#     # define the enclosing geometry
#     h0 = Node(6.00, 0.00)
#     v0 = h0.rotate_about(n0, 90, True)
#
#     rotor_geo.add_node(h0)
#     rotor_geo.add_node(v0)
#
#     encl_r = Line(h0, co_arc_ep_r)
#     encl_l = Line(v0, co_arc_ep_l)
#
#     rotor_geo.add_line(encl_r)
#     rotor_geo.add_line(encl_l)
#
#     enc_arc_0 = CircleArc(h0, n0, v0)
#
#     rotor_geo.add_arc(enc_arc_0)
#
#     # define inner barriers
#     co_arc_ep = co_arc.selection_point()  # Cut-off barrier arc point at 45 deg.
#     co_arc_cp = co_arc.center_point()  # Cut-off barrier arc center point.
#
#     # rotor_geo.add_node(co_arc_ep)
#
#     d_ep_cp = co_arc_ep.distance_to(co_arc_cp)
#     d_n0_ep = co_arc_ep.distance_to(n0)
#     d_n0_cp = co_arc_cp.distance_to(n0)
#
#     # define upper arc of inner barrier
#     ib_base1 = Node(d_n0_ep - var.bd, 0.00).rotate_about(n0, 45, True)
#
#     ib_1_ang = math.atan2(var.bw / 2, (d_ep_cp + var.bd))
#     ib_1l = ib_base1.rotate_about(co_arc_cp, -ib_1_ang, False)
#     ib_1r = ib_base1.rotate_about(co_arc_cp, ib_1_ang, False)
#
#     ib_1l_r = ib_1l.rotate_about(n0, -45, True)
#     ib_1r_l = ib_1r.rotate_about(n0, 45, True)
#
#     # rotor_geo.add_node(ib_base1)
#     rotor_geo.add_node(ib_1l)
#     rotor_geo.add_node(ib_1r)
#     rotor_geo.add_node(ib_1r_l)
#     rotor_geo.add_node(ib_1l_r)
#
#     A = d_ep_cp + var.bd
#     B = d_n0_cp
#     C = 22 - var.bg
#     ib_3_ang = math.acos((A ** 2 + B ** 2 - C ** 2) / (2 * A * B))
#     ib_3l = ib_base1.rotate_about(co_arc_cp, -ib_3_ang, False)
#     ib_3r = ib_base1.rotate_about(co_arc_cp, ib_3_ang, False)
#
#     ib_3l_r = ib_3l.rotate_about(n0, -45, True)
#     ib_3r_l = ib_3r.rotate_about(n0, 45, True)
#
#     rotor_geo.add_node(ib_3l)
#     rotor_geo.add_node(ib_3r)
#     rotor_geo.add_node(ib_3r_l)
#     rotor_geo.add_node(ib_3l_r)
#
#     # define under arc of inner barrier
#     ib_base2 = Node(d_n0_ep - var.bd - var.bh, 0.00).rotate_about(n0, 45, True)
#
#     ib_2_ang = math.atan2(var.bw / 2, (d_ep_cp + var.bd + var.bh))
#     ib_2l = ib_base2.rotate_about(co_arc_cp, -ib_2_ang, False)
#     ib_2r = ib_base2.rotate_about(co_arc_cp, ib_2_ang, False)
#
#     ib_2l_r = ib_2l.rotate_about(n0, -45, True)
#     ib_2r_l = ib_2r.rotate_about(n0, 45, True)
#
#     # rotor_geo.add_node(ib_base)
#     rotor_geo.add_node(ib_2l)
#     rotor_geo.add_node(ib_2r)
#     rotor_geo.add_node(ib_2r_l)
#     rotor_geo.add_node(ib_2l_r)
#
#     A = d_ep_cp + var.bd + var.bh
#     B = d_n0_cp
#     C = 22 - var.bg
#     ib_4_ang = math.acos((A ** 2 + B ** 2 - C ** 2) / (2 * A * B))
#     ib_4l = ib_base2.rotate_about(co_arc_cp, -ib_4_ang, False)
#     ib_4r = ib_base2.rotate_about(co_arc_cp, ib_4_ang, False)
#
#     ib_4l_r = ib_4l.rotate_about(n0, -45, True)
#     ib_4r_l = ib_4r.rotate_about(n0, 45, True)
#
#     rotor_geo.add_node(ib_4l)
#     rotor_geo.add_node(ib_4r)
#     rotor_geo.add_node(ib_4r_l)
#     rotor_geo.add_node(ib_4l_r)
#
#     # define line between upper and under barrier arcs
#
#     ibl_1l = Line(ib_1l, ib_2l)
#     ibl_1r = Line(ib_1r, ib_2r)
#     ibl_2l = Line(ib_3l, ib_4l)
#     ibl_2r = Line(ib_3r, ib_4r)
#
#     ibl_1r_l = Line(ib_1r_l, ib_2r_l)
#     ibl_1l_r = Line(ib_1l_r, ib_2l_r)
#     ibl_2r_l = Line(ib_3r_l, ib_4r_l)
#     ibl_2l_r = Line(ib_3l_r, ib_4l_r)
#
#     rotor_geo.add_line(ibl_1l)
#     rotor_geo.add_line(ibl_1r)
#     rotor_geo.add_line(ibl_2l)
#     rotor_geo.add_line(ibl_2r)
#
#     rotor_geo.add_line(ibl_1l_r)
#     rotor_geo.add_line(ibl_1r_l)
#     rotor_geo.add_line(ibl_2l_r)
#     rotor_geo.add_line(ibl_2r_l)
#
#     iblu_arc = Sector(ib_3l, ib_1l, var.deg_co / 2)
#     ibru_arc = Sector(ib_1r, ib_3r, var.deg_co / 2)
#     iblo_arc = Sector(ib_4l, ib_2l, var.deg_co / 2)
#     ibro_arc = Sector(ib_2r, ib_4r, var.deg_co / 2)
#
#     iblu_arc_r = Sector(ib_3l_r, ib_1l_r, var.deg_co / 2)
#     ibru_arc_l = Sector(ib_1r_l, ib_3r_l, var.deg_co / 2)
#     iblo_arc_r = Sector(ib_4l_r, ib_2l_r, var.deg_co / 2)
#     ibro_arc_l = Sector(ib_2r_l, ib_4r_l, var.deg_co / 2)
#
#     rotor_geo.add_sector(iblu_arc)
#     rotor_geo.add_sector(ibru_arc)
#     rotor_geo.add_sector(iblo_arc)
#     rotor_geo.add_sector(ibro_arc)
#     rotor_geo.add_sector(iblu_arc_r)
#     rotor_geo.add_sector(ibru_arc_l)
#     rotor_geo.add_sector(iblo_arc_r)
#     rotor_geo.add_sector(ibro_arc_l)
#
#     # calculate the midpoint of every flux barrier to define material labels later on
#
#     ib_mp1 = Line(iblu_arc_r.selection_point(), iblo_arc_r.selection_point()).selection_point()
#     ib_mp2 = Line(ibru_arc.selection_point(), ibro_arc.selection_point()).selection_point()
#     ib_mp3 = Line(iblu_arc.selection_point(), iblo_arc.selection_point()).selection_point()
#     ib_mp4 = Line(ibru_arc_l.selection_point(), ibro_arc_l.selection_point()).selection_point()
#
#     rot_bound1_l = encl_l.selection_point()
#     rot_bound1_r = encl_r.selection_point()
#     rot_bound2_l = sbl_l.selection_point()
#     rot_bound2_r = sbl_r.selection_point()
#     rot_bound_arc1 = enc_arc_0.selection_point()
#     rot_bound_arc2 = sb_arc.selection_point()
#
#     # LEFT ROTOR MAGNET------------------------------------------------------------------------------------------------
#     nmbase_lo = Node(22, 0).rotate_about(n0, 67.5, True)
#     nmbase_lu = Node(22 - var.mh - 0.01, 0).rotate_about(n0, 67.5, True)
#
#     nm_llo = nmbase_lo.rotate_about(n0, var.ang_m / 2, True)
#     nm_rlo = nmbase_lo.rotate_about(n0, -var.ang_m / 2, True)
#     nm_llu = nmbase_lu.rotate_about(n0, var.ang_m / 2, True)
#     nm_rlu = nmbase_lu.rotate_about(n0, -var.ang_m / 2, True)
#
#     rotor_geo.add_node(nm_llo)
#     rotor_geo.add_node(nm_rlo)
#     rotor_geo.add_node(nm_llu)
#     rotor_geo.add_node(nm_rlu)
#
#     lm_ll = Line(nm_llo, nm_llu)
#     lm_lr = Line(nm_rlo, nm_rlu)
#
#     rotor_geo.add_line(lm_ll)
#     rotor_geo.add_line(lm_lr)
#
#     am_lu = CircleArc(nm_rlu, n0, nm_llu)
#
#     rotor_geo.add_arc(am_lu)
#
#     lab_mag_l = Line(lm_ll.selection_point(), lm_lr.selection_point()).selection_point()
#
#     rot_arc_ll = CircleArc(nm_llo, n0, co_l)
#     rot_arc_lr = CircleArc(co_e, n0, nm_rlo)
#     rot_arc_lc = CircleArc(nm_rlo, n0, nm_llo)
#
#     rotor_geo.add_arc(rot_arc_ll)
#     rotor_geo.add_arc(rot_arc_lr)
#     rotor_geo.add_arc(rot_arc_lc)
#
#     # RIGHT ROTOR MAGNET------------------------------------------------------------------------------------------------
#     nmbase_ro = Node(22, 0).rotate_about(n0, 22.5, True)
#     nmbase_ru = Node(22 - var.mh - 0.01, 0).rotate_about(n0, 22.5, True)
#
#     nm_lro = nmbase_ro.rotate_about(n0, var.ang_m / 2, True)
#     nm_rro = nmbase_ro.rotate_about(n0, -var.ang_m / 2, True)
#     nm_lru = nmbase_ru.rotate_about(n0, var.ang_m / 2, True)
#     nm_rru = nmbase_ru.rotate_about(n0, -var.ang_m / 2, True)
#
#     rotor_geo.add_node(nm_lro)
#     rotor_geo.add_node(nm_rro)
#     rotor_geo.add_node(nm_lru)
#     rotor_geo.add_node(nm_rru)
#
#     lm_rl = Line(nm_lro, nm_lru)
#     lm_rr = Line(nm_rro, nm_rru)
#
#     rotor_geo.add_line(lm_rl)
#     rotor_geo.add_line(lm_rr)
#
#     rot_arc_rl = CircleArc(co_r, n0, nm_rro)
#     rot_arc_rr = CircleArc(nm_lro, n0, co_s)
#     rot_arc_rc = CircleArc(nm_rro, n0, nm_lro)
#
#     rotor_geo.add_arc(rot_arc_rl)
#     rotor_geo.add_arc(rot_arc_rr)
#     rotor_geo.add_arc(rot_arc_rc)
#
#     am_ru = CircleArc(nm_rru, n0, nm_lru)
#
#     rotor_geo.add_arc(am_ru)
#
#     lab_mag_r = Line(lm_rl.selection_point(), lm_rr.selection_point()).selection_point()
#
#     femm_problem.create_geometry(rotor_geo)
#
#     return ib_mp1, ib_mp2, ib_mp3, ib_mp4, rot_bound1_l, rot_bound1_r, rot_bound2_l, rot_bound2_r, rot_bound_arc1, \
#         rot_bound_arc2, lab_mag_l, lab_mag_r
#
#
# def add_boundaries(femm_problem: FemmProblem, var: VariableParameters, rot: rotor_geometry):
#     # Define all boundary conditions
#     a0 = MagneticDirichlet(name="a0", a_0=0, a_1=0, a_2=0, phi=0)  # A0 Boundary Condition
#
#     pbca = MagneticPeriodicAirgap(name="pbca")  # Periodic Air Gap Boundary Condition
#
#     pbc1 = MagneticPeriodic(name="pbc1")  # Periodic Boundary Condition
#     pbc2 = MagneticPeriodic(name="pbc2")  # Periodic Boundary Condition
#     pbc3 = MagneticPeriodic(name="pbc3")  # Periodic Boundary Condition
#     pbc4 = MagneticPeriodic(name="pbc4")  # Periodic Boundary Condition
#
#     # Add all boundary conditions
#     femm_problem.add_boundary(a0)
#     femm_problem.add_boundary(pbca)
#     femm_problem.add_boundary(pbc1)
#     femm_problem.add_boundary(pbc2)
#     femm_problem.add_boundary(pbc3)
#     femm_problem.add_boundary(pbc4)
#
#     # Modify Periodic Air Gap Boundary Condition Inner Angle to imitate rotation
#     # modify_boundary added, because there is a FEMM bug with add_boundary, that ia is set by oa and oa is not possible
#     # to set. If you need to set oa, you need modify_boundary.
#     pbca = MagneticBoundaryModification(pbca.name, pbca.boundary_format, propnum=10, value=var.ia)
#
#     # Add modified Periodic Air Gap Boundary Condition
#     femm_problem.modify_boundary(pbca)
#
#     # Add boundary conditions to stator segments
#     femm_problem.set_boundary_definition_segment(Node(0, 22.4), pbc3)
#     femm_problem.set_boundary_definition_segment(Node(22.4, 0), pbc3)
#     femm_problem.set_boundary_definition_segment(Node(0, 34), pbc4)
#     femm_problem.set_boundary_definition_segment(Node(34, 0), pbc4)
#
#     # Define and add boundary conditions to stator circle arcs
#     a02 = Node(22.30, 0).rotate_about(n0, 45, degrees=True)
#     a03 = Node(43.25, 0).rotate_about(n0, 45, degrees=True)
#
#     femm_problem.set_boundary_definition_arc(a02, pbca)
#     femm_problem.set_boundary_definition_arc(a03, a0)
#
#     # Add boundary conditions to rotor segments
#     femm_problem.set_boundary_definition_segment(rot[4], pbc1)
#     femm_problem.set_boundary_definition_segment(rot[5], pbc1)
#     femm_problem.set_boundary_definition_segment(rot[6], pbc2)
#     femm_problem.set_boundary_definition_segment(rot[7], pbc2)
#
#     # Add boundary conditions to rotor arcs
#     femm_problem.set_boundary_definition_arc(rot[8], a0)
#     femm_problem.set_boundary_definition_arc(rot[9], pbca)
#
#
# def add_materials(femm_problem: FemmProblem, var: VariableParameters, rot: rotor_geometry):
#     # Define wire material, air and steel material.
#     # There is an interesting bug in FEMM, that you can't add source current density to magnet wire, but it is possible
#     # using .lua code
#     # To get the correct winding scheme, check: https://bavaria-direct.co.za/scheme/calculator/
#     copper_Ap = MagneticMaterial(material_name="U+", J=var.JAp, Sigma=58, LamType=LamType.MAGNET_WIRE, WireD=1)
#     copper_An = MagneticMaterial(material_name="U-", J=var.JAn, Sigma=58, LamType=LamType.MAGNET_WIRE, WireD=1)
#     copper_Bp = MagneticMaterial(material_name="V+", J=var.JBp, Sigma=58, LamType=LamType.MAGNET_WIRE, WireD=1)
#     copper_Bn = MagneticMaterial(material_name="V-", J=var.JBn, Sigma=58, LamType=LamType.MAGNET_WIRE, WireD=1)
#     copper_Cp = MagneticMaterial(material_name="W+", J=var.JCp, Sigma=58, LamType=LamType.MAGNET_WIRE, WireD=1)
#     copper_Cn = MagneticMaterial(material_name="W-", J=var.JCn, Sigma=58, LamType=LamType.MAGNET_WIRE, WireD=1)
#
#     air = MagneticMaterial(material_name="air")
#
#     steel = MagneticMaterial(material_name="steel", Sigma=5.8, Lam_d=0.5, lam_fill=0.98)
#     FeSi65 = MagneticMaterial(material_name="FeSi65", Sigma=5.8, Lam_d=0, lam_fill=1)
#
#     # Add wire material, air and steel material.
#     femm_problem.add_material(copper_Ap)
#     femm_problem.add_material(copper_An)
#     femm_problem.add_material(copper_Bp)
#     femm_problem.add_material(copper_Bn)
#     femm_problem.add_material(copper_Cp)
#     femm_problem.add_material(copper_Cn)
#     femm_problem.add_material(air)
#     femm_problem.add_material(steel)
#     femm_problem.add_material(FeSi65)
#
#     # Add BH curve for stator steel material.
#     # There is an interesting bug in FEMM, that you can add any number of BH point, but it will only plot it manually
#     # to B~10.000. If you check the BH list, all the points are there.
#     femm_problem.add_bh_curve(material_name="steel",
#                               data_b=[0, 0.670856255, 0.791524678, 0.871414555, 0.931231537, 0.979063683, 1.0189211,
#                                       1.053086796, 1.082985065, 1.109564545, 1.126953298, 1.20365399, 1.250426447,
#                                       1.284175967, 1.31059707, 1.332311427, 1.350745115, 1.366760558, 1.380919281,
#                                       1.393607415, 1.405101905, 1.41560815, 1.42528271, 1.434247653, 1.442600004,
#                                       1.450418152, 1.457766344, 1.464697889, 1.47125751, 1.477483095, 1.476550438,
#                                       1.488764478, 1.498939108, 1.507658923, 1.515288382, 1.52207011, 1.528173797,
#                                       1.533722786, 1.538809552, 1.543505214, 1.547865643, 1.551935531, 1.555751191,
#                                       1.559342524, 1.56273445, 1.565947951, 1.569000866, 1.571908482, 1.574684004,
#                                       1.577338915, 1.579883262, 1.582325887, 1.584674612, 1.586936389, 1.589117427,
#                                       1.591223293, 1.593258995, 1.595229059, 1.597137587, 1.598988305],
#                               data_h=[0, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1615.789474,
#                                       2131.578947, 2647.368421, 3163.157895, 3678.947368, 4194.736842, 4710.526316,
#                                       5226.315789, 5742.105263, 6257.894737, 6773.684211, 7289.473684, 7805.263158,
#                                       8321.052632, 8836.842105, 9352.631579, 9868.421053, 10384.21053, 10900, 11000,
#                                       12344.82759, 13689.65517, 15034.48276, 16379.31034, 17724.13793, 19068.96552,
#                                       20413.7931, 21758.62069, 23103.44828, 24448.27586, 25793.10345, 27137.93103,
#                                       28482.75862, 29827.58621, 31172.41379, 32517.24138, 33862.06897, 35206.89655,
#                                       36551.72414, 37896.55172, 39241.37931, 40586.2069, 41931.03448, 43275.86207,
#                                       44620.68966, 45965.51724, 47310.34483, 48655.17241, 50000])
#
#     femm_problem.add_bh_curve(material_name="FeSi65",
#                               data_b=[0, 0.358294627, 0.478028092, 0.563148872, 0.629244556, 0.683285138,
#                                       0.728997037,
#                                       0.768607936, 0.803556282, 0.834825031, 0.863115728, 0.888946635, 0.912711487,
#                                       0.934716448, 0.955204299, 1.030452669, 1.086202243, 1.130688402, 1.167706237,
#                                       1.199406524, 1.227126836, 1.251755988, 1.273914738, 1.294053804, 1.3125108,
#                                       1.329545176, 1.34536063, 1.360120017, 1.373955589, 1.402248493, 1.425268547,
#                                       1.443943891, 1.459657021, 1.473220258, 1.485151723, 1.495802219, 1.505420324,
#                                       1.514188618, 1.522245155, 1.529696862, 1.536628245, 1.54310725, 1.549189325,
#                                       1.554920311, 1.560338538, 1.565476384, 1.570361444, 1.575017432, 1.579464871,
#                                       1.583721646, 1.587803435, 1.591724059, 1.595495761, 1.599129443, 1.60263485,
#                                       1.606020731, 1.609294969, 1.612464692],
#                               data_h=[0, 235.7142857, 371.4285714, 507.1428571, 642.8571429, 778.5714286,
#                                       914.2857143,
#                                       1050, 1185.714286, 1321.428571, 1457.142857, 1592.857143, 1728.571429,
#                                       1864.285714, 2000, 2571.428571, 3142.857143, 3714.285714, 4285.714286,
#                                       4857.142857, 5428.571429, 6000, 6571.428571, 7142.857143, 7714.285714,
#                                       8285.714286, 8857.142857, 9428.57429, 10000, 11379.31034, 12758.62069,
#                                       14137.93103, 15517.24138, 16896.55172, 18275.86207, 19655.17241, 21034.48276,
#                                       22413.7931, 23793.10345, 25172.41379, 26551.72414, 27931.03448, 29310.34483,
#                                       30689.65517, 32068.96552, 33448.27586, 34827.58621, 6206.89655, 37586.2069,
#                                       38965.51724, 40344.82759, 41724.13793, 43103.44828, 44482.75862, 45862.06897,
#                                       47241.37931, 48620.68966, 50000])
#
#     ferrite_left = MagneticMaterial(material_name="ml", H_c=200106)
#     ferrite_right = MagneticMaterial(material_name="mr", H_c=200106)
#
#     ferrite_left.remanence_angle = 247.5
#     ferrite_right.remanence_angle = 22.5
#
#     femm_problem.add_material(ferrite_left)
#     femm_problem.add_material(ferrite_right)
#
#     femm_problem.add_bh_curve(material_name="ml",
#                               data_b=[0.000000, 0.066000, 0.131390, 0.144000, 0.153280, 0.162400, 0.171530,
#                                       0.211680, 0.273720, 0.386860],
#                               data_h=[0.000000, 1160.000000, 2323.660000, 3490.000000, 6000.000000, 11630.000000,
#                                       18613.200000, 51192.200000, 102376.000000, 200106.000000])
#
#     femm_problem.add_bh_curve(material_name="mr",
#                               data_b=[0.000000, 0.066000, 0.131390, 0.144000, 0.153280, 0.162400, 0.171530,
#                                       0.211680, 0.273720, 0.386860],
#                               data_h=[0.000000, 1160.000000, 2323.660000, 3490.000000, 6000.000000, 11630.000000,
#                                       18613.200000, 51192.200000, 102376.000000, 200106.000000])
#
#     # Add block labels to the stator
#     femm_problem.define_block_label(Node(17, 17), air)
#
#     femm_problem.define_block_label(Node(28.00, 28.00), steel)
#
#     femm_problem.define_block_label(Node(31, 0).rotate_about(n0, 80, True), copper_An)
#     femm_problem.define_block_label(Node(31, 0).rotate_about(n0, 70, True), copper_Bp)
#     femm_problem.define_block_label(Node(31, 0).rotate_about(n0, 50, True), copper_Bn)
#     femm_problem.define_block_label(Node(31, 0).rotate_about(n0, 40, True), copper_Cp)
#     femm_problem.define_block_label(Node(31, 0).rotate_about(n0, 20, True), copper_Cn)
#     femm_problem.define_block_label(Node(31, 0).rotate_about(n0, 10, True), copper_Ap)
#
#     # Add block labels to the rotor
#     femm_problem.define_block_label(rot[0], air)
#     femm_problem.define_block_label(rot[1], air)
#     femm_problem.define_block_label(rot[2], air)
#     femm_problem.define_block_label(rot[3], air)
#
#     femm_problem.define_block_label(Node(22.05, 0.00).rotate_about(n0, 45, True), air)
#     femm_problem.define_block_label(Node(7, 0.00).rotate_about(n0, 45, True), FeSi65)
#
#     femm_problem.define_block_label(rot[10], ferrite_left)
#     femm_problem.define_block_label(rot[11], ferrite_right)

def model_creation(variables: VariableParameters):
    """Put all the block together to create the machine model."""

    if not Path(variables.output_folder_name).exists():
        Path(variables.output_folder_name).mkdir(parents=True, exist_ok=True)

    # Call the FEMM solver ---------------------------------------------------------------------------------------------
    solver = FemmProblem(out_file=variables.output_file_name + ".csv")

    # Initialise the FEMM class.
    solver.magnetic_problem(0, LengthUnit.MILLIMETERS, "planar", depth=37)

    # Initialise the machine model blocks ------------------------------------------------------------------------------
    stator = define_stator_geometry(solver)
    rotor = define_rotor_geometry(solver, variables)
    # materials = material_definition(problem, variables, rotor)
    # winding_definition(problem, variables)
    # boundary_definition(problem, variables)

    # Create the .lua file's content as txt ----------------------------------------------------------------------------
    solver.make_analysis(filename=variables.output_file_path)

    # Initialise the intended output torque to calculate ---------------------------------------------------------------
    # solver.get_integral_values(label_list=label(), save_image=False,
    #                             variable_name=MagneticVolumeIntegral.wTorque)

    # Create .lua file.
    solver.write(file_name=variables.output_file_path + '.lua')

    # To manually free memory ------------------------------------------------------------------------------------------
    del stator
    del rotor

# def problem_definition(var: VariableParameters):
#     problem = FemmProblem(out_file=os.path.join(folder_path, f'temp_{var.fold}/{var.out}{var.counter}.csv'))
#
#     problem.magnetic_problem(0, LengthUnit.MILLIMETERS, "planar", depth=40)
#
#     stator_geometry(problem)
#     rot = rotor_geometry(problem, var)
#     add_boundaries(problem, var, rot)
#     add_materials(problem, var, rot)
#
#     problem.make_analysis(os.path.join(folder_path, f'temp_{var.fold}/{var.out}{var.counter}'))
#
#     problem.get_integral_values(label_list=[list(rot)[0], list(rot)[1], list(rot)[2], list(rot)[3], list(rot)[10],
#                                             list(rot)[11], Node(5, 5)],
#                                 save_image=False,
#                                 variable_name=MagneticVolumeIntegral.wTorque)
#
#     problem.write(os.path.join(folder_path, f'temp_{var.fold}/{var.out}{var.counter}.lua'))
#
#     rot = []  # To make sure that there is no memory leak
