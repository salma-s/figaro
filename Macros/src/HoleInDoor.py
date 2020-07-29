from Shape import Shape
from CentrelineInfo import CentrelineInfo
from CentreArcInfo import CentreArcInfo
import FreeCAD
import random

class HoleInDoor(Shape):
    NEXT_ID = 1
    ROTATIONS = [
        FreeCAD.Rotation(0, 0, 0), # Top
        FreeCAD.Rotation(90, 0, 0), 
        FreeCAD.Rotation(180, 0, 0), 
        FreeCAD.Rotation(270, 0, 0), 

        FreeCAD.Rotation(0, 90, 0), # Right
        FreeCAD.Rotation(180, 90, 0), 
        FreeCAD.Rotation(90, 0, 90), 
        FreeCAD.Rotation(90, 0, 270),

        FreeCAD.Rotation(90, 90, 0), # Front
        FreeCAD.Rotation(270, 90, 0), 
        FreeCAD.Rotation(0, 0, 90), 
        FreeCAD.Rotation(0, 0, 270), 
    ]

    @staticmethod
    def generateCentrelines(dimension):
        baseShapeType = 'SemiCircle'
        return [
            CentrelineInfo(dimension/2, dimension/2, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [dimension/4, dimension], dimension/2)), # 0,0,0
            CentrelineInfo(dimension/2, dimension/2, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, 3/4 * dimension], [0, dimension], dimension/2)), # 90,0,0
            CentrelineInfo(dimension/2, dimension/2, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [0, 3/4 * dimension], dimension/2)), #180,0,0
            CentrelineInfo(dimension/2, dimension/2, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [dimension/4, dimension], [0, dimension], dimension/2)), #270,0,0

            CentrelineInfo(None, dimension/2, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [dimension/4, dimension], [0, dimension], dimension/2)), # 0,90,0
            CentrelineInfo(None, dimension/2, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, 3/4 * dimension], [0, dimension], dimension/2)), #180,90,0
            CentrelineInfo(None, dimension/2, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [dimension/4, dimension], dimension/2)), # 90,0,90
            CentrelineInfo(None, dimension/2, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [0, 3/4 * dimension], dimension/2)), # 90,0,270
            
            CentrelineInfo(dimension/2, None, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, 3/4 * dimension], [0, dimension], dimension/2)), # 90,90,0
            CentrelineInfo(dimension/2, None, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [dimension/4, dimension], [0, dimension], dimension/2)), # 270,90, 0
            CentrelineInfo(dimension/2, None, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [dimension/4, dimension], dimension/2)), #0,0,90
            CentrelineInfo(dimension/2, None, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [0, 3/4 * dimension], dimension/2)), # 0,0,270
        ]

    def __init__(self, doc, dimension, matrixPos, rotationIndex = None):
        self.baseShapeType = 'HoleInDoor'
        self.matrixPos = matrixPos
        id = "HoleInDoor" + str(HoleInDoor.NEXT_ID)
        super().__init__(id, dimension, HoleInDoor.ROTATIONS, HoleInDoor.generateCentrelines(dimension))
        
        cubeID = "HoleInDoorCuboid" + str(HoleInDoor.NEXT_ID)
        doc.addObject("Part::Box", cubeID)
        doc.getObject(cubeID).Length = dimension
        doc.getObject(cubeID).Width = dimension/2
        doc.getObject(cubeID).Height = dimension

        mainCylinderID = "HoleInDoorMainCylinder" + str(HoleInDoor.NEXT_ID)
       	doc.addObject("Part::Cylinder", mainCylinderID)
        doc.getObject(mainCylinderID).Radius = dimension/2
        doc.getObject(mainCylinderID).Height = dimension
        doc.getObject(mainCylinderID).Angle = 180
        doc.getObject(mainCylinderID).Placement = FreeCAD.Placement(FreeCAD.Vector(dimension/2, dimension/2, 0), FreeCAD.Rotation(0, 0, 0))

        cutCylinderID = "HoleInDoorCutCylinder" + str(HoleInDoor.NEXT_ID)
       	doc.addObject("Part::Cylinder", cutCylinderID)
        doc.getObject(cutCylinderID).Radius = dimension/4
        doc.getObject(cutCylinderID).Height = dimension
        doc.getObject(cutCylinderID).Angle = 360
        doc.getObject(cutCylinderID).Placement = FreeCAD.Placement(FreeCAD.Vector(dimension/2, dimension/2, 0), FreeCAD.Rotation(0, 0, 0))
        
        # Fuse cuboid and semicircle
        partialId = "PartialHoleInDoor" + str(HoleInDoor.NEXT_ID)
        doc.addObject("Part::Fuse", partialId)
        doc.getObject(partialId).Base = doc.getObject(cubeID)
        doc.getObject(partialId).Tool = doc.getObject(mainCylinderID)

        # Cut hole in partial fused part
        doc.addObject("Part::Cut", id)
        doc.getObject(id).Base = doc.getObject(partialId)
        doc.getObject(id).Tool = doc.getObject(cutCylinderID)

        # If a rotation is not given, generate a random rotation
        if rotationIndex is None:
            self.rotationIndex = self.getRandomRotationIndex()
        else:
            self.rotationIndex = rotationIndex
            self.centrelineInfo = self.CENTRELNIES[rotationIndex]

        # Translate block to actual position
        doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(matrixPos[0] * dimension, matrixPos[1] * dimension, matrixPos[2] * dimension), 
            HoleInDoor.ROTATIONS[self.rotationIndex], FreeCAD.Vector(dimension/2, dimension/2, dimension/2))

        HoleInDoor.NEXT_ID += 1
    
    # Returns [HoleInDoor] a deep copy of the shape with the same dimension, matrix position,
    # but in a specified FreeCAD document
    def deepCopy(self, doc):
        return HoleInDoor(doc, self.dimension, self.matrixPos, self.rotationIndex)

    def generateDissimilarShape(self, doc):
        shapes = ['Cuboid', 'QuarterCircle','Wedge', 'HoleInWedge', 'QuarterHoleInCuboid', 'SemiHoleInCuboid']
        shapeType = shapes[random.randint(0, len(shapes) - 1)]
        return [shapeType, None]

    def generateSimilarShape(self, doc):
        shapes = ['HoleInBox', 'SemiCircle']
        shapeType = shapes[random.randint(0, len(shapes) - 1)]
        rotIdx = None
        if shapeType == 'HoleInBox':
            rotIdx = self.rotationIndex // 4
        elif shapeType == 'SemiCircle':
            rotIdx = self.rotationIndex
        return [shapeType, rotIdx]

    def deepCopyWithDifferentRotation(self, doc):
        return HoleInDoor(doc, self.dimension, self.matrixPos, self.getRandomRotationIndexWithException(self.rotationIndex))
    