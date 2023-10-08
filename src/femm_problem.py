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
from typing import Union

from shapely import Point
from src.magnetics import MagneticMaterial
from src.geometry import Geometry, Node
from src.general import Material, AutoMeshOption, Boundary, FemmFields, LengthUnit


class FemmProblem:
    """Writes out a model snapshot"""

    def __init__(self, out_file="fem_data.csv"):
        self.field = None
        self.lua_script = []
        self.out_file = out_file

    def write(self, file_name):
        """Generate a runnable lua-script for a FEMM calculation.

        :param file_name: the code (re)writes the snapshot from the created
                          geometry to the given code
        """
        with open(file_name, "w") as writer:
            for line in self.lua_script:
                writer.write(line + "\n")

    def create_geometry(self, geometry: Geometry):
        """Creates a FEMM geometry with lua file from the model geometry.

        Building patterns can be:
            - nodes,
            - line segments
            - circle_arcs.

        The field type should be defined separately.
        """

        # 1 - generate the nodes
        [self.lua_script.append(self.add_node(node)) for node in geometry.nodes]

        for line in geometry.lines:
            self.lua_script.append(self.add_segment(line.start_pt, line.end_pt))

        for arc in geometry.circle_arcs:
            # calculate the angle for the femm circle arc generation
            radius = arc.start_pt.distance_to(arc.center_pt)
            clamp = arc.start_pt.distance_to(arc.end_pt) / 2.0

            deg = 2 * round(degrees(asin(clamp / radius)), 2)

            self.lua_script.append(
                self.add_arc(
                    arc.start_pt,
                    arc.end_pt,
                    angle=deg,
                    maxseg=1,
                )
            )

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

        self.lua_script.extend(cmd_list)

        return cmd_list

    def close(self):

        cmd_list = []
        cmd_list.append("closefile(file_out)")
        cmd_list.append(f"{self.field.output_to_string()}_close()")
        cmd_list.append(f"{self.field.input_to_string()}_close()")
        cmd_list.append("quit()")
        self.lua_script.extend(cmd_list)
        return cmd_list

    def analyze(self, flag=1):
        """
        Runs a FEMM analysis to solve a problem. By default, the analysis runs
        in non-visible mode.

        The flag parameter controls whether the fkern window is visible or
        minimized. For a visible window, either specify no value for flag or
        specify 0. For a minimized window, flag should be set to 1.
        """
        cmd = Template("${field}_analyze($flag)")
        cmd = cmd.substitute(field=self.field.input_to_string(), flag=flag)
        self.lua_script.append(cmd)
        return cmd

    def add_node(self, node: Node):
        """Adds a node to the given point (x,y)"""
        cmd = Template("${field}_addnode($x_coord, $y_coord)")
        cmd = cmd.substitute(field=self.field.input_to_string(), x_coord=node.x, y_coord=node.y)
        return cmd

    def add_segment(self, start_pt: Node, end_pt: Node):
        """
        Add a new line segment from the node closest to (x1,y1) to the node closest to
        (x2,y2)
        """
        cmd = Template("${field}_addsegment($x1_coord, $y1_coord, $x2_coord, $y2_coord)")
        cmd = cmd.substitute(field=self.field.input_to_string(), x1_coord=start_pt.x, y1_coord=start_pt.y,
                             x2_coord=end_pt.x, y2_coord=end_pt.y)
        self.lua_script.append(cmd)
        return cmd

    def add_blocklabel(self, label: Node):
        """Add a new block label at (x,y)"""
        cmd = Template("${field}_addblocklabel($x_coord, $y_coord)")
        cmd = cmd.substitute(field=self.field.input_to_string(), x_coord=label.x, y_coord=label.y)
        self.lua_script.append(cmd)
        return cmd

    def add_arc(self, start_pt: Node, end_pt: Node, angle, maxseg):
        """
        Add a new arc segment from the nearest node to (x1,y1) to the nearest
        node to (x2,y2) with angle 'angle' divided into 'maxseg' segments.
        """
        cmd = Template("${field}_addarc($x_1, $y_1, $x_2, $y_2, $angle, $maxseg)")
        cmd = cmd.substitute(field=self.field.input_to_string(), x_1=start_pt.x, y_1=start_pt.y, x_2=end_pt.x,
                             y_2=end_pt.y, angle=angle, maxseg=maxseg)
        self.lua_script.append(cmd)

        return cmd

    def add_boundary(self, boundary: Boundary):
        """
        :param boundary: checks the type of the boundary parameter, then
        """
        cmd = str(boundary)
        self.lua_script.append(cmd)
        return cmd

    def add_material(self, material: Material):
        """
        Add a material definition to the FEMM simulation.
        Returns:
            str: The FEMM command string added to the Lua model.
        """
        cmd = str(material)
        if cmd is not None:
            self.lua_script.append(cmd)
        return cmd

    def delete_selected(self):
        """Delete all selected objects"""

        cmd = f"{self.field.input_to_string()}_deleteselected"
        self.lua_script.append(cmd)
        return cmd

    def delete_selected_nodes(self):
        """
        Delete all selected nodes. The object should be selected using the node
        selection command.
        """
        cmd = f"{self.field.input_to_string()}_deleteselectednodes"
        self.lua_script.append(cmd)
        return cmd

    def delete_selected_labels(self):
        """Delete all selected labels."""

        cmd = f"{self.field.input_to_string()}_deleteselectedlabels"
        self.lua_script.append(cmd)

        return cmd

    def delete_selected_segments(self):
        """Delete all selected segments."""
        cmd = f"{self.field.input_to_string()}_deleteselectedsegments"
        self.lua_script.append(cmd)

        return cmd

    def delete_selected_arc_segments(self):
        """Delete all selected arc segments."""

        cmd = f"{self.field.input_to_string()}_deleteselectedarcsegments"
        self.lua_script.append(cmd)

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

        self.lua_script.append(cmd)
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
        self.lua_script.append(cmd)
        return cmd

    def clear_selected(self):
        """Clears all selected nodes, blocks, segments, and arc segments."""
        cmd = f"{self.field.input_to_string()}_clearselected()"
        self.lua_script.append(cmd)

        return cmd

    def select_segment(self, x, y):
        """Select the line segment closest to (x, y)"""
        cmd = f"{self.field.input_to_string()}_selectsegment({x}, {y})"
        self.lua_script.append(cmd)

        return cmd

    def select_arc_segment(self, x, y):
        """Select the arc segment closest to (x, y)"""
        cmd = f"{self.field.input_to_string()}_selectarcsegment({x}, {y})"
        self.lua_script.append(cmd)

        return cmd

    def select_node(self, node: Node):
        """Select the node closest to (x, y) and return its coordinates."""
        cmd = f"{self.field.input_to_string()}_selectnode({node.x}, {node.y})"
        self.lua_script.append(cmd)
        return cmd

    def select_label(self, label: Node):
        """Select the label closest to (x, y) and return its coordinates."""
        cmd = f"{self.field.input_to_string()}_selectlabel({label.x}, {label.y})"
        self.lua_script.append(cmd)

        return cmd

    def select_group(self, n):
        """
        Select the n-th group of nodes, segments, arc segments, and block labels.
        Clears all previously selected elements and sets the edit mode to 4 (group).
        """
        cmd = f'{self.field.input_to_string()}_selectgroup({n})'
        self.lua_script.append(cmd)
        return cmd

    def select_circle(self, x, y, R, editmode):
        """
        Select circle selects objects within a circle of radius R centered
        at(x, y).If only x, y, and R paramters are given, the current edit mode
        is used.If the editmode parameter is used, 0 denotes nodes, 2 denotes
        block labels, 2 denotes segments, 3 denotes arcs, and 4 specifies that
        all entity types are to be selected.
        """

        cmd = Template("${field}_selectcircle($xp, $yp, $Rp, $Editmode)")
        cmd = cmd.substitute(field=self.field.input_to_string(), xp=x, yp=y, Rp=R, Editmode=editmode)
        self.lua_script.append(cmd)
        return cmd

    def select_rectangle(self, x1, y1, x2, y2, editmode):
        """
        This command selects objects within a rectangle definedby points (x1,y1) and (x2,y2).
        If no editmode parameter is supplied, the current edit mode isused. If the editmode parameter is used,
        0 denotes nodes, 2 denotes block labels, 2 denotessegments, 3 denotes arcs, and 4 specifies that all
        entity types are to be selected.
        """

        cmd = Template("${field}_selectrectangle($x1p,$y1p,$x2p,$y2p,$Editmode)")
        cmd = cmd.substitute(field=self.field.input_to_string(), x1p=x1, y1p=y1, x2p=x2, y2p=y2, Editmode=editmode)
        self.lua_script.append(cmd)
        return cmd

    def set_pointprop(self, propname, groupno=0, inductor="<None>"):
        """
        :param propname: Set the selected nodes to have the nodal property 'propname'
        :param groupno: Set the selected nodes to have the group number 'groupno'
        :param inductor: Specifies which conductor the node belongs to. Default value is '<None>'
        """
        cmd = f'{self.field.input_to_string()}_setnodeprop("{propname}", {groupno}, "{inductor}")'
        self.lua_script.append(cmd)
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
        cmd = f'{self.field.input_to_string()}_setsegmentprop("{propname}", {elementsize}, {automesh}, {hide}, {group}, "{inductor}")'
        self.lua_script.append(cmd)

        return cmd

    def set_arc_segment_prop(self, maxsegdeg, propname, hide, group):
        """
        :param maxsegdeg: Meshed with elements that span at most maxsegdeg degrees per element
        :param propname: boundary property
        :param hide: 0 = not hidden in post-processor, 1 == hidden in post processor
        :param group: a member of group number group
        """
        cmd = None
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

        self.lua_script.append(cmd)
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

        self.lua_script.append(cmd)
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

        self.field = FemmFields.MAGNETIC
        self.init_problem(out_file=self.out_file)
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

        self.lua_script.append(cmd)
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
        self.field = FemmFields.HEAT_FLOW
        self.init_problem(out_file=self.out_file)
        if type not in {"planar", "axi"}:
            raise ValueError(f"Choose either 'planar' or 'axi', not {type}. ")

        if not prevsoln:
            prevsoln = ""
            timestep = 0

        cmd = f'hi_probdef("{units.value}", "{type}", {precision}, {depth}, {minangle}, "{prevsoln}", {timestep})'

        self.lua_script.append(cmd)
        return cmd

    def electrostatic_problem(self, units: LengthUnit, type, precision=1e-8, depth=1, minangle=30):
        """
        :param units: "inches", "millimeters", "centimeters", "mils", "meters", "micrometers"
        :param type: "planar", "axi",
        :param precision: Precision required by the solver. Default value is 1E-8
        :param depth: Depth of the problem into the page for 2D problems
        :param minangle: Minimum angle constraint sen to the mesh generator
        """
        self.field = FemmFields.ELECTROSTATIC
        self.init_problem(out_file=self.out_file)

        if type not in {"planar", "axi"}:
            raise ValueError(f"Choose either 'planar' or 'axi', not {type}. ")

        cmd = f'ei_probdef("{units.value}", "{type}", {precision}, {depth}, {minangle})'

        self.lua_script.append(cmd)
        return cmd

    def currentflow_problem(self, units: LengthUnit, type, frequency=0, precision=1e-8, depth=1, minangle=30):

        self.field = FemmFields.CURRENT_FLOW
        self.init_problem(out_file=self.out_file)

        if type not in {"planar", "axi"}:
            raise ValueError(f"Choose either 'planar' or 'axi', not {type}. ")

        cmd = f'ci_probdef("{units.value}", "{type}", {frequency}, {precision}, {depth}, {minangle})'

        self.lua_script.append(cmd)
        return cmd

    def save_as(self, file_name):
        """
        To solve the problem with FEMM, you have to save it with the save_as
        command.
    
        mi_saveas("filename") saves the file with name "filename". Note if you
        use a path you must use two backslashes e.g. "c:\\temp\\myfemmfile.fem
        """

        file_name = str(Path(file_name).resolve().as_posix())
        cmd = Template("${field}_saveas($filename)")
        cmd = cmd.substitute(field=self.field.input_to_string(), filename='"' + file_name + '"')
        self.lua_script.append(cmd)
        return cmd

    def load_solution(self):
        """Loads  and displays the solution."""
        cmd = f"{self.field.input_to_string()}_loadsolution()"
        self.lua_script.append(cmd)
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

        if self.field == FemmFields.MAGNETIC:
            cmd = Template("mo_blockintegral($type)")
            cmd = cmd.substitute(type=type)
        self.lua_script.append(cmd)
        return cmd

    def get_point_values(self, node: Node):
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
        if self.field == FemmFields.MAGNETIC:
            cmd = Template("mo_getpointvalues($x, $y)")
            cmd = cmd.substitute(x=node.x, y=node.y)

        # Symbol Definition
        # -----------------
        # V Voltage
        # Dx x- or r- direction component of displacement
        # Dy y- or z- direction component of displacement
        # Ex x- or r- direction component of electric field intensity
        # Ey y- or z- direction component of electric field intensity
        # ex x- or r- direction component of permittivity
        # ey y- or z- direction component of permittivity
        # nrg electric field energy density
        #
        if self.field == FemmFields.ELECTROSTATIC:
            cmd = f"V, Dx, Dy, Ex, Ey, ex, ey, nrg = eo_getpointvalues({node.x}, {node.y})"
            self.lua_script.append(cmd)
            cmd = f'write(file_out, \"x = \", {round(node.x, 4)}, \"y = \",{round(node.y, 4)}, \"E_x =\", Ex,\"\\n\")'
            self.lua_script.append(cmd)
            cmd = f'write(file_out, \"x = \", {round(node.x, 4)}, \"y = \",{round(node.y, 4)}, \"E_y =\", Ey, \"\\n\")'
            self.lua_script.append(cmd)
        return cmd

    def get_integral_values(self, label_list: list, save_image: bool, variable_name: str):
        if self.field == FemmFields.MAGNETIC:
            int_type = {"Fx": 18, "Fy": 19, "Area": 5, "Energy": 2, "Torque": 22, "Flux": 1, "Current": 7}
            for node in label_list:
                self.lua_script.append(f"{self.field.output_to_string()}_selectblock({node.x}, {node.y})")

            self.lua_script.append(
                f"{variable_name} = {self.field.input_to_string}_blockintegral({int_type[variable_name]})")
            if variable_name == "Flux":
                self.lua_script.append(f"coil_area = {self.field.input_to_string}_blockintegral(5)")
            self.lua_script.append(f"{self.field.input_to_string}_clearblock()")
            if variable_name == "Flux":
                self.lua_script.append(f'write(file_out, "{self.out_file}, ", {variable_name}/coil_area, "\\n")')
            else:
                self.lua_script.append(f'write(file_out, "{self.out_file}, ", {variable_name}, "\\n")')

        if self.field == FemmFields.ELECTROSTATIC:
            int_type = {"Energy": 0}

            for node in label_list:
                self.lua_script.append(f"{self.field.output_to_string()}_selectblock({node.x}, {node.y})")

            self.lua_script.append(
                f"{variable_name} = {self.field.output_to_string()}_blockintegral({int_type[variable_name]})")
            self.lua_script.append(f"{self.field.output_to_string()}_clearblock()")
            self.lua_script.append(f'write(file_out, "{self.out_file}, ", {variable_name}, "\\n")')

        if save_image == "saveimage":
            self.lua_script.append(f"{self.field.output_to_string()}_showdensityplot(0, 0, 0.0, 0.1, 'bmag')")
            self.lua_script.append(f"{self.field.output_to_string()}_showcontourplot(-1)")
            self.lua_script.append(f"{self.field.output_to_string()}_resize(600, 600)")
            self.lua_script.append(f"{self.field.output_to_string()}_refreshview()")
            self.lua_script.append(f'{self.field.output_to_string()}_save_bitmap(f"{label_list.__str__()}.bmp");')

    def get_circuit_properties(self, circuit_name, result="current, volt, flux"):
        """Used primarily to obtain impedance information associated with circuit properties.
        Properties are returned for the circuit property named "circuit".
        Three values are returned by the function.
    
        In order, these results are current, volt and flux of the circuit.
        """

        cmd = None
        if self.field == FemmFields.MAGNETIC:
            cmd = Template("$result = mo_getcircuitproperties($circuit)")

        cmd = cmd.substitute(circuit="'" + circuit_name + "'", result=result)
        self.lua_script.append(cmd)
        return cmd

    def write_out_result(self, key, value):
        # writes out a key_value pair
        cmd = Template("write(file_out, '$key', ', ', $value, \"\\{}\")".format("n"))
        cmd = cmd.substitute(key=key, value=value)
        self.lua_script.append(cmd)
        return cmd

    def define_block_label(self, label: Node, material: Material):
        # simplifying the material definition
        self.add_blocklabel(label)
        self.select_label(label)

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

    def make_analysis(self, filename="temp"):

        if self.field == FemmFields.MAGNETIC:
            filename += ".fem"
        elif self.field == FemmFields.ELECTROSTATIC:
            filename += ".fee"
        elif self.field == FemmFields.CURRENT_FLOW:
            filename += ".fec"
        elif self.field == FemmFields.HEAT_FLOW:
            filename += ".feh"

        self.save_as(filename)
        self.analyze()
        self.load_solution()
