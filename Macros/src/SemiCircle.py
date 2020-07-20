from Shape import Shape
from CentrelineInfo import CentrelineInfo
from CentreArcInfo import CentreArcInfo
import FreeCAD

class SemiCircle(Shape):
    NEXT_ID = 1
    ROTATIONS = [
        FreeCAD.Rotation(0, 0, 0), 
        FreeCAD.Rotation(0, 90, 0),
        FreeCAD.Rotation(90, 0, 0),
        FreeCAD.Rotation(90, 90, 0), 
        FreeCAD.Rotation(180, 0, 0), 
        FreeCAD.Rotation(180, 90, 0),
        FreeCAD.Rotation(270, 0, 0),
        FreeCAD.Rotation(270, 90, 0),
        FreeCAD.Rotation(0, 0, 90), 
        FreeCAD.Rotation(90, 0, 90),
        FreeCAD.Rotation(0, 0, 270),
        FreeCAD.Rotation(90, 0, 270) 
    ]

    @staticmethod
    def generateCentrelines(dimension):
        baseShapeType = 'SemiCircle'
        return [
            CentrelineInfo(dimension/2, dimension/2, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [dimension/2, dimension], dimension/2)),
            CentrelineInfo(None, dimension/2, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [dimension/2, dimension], [0, dimension], dimension/2)),
            CentrelineInfo(dimension/2, dimension/2, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension/2], [0, dimension], dimension/2)),
            CentrelineInfo(dimension/2, None, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType,  [0, dimension/2], [0, dimension], dimension/2)),
            CentrelineInfo(dimension/2, dimension/2, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [0, dimension/2], dimension/2)),
            CentrelineInfo(None, dimension/2, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension/2], [0, dimension], dimension/2)),
            CentrelineInfo(dimension/2, dimension/2, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [dimension/2, dimension], [0, dimension], dimension/2)),
            CentrelineInfo(dimension/2, None, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [dimension/2, dimension], [0, dimension], dimension/2)),
            CentrelineInfo(dimension/2, None, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [dimension/2, dimension], dimension/2)),
            CentrelineInfo(None, dimension/2, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [dimension/2, dimension], dimension/2)),
            CentrelineInfo(dimension/2, None, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [0, dimension/2], dimension/2)),
            CentrelineInfo(None, dimension/2, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [0, dimension/2], dimension/2)),
        ]

    def __init__(self, doc, dimension, matrixPos):
        id = "SemiCircle" + str(SemiCircle.NEXT_ID)
        super().__init__(id, dimension, SemiCircle.ROTATIONS, SemiCircle.generateCentrelines(dimension))

        cubeID = "SemiCircleCuboid" + str(SemiCircle.NEXT_ID)
        doc.addObject("Part::Box", cubeID)
        doc.getObject(cubeID).Length = dimension
        doc.getObject(cubeID).Width = dimension/2
        doc.getObject(cubeID).Height = dimension

        cylinderID = "SemiCircleCylinder" + str(SemiCircle.NEXT_ID)
       	doc.addObject("Part::Cylinder", cylinderID)
        doc.getObject(cylinderID).Radius = dimension/2
        doc.getObject(cylinderID).Height = dimension
        doc.getObject(cylinderID).Angle = 180
        doc.getObject(cylinderID).Placement = FreeCAD.Placement(FreeCAD.Vector(dimension/2, dimension/2, 0), FreeCAD.Rotation(0, 0, 0))

        doc.addObject("Part::Fuse", id)
        doc.getObject(id).Base = doc.getObject(cubeID)
        doc.getObject(id).Tool = doc.getObject(cylinderID)

        # Translate block to actual position
        doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(matrixPos[0] * dimension, matrixPos[1] * dimension, matrixPos[2] * dimension), 
            self.getRandomRotation(), FreeCAD.Vector(dimension/2, dimension/2, dimension/2))

        SemiCircle.NEXT_ID += 1
