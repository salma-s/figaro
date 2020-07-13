from Shape import Shape
from CentrelineInfo import CentrelineInfo
import FreeCAD

class Cylinder(Shape):
    NEXT_ID = 1
    ROTATIONS = [
        FreeCAD.Rotation(90, 0, 0),
        FreeCAD.Rotation(0, 90, 0), 
        FreeCAD.Rotation(0, 0, 90)
    ]

    def generateCentrelines(dimension):
        return [
            CentrelineInfo(dimension/2, dimension/2, None, 0, dimension, dimension/2 + 10),
            CentrelineInfo(None, dimension/2, dimension/2, 0, dimension, dimension/2 + 10),
            CentrelineInfo(dimension/2, None, dimension/2, 0, dimension, dimension/2 + 10),
        ]

    def __init__(self, doc, dimension, matrixPos):
        id = "Cylinder" + str(Cylinder.NEXT_ID)
        allCentrelines = Cylinder.generateCentrelines(dimension)
        super().__init__(id, dimension, Cylinder.ROTATIONS, allCentrelines)
       	doc.addObject("Part::Cylinder", id)
        doc.getObject(id).Radius = dimension/2
        doc.getObject(id).Height = dimension
        doc.getObject(id).Angle = 360
        doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(matrixPos[0] * dimension + dimension/2, matrixPos[1] * dimension + dimension/2, matrixPos[2] * dimension), 
            self.getRandomRotation(), FreeCAD.Vector(0, 0, dimension/2))		

        Cylinder.NEXT_ID += 1