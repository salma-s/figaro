from Shape import Shape
from Cuboid import Cuboid
from Cylinder import Cylinder
import FreeCAD

class QuarterCircle(Shape):
    NEXT_ID = 1

    def __init__(self, doc, dimension, matrixPos):
        id = "QuarterCircle" + str(QuarterCircle.NEXT_ID)
        super().__init__(id, dimension)

        doc.addObject("Part::Cylinder", id)
        doc.getObject(id).Radius = dimension
        doc.getObject(id).Height = dimension
        doc.getObject(id).Angle = 90
        
        # Translate block to actual position
        doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(matrixPos[0] * dimension, matrixPos[1] * dimension, matrixPos[2] * dimension), FreeCAD.Rotation(0, 0, 0))	

        QuarterCircle.NEXT_ID += 1


