"""
The goal of this module is to write out the given geometry into a FEMM's lua
script.  The code generated one snapshot from the created model, which can be
run during the Optimization.

The original FEMM code has separate scripting commands for the geometry
generation in different subfields

"""
from math import asin, degrees
from pathlib import Path
from string import Template
from enum import Enum
from typing import Union

from src.current_flow import CurrentFlowMaterial, CurrentFlowFixedVoltage, CurrentFlowMixed, CurrentFlowSurfaceCurrent, \
    CurrentFlowPeriodic, CurrentFlowAntiPeriodic
from src.electrostatics import ElectrostaticMaterial, ElectrostaticFixedVoltage, ElectrostaticMixed, \
    ElectrostaticSurfaceCharge, ElectrostaticPeriodic, ElectrostaticAntiPeriodic
from src.heatflow import HeatFlowMaterial, HeatFlowFixedTemperature, HeatFlowHeatFlux, HeatFlowConvection, \
    HeatFlowRadiation, HeatFlowPeriodic, HeatFlowAntiPeriodic
from src.magnetics import MagneticMaterial, MagneticDirichlet, MagneticMixed, MagneticAnti, MagneticPeriodic, \
    MagneticAntiPeriodicAirgap, MagneticPeriodicAirgap
from src.geometry import Geometry, Node, Line, CircleArc
from src.general import Material, AutoMeshOption, Boundary


class FemmFields(Enum):
    CURRENT_FLOW = "current_flow"
    ELECTROSTATIC = "electrostatic"
    MAGNETIC = "magnetic"
    HEAT_FLOW = "heat_flow"


class LengthUnit(Enum):
    INCHES = "inches"
    MILLIMETERS = "millimeters"
    CENTIMETERS = "centimeters"
    MILS = "mils"
    METERS = "meters"
    MICROMETERS = "micrometers"


