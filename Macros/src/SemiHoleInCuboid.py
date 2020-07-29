from Shape import Shape
from CentrelineInfo import CentrelineInfo
from CentreArcInfo import CentreArcInfo
import FreeCAD
import random

class SemiHoleInCuboid(Shape):
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
        baseShapeType = 'SemiHoleInCuboid'
        return [
            CentrelineInfo(dimension/2, dimension, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [dimension/2, dimension], [dimension/2, dimension])),
            CentrelineInfo(None, dimension, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [dimension/2, dimension], [0, dimension], [dimension, dimension/2])),
            CentrelineInfo(0, dimension/2, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension/2], [0, dimension], [0, dimension/2])),
            CentrelineInfo(0, None, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension/2], [0, dimension], [0, dimension/2])),
            CentrelineInfo(dimension/2, 0, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [0, dimension/2], [dimension/2, 0])),
            CentrelineInfo(None, 0, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension/2], [0, dimension], [0, dimension/2])),
            CentrelineInfo(dimension, dimension/2, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [dimension/2, dimension], [0, dimension], [dimension, dimension/2])),
            CentrelineInfo(dimension, None, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [dimension/2, dimension], [0, dimension], [dimension, dimension/2])),
            CentrelineInfo(dimension/2, None, dimension, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [dimension/2, dimension], [dimension/2, dimension])),
            CentrelineInfo(None, dimension/2, dimension, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [dimension/2, dimension], [dimension/2, dimension])),
            CentrelineInfo(dimension/2, None, 0, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [0, dimension/2], [dimension/2, 0])),
            CentrelineInfo(None, dimension/2, 0, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [0, dimension/2], [dimension/2, 0])),
        ]

    def __init__(self, doc, dimension, matrixPos, rotationIndex = None):
        self.baseShapeType = 'SemiHoleInCuboid'
        self.matrixPos = matrixPos
        id = "SemiHoleInCuboid" + str(SemiHoleInCuboid.NEXT_ID)
        super().__init__(id, dimension, SemiHoleInCuboid.ROTATIONS, SemiHoleInCuboid.generateCentrelines(dimension))
        
        cubeID = "SemiHoleInCuboidCuboid" + str(SemiHoleInCuboid.NEXT_ID)
        doc.addObject("Part::Box", cubeID)
        doc.getObject(cubeID).Length = dimension
        doc.getObject(cubeID).Width = dimension
        doc.getObject(cubeID).Height = dimension

        semiHoleID = "SemiHoleInCuboidCylinder" + str(SemiHoleInCuboid.NEXT_ID)
        doc.addObject("Part::Cylinder", semiHoleID)
        doc.getObject(semiHoleID).Radius = dimension/2
        doc.getObject(semiHoleID).Height = dimension
        doc.getObject(semiHoleID).Angle = 360
        doc.getObject(semiHoleID).Placement = FreeCAD.Placement(FreeCAD.Vector(dimension/2, dimension, 0), FreeCAD.Rotation(0, 0, 0))	

        # Cut hole from cube
        doc.addObject("Part::Cut", id)
        doc.getObject(id).Base = doc.getObject(cubeID)
        doc.getObject(id).Tool = doc.getObject(semiHoleID)

        # If a rotation is not given, generate a random rotation
        if rotationIndex is None:
            self.rotationIndex = self.getRandomRotationIndex()
        else:
            self.rotationIndex = rotationIndex
            self.centrelineInfo = self.CENTRELNIES[rotationIndex]

        # Translate block to actual position
        doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(matrixPos[0] * dimension, matrixPos[1] * dimension, matrixPos[2] * dimension), 
            SemiHoleInCuboid.ROTATIONS[self.rotationIndex], FreeCAD.Vector(dimension/2, dimension/2, dimension/2))

        SemiHoleInCuboid.NEXT_ID += 1

    # Returns [SemiHoleInCuboid] a deep copy of the shape with the same dimension, matrix position,
    # but in a specified FreeCAD document
    def deepCopy(self, doc):
        return SemiHoleInCuboid(doc, self.dimension, self.matrixPos, self.rotationIndex)

    def generateDissimilarShape(self, doc):
        shapes = ['Cuboid', 'HoleInDoor', 'HoleInBox', 'Wedge', 'HoleInWedge', 'QuarterCircle', 'SemiCircle']
        shapeType = shapes[random.randint(0, len(shapes) - 1)]
        return [shapeType, None]
        # if shapeType == 'Cuboid':
        #     return Cuboid(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'HoleInDoor':
        #     return HoleInDoor(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'HoleInBox':
        #     return HoleInBox(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'Wedge':
        #     return Wedge(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'HoleInWedge':
        #     return HoleInWedge(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'QuarterCircle':
        #     return QuarterCircle(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'SemiCircle':
        #     return SemiCircle(doc, self.dimension, self.matrixPos)  

    def generateSimilarShape(self, doc):
        return ['QuarterHoleInCuboid', None]

    def deepCopyWithDifferentRotation(self, doc):
        return SemiHoleInCuboid(doc, self.dimension, self.matrixPos, self.getRandomRotationIndexWithException(self.rotationIndex))
