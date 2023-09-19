import os
from unittest import TestCase

from src.current_flow import CurrentFlowMaterial, CurrentFlowFixedVoltage, CurrentFlowMixed, CurrentFlowSurfaceCurrent, \
    CurrentFlowPeriodic, CurrentFlowAntiPeriodic
from src.electrostatics import ElectrostaticMaterial, ElectrostaticFixedVoltage, ElectrostaticMixed, \
    ElectrostaticSurfaceCharge, ElectrostaticPeriodic, ElectrostaticAntiPeriodic
from src.geometry import Geometry, Node, Line, CircleArc
from src.heatflow import HeatFlowMaterial, HeatFlowFixedTemperature, HeatFlowHeatFlux, HeatFlowConvection, \
    HeatFlowRadiation, HeatFlowPeriodic, HeatFlowAntiPeriodic
from src.magnetics import MagneticMaterial, MagneticDirichlet, MagneticMixed, LamType
from src.femm_problem import FemmProblem
from src.general import FemmFields, LengthUnit, AutoMeshOption


class FemmTester(TestCase):
    def test_not_defined_writer(self):
        writer = FemmProblem()
        writer.field = None

        self.assertRaises(ValueError)

    def test_write(self):
        writer = FemmProblem()
        writer.field = FemmFields.HEAT_FLOW
        writer.lua_model.append("alma")
        writer.write("test_write.lua")
        self.assertEqual(True, os.path.exists("test_write.lua"))
        os.remove("test_write.lua")

    def test_addnode(self):
        x = 1.0
        y = 0.0

        # magnetic field
        res = FemmProblem().add_node(Node(x, y))
        self.assertEqual("mi_addnode(1.0, 0.0)", res)

        # current flow
        fmw = FemmProblem()
        fmw.field = FemmFields.CURRENT_FLOW
        res = fmw.add_node(Node(x, y))
        self.assertEqual("ci_addnode(1.0, 0.0)", res)

        # electrostatic
        fmw = FemmProblem()
        fmw.field = FemmFields.ELECTROSTATIC
        res = fmw.add_node(Node(x, y))
        self.assertEqual("ei_addnode(1.0, 0.0)", res)

        fmw = FemmProblem()
        fmw.field = FemmFields.HEAT_FLOW
        res = fmw.add_node(Node(x, y))
        self.assertEqual("hi_addnode(1.0, 0.0)", res)

    def test_add_segment(self):
        start_node = Node(1.0, 0.0)
        end_node = Node(1.0, 1.0)

        res = FemmProblem().add_segment(start_node, end_node)
        self.assertEqual("mi_addsegment(1.0, 0.0, 1.0, 1.0)", res)

        # current field
        fmw = FemmProblem()
        fmw.field = FemmFields.CURRENT_FLOW
        res = fmw.add_segment(start_node, end_node)
        self.assertEqual("ci_addsegment(1.0, 0.0, 1.0, 1.0)", res)

        # electrostatic field
        fmw = FemmProblem()
        fmw.field = FemmFields.ELECTROSTATIC
        res = fmw.add_segment(start_node, end_node)
        self.assertEqual("ei_addsegment(1.0, 0.0, 1.0, 1.0)", res)

        # heat flow
        fmw = FemmProblem()
        fmw.field = FemmFields.HEAT_FLOW
        res = fmw.add_segment(start_node, end_node)
        self.assertEqual("hi_addsegment(1.0, 0.0, 1.0, 1.0)", res)

    def test_addblocklabel(self):
        label = Node(1.0, 0.0)
        res = FemmProblem().add_blocklabel(label)
        self.assertEqual("mi_addblocklabel(1.0, 0.0)", res)

        fmw = FemmProblem()
        fmw.field = FemmFields.CURRENT_FLOW
        res = fmw.add_blocklabel(label)
        self.assertEqual("ci_addblocklabel(1.0, 0.0)", res)

        fmw.field = FemmFields.HEAT_FLOW
        res = fmw.add_blocklabel(label)
        self.assertEqual("hi_addblocklabel(1.0, 0.0)", res)

        fmw.field = FemmFields.ELECTROSTATIC
        res = fmw.add_blocklabel(label)
        self.assertEqual("ei_addblocklabel(1.0, 0.0)", res)

    def test_addarc(self):
        start_pt = Node(1.0, 0.0)
        end_pt = Node(1.0, 1.0)

        res = FemmProblem().add_arc(start_pt, end_pt, 90.0, 1)
        self.assertEqual("mi_addarc(1.0, 0.0, 1.0, 1.0, 90.0, 1)", res)

        fmw = FemmProblem()
        fmw.field = FemmFields.CURRENT_FLOW
        res = fmw.add_arc(start_pt, end_pt, 90.0, 1)
        self.assertEqual("ci_addarc(1.0, 0.0, 1.0, 1.0, 90.0, 1)", res)

        fmw.field = FemmFields.ELECTROSTATIC
        res = fmw.add_arc(start_pt, end_pt, 90.0, 1)
        self.assertEqual("ei_addarc(1.0, 0.0, 1.0, 1.0, 90.0, 1)", res)

        fmw.field = FemmFields.HEAT_FLOW
        res = fmw.add_arc(start_pt, end_pt, 90.0, 1)
        self.assertEqual("hi_addarc(1.0, 0.0, 1.0, 1.0, 90.0, 1)", res)

    def test_delete_selected(self):
        self.assertEqual("mi_deleteselected", FemmProblem().delete_selected())

        fmw = FemmProblem()
        fmw.field = FemmFields.CURRENT_FLOW
        self.assertEqual("ci_deleteselected", fmw.delete_selected())

        fmw.field = FemmFields.HEAT_FLOW
        self.assertEqual("hi_deleteselected", fmw.delete_selected())

        fmw.field = FemmFields.ELECTROSTATIC
        self.assertEqual("ei_deleteselected", fmw.delete_selected())

    def test_delete_selected_nodes(self):
        self.assertEqual("mi_deleteselectednodes", FemmProblem().delete_selected_nodes())

        fmw = FemmProblem()
        fmw.field = FemmFields.CURRENT_FLOW
        self.assertEqual("ci_deleteselectednodes", fmw.delete_selected_nodes())

        fmw.field = FemmFields.HEAT_FLOW
        self.assertEqual("hi_deleteselectednodes", fmw.delete_selected_nodes())

        fmw.field = FemmFields.ELECTROSTATIC
        self.assertEqual("ei_deleteselectednodes", fmw.delete_selected_nodes())

    def test_delete_selected_labels(self):
        self.assertEqual("mi_deleteselectedlabels", FemmProblem().delete_selected_labels())

        fmw = FemmProblem()
        fmw.field = FemmFields.CURRENT_FLOW
        self.assertEqual("ci_deleteselectedlabels", fmw.delete_selected_labels())

        fmw.field = FemmFields.HEAT_FLOW
        self.assertEqual("hi_deleteselectedlabels", fmw.delete_selected_labels())

        fmw.field = FemmFields.ELECTROSTATIC
        self.assertEqual("ei_deleteselectedlabels", fmw.delete_selected_labels())

    def test_delete_selected_segments(self):
        self.assertEqual("mi_deleteselectedsegments", FemmProblem().delete_selected_segments())

        fmw = FemmProblem()
        fmw.field = FemmFields.CURRENT_FLOW
        self.assertEqual("ci_deleteselectedsegments", fmw.delete_selected_segments())

        fmw.field = FemmFields.HEAT_FLOW
        self.assertEqual("hi_deleteselectedsegments", fmw.delete_selected_segments())

        fmw.field = FemmFields.ELECTROSTATIC
        self.assertEqual("ei_deleteselectedsegments", fmw.delete_selected_segments())

    def test_delete_selected_arc_segments(self):
        self.assertEqual(
            "mi_deleteselectedarcsegments",
            FemmProblem().delete_selected_arc_segments(),
        )

        fmw = FemmProblem()
        fmw.field = FemmFields.CURRENT_FLOW
        self.assertEqual("ci_deleteselectedarcsegments", fmw.delete_selected_arc_segments())

        fmw.field = FemmFields.HEAT_FLOW
        self.assertEqual("hi_deleteselectedarcsegments", fmw.delete_selected_arc_segments())

        fmw.field = FemmFields.ELECTROSTATIC
        self.assertEqual("ei_deleteselectedarcsegments", fmw.delete_selected_arc_segments())

    def test_clear_seelcted(self):
        self.assertEqual("mi_clearselected()", FemmProblem().clear_selected())

        fmw = FemmProblem()
        fmw.field = FemmFields.CURRENT_FLOW
        self.assertEqual("ci_clearselected()", fmw.clear_selected())

        fmw.field = FemmFields.HEAT_FLOW
        self.assertEqual("hi_clearselected()", fmw.clear_selected())

        fmw.field = FemmFields.ELECTROSTATIC
        self.assertEqual("ei_clearselected()", fmw.clear_selected())

    def test_select_segment(self):
        self.assertEqual("mi_selectsegment(1.0, 1.0)", FemmProblem().select_segment(1.0, 1.0))

        fmw = FemmProblem()
        fmw.field = FemmFields.CURRENT_FLOW
        self.assertEqual("ci_selectsegment(1.0, 1.0)", fmw.select_segment(1.0, 1.0))

        fmw.field = FemmFields.HEAT_FLOW
        self.assertEqual("hi_selectsegment(1.0, 1.0)", fmw.select_segment(1.0, 1.0))

        fmw.field = FemmFields.ELECTROSTATIC
        self.assertEqual("ei_selectsegment(1.0, 1.0)", fmw.select_segment(1.0, 1.0))

    def test_select_node(self):
        self.assertEqual("mi_selectnode(1.0, 1.0)", FemmProblem().select_node(1.0, 1.0))

        fmw = FemmProblem()
        fmw.field = FemmFields.CURRENT_FLOW
        self.assertEqual("ci_selectnode(1.0, 1.0)", fmw.select_node(1.0, 1.0))

        fmw.field = FemmFields.HEAT_FLOW
        self.assertEqual("hi_selectnode(1.0, 1.0)", fmw.select_node(1.0, 1.0))

        fmw.field = FemmFields.ELECTROSTATIC
        self.assertEqual("ei_selectnode(1.0, 1.0)", fmw.select_node(1.0, 1.0))

    def test_select_label(self):
        self.assertEqual("mi_selectlabel(1.0, 1.0)", FemmProblem().select_label(1.0, 1.0))

        fmw = FemmProblem()
        fmw.field = FemmFields.CURRENT_FLOW
        self.assertEqual("ci_selectlabel(1.0, 1.0)", fmw.select_label(1.0, 1.0))

        fmw.field = FemmFields.HEAT_FLOW
        self.assertEqual("hi_selectlabel(1.0, 1.0)", fmw.select_label(1.0, 1.0))

        fmw.field = FemmFields.ELECTROSTATIC
        self.assertEqual("ei_selectlabel(1.0, 1.0)", fmw.select_label(1.0, 1.0))

    def test_select_group(self):
        self.assertEqual("mi_selectgroup(4)", FemmProblem().select_group(4))

        fmw = FemmProblem()
        fmw.field = FemmFields.CURRENT_FLOW
        self.assertEqual("ci_selectgroup(4)", fmw.select_group(4))

        fmw.field = FemmFields.HEAT_FLOW
        self.assertEqual("hi_selectgroup(4)", fmw.select_group(4))

        fmw.field = FemmFields.ELECTROSTATIC
        self.assertEqual("ei_selectgroup(4)", fmw.select_group(4))

    def test_select_circle(self):
        self.assertEqual(
            "mi_selectcircle(1.0, 2.0, 0.4, 3)",
            FemmProblem().select_circle(1.0, 2.0, 0.4, 3),
        )

        fmw = FemmProblem()
        fmw.field = FemmFields.CURRENT_FLOW
        self.assertEqual(
            "ci_selectcircle(1.0, 2.0, 0.4, 3)",
            fmw.select_circle(1.0, 2.0, 0.4, 3),
        )

        fmw.field = FemmFields.HEAT_FLOW
        self.assertEqual(
            "hi_selectcircle(1.0, 2.0, 0.4, 3)",
            fmw.select_circle(1.0, 2.0, 0.4, 3),
        )

        fmw.field = FemmFields.ELECTROSTATIC
        self.assertEqual(
            "ei_selectcircle(1.0, 2.0, 0.4, 3)",
            fmw.select_circle(1.0, 2.0, 0.4, 3),
        )

    def test_select_rectangle(self):
        self.assertEqual(
            "mi_selectrectangle(1.0,2.0,3.0,4.0,3)",
            FemmProblem().select_rectangle(1.0, 2.0, 3.0, 4.0, 3),
        )

        fmw = FemmProblem()
        fmw.field = FemmFields.CURRENT_FLOW
        self.assertEqual(
            "ci_selectrectangle(1.0,2.0,3.0,4.0,3)",
            fmw.select_rectangle(1.0, 2.0, 3.0, 4.0, 3),
        )

        fmw.field = FemmFields.HEAT_FLOW
        self.assertEqual(
            "hi_selectrectangle(1.0,2.0,3.0,4.0,3)",
            fmw.select_rectangle(1.0, 2.0, 3.0, 4.0, 3),
        )

        fmw.field = FemmFields.ELECTROSTATIC
        self.assertEqual(
            "ei_selectrectangle(1.0,2.0,3.0,4.0,3)",
            fmw.select_rectangle(1.0, 2.0, 3.0, 4.0, 3),
        )

    def test_magnetic_problem(self):
        self.assertEqual(
            r"mi_probdef(50,'millimeters','axi',1e-08, 1, 30, 0)",
            FemmProblem().magnetic_problem(50, LengthUnit.MILLIMETERS, "axi"),
        )

    def test_heat_problem(self):
        writer = FemmProblem()
        writer.field = FemmFields.HEAT_FLOW
        self.assertEqual(
            'hi_probdef("inches", "planar", 1e-08, 1, 30, "", 0)',
            writer.heat_problem(LengthUnit.INCHES, "planar"),
        )
        self.assertRaises(ValueError, writer.heat_problem, LengthUnit.METERS, "not equal")

    def test_current_flow_problem(self):
        writer = FemmProblem()
        writer.field = FemmFields.CURRENT_FLOW
        self.assertEqual(
            'ci_probdef("inches", "planar", 100, 1e-08, 1, 30)',
            writer.currentflow_problem(LengthUnit.INCHES, "planar", 100, 1e-8, 1, 30),
        )
        self.assertRaises(ValueError, writer.currentflow_problem, "meters", "qwertz")

    def test_electrostatic_problem(self):
        writer = FemmProblem()
        writer.field = FemmFields.ELECTROSTATIC
        self.assertEqual(
            'ei_probdef("inches", "planar", 1e-08, 1, 30)',
            writer.electrostatic_problem(LengthUnit.INCHES, "planar", 1e-8, 1, 30),
        )
        self.assertRaises(ValueError, writer.electrostatic_problem, "mils", "xxx")

    def test_init_problem(self):
        writer = FemmProblem()
        writer.field = FemmFields.MAGNETIC
        print(writer.init_problem())
        self.assertEqual("newdocument(0)", writer.init_problem()[1])

        writer.field = FemmFields.ELECTROSTATIC
        self.assertEqual("newdocument(1)", writer.init_problem()[1])

        writer.field = FemmFields.HEAT_FLOW
        self.assertEqual("newdocument(2)", writer.init_problem()[1])

        writer.field = FemmFields.CURRENT_FLOW
        self.assertEqual("newdocument(3)", writer.init_problem()[1])

    def test_close(self):
        writer = FemmProblem()
        writer.field = FemmFields.ELECTROSTATIC
        self.assertEqual("eo_close()", writer.close()[1])
        self.assertEqual("ei_close()", writer.close()[2])

        writer.field = FemmFields.HEAT_FLOW
        self.assertEqual("ho_close()", writer.close()[1])
        self.assertEqual("hi_close()", writer.close()[2])

        writer.field = FemmFields.CURRENT_FLOW
        self.assertEqual("co_close()", writer.close()[1])
        self.assertEqual("ci_close()", writer.close()[2])

        writer.field = FemmFields.MAGNETIC
        self.assertEqual("mo_close()", writer.close()[1])
        self.assertEqual("mi_close()", writer.close()[2])

    def test_add_circ_prop(self):
        self.assertEqual(
            'mi_addcircprop("test",1,0)',
            FemmProblem().add_circuit_property("test", 1, 0),
        )

    def test_add_magnetic_material(self):
        coil = MagneticMaterial(
            material_name="coil",
            auto_mesh=AutoMeshOption.AUTOMESH,
            mesh_size=0,
            mu_x=1,
            mu_y=1,
            H_c=0,
            J=0,
            Cduct=0,
            Lam_d=0,
            Phi_hmax=0,
            lam_fill=1,
            LamType=LamType.NOT_LAMINATED,
            Phi_hx=0,
            Phi_hy=0,
            NStrands=0,
            WireD=0
        )

        self.assertEqual(
            "mi_addmaterial('coil', 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0)",
            FemmProblem().add_material(coil),
        )

    def test_add_electrostatic_material(self):
        # Electrostatics
        writer = FemmProblem()
        writer.field = FemmFields.ELECTROSTATIC
        mat = ElectrostaticMaterial(material_name="Teflon", ex=2.1, ey=2.1, qv=0)
        self.assertEqual('ei_addmaterial("Teflon", 2.1, 2.1, 0)', writer.add_material(mat))

    def test_thermal_material(self):
        # Heat Flow
        writer = FemmProblem()
        writer.field = FemmFields.HEAT_FLOW
        mat = HeatFlowMaterial(material_name="a", kx=1, ky=2, qv=3, kt=4)
        self.assertEqual('hi_addmaterial("a", 1, 2, 3, 4)', writer.add_material(mat))

    def test_current_field(self):
        # Current Flow
        writer = FemmProblem()
        writer.field = FemmFields.CURRENT_FLOW
        mat = CurrentFlowMaterial(material_name="c", ox=1, oy=2, ex=3, ey=4, ltx=5, lty=6)
        self.assertEqual(
            'ci_addmaterial("c", 1, 2, 3, 4, 5, 6)',
            writer.add_material(mat),
        )

    def test_add_boundary(self):
        # mi_addboundprop('abc', 0, 0, 0, 0, 0, 0, 1 / (r * 0.0254 * pi * 4.e-7), 0, 2);

        # dirichlet boundary condition
        dirichlet_boundary = MagneticDirichlet(name="dirichlet", a_0=1, a_1=2, a_2=3, phi=4)
        self.assertEqual(
            "mi_addboundprop('dirichlet', 1, 2, 3, 4, 0, 0, 0, 0, 0, 0, 0)",
            FemmProblem().add_boundary(dirichlet_boundary),
        )

        # mixed boundary condition
        mixed_boundary = MagneticMixed("mixed_test", 1, 2)
        self.assertEqual(
            "mi_addboundprop('mixed_test', 0, 0, 0, 0, 0, 0, 1, 2, 2, 0, 0)",
            FemmProblem().add_boundary(mixed_boundary),
        )

        # Heatflow tests
        writer = FemmProblem()
        writer.field = FemmFields.HEAT_FLOW

        ht_bc = HeatFlowFixedTemperature("Alma", 110)
        self.assertEqual(
            'hi_addboundprop("Alma", 0, 110, 0, 0, 0, 0)',
            writer.add_boundary(ht_bc),
        )

        ht_bc = HeatFlowHeatFlux("Alma", 27)
        self.assertEqual(
            'hi_addboundprop("Alma", 1, 0, 27, 0, 0, 0)',
            writer.add_boundary(ht_bc),
        )

        ht_bc = HeatFlowConvection("Alma", 33, 27)
        self.assertEqual(
            'hi_addboundprop("Alma", 2, 0, 0, 33, 27, 0)',
            writer.add_boundary(ht_bc),
        )

        ht_bc = HeatFlowRadiation("Alma", 27, 66)
        self.assertEqual(
            'hi_addboundprop("Alma", 3, 0, 0, 27, 0, 66)',
            writer.add_boundary(ht_bc),
        )

        ht_bc = HeatFlowPeriodic("Alma")
        self.assertEqual(
            'hi_addboundprop("Alma", 4, 0, 0, 0, 0, 0)',
            writer.add_boundary(ht_bc),
        )

        ht_bc = HeatFlowAntiPeriodic("Alma")
        self.assertEqual(
            'hi_addboundprop("Alma", 5, 0, 0, 0, 0, 0)',
            writer.add_boundary(ht_bc),
        )

        # Electrostatic tests
        writer = FemmProblem()
        writer.field = FemmFields.ELECTROSTATIC

    def test_add_electrostatic_boundary(self):
        writer = FemmProblem()
        el_bc = ElectrostaticFixedVoltage("eper", 10)
        self.assertEqual(
            'ei_addboundprop("eper", 10, 0, 0, 0, 0)',
            writer.add_boundary(el_bc),
        )

        el_bc = ElectrostaticMixed("eper", 1, 9)
        self.assertEqual('ei_addboundprop("eper", 0, 0, 1, 9, 1)', writer.add_boundary(el_bc))

        el_bc = ElectrostaticSurfaceCharge("eper", 156)
        self.assertEqual(
            'ei_addboundprop("eper", 0, 156, 0, 0, 2)',
            writer.add_boundary(el_bc),
        )

        el_bc = ElectrostaticPeriodic("eper")
        self.assertEqual('ei_addboundprop("eper", 0, 0, 0, 0, 3)', writer.add_boundary(el_bc))

        el_bc = ElectrostaticAntiPeriodic("eper")
        self.assertEqual('ei_addboundprop("eper", 0, 0, 0, 0, 4)', writer.add_boundary(el_bc))

    def test_current_flow_boundary(self):
        # Current Flow
        writer = FemmProblem()
        writer.field = FemmFields.CURRENT_FLOW
        el_bc = CurrentFlowFixedVoltage("alma", 10)
        self.assertEqual(
            'ci_addboundprop("alma", 10, 0, 0, 0, 0)',
            writer.add_boundary(el_bc),
        )

        el_bc = CurrentFlowMixed("alma", 40, 50)
        self.assertEqual(
            'ci_addboundprop("alma", 0, 0, 40, 50, 2)',
            writer.add_boundary(el_bc),
        )

        el_bc = CurrentFlowSurfaceCurrent("alma", 33)
        self.assertEqual(
            'ci_addboundprop("alma", 0, 33, 0, 0, 2)',
            writer.add_boundary(el_bc),
        )

        el_bc = CurrentFlowPeriodic("alma")
        self.assertEqual('ci_addboundprop("alma", 0, 0, 0, 0, 3)', writer.add_boundary(el_bc))

        el_bc = CurrentFlowAntiPeriodic("alma")
        self.assertEqual('ci_addboundprop("alma", 0, 0, 0, 0, 4)', writer.add_boundary(el_bc))

    def test_addpointprop(self):
        writer = FemmProblem()
        writer.field = FemmFields.ELECTROSTATIC
        self.assertEqual(
            'ei_addpointprop("alma", 10, 0)',
            writer.add_point_property("alma", Vp=10),
        )
        self.assertEqual(
            'ei_addpointprop("abc", 0, 0.324)',
            writer.add_point_property("abc", qp=0.324),
        )

        writer.field = FemmFields.HEAT_FLOW
        self.assertEqual(
            'hi_addpointprop("barack", 10, 0)',
            writer.add_point_property("barack", Tp=10),
        )
        self.assertEqual(
            'hi_addpointprop("cba", 0, 0.324)',
            writer.add_point_property("cba", qp=0.324),
        )

        writer.field = FemmFields.CURRENT_FLOW
        self.assertEqual(
            'ci_addpointprop("dinnye", 10, 0)',
            writer.add_point_property("dinnye", Vp=10),
        )
        self.assertEqual(
            'ci_addpointprop("qwert", 0, 0.324)',
            writer.add_point_property("qwert", qp=0.324),
        )

        writer.field = FemmFields.MAGNETIC
        self.assertEqual(
            'mi_addpointprop("ribizli", 10, 0)',
            writer.add_point_property("ribizli", a=10),
        )
        self.assertEqual(
            'mi_addpointprop("qwert123", 0, 0.324)',
            writer.add_point_property("qwert123", j=0.324),
        )
        self.assertEqual(
            'mi_addpointprop("qwert123", 0, 0)',
            writer.add_point_property("qwert123"),
        )

    def test_block_prop(self):
        self.assertEqual(
            "mi_setblockprop('coil', 0, 0.05, 'icoil', 0, 0, 100)",
            FemmProblem().set_blockprop(
                "coil",
                AutoMeshOption.CUSTOM_MESH,
                0.05,
                0,
                circuit_name="icoil",
                turns=100,
                magdirection=0,
            ),
        )

        writer = FemmProblem()
        writer.field = FemmFields.ELECTROSTATIC
        self.assertEqual(
            'ei_setblockprop("alma", 1, 2, 3)',
            writer.set_blockprop("alma", AutoMeshOption.AUTOMESH, 2, 3),
        )

        writer.field = FemmFields.CURRENT_FLOW
        self.assertEqual(
            'ci_setblockprop("alma", 1, 5, 6)',
            writer.set_blockprop("alma", AutoMeshOption.AUTOMESH, 5, 6),
        )

        writer.field = FemmFields.HEAT_FLOW
        self.assertEqual(
            'hi_setblockprop("alma", 1, 8, 9)',
            writer.set_blockprop("alma", AutoMeshOption.AUTOMESH, 8, 9),
        )

    def test_setarcsegment(self):
        self.assertEqual(
            "mi_setarcsegmentprop(5, 'abc', 0, 0)",
            FemmProblem().set_arc_segment_prop(5, "abc", 0, 0),
        )

    def test_setpointprop(self):
        writer = FemmProblem()
        writer.field = FemmFields.ELECTROSTATIC
        self.assertEqual('ei_setnodeprop("eper", 0, "<None>")', writer.set_pointprop("eper"))
        self.assertEqual(
            'ei_setnodeprop("eper", 0, "abc")',
            writer.set_pointprop("eper", inductor="abc"),
        )
        self.assertEqual(
            'ei_setnodeprop("eper", 34, "<None>")',
            writer.set_pointprop("eper", groupno=34),
        )

        writer.field = FemmFields.HEAT_FLOW
        self.assertEqual(
            'hi_setnodeprop("alma", 23, "barack")',
            writer.set_pointprop("alma", 23, "barack"),
        )
        self.assertEqual('hi_setnodeprop("alma", 0, "<None>")', writer.set_pointprop("alma"))

        writer.field = FemmFields.CURRENT_FLOW
        self.assertEqual('ci_setnodeprop("eper", 0, "<None>")', writer.set_pointprop("eper"))
        self.assertEqual(
            'ci_setnodeprop("eper", 0, "abc")',
            writer.set_pointprop("eper", inductor="abc"),
        )
        self.assertEqual(
            'ci_setnodeprop("eper", 34, "<None>")',
            writer.set_pointprop("eper", groupno=34),
        )

        writer.field = FemmFields.MAGNETIC
        self.assertEqual(
            'mi_setnodeprop("alma", 23, "barack")',
            writer.set_pointprop("alma", 23, "barack"),
        )
        self.assertEqual('mi_setnodeprop("alma", 0, "<None>")', writer.set_pointprop("alma"))

    def test_setsegmentprop(self):
        writer = FemmProblem()
        writer.field = FemmFields.HEAT_FLOW
        self.assertEqual(
            'hi_setsegmentprop("alma", 1, 0, 1, 0, "<None>")',
            writer.set_segment_prop("alma", 1, 0, 1, 0),
        )

        writer.field = FemmFields.MAGNETIC
        self.assertEqual(
            'mi_setsegmentprop("eper", 1, 0, 1, 0, "abc")',
            writer.set_segment_prop("eper", 1, 0, 1, 0, "abc"),
        )

        writer.field = FemmFields.ELECTROSTATIC
        self.assertEqual(
            'ei_setsegmentprop("barak", 0, 0.2, 1, 0, "<None>")',
            writer.set_segment_prop("barak", 0, 0.2, 1, 0),
        )

        writer.field = FemmFields.CURRENT_FLOW
        self.assertEqual(
            'ci_setsegmentprop("ribizli", 0, 0.13, 1, 20, "cba")',
            writer.set_segment_prop("ribizli", 0, 0.13, 1, 20, "cba"),
        )

    def test_run_analysis(self):
        writer = FemmProblem()
        writer.field = FemmFields.ELECTROSTATIC
        self.assertEqual("ei_analyze(1)", writer.analyze(1))

        writer.field = FemmFields.HEAT_FLOW
        self.assertEqual("hi_analyze(0)", writer.analyze(0))

        writer.field = FemmFields.CURRENT_FLOW
        self.assertEqual("ci_analyze(1)", writer.analyze())

        writer.field = FemmFields.MAGNETIC
        self.assertEqual("mi_analyze(2)", writer.analyze(2))

    def test_save_as_command(self):
        writer = FemmProblem()
        writer.field = FemmFields.ELECTROSTATIC
        self.assertIn("ei_saveas(", writer.save_as("test"))

        writer.field = FemmFields.CURRENT_FLOW
        self.assertIn("ci_saveas(", writer.save_as("test"))

        writer.field = FemmFields.MAGNETIC
        self.assertIn("mi_saveas(", writer.save_as("test"))

        writer.field = FemmFields.HEAT_FLOW
        self.assertIn("hi_saveas(", writer.save_as("test"))

    def test_get_circuit_name(self):
        self.assertEqual(
            "current, volt, flux = mo_getcircuitproperties('icoil')",
            FemmProblem().get_circuit_properties("icoil"),
        )

    def test_load_solution(self):
        writer = FemmProblem()
        writer.field = FemmFields.ELECTROSTATIC
        self.assertEqual("ei_loadsolution()", writer.load_solution())

        writer.field = FemmFields.CURRENT_FLOW
        self.assertEqual("ci_loadsolution()", writer.load_solution())

        writer.field = FemmFields.MAGNETIC
        self.assertEqual("mi_loadsolution()", writer.load_solution())

        writer.field = FemmFields.HEAT_FLOW
        self.assertEqual("hi_loadsolution()", writer.load_solution())

    def test_line_integral(self):
        self.assertEqual("mo_lineintegral(0)", FemmProblem().line_integral(0))

    def test_block_integral(self):
        self.assertEqual("mo_blockintegral(30)", FemmProblem().block_integral(30))

    def test_get_point_values(self):
        self.assertEqual("mo_getpointvalues(0.01, 0)", FemmProblem().get_point_values(0.01, 0))

    def test_create_geometry(self):
        """create basic objects: nodes, lines and a circle arc to test the basic functionality of the command."""

        geo = Geometry()

        # test nodes
        a = Node(0.0, 0.0)
        b = Node(0.0, 1.0)
        c = Node(1.0, 0.0)

        geo.nodes = [a, b, c]

        geo.lines = [Line(start_pt=a, end_pt=b), Line(start_pt=a, end_pt=c)]
        geo.circle_arcs = [CircleArc(start_pt=c, center_pt=a, end_pt=b)]

        cmds = FemmProblem().create_geometry(geo)

        self.assertIn("mi_addnode(0.0, 0.0)", cmds)
        self.assertIn("mi_addsegment(0.0, 0.0, 0.0, 1.0)", cmds)
        self.assertIn("mi_addarc(1.0, 0.0, 0.0, 1.0, 90.0, 1)", cmds)

        print(cmds)