class FemmWriter:
    """Writes out a model snapshot"""

    push = True

    def __init__(self):
        self.field = FemmFields.MAGNETIC
        self.lua_model = []
        self.out_file = "femm_data.csv"

    def validate_field(self, shouldbe=None):
        if self.field not in FemmFields:
            raise ValueError(f"The physical field ({self.field}) is not defined!")

        if shouldbe and shouldbe != self.field:
            raise ValueError(f"({self.field}) != {shouldbe}")

        return True
    def write(self, file_name):
        """Generate a runnable lua-script for a FEMM calculation.

        :param file_name: the code (re)writes the snapshot from the created
                          geometry to the given code
        """
        with open(file_name, "w") as writer:
            for line in self.lua_model:
                writer.write(line + "\n")

    def create_geometry(self, geometry: Geometry):
        """Creates a FEMM geometry with lua file from the model geometry.

        Building patterns can be:
            - nodes,
            - line segments
            - circle_arcs.

        The field type should be defined separately.
        """
        lua_geometry = []

        # 1 - generate the nodes
        for node in geometry.nodes:
            lua_geometry.append(self.add_node(node.x, node.y))

        for line in geometry.lines:
            lua_geometry.append(
                self.add_segment(
                    line.start_pt.x,
                    line.start_pt.y,
                    line.end_pt.x,
                    line.end_pt.y,
                )
            )

        for arc in geometry.circle_arcs:
            # calculate the angle for the femm circle arc generation
            radius = arc.start_pt.distance_to(arc.center_pt)
            clamp = arc.start_pt.distance_to(arc.end_pt) / 2.0

            deg = 2 * round(degrees(asin(clamp / radius)), 2)

            lua_geometry.append(
                self.add_arc(
                    arc.start_pt.x,
                    arc.start_pt.y,
                    arc.end_pt.x,
                    arc.end_pt.y,
                    angle=deg,
                    maxseg=1,
                )
            )

        return lua_geometry

    def init_problem(self, out_file="femm_data.csv"):
        """
        This commands initialize a femm console and flush the variables
        :param out_file: defines the default output file
        """
        out_file = str(Path(out_file).resolve().as_posix())
        cmd_list = []
        cmd_list.append(f'remove("{out_file}")')  # get rid of the old data file, if it exists

        if self.field == FemmFields.MAGNETIC:
            cmd_list.append("newdocument(0)")  # the 0 specifies a magnetics problem
        if self.field == FemmFields.ELECTROSTATIC:
            cmd_list.append("newdocument(1)")  # the 1 specifies electrostatics problem
        if self.field == FemmFields.HEAT_FLOW:
            cmd_list.append("newdocument(2)")  # the 2 specifies heat flow problem
        if self.field == FemmFields.CURRENT_FLOW:
            cmd_list.append("newdocument(3)")  # the 3 specifies current flow problem

        cmd = Template('file_out = openfile("$outfile", "w")')
        cmd = cmd.substitute(outfile=out_file)
        cmd_list.append(cmd)

        if FemmWriter.push:
            self.lua_model.extend(cmd_list)

        return cmd_list

    def close(self):

        cmd_list = []
        cmd_list.append("closefile(file_out)")
        if self.field == FemmFields.MAGNETIC:
            cmd_list.append("mo_close()")
            cmd_list.append("mi_close()")

        if self.field == FemmFields.HEAT_FLOW:
            cmd_list.append("ho_close()")
            cmd_list.append("hi_close()")

        if self.field == FemmFields.ELECTROSTATIC:
            cmd_list.append("eo_close()")
            cmd_list.append("ei_close()")

        if self.field == FemmFields.CURRENT_FLOW:
            cmd_list.append("co_close()")
            cmd_list.append("ci_close()")

        cmd_list.append("quit()")

        if FemmWriter.push:
            self.lua_model.extend(cmd_list)

        return cmd_list

    def analyze(self, flag=1):
        """
        Runs a FEMM analysis to solve a problem. By default, the analysis runs
        in non-visible mode.

        The flag parameter controls whether the fkern window is visible or
        minimized. For a visible window, either specify no value for flag or
        specify 0. For a minimized window, flag should be set to 1.
        """
        cmd = None
        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = Template("mi_analyze($flag)")

        if self.field == FemmFields.HEAT_FLOW:
            cmd = Template("hi_analyze($flag)")

        if self.field == FemmFields.ELECTROSTATIC:
            cmd = Template("ei_analyze($flag)")

        if self.field == FemmFields.CURRENT_FLOW:
            cmd = Template("ci_analyze($flag)")

        if FemmWriter.push:
            self.lua_model.append(cmd.substitute(flag=flag))

        return cmd.substitute(flag=flag)

    def add_node(self, x, y):
        """Adds a node to the given point (x,y)"""
        cmd = None
        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = Template("mi_addnode($x_coord, $y_coord)")

        if self.field == FemmFields.ELECTROSTATIC:
            cmd = Template("ei_addnode($x_coord, $y_coord)")

        if self.field == FemmFields.HEAT_FLOW:
            cmd = Template("hi_addnode($x_coord, $y_coord)")

        if self.field == FemmFields.CURRENT_FLOW:
            cmd = Template("ci_addnode($x_coord, $y_coord)")

        cmd = cmd.substitute(x_coord=x, y_coord=y)

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def add_segment(self, x1, y1, x2, y2, push=True):
        """
        Add a new line segment from the node closest to (x1,y1) to the node closest to
        (x2,y2)
        """

        cmd = None
        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = Template("mi_addsegment($x1_coord, $y1_coord, $x2_coord, $y2_coord)")

        if self.field == FemmFields.ELECTROSTATIC:
            cmd = Template("ei_addsegment($x1_coord, $y1_coord, $x2_coord, $y2_coord)")

        if self.field == FemmFields.HEAT_FLOW:
            cmd = Template("hi_addsegment($x1_coord, $y1_coord, $x2_coord, $y2_coord)")

        if self.field == FemmFields.CURRENT_FLOW:
            cmd = Template("ci_addsegment($x1_coord, $y1_coord, $x2_coord, $y2_coord)")

        cmd = cmd.substitute(x1_coord=x1, y1_coord=y1, x2_coord=x2, y2_coord=y2)

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def add_blocklabel(self, x, y):
        """Add a new block label at (x,y)"""
        cmd = None
        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = Template("mi_addblocklabel($x_coord, $y_coord)")

        if self.field == FemmFields.ELECTROSTATIC:
            cmd = Template("ei_addblocklabel($x_coord, $y_coord)")

        if self.field == FemmFields.HEAT_FLOW:
            cmd = Template("hi_addblocklabel($x_coord, $y_coord)")

        if self.field == FemmFields.CURRENT_FLOW:
            cmd = Template("ci_addblocklabel($x_coord, $y_coord)")

        cmd = cmd.substitute(x_coord=x, y_coord=y)

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def add_arc(self, x1, y1, x2, y2, angle, maxseg):
        """
        Add a new arc segment from the nearest node to (x1,y1) to the nearest
        node to (x2,y2) with angle 'angle' divided into 'maxseg' segments.
        """
        cmd = None
        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = Template("mi_addarc($x_1, $y_1, $x_2, $y_2, $angle, $maxseg)")

        if self.field == FemmFields.ELECTROSTATIC:
            cmd = Template("ei_addarc($x_1, $y_1, $x_2, $y_2, $angle, $maxseg)")

        if self.field == FemmFields.HEAT_FLOW:
            cmd = Template("hi_addarc($x_1, $y_1, $x_2, $y_2, $angle, $maxseg)")

        if self.field == FemmFields.CURRENT_FLOW:
            cmd = Template("ci_addarc($x_1, $y_1, $x_2, $y_2, $angle, $maxseg)")

        cmd = cmd.substitute(x_1=x1, y_1=y1, x_2=x2, y_2=y2, angle=angle, maxseg=maxseg)

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def add_boundary(self, boundary: Boundary):
        """
        :param boundary: checks the type of the boundary parameter, then
        """
        cmd = None
        self.validate_field()

        if FemmWriter.push:
            self.lua_model.append(str(boundary))

        return cmd

    def add_material(self, material: Material):
        """
        Add a material definition to the FEMM simulation.
        Returns:
            str: The FEMM command string added to the Lua model.
        """

        cmd = None
        self.validate_field()

        cmd = str(material)
        if cmd is not None:
            if FemmWriter.push:
                self.lua_model.append(cmd)

        return cmd

    def delete_selected(self):
        """Delete all selected objects"""

        cmd = None
        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = "mi_deleteselected"

        if self.field == FemmFields.ELECTROSTATIC:
            cmd = "ei_deleteselected"

        if self.field == FemmFields.HEAT_FLOW:
            cmd = "hi_deleteselected"

        if self.field == FemmFields.CURRENT_FLOW:
            cmd = "ci_deleteselected"

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def delete_selected_nodes(self):
        """
        Delete all selected nodes. The object should be selected using the node
        selection command.
        """
        cmd = None
        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = "mi_deleteselectednodes"

        if self.field == FemmFields.ELECTROSTATIC:
            cmd = "ei_deleteselectednodes"

        if self.field == FemmFields.HEAT_FLOW:
            cmd = "hi_deleteselectednodes"

        if self.field == FemmFields.CURRENT_FLOW:
            cmd = "ci_deleteselectednodes"

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def delete_selected_labels(self):
        """Delete all selected labels."""
        cmd = None
        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = "mi_deleteselectedlabels"

        if self.field == FemmFields.ELECTROSTATIC:
            cmd = "ei_deleteselectedlabels"

        if self.field == FemmFields.HEAT_FLOW:
            cmd = "hi_deleteselectedlabels"

        if self.field == FemmFields.CURRENT_FLOW:
            cmd = "ci_deleteselectedlabels"

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def delete_selected_segments(self):
        """Delete all selected segments."""
        cmd = None
        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = "mi_deleteselectedsegments"

        if self.field == FemmFields.ELECTROSTATIC:
            cmd = "ei_deleteselectedsegments"

        if self.field == FemmFields.HEAT_FLOW:
            cmd = "hi_deleteselectedsegments"

        if self.field == FemmFields.CURRENT_FLOW:
            cmd = "ci_deleteselectedsegments"

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def delete_selected_arc_segments(self):
        """Delete all selected arc segments."""
        cmd = None
        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = "mi_deleteselectedarcsegments"

        if self.field == FemmFields.ELECTROSTATIC:
            cmd = "ei_deleteselectedarcsegments"

        if self.field == FemmFields.HEAT_FLOW:
            cmd = "hi_deleteselectedarcsegments"

        if self.field == FemmFields.CURRENT_FLOW:
            cmd = "ci_deleteselectedarcsegments"

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def add_point_property(self, prop_name, **kwargs):
        """
        Adds a new point property with the specified name and attributes.

        Attributes by field:
        Electrostatics:
            - Vp: specified potential Vp (V)
            - qp: point charge density qp (C / m)

        Magnetics:
            - a: specified potential a (Wb / m)
            - j: point current j (A)

        Heat Flow:
            - Tp: specified temperature Tp at the point (K)
            - qp: point heat generation (W / m)

        Current Flow:
            - Vp: specified potential Vp (V)
            - qp: point current density qp (A / m)
        """
        cmd = None
        self.validate_field()

        if self.field == FemmFields.ELECTROSTATIC:
            Vp = kwargs.get("Vp", 0)
            qp = kwargs.get("qp", 0)
            cmd = f'ei_addpointprop("{prop_name}", {Vp}, {qp})'

        elif self.field == FemmFields.MAGNETIC:
            a = kwargs.get("a", 0)
            j = kwargs.get("j", 0)
            cmd = f'mi_addpointprop("{prop_name}", {a}, {j})'

        elif self.field == FemmFields.HEAT_FLOW:
            Tp = kwargs.get("Tp", 0)
            qp = kwargs.get("qp", 0)
            cmd = f'hi_addpointprop("{prop_name}", {Tp}, {qp})'

        elif self.field == FemmFields.CURRENT_FLOW:
            Vp = kwargs.get("Vp", 0)
            qp = kwargs.get("qp", 0)
            cmd = f'ci_addpointprop("{prop_name}", {Vp}, {qp})'

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def add_circuit_property(self, circuit_name, i, circuit_type):
        """
        Adds a new circuit property with the specified name, current, and type.

        Parameters:
        - circuit_name: name of the magnetic circuit
        - i: prescribed current in Amperes
        - circuit_type: 0 for a parallel-connected circuit and 1 for a series-connected circuit
        """
        cmd = f'mi_addcircprop("{circuit_name}",{i},{circuit_type})'

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def clear_selected(self):
        """Clears all selected nodes, blocks, segments, and arc segments."""
        cmd = None
        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = "mi_clearselected()"

        elif self.field == FemmFields.ELECTROSTATIC:
            cmd = "ei_clearselected()"

        elif self.field == FemmFields.HEAT_FLOW:
            cmd = "hi_clearselected()"

        elif self.field == FemmFields.CURRENT_FLOW:
            cmd = "ci_clearselected()"

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def select_segment(self, x, y):
        """Select the line segment closest to (x, y)"""
        cmd = None
        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = f'mi_selectsegment({x}, {y})'

        elif self.field == FemmFields.ELECTROSTATIC:
            cmd = f'ei_selectsegment({x}, {y})'

        elif self.field == FemmFields.HEAT_FLOW:
            cmd = f'hi_selectsegment({x}, {y})'

        elif self.field == FemmFields.CURRENT_FLOW:
            cmd = f'ci_selectsegment({x}, {y})'

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def select_arc_segment(self, x, y):
        """Select the arc segment closest to (x, y)"""
        cmd = None
        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = f'mi_selectarcsegment({x}, {y})'

        elif self.field == FemmFields.ELECTROSTATIC:
            cmd = f'ei_selectarcsegment({x}, {y})'

        elif self.field == FemmFields.HEAT_FLOW:
            cmd = f'hi_selectarcsegment({x}, {y})'

        elif self.field == FemmFields.CURRENT_FLOW:
            cmd = f'ci_selectarcsegment({x}, {y})'

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def select_node(self, x, y):
        """Select the node closest to (x, y) and return its coordinates."""
        cmd = None
        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = f'mi_selectnode({x}, {y})'

        elif self.field == FemmFields.ELECTROSTATIC:
            cmd = f'ei_selectnode({x}, {y})'

        elif self.field == FemmFields.HEAT_FLOW:
            cmd = f'hi_selectnode({x}, {y})'

        elif self.field == FemmFields.CURRENT_FLOW:
            cmd = f'ci_selectnode({x}, {y})'

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def select_label(self, x, y):
        """Select the label closest to (x, y) and return its coordinates."""
        cmd = None
        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = f'mi_selectlabel({x}, {y})'

        elif self.field == FemmFields.ELECTROSTATIC:
            cmd = f'ei_selectlabel({x}, {y})'

        elif self.field == FemmFields.HEAT_FLOW:
            cmd = f'hi_selectlabel({x}, {y})'

        elif self.field == FemmFields.CURRENT_FLOW:
            cmd = f'ci_selectlabel({x}, {y})'

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def select_group(self, n):
        """
        Select the n-th group of nodes, segments, arc segments, and block labels.
        Clears all previously selected elements and sets the edit mode to 4 (group).
        """
        cmd = None
        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = f'mi_selectgroup({n})'

        elif self.field == FemmFields.ELECTROSTATIC:
            cmd = f'ei_selectgroup({n})'

        elif self.field == FemmFields.HEAT_FLOW:
            cmd = f'hi_selectgroup({n})'

        elif self.field == FemmFields.CURRENT_FLOW:
            cmd = f'ci_selectgroup({n})'

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def select_circle(self, x, y, R, editmode):
        """
        Select circle selects objects within a circle of radius R centered
        at(x, y).If only x, y, and R paramters are given, the current edit mode
        is used.If the editmode parameter is used, 0 denotes nodes, 2 denotes
        block labels, 2 denotes segments, 3 denotes arcs, and 4 specifies that
        all entity types are to be selected.
        """

        cmd = None
        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = Template("mi_selectcircle($xp, $yp, $Rp, $Editmode)")

        if self.field == FemmFields.ELECTROSTATIC:
            cmd = Template("ei_selectcircle($xp, $yp, $Rp, $Editmode)")

        if self.field == FemmFields.HEAT_FLOW:
            cmd = Template("hi_selectcircle($xp, $yp, $Rp, $Editmode)")

        if self.field == FemmFields.CURRENT_FLOW:
            cmd = Template("ci_selectcircle($xp, $yp, $Rp, $Editmode)")

        cmd = cmd.substitute(xp=x, yp=y, Rp=R, Editmode=editmode)

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def select_rectangle(self, x1, y1, x2, y2, editmode):
        """
        This command selects objects within a rectangle definedby points (x1,y1) and (x2,y2).
        If no editmode parameter is supplied, the current edit mode isused. If the editmode parameter is used,
        0 denotes nodes, 2 denotes block labels, 2 denotessegments, 3 denotes arcs, and 4 specifies that all
        entity types are to be selected.
        """

        cmd = None
        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = Template("mi_selectrectangle($x1p,$y1p,$x2p,$y2p,$Editmode)")

        if self.field == FemmFields.ELECTROSTATIC:
            cmd = Template("ei_selectrectangle($x1p,$y1p,$x2p,$y2p,$Editmode)")

        if self.field == FemmFields.HEAT_FLOW:
            cmd = Template("hi_selectrectangle($x1p,$y1p,$x2p,$y2p,$Editmode)")

        if self.field == FemmFields.CURRENT_FLOW:
            cmd = Template("ci_selectrectangle($x1p,$y1p,$x2p,$y2p,$Editmode)")

        cmd = cmd.substitute(x1p=x1, y1p=y1, x2p=x2, y2p=y2, Editmode=editmode)

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def set_pointprop(self, propname, groupno=0, inductor="<None>"):
        """
        :param propname: Set the selected nodes to have the nodal property 'propname'
        :param groupno: Set the selected nodes to have the group number 'groupno'
        :param inductor: Specifies which conductor the node belongs to. Default value is '<None>'
        """
        prefix = None
        cmd = None
        if self.field == FemmFields.MAGNETIC:
            prefix = "mi"
        elif self.field == FemmFields.HEAT_FLOW:
            prefix = "hi"
        elif self.field == FemmFields.CURRENT_FLOW:
            prefix = "ci"
        elif self.field == FemmFields.ELECTROSTATIC:
            prefix = "ei"

        cmd = f'{prefix}_setnodeprop("{propname}", {groupno}, "{inductor}")'

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def set_segment_prop(
            self,
            propname,
            elementsize=1,
            automesh=1,
            hide=0,
            group=0,
            inductor="<None>",
    ):
        """
        :param propname: boundary property
        :param elementsize: Local element size along segment no greater than
                            elementsize.
        :param automesh: mesher defers to the element constraint defined by
                         elementsize, 1 = mesher automatically chooses mesh
                         size along the selected segments
        :param hide: 0 = not hidden in post-processor, 1 == hidden in post
                     processor
        :param group: A member of group number group
        :param inductor: A member of the conductor specified by the string
                         "inconductor". If the segment is not part of a
                         conductor, this parameter can be specified as
                         "<None>".
        """
        prefix = None
        if self.field == FemmFields.MAGNETIC:
            prefix = "mi"
        elif self.field == FemmFields.HEAT_FLOW:
            prefix = "hi"
        elif self.field == FemmFields.CURRENT_FLOW:
            prefix = "ci"
        elif self.field == FemmFields.ELECTROSTATIC:
            prefix = "ei"

        cmd = f'{prefix}_setsegmentprop("{propname}", {elementsize}, {automesh}, {hide}, {group}, "{inductor}")'

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def set_arc_segment_prop(self, maxsegdeg, propname, hide, group):
        """
        :param maxsegdeg: Meshed with elements that span at most maxsegdeg degrees per element
        :param propname: boundary property
        :param hide: 0 = not hidden in post-processor, 1 == hidden in post processor
        :param group: a member of group number group
        """
        cmd = None
        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = Template("mi_setarcsegmentprop($maxsegdeg, $propname, $hide, $group)")
            cmd = cmd.substitute(
                maxsegdeg=maxsegdeg,
                propname="'" + propname + "'",
                hide=hide,
                group=group,
            )

        if self.field == FemmFields.ELECTROSTATIC:
            cmd = Template("ei_setarcsegmentprop($maxsegdeg, $propname, $hide, $group)")
            cmd = cmd.substitute(
                maxsegdeg=maxsegdeg,
                propname="'" + propname + "'",
                hide=hide,
                group=group,
            )

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def set_blockprop(self, blockname, automesh: AutoMeshOption = AutoMeshOption.AUTOMESH, meshsize=1, group=0,
                      **kwargs):
        """
        :param meshsize: default value is None -> invokes automesh
            this command will use automesh option as the default, if the mesh size is not defined
    
        # these parameters used only in the case of magnetic field
    
        :param magdirection:
    
            The magnetization is directed along an angle in measured in degrees denoted by the
            parameter magdirection. Alternatively, magdirection can be a string containing a
            formula that prescribes the magnetization direction as a function of element position.
            In this formula theta and R denotes the angle in degrees of a line connecting the center
            each element with the origin and the length of this line, respectively; x and y denote
            the x- and y-position of the center of the each element. For axisymmetric problems, r
            and z should be used in place of x and y.
    
        :param group: None, mebmer of the named group
    
        """
        cmd = None
        circuit_name = kwargs.get("circuit_name", "<None>")
        magdirection = kwargs.get("magdirection", 0)
        turns = kwargs.get("turns", 0)

        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = Template(
                "mi_setblockprop($blockname, $automesh, $meshsize, $incircuit, $magdirection, $group, $turns)"
            )
            cmd = cmd.substitute(
                blockname="'" + blockname + "'",
                automesh=automesh.value,
                meshsize=meshsize,
                incircuit="'" + circuit_name + "'",
                magdirection=magdirection,
                group=group,
                turns=turns,
            )

        if self.field == FemmFields.HEAT_FLOW:
            cmd = Template("hi_setblockprop($blockname, $automesh, $meshsize, $group)")
            cmd = cmd.substitute(
                blockname=f'"{blockname}"',
                automesh=automesh.value,
                meshsize=meshsize,
                group=group,
            )

        if self.field == FemmFields.ELECTROSTATIC:
            cmd = Template("ei_setblockprop($blockname, $automesh, $meshsize, $group)")
            cmd = cmd.substitute(
                blockname=f'"{blockname}"',
                automesh=automesh.value,
                meshsize=meshsize,
                group=group,
            )

        if self.field == FemmFields.CURRENT_FLOW:
            cmd = Template("ci_setblockprop($blockname, $automesh, $meshsize, $group)")
            cmd = cmd.substitute(
                blockname=f'"{blockname}"',
                automesh=automesh.value,
                meshsize=meshsize,
                group=group,
            )

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

        # problem commands for the magnetic problem

    def magnetic_problem(self, freq, unit: LengthUnit, type, precision=1e-8, depth=1, minangle=30, acsolver=0):
        """
         Definition of the magnetic problem, like probdef(0,'inches','axi',1e-8,0,30);
    
         :param freq: Frequency in Hertz (required)
         :param unit: "inches","millimeters","centimeters","mils","meters, and"micrometers" (required)
         :param type: "planar", "axi" (required)
         :param precision: 1e-8 (required)
         :param depth: depth of the analysis (not mandatory)
         :param minangle: sent to the mesh generator to define the minimum angle of the meshing triangles(not mandatory)
         :param acsolver: the selected acsolver for the problem (not mandatory) - 0 successive approximation, 1 Newton solver
    
    
        The generated lua command has the following role:
    
         miprobdef(frequency,units,type,precision,(depth),(minangle),(acsolver) changes the problem definition.
         Set frequency to the desired frequency in Hertz. The units parameter specifies the units used for measuring
         length in the problem domain. Valid"units"en-tries are"inches","millimeters","centimeters","mils","meters,
         and"micrometers".Set the parameter problem type to"planar"for a 2-D planar problem, or to"axi"for
         anaxisymmetric problem. The precision parameter dictates the precision required by the solver.
         For example, entering 1E-8 requires the RMS of the residual to be less than 10−8.A fifth parameter,
         representing the depth of sthe problem in the into-the-page direction for2-D planar problems, can also also be
         specified. A sixth parameter represents the minimumangle constraint sent to the mesh generator, 30 degress is
         the usual choice. The acsolver parameter specifies which solver is to be used for AC problems:
         0 for successive approximation, 1 for Newton. A seventh parameter specifies the solver type tobe used
         for AC problems.
        """

        self.validate_field(FemmFields.MAGNETIC)

        cmd = Template("mi_probdef($frequency,$units,$type,$precision, $depth, $minangle, $acsolver)")
        cmd = cmd.substitute(
            frequency=freq,
            units=r"'" + unit.value + r"'",
            type=r"'" + type + r"'",
            precision=precision,
            depth=depth,
            minangle=minangle,
            acsolver=acsolver,
        )

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def heat_problem(
            self,
            units: LengthUnit,
            type,
            precision=1e-8,
            depth=1,
            minangle=30,
            prevsoln=None,
            timestep=1e-3,
    ):
        """
        :param units: "inches", "millimeters", "centimeters", "mils", "meters", "micrometers"
        :param type: "planar", "axi",
        :param precision: Precision required by the solver. Default value is 1E-8
        :param depth: Depth of the problem into the page for 2D problems
        :param minangle: Minimum angle constraint sen to the mesh generator
        :param prevsoln: Indicates the solution from the previous time step assuming transient time problems
        """
        self.validate_field(FemmFields.HEAT_FLOW)
        if type not in {"planar", "axi"}:
            raise ValueError(f"Choose either 'planar' or 'axi', not {type}. ")

        if not prevsoln:
            prevsoln = ""
            timestep = 0

        cmd = f'hi_probdef("{units.value}", "{type}", {precision}, {depth}, {minangle}, "{prevsoln}", {timestep})'

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def electrostatic_problem(self, units: LengthUnit, type, precision=1e-8, depth=1, minangle=30):
        """
        :param units: "inches", "millimeters", "centimeters", "mils", "meters", "micrometers"
        :param type: "planar", "axi",
        :param precision: Precision required by the solver. Default value is 1E-8
        :param depth: Depth of the problem into the page for 2D problems
        :param minangle: Minimum angle constraint sen to the mesh generator
        """

        self.validate_field(FemmFields.ELECTROSTATIC)

        if type not in {"planar", "axi"}:
            raise ValueError(f"Choose either 'planar' or 'axi', not {type}. ")

        cmd = f'ei_probdef("{units.value}", "{type}", {precision}, {depth}, {minangle})'

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def currentflow_problem(self, units: LengthUnit, type, frequency=0, precision=1e-8, depth=1, minangle=30):

        self.validate_field(FemmFields.CURRENT_FLOW)

        if type not in {"planar", "axi"}:
            raise ValueError(f"Choose either 'planar' or 'axi', not {type}. ")

        cmd = f'ci_probdef("{units.value}", "{type}", {frequency}, {precision}, {depth}, {minangle})'

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def save_as(self, file_name):
        """
        To solve the problem with FEMM, you have to save it with the save_as
        command.
    
        mi_saveas("filename") saves the file with name "filename". Note if you
        use a path you must use two backslashes e.g. "c:\\temp\\myfemmfile.fem
        """

        cmd = None
        self.validate_field()
        file_name = str(Path(file_name).resolve().as_posix())

        if self.field == FemmFields.MAGNETIC:
            cmd = Template("mi_saveas($filename)")

        if self.field == FemmFields.HEAT_FLOW:
            cmd = Template("hi_saveas($filename)")

        if self.field == FemmFields.ELECTROSTATIC:
            cmd = Template("ei_saveas($filename)")

        if self.field == FemmFields.CURRENT_FLOW:
            cmd = Template("ci_saveas($filename)")

        cmd = cmd.substitute(filename='"' + file_name + '"')

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def load_solution(self):
        """Loads  and displays the solution."""

        cmd = None
        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = "mi_loadsolution()"

        if self.field == FemmFields.HEAT_FLOW:
            cmd = "hi_loadsolution()"

        if self.field == FemmFields.ELECTROSTATIC:
            cmd = "ei_loadsolution()"

        if self.field == FemmFields.CURRENT_FLOW:
            cmd = "ci_loadsolution()"

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

        # post processing commands --- data extraction

    def line_integral(self, type):
        """
        Calculate the line integral of the defined contour.
    
        Parameter name, values 1, values 2, values 3, values 4
        0 -- Bn ---  total Bn, avg Bn, - , -
        1 -- Ht ---  total Ht, avg Ht, -, -
        2 -- Contour length  --- surface area, - , - , -
        3 -- Stress Tensor Force --- DC r/x force, DC y/z force, 2x r/x force, 2x y/z force
        4 -- Stress Tensor Torque --- total (B.n)^2, avg (B.n)^2
        """

        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = Template("mo_lineintegral($type)")
            cmd = cmd.substitute(type=type)

        return cmd

    def block_integral(self, type):
        """
        Calculate the block integral of the selected blocks.
    
             Type        Definition
            ------      ------------
             0            AJ
             1            A
             2            Magnetic Field Energy
             3            Hysteresis and/or lamination losses
             4            Resistive losses
             5            Block cross-section area
             6            Total losses
             7            Total current
             8            Integral of Bx (Br) over the block
             9            Integral of By (Bax) over the block
             10           Block volume
             11           x (or r) part of steady state Lorentz force
             12           y (or z) part of stead state Lorentz force
             13           x (or r) part of steady state 2x Lorentz force
             14           y (or z) part of stead state 2x Lorentz force
             15           steady state lorentz torque
             16           2×component of Lorentz torque
             17           Magnetic field coenergy
             18           x (or r) part of steady-state weighted stress tensor force
             19           y (or z) part of steady-state weighted stress tensor force
             20           x (or r) part of 2×weighted stress tensor force
             21           y (or z) part of 2×weighted stress tensor force
             22           Steady-state weighted stress tensor torque
             23           2×component of weighted stress tensor torque
             24           R2(i.e.moment of inertia / density)
             25           x (or r) part of 1×weighted stress tensor force
             26           y (or z) part of 1×weighted stress tensor force
             27           1×component of weighted stress tensor torque
             28           x (or r) part of 1×Lorentz force
             29           y (or z) part of 1×Lorentz force
             30           1×component of Lorentz torque
    
             This function returns one (possibly complex) value,e.g.:volume =
             moblockintegral(10)
        """

        cmd = None
        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = Template("mo_blockintegral($type)")
            cmd = cmd.substitute(type=type)

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def get_point_values(self, x, y):
        """
        Get the values associated with the point at x,y Return in order
    
        Symbol      Definition
        ------      ----------
        A           vector potential A or flux φ
        B1          flux density Bx if planar, Brif axisymmetric
        B2          flux density By if planar, Bzif axisymmetric
        Sig         electrical conductivity σ
        E           stored energy density
        H1          field intensity Hxif planar,Hrif axisymmetric
        H2          field intensity Hyif planar,Hzif axisymmetric
        Je          eddy current density
        Js          source current density
        Mu1         relative permeability μxif planar,μrif axisymmetric
        Mu2relative permeability μyif planar,μzif axisymmetric
        Pe          Power density dissipated through ohmic losses
        Ph          Power density dissipated by hysteresis
        """

        cmd = None
        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = Template("mo_getpointvalues($x, $y)")
            cmd = cmd.substitute(x=x, y=y)

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def get_circuit_properties(self, circuit_name, result="current, volt, flux"):
        """Used primarily to obtain impedance information associated with circuit properties.
        Properties are returned for the circuit property named "circuit".
        Three values are returned by the function.
    
        In order, these results are current, volt and flux of the circuit.
        """

        cmd = None
        self.validate_field()

        if self.field == FemmFields.MAGNETIC:
            cmd = Template("$result = mo_getcircuitproperties($circuit)")

        cmd = cmd.substitute(circuit="'" + circuit_name + "'", result=result)

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def write_out_result(self, key, value):
        # writes out a key_value pair
        cmd = Template("write(file_out, '$key', ', ', $value, \"\\{}\")".format("n"))
        cmd = cmd.substitute(key=key, value=value)

        if FemmWriter.push:
            self.lua_model.append(cmd)

        return cmd

    def define_block_label(self, x: float, y: float, material: Material):
        # simplifying the material definition
        self.add_blocklabel(x, y)
        self.select_label(x, y)

        if isinstance(material, MagneticMaterial):
            self.set_blockprop(blockname=material.material_name, automesh=material.auto_mesh,
                               meshsize=material.mesh_size,
                               magdirection=material.remanence_angle)
        else:
            self.set_blockprop(blockname=material.material_name, automesh=material.auto_mesh,
                               meshsize=material.mesh_size)

        self.clear_selected()

    def set_boundary_definition(self, selection_point: Node, boundary: Union[Boundary, None], elementsize=None):
        self.select_segment(selection_point.x, selection_point.y)
        if elementsize:
            automesh = AutoMeshOption.CUSTOM_MESH.value
            elementsize = elementsize

        else:
            automesh = AutoMeshOption.CUSTOM_MESH.value

        self.set_segment_prop(boundary.name or "<None>", automesh=automesh, elementsize=elementsize)
        self.clear_selected()
