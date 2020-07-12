from Shape import Shape
import FreeCAD

class SemiCircle(Shape):
    NEXT_ID = 1

    def __init__(self, doc, dimension, matrixPos):
        id = "SemiCircle" + str(SemiCircle.NEXT_ID)
        super().__init__(id, dimension)

       	doc.addObject("Part::Cylinder", id)
        doc.getObject(id).Radius = dimension / 2
        doc.getObject(id).Height = dimension
        doc.getObject(id).Angle = 180.0

        # Translate block to actual position
        doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(matrixPos[0] * dimension + dimension/2, matrixPos[1] * dimension, matrixPos[2] * dimension), 
            FreeCAD.Rotation(0, 0, 0))

        SemiCircle.NEXT_ID += 1