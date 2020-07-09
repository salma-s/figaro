from Shape import Shape
from Placement import Placement
import FreeCAD

class Cuboid(Shape):
    def __init__(self, doc, id, dimension):
        super().__init__(doc, id, dimension)
        print(id)
        print(dimension[0])
        doc.addObject("Part::Box", id)
        doc.getObject(id).Length = dimension[0]
        doc.getObject(id).Width = dimension[1]
        doc.getObject(id).Height = dimension[2]