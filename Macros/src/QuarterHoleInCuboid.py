from Shape import Shape
from CentrelineInfo import CentrelineInfo
from CentreArcInfo import CentreArcInfo
import FreeCAD
import random

class QuarterHoleInCuboid(Shape):
    NEXT_ID = 1
    ROTATIONS = [
        FreeCAD.Rotation(0, 0, 0), 
        FreeCAD.Rotation(0, 0, 180), 
        FreeCAD.Rotation(0, 180, 180), 
        FreeCAD.Rotation(0, 180, 0), 
        
        FreeCAD.Rotation(0, 90, 0), 
        FreeCAD.Rotation(0, 270, 180),
        FreeCAD.Rotation(0, 90, 180), 
        FreeCAD.Rotation(0, 270, 0),
        
        FreeCAD.Rotation(0, 0, 90),
        FreeCAD.Rotation(0, 180, 90),
        FreeCAD.Rotation(0, 90, 90),
        FreeCAD.Rotation(0, 270, 90),
    ]

    @staticmethod
    def generateCentrelines(dimension):
        baseShapeType = 'QuarterShape'
        return [
            CentrelineInfo(0, dimension, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, 0, dimension, dimension)),
            CentrelineInfo(0, 0, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, 0, 0, dimension)),
            CentrelineInfo(dimension, 0, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, dimension, 0, dimension)),
            CentrelineInfo(dimension, dimension, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, dimension, dimension, dimension)),

            CentrelineInfo(None, dimension, dimension, -10, dimension + 10, None, CentreArcInfo(baseShapeType, dimension, dimension, dimension)),
            CentrelineInfo(None, 0, 0, -10, dimension + 10, None, CentreArcInfo(baseShapeType, 0, 0, dimension)),
            CentrelineInfo(None, 0, dimension, -10, dimension + 10, None, CentreArcInfo(baseShapeType, 0, dimension, dimension)),
            CentrelineInfo(None, dimension, 0, -10, dimension + 10, None, CentreArcInfo(baseShapeType, dimension, 0, dimension)),

            CentrelineInfo(0, None, dimension, -10, dimension + 10, None, CentreArcInfo(baseShapeType, 0, dimension, dimension)),
            CentrelineInfo(dimension, None, 0, -10, dimension + 10, None, CentreArcInfo(baseShapeType, dimension, 0, dimension)),
            CentrelineInfo(dimension, None, dimension, -10, dimension + 10, None, CentreArcInfo(baseShapeType, dimension, dimension, dimension)),
            CentrelineInfo(0, None, 0, -10, dimension + 10, None, CentreArcInfo(baseShapeType, 0, 0, dimension)),
        ]

    def __init__(self, doc, dimension, matrixPos, rotationIndex = None):
        self.baseShapeType = 'QuarterHoleInCuboid'
        self.matrixPos = matrixPos
        id = "QuarterHoleInCuboid" + str(QuarterHoleInCuboid.NEXT_ID)
        super().__init__(id, dimension, QuarterHoleInCuboid.ROTATIONS, QuarterHoleInCuboid.generateCentrelines(dimension))
        
        cubeID = "QuarterHoleInCuboidCube" + str(QuarterHoleInCuboid.NEXT_ID)
        doc.addObject("Part::Box", cubeID)
        doc.getObject(cubeID).Length = dimension
        doc.getObject(cubeID).Width = dimension
        doc.getObject(cubeID).Height = dimension

        quarterHoleID = "QuarterHoleInCuboidCylinder" + str(QuarterHoleInCuboid.NEXT_ID)
        doc.addObject("Part::Cylinder", quarterHoleID)
        doc.getObject(quarterHoleID).Radius = dimension
        doc.getObject(quarterHoleID).Height = dimension
        doc.getObject(quarterHoleID).Angle = 360
        doc.getObject(quarterHoleID).Placement = FreeCAD.Placement(FreeCAD.Vector(0, dimension, 0), FreeCAD.Rotation(0, 0, 0))	
        
        # Cut hole from cube
        doc.addObject("Part::Cut", id)
        doc.getObject(id).Base = doc.getObject(cubeID)
        doc.getObject(id).Tool = doc.getObject(quarterHoleID)

        # If a rotation is not given, generate a random rotation
        if rotationIndex is None:
            self.rotationIndex = self.getRandomRotationIndex()
        else:
            self.rotationIndex = rotationIndex
            self.centrelineInfo = self.CENTRELNIES[rotationIndex]

        # Translate block to actual position
        doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(matrixPos[0] * dimension, matrixPos[1] * dimension, matrixPos[2] * dimension), 
            QuarterHoleInCuboid.ROTATIONS[self.rotationIndex], FreeCAD.Vector(dimension/2, dimension/2, dimension/2))	

        QuarterHoleInCuboid.NEXT_ID += 1
    
    # Returns [QuarterHoleInCuboid] a deep copy of the shape with the same dimension, matrix position,
    # but in a specified FreeCAD document
    def deepCopy(self, doc):
        return QuarterHoleInCuboid(doc, self.dimension, self.matrixPos, self.rotationIndex)

    def generateDissimilarShape(self, doc):
        shapes = ['Cuboid', 'HoleInDoor', 'HoleInBox', 'Wedge', 'HoleInWedge', 'QuarterCircle', 'SemiCircle']
        shapeType = shapes[random.randint(0, len(shapes) - 1)]
        return [shapeType, None]

    def generateSimilarShape(self, doc):
        shapes = ['SemiHoleInCuboid']
        shapeType = shapes[random.randint(0, len(shapes) - 1)]
        rotIdx = None
        if shapeType == 'SemiHoleInCuboid':
            rotIdx = self.rotationIndex
        return [shapeType, rotIdx]

    def deepCopyWithDifferentRotation(self, doc):
        return QuarterHoleInCuboid(doc, self.dimension, self.matrixPos, self.getRandomRotationIndexWithException(self.rotationIndex))
