from Shape import Shape
import FreeCAD

class Cylinder(Shape):
    NEXT_ID = 1

    def __init__(self, doc, dimension, matrixPos):
        id = "Cylinder" + str(Cylinder.NEXT_ID)
        super().__init__(id, dimension)
       	doc.addObject("Part::Cylinder", id)
        doc.getObject(id).Radius = dimension/2
        doc.getObject(id).Height = dimension
        doc.getObject(id).Angle = 360
        doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(dimension/2, dimension/2, 0), FreeCAD.Rotation(0, 0, 0))
        # doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(50, 50, 0), FreeCAD.Rotation(0, 90, 0), FreeCAD.Vector(0, 0, 50))	

        Cylinder.NEXT_ID += 1