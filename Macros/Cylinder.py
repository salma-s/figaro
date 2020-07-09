from Shape import Shape
from Placement import Placement
import FreeCAD

class Cylinder(Shape):
    def __init__(self, doc, id, dimension):
        super().__init__(id, dimension)
       	doc.addObject("Part::Cylinder", id)
        doc.getObject(id).Radius = dimension[0]
        doc.getObject(id).Height = dimension[1]
        doc.getObject(id).Angle = dimension[2]