import math
from copy import copy
from dataclasses import dataclass
import uuid
import ezdxf
import sys

"""
This class defines the basic entities, which can be used for the geometry description in FEMM. 
In this concept does not need to define a different geometry for electrostatic-magnetic and thermal fields.
"""


class Node:
    """
    A Node identified by (x,y) coordinates, optionally it can contains an id number or a label. The id_number and
    the label can be important to rotate and copy and rotate the selected part of the geometry.
    """

    def __init__(self, x=0.0, y=0.0, id=None, label=None, precision=6):
        self.x = x
        self.y = y
        self.id = uuid.uuid4()  # a node has to got a unique id to be translated or moved
        self.label = label  # can be used to denote a group of the elements and make some operation with them
        self.precision = precision  # number of the digits, every coordinate represented in the same precision

    def __add__(self, p):
        """Point(x1+x2, y1+y2)"""
        return Node(self.x + p.x, self.y + p.y)

    def __sub__(self, p):
        """Point(x1-x2, y1-y2)"""
        return Node(self.x - p.x, self.y - p.y)

    def __mul__(self, scalar):
        """Point(x1*x2, y1*y2)"""
        return Node(self.x * scalar, self.y * scalar)

    def __str__(self):
        return f"({self.x}, {self.y}, id={self.id},label={self.label})"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x!r}, {self.y!r}, id={self.id!r},label={self.label!r})"

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def distance_to(self, p):
        """Calculate the distance between two points."""
        return (self - p).length()

    def as_tuple(self):
        """(x, y)"""
        return (self.x, self.y)

    def clone(self):
        """Return a full copy of this point."""
        return Node(self.x, self.y, self.id, self.label, self.precision)

    def move_xy(self, dx, dy):
        """Move to new (x+dx,y+dy)."""
        self.x = round(self.x + dx, self.precision)
        self.y = round(self.y + dy, self.precision)

    def rotate(self, rad):
        """Rotate counter-clockwise by rad radians.

        Positive y goes *up,* as in traditional mathematics.

        Interestingly, you can use this in y-down computer graphics, if
        you just remember that it turns clockwise, rather than
        counter-clockwise.

        The new position is returned as a new Point.
        """
        s, c = [f(rad) for f in (math.sin, math.cos)]
        x, y = (c * self.x - s * self.y, s * self.x + c * self.y)

        return Node(round(x, self.precision), round(y, self.precision), id=self.id)

    def rotate_about(self, p, theta):
        """Rotate counter-clockwise around a point, by theta degrees. The new position is returned as a new Point."""
        result = self.clone()
        result.move_xy(-p.x, -p.y)
        result = result.rotate(theta)
        result.move_xy(p.x, p.y)
        return result


@dataclass
class Line:
    start_pt: Node
    end_pt: Node

    def selection_point(self):
        m_x = (self.start_pt.x + self.end_pt.x) * 0.5
        m_y = (self.start_pt.y + self.end_pt.y) * 0.5
        return Node(m_x, m_y)


@dataclass
class CircleArc:
    start_pt: Node
    center_pt: Node
    end_pt: Node

    def selection_point(self):
        clamp = self.start_pt.distance_to(self.end_pt) / 2.0
        self.radius = self.start_pt.distance_to(self.center_pt)

        theta = round(math.asin(clamp / self.radius) * 180 / math.pi * 2, 2)
        selection_pt = self.start_pt.rotate_about(self.center_pt, math.radians(theta / 2))
        return selection_pt


