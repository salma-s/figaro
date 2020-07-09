from Shape import Shape
from Placement import Placement
import FreeCAD

class Cuboid(Shape):
    NEXT_ID = 1

    def __init__(self, doc, dimension):
        id = "Box" + str(Cuboid.NEXT_ID)
        super().__init__(id, dimension)
        doc.addObject("Part::Box", id)
        doc.getObject(id).Length = dimension[0]
        doc.getObject(id).Width = dimension[1]
        doc.getObject(id).Height = dimension[2]
        Cuboid.NEXT_ID += 1