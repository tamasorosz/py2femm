import math
from copy import copy
from dataclasses import dataclass
import uuid
import ezdxf
import sys
from itertools import pairwise

from numpy import linspace

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
        self.label = label  # can be used to denote a group of the elements and make some operation with them
        self.precision = precision  # number of the digits, every coordinate represented in the same precision
        if id is None:
            self.id = uuid.uuid4()  # a node has to got a unique id to be translated or moved
        else:
            self.id = id

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
    id = uuid.uuid4()
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
    id = uuid.uuid4()

    def selection_point(self):
        clamp = self.start_pt.distance_to(self.end_pt) / 2.0
        self.radius = self.start_pt.distance_to(self.center_pt)

        theta = round(math.asin(clamp / self.radius) * 180 / math.pi * 2, 2)
        selection_pt = self.start_pt.rotate_about(self.center_pt, math.radians(theta / 2))
        return selection_pt


class CubicBezier:
    def __init__(
            self,
            start_pt,
            control1,
            control2,
            end_pt,
            attributes: dict = {},
            n_segment=51,
    ):
        self.start_pt = start_pt
        self.control1 = control1
        self.control2 = control2
        self.end_pt = end_pt
        self.id = uuid.uuid4()
        self.attributes = attributes.copy()
        self.n_segment = attributes.get("meshScaling", n_segment)
        self.precision = 1e-5

    def approximate(self):
        X, Y = zip(*(self(ti) for ti in linspace(0, 1, self.n_segment + 1)))

        for Xi, Yi in zip(pairwise(X), pairwise(Y)):
            n0 = Node(Xi[0], Yi[0])
            n1 = Node(Xi[1], Yi[1])
            yield Line(n0, n1)

    def __call__(self, t: float):
        assert (0 <= t) and (t <= 1), f"t [0, 1] not {t}"
        X = (
                (1 - t) ** 3 * self.start_pt.x
                + 3 * (1 - t) ** 2 * t * self.control1.x
                + 3 * (1 - t) * t ** 2 * self.control2.x
                + t ** 3 * self.end_pt.x
        )

        Y = (
                (1 - t) ** 3 * self.start_pt.y
                + 3 * (1 - t) ** 2 * t * self.control1.y
                + 3 * (1 - t) * t ** 2 * self.control2.y
                + t ** 3 * self.end_pt.y
        )

        return X, Y

    def __eq__(self, other):
        """
        If 2 Bezier-Curves have the same set of points, then they are equal.
        """

        if math.dist(self.start_pt, other.start_pt) > self.precision:
            return False

        if math.dist(self.control1, other.control1) > self.precision:
            return False

        if math.dist(self.control2, other.control2) > self.precision:
            return False

        if math.dist(self.end_pt, other.end_pt) > self.precision:
            return False

        return True


class Geometry:
    precision = 1e-5

    def __init__(self):
        self.nodes = []
        self.lines = []
        self.circle_arcs = []
        self.cubic_beziers = []

    def __add__(self, g):
        """Geometry(g1+g2) means that the nodes and the arcs added"""

        geo = Geometry()
        geo.nodes = self.nodes + g.nodes
        geo.lines = self.lines + g.lines
        geo.circle_arcs = self.circle_arcs + g.circle_arcs

        return geo

    def update_nodes(self, node: Node):
        """Update all of the deprecated node ids after rotating the points """

        # lines
        for line in self.lines:
            if line.start_pt.id == node.id:
                line.start_pt = node
            if line.end_pt.id == node.id:
                line.end_pt = node

        # arcs
        for arc in self.circle_arcs:
            if arc.start_pt.id == node.id:
                arc.start_pt = node

            if arc.center_pt == node.id:
                arc.center_pt = node

            if arc.end_pt.id == node.id:
                arc.end_pt = node

        # bezier
        for bez in self.cubic_beziers:
            if bez.start_pt.id == node.id:
                bez.start_pt = node

            if bez.end_pt == node.id:
                bez.end_pt = node

            if bez.control1.id == node.id:
                bez.control1 = node

            if bez.control2.id == node.id:
                bez.control2 = node
        return

    def rotate_about(self, node: Node, angle: float):
        for index, item in enumerate(self.nodes):
            self.nodes[index] = item.rotate_about(node, angle)
            self.update_nodes(self.nodes[index])

    def append_node(self, new_node):
        """Appends the node to the node list only if its not exists, gives back that node object"""
        for i in range(len(self.nodes)):
            if self.nodes[i].distance_to(new_node) < self.precision:
                return self.nodes[i]

        self.nodes.append(new_node)
        return new_node

    def add_node(self, node):
        # self.nodes.append(copy(node))
        self.append_node(node)
        return node

    def add_line(self, line):
        # save every start and end points for the geoemtry
        line.start_pt = self.append_node(line.start_pt)
        line.end_pt = self.append_node(line.end_pt)

        if line not in self.lines:
            self.lines.append(line)

    def add_arc(self, arc):
        # save every start and end points for the geoemtry if they are not exists
        arc.start_pt = self.append_node(arc.start_pt)
        arc.end_pt = self.append_node(arc.end_pt)

        if arc not in self.circle_arcs:
            self.circle_arcs.append(arc)

    def add_cubic_bezier(self, cb):
        # save every start and end points for the geoemtry if they are not exists
        cb.start_pt = self.append_node(cb.start_pt)
        cb.end_pt = self.append_node(cb.end_pt)

        if cb not in self.cubic_beziers:
            self.cubic_beziers.append(cb)

    def delete_hanging_nodes(self):
        """Delete all nodes, which not part of a another object (Line, Circle, etc)"""
        temp = []
        for node in self.nodes:
            hanging = True
            for line in self.lines:
                if node.id == line.start_pt.id or node.id == line.end_pt.id:
                    hanging = False

            for arc in self.circle_arcs:
                if node.id == arc.start_pt.id or node.id == arc.end_pt.id:
                    hanging = False

            if not hanging:
                temp.append(node)

        del self.nodes
        self.nodes = temp

    def append_node(self, new_node):
        """Appends the node to the node list only if its not exists, gives back that node object"""
        for i in range(len(self.nodes)):
            if self.nodes[i].distance_to(new_node) < self.precision:
                return self.nodes[i]

        self.nodes.append(new_node)
        return new_node

    def merge_geometry(self, other):

        for ni in other.nodes:
            self.add_node(copy(ni))

        for li in other.lines:
            self.add_line(copy(li))

        for i, ca in enumerate(other.circle_arcs):
            self.add_arc(copy(ca))

        for cb in other.cubic_beziers:
            self.add_cubic_bezier(copy(cb))

    def merge_lines(self):
        lines = self.lines.copy()
        self.lines.clear()

        for li in lines:
            if li not in self.lines:
                self.add_line(li)

    def meshi_it(self, mesh_strategy):
        mesh = mesh_strategy(self.nodes, self.lines, self.circle_arcs, self.cubic_beziers)
        return mesh

    def delete_line(self, x: float, y: float):
        """
        This functin deletes the line from the geometry closest to the x, y coordinates.
        """
        closest_line = min(self.lines, key=lambda li: li.distance_to_point(x, y))
        idx = self.lines.index(closest_line)
        self.lines.pop(idx)

    def find_node(self, id: int):
        """Finds and gives back a node with the given id"""
        return next((x for x in self.nodes if x.id == id), None)

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
    def casteljau(bezier: CubicBezier):
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
