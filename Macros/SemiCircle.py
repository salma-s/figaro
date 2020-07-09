from Shape import Shape
from Placement import Placement
import FreeCAD

class SemiCircle(Shape):
    NEXT_ID = 1

    def __init__(self, doc, dimension):
        n = dimension[0]
        id = "SemiCircle" + str(SemiCircle.NEXT_ID)
        super().__init__(id, dimension)
       	doc.addObject("Part::Cylinder", id)
        doc.getObject(id).Radius = n / 2
        doc.getObject(id).Height = n
        doc.getObject(id).Angle = 180.0
        doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(n/2, 0, 0), FreeCAD.Rotation(0, 0, 0))	
        SemiCircle.NEXT_ID += 1