from Shape import Shape
from Placement import Placement
import FreeCAD

class Cuboid(Shape):
    NEXT_ID = 1

    def __init__(self, doc, dimension, pos = -1):
        id = "Box" + str(Cuboid.NEXT_ID)
        super().__init__(id, dimension)
        doc.addObject("Part::Box", id)
        doc.getObject(id).Length = dimension[0]
        doc.getObject(id).Width = dimension[1]
        doc.getObject(id).Height = dimension[2]

        if pos != -1:
            doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(pos.trans[0], pos.trans[1], pos.trans[2]), FreeCAD.Rotation(pos.rot[0], pos.rot[1], pos.rot[2]))	

        Cuboid.NEXT_ID += 1