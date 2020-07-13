from Shape import Shape
import FreeCAD
import random

class SemiCircle(Shape):
    NEXT_ID = 1
    ROTATIONS = [
        FreeCAD.Rotation(0, 0, 0), FreeCAD.Rotation(0, 90, 0), 
        FreeCAD.Rotation(90, 0, 0), FreeCAD.Rotation(90, 90, 0), 
        FreeCAD.Rotation(180, 0, 0), FreeCAD.Rotation(180, 90, 0),
        FreeCAD.Rotation(270, 0, 0), FreeCAD.Rotation(270, 90, 0),
        FreeCAD.Rotation(0, 0, 90), FreeCAD.Rotation(90, 0, 90),
        FreeCAD.Rotation(0, 0, 270), FreeCAD.Rotation(90, 0, 270) 
    ]

    def __init__(self, doc, dimension, matrixPos):
        id = "SemiCircle" + str(SemiCircle.NEXT_ID)
        super().__init__(id, dimension, SemiCircle.ROTATIONS)

       	doc.addObject("Part::Cylinder", id)
        doc.getObject(id).Radius = dimension / 2
        doc.getObject(id).Height = dimension
        doc.getObject(id).Angle = 180.0

        # Translate block to actual position
        doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(matrixPos[0] * dimension + dimension/2, matrixPos[1] * dimension, matrixPos[2] * dimension), 
            self.getRandomRotation(), FreeCAD.Vector(0, dimension/2, dimension/2))

        SemiCircle.NEXT_ID += 1
