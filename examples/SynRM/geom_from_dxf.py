import ezdxf
from src.geometry import Geometry, Node, Line, CircleArc


def geom_from_dxf(filename,precision):
    geo = Geometry()
    doc = ezdxf.readfile(filename)
    msp = doc.modelspace()
    NodeBuffer = []
    ii = 1
    for e in msp.query("ARC"):
        geo.circle_arcs += [CircleArc(Node(round(e.start_point.x,precision),round(e.start_point.y,precision),label=ii),Node(round(e.dxf.center.x,precision),round(e.dxf.center.y,precision),label=ii+1),Node(round(e.end_point.x,precision),round(e.end_point.y,precision),label=ii+2))]
        NodeBuffer.append([round(e.end_point.x,precision),round(e.start_point.y,precision),ii])
        NodeBuffer.append([round(e.dxf.center.x,precision),round(e.dxf.center.y,precision),ii+1])
        NodeBuffer.append([round(e.end_point.x,precision),round(e.end_point.y,precision),ii+2])
        ii+=3
    arcNodes = ii
    for e in msp.query("LINE"):
        NodeBuffer.append([round(e.dxf.start.x,precision),round(e.dxf.start.y,precision),ii])
        NodeBuffer.append([round(e.dxf.end.x,precision), round(e.dxf.end.y,precision),ii+1])
        geo.lines += [Line(Node(round(e.dxf.start.x,precision),round(e.dxf.start.y,precision),ii),Node(round(e.dxf.end.x,precision),round(e.dxf.end.y,precision),ii+1))]
        ii+=2
    lineNodes = ii
    # Remove unneeded nodes

    for ii in NodeBuffer:
        geo.nodes += [Node(ii[0], ii[1], ii[2], precision)]
    # for ii in LineBuffer:

    return geo