class Geometry:
    precision = 1e-5

    def __init__(self):
        self.nodes = []
        self.lines = []
        self.circle_arcs = []

    def __add__(self, g):
        """Geometry(g1+g2) means that the nodes and the arcs added"""

        geo = Geometry()
        geo.nodes = self.nodes + g.nodes
        geo.lines = self.lines + g.lines
        geo.circle_arcs = self.circle_arcs + g.circle_arcs

        return geo

    def update_opbjects(self):

        return

    def append_node(self, new_node):
        """Appends the node to the node list only if its not exists, gives back that node object"""
        for i in range(len(self.nodes)):
            if self.nodes[i].distance_to(new_node) < self.epsilon:
                return self.nodes[i]

        self.nodes.append(new_node)
        return new_node

    def import_dxf(self, dxf_file):
        try:
            doc = ezdxf.readfile(str(dxf_file))
        except OSError:
            print("Not a DXF file or a generic I/O error.")
            sys.exit(1)
        except ezdxf.DXFStructureError:
            print("Invalid or corrupted DXF file.")
            sys.exit(2)

        # iterate over all entities in modelspace
        # id start from the given number
        id = 0

        msp = doc.modelspace()
        for e in msp:
            if e.dxftype() == "LINE":
                start = Node(e.dxf.start[0], e.dxf.start[1])
                end = Node(e.dxf.end[0], e.dxf.end[1])
                self.add_line(Line(start, end))
                id += 3

            if e.dxftype() == "ARC":
                start = Node(e.start_point.x, e.start_point.y)
                end = Node(e.end_point.x, e.end_point.y)
                center = Node(e.dxf.center[0], e.dxf.center[1])

                self.add_arc(CircleArc(start, center, end))

                id += 4

            if e.dxftype() == "POLYLINE":
                print(e.__dict__)

    @staticmethod
    def approx_circle(circle: CircleArc):
        """
        This function gets a circle arc and divides it 10 lines, which approximates the outline of the curve.
        :return: list of the lines
        """

        divisions = 10
        lines = []
        start_pt = copy(circle.start_pt)
        for i in range(1, divisions + 1):
            new_node = copy(circle.start_pt.rotate_about(circle.center_pt, i * circle.theta / 180.0 * 3.14 / divisions))
            lines.append(Line(start_pt, new_node))
            start_pt = copy(new_node)
        return lines

    @staticmethod
    def casteljau(bezier: obj.CubicBezier):
        """
        Gets a Bezier object and makes only one Casteljau's iteration step on it without the recursion.

        The algorithm splits the bezier into two, smaller parts denoted by r is the 'right-sides' and l denotes the
        'left sided' one. The algorithm is limited to use cubic beziers only.

        :return: 2 bezier objects, the right and the left one

        """
        # calculating the mid point [m]
        m = (bezier.control1 + bezier.control2) * 0.5

        l0 = bezier.start_pt
        r3 = bezier.end_pt

        l1 = (bezier.start_pt + bezier.control1) * 0.5
        r2 = (bezier.control2 + bezier.end_pt) * 0.5

        l2 = (l1 + m) * 0.5
        r1 = (r2 + m) * 0.5

        l3 = (l2 + r1) * 0.5
        r0 = l3

        r = CubicBezier(start_pt=r0, control1=r1, control2=r2, end_pt=r3)
        l = CubicBezier(start_pt=l0, control1=l1, control2=l2, end_pt=l3)

        return r, l

    def delete_hanging_nodes(self):
        """Delete all nodes, which not part of a another object (Line, Circle, etc)"""
        temp = []
        for node in self.nodes:
            hanging = True
            for line in self.lines:
                if node.id == line.start_pt.id or node.id == line.end_pt.id:
                    hanging = False

            for arc in self.circle_arcs:
                if node.id == arc.start_pt.id or node.id == arc.end_pt.id or node.id == arc.center_pt.id:
                    hanging = False

            if not hanging:
                temp.append(node)

        del self.nodes
        self.nodes = temp

    def clone(self):
        """Return a full copy of this point."""

        geo = Geometry()
        geo.nodes = self.nodes
        geo.lines = self.lines
        geo.circle_arcs = self.circle_arcs

        return geo

    # def node_by_id(self, node_id):
    #
    #     for node in self.nodes:
    #         if node.id == node_id:
    #             return node
    #     return None

    def rotate_about(self, p, theta):
        """Rotate counter-clockwise around a point, by theta degrees. The new position is returned as a new Geometry."""

        # new_nodes = []
        # node_pairs = {}  # node mapping
        for index, node in enumerate(self.nodes):
            self.nodes[index] = node.rotate_about(p, theta)

    # def rotate_about(self, p, theta):
    #     """Rotate counter-clockwise around a point, by theta degrees. The new position is returned as a new Geometry."""
    #
    #     new_nodes = []
    #     node_pairs = {}  # node mapping
    #     for node in self.nodes:
    #         new_node = node.rotate_about(p, theta)
    #         new_nodes.append(new_node)
    #         node_pairs[node.id] = new_node.id
    #
    #     self.nodes = new_nodes
    #
    #     # create the connecting lines
    #     new_lines = []
    #     for line in self.lines:
    #         start_node = self.node_by_id(node_pairs[line.start_pt.id])
    #         end_node = self.node_by_id(node_pairs[line.end_pt.id])
    #         new_lines.append(Line(start_node, end_node))
    #     self.lines = new_lines
    #
    #     # create the bounding arcs for the project
    #     new_arcs = []
    #     for arc in self.circle_arcs:
    #         start_node = self.node_by_id(node_pairs[arc.start_pt.id])
    #         center_node = self.node_by_id(node_pairs[arc.center_pt.id])
    #         end_node = self.node_by_id(node_pairs[arc.end_pt.id])
    #         new_arcs.append(CircleArc(start_node, center_node, end_node))
    #     self.circle_arcs = new_arcs
    #
    #     return self
