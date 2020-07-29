from Shape import Shape
from CentrelineInfo import CentrelineInfo
from CentreArcInfo import CentreArcInfo
import FreeCAD
import random

class SemiCircle(Shape):
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
            CentrelineInfo(dimension/2, dimension/2, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [dimension/2, dimension], dimension/2)), #0,0,0
            CentrelineInfo(dimension/2, dimension/2, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension/2], [0, dimension], dimension/2)), #90,0,0
            CentrelineInfo(dimension/2, dimension/2, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [0, dimension/2], dimension/2)),
            CentrelineInfo(dimension/2, dimension/2, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [dimension/2, dimension], [0, dimension], dimension/2)),

            CentrelineInfo(None, dimension/2, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [dimension/2, dimension], [0, dimension], dimension/2)), #0,90,0
            CentrelineInfo(None, dimension/2, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension/2], [0, dimension], dimension/2)),
            CentrelineInfo(None, dimension/2, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [dimension/2, dimension], dimension/2)),
            CentrelineInfo(None, dimension/2, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [0, dimension/2], dimension/2)),

            CentrelineInfo(dimension/2, None, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType,  [0, dimension/2], [0, dimension], dimension/2)), 
            CentrelineInfo(dimension/2, None, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [dimension/2, dimension], [0, dimension], dimension/2)),
            CentrelineInfo(dimension/2, None, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [dimension/2, dimension], dimension/2)),
            CentrelineInfo(dimension/2, None, dimension/2, -10, dimension + 10, None, CentreArcInfo(baseShapeType, [0, dimension], [0, dimension/2], dimension/2)),
        ]

    def __init__(self, doc, dimension, matrixPos, rotationIndex = None):
        self.baseShapeType = 'SemiCircle'
        self.matrixPos = matrixPos
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

         # If a rotation is not given, generate a random rotation
        if rotationIndex is None:
            self.rotationIndex = self.getRandomRotationIndex()
        else:
            self.rotationIndex = rotationIndex        
        
        # Translate block to actual position
        doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(matrixPos[0] * dimension, matrixPos[1] * dimension, matrixPos[2] * dimension), 
            SemiCircle.ROTATIONS[self.rotationIndex], FreeCAD.Vector(dimension/2, dimension/2, dimension/2))

        SemiCircle.NEXT_ID += 1
    
    # Arguments:
    # - doc: The FreeCAD document to create the deep copy in
    # Returns [SemiCircle] a deep copy of the shape with the same dimension, matrix position,
    # but in a specified FreeCAD document
    def deepCopy(self, doc):
        return SemiCircle(doc, self.dimension, self.matrixPos, self.rotationIndex)

    def generateDissimilarShape(self, doc):
        shapes = ['QuarterCircle', 'Wedge', 'HoleInWedge', 'QuarterHoleInCuboid', 'SemiHoleInCuboid', 'HoleInBox']
        shapeType = shapes[random.randint(0, len(shapes) - 1)]
        # if shapeType == 'QuarterCircle':
        #     return QuarterCircle(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'HoleInBox':
        #     return HoleInBox(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'Wedge':
        #     return Wedge(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'HoleInWedge':
        #     return HoleInWedge(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'QuarterHoleInCuboid':
        #     return QuarterHoleInCuboid(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'SemiHoleInCuboid':
        #     return SemiHoleInCuboid(doc, self.dimension, self.matrixPos)  
        return [shapeType, None]

    def generateSimilarShape(self, doc):
        # TODO: confirm cuboid should be here
        shapes = ['HoleInDoor', 'Cuboid']
        shapeType = shapes[random.randint(0, len(shapes) - 1)]
        # if shapeType == 'HoleInDoor':
        #     return HoleInDoor(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'Cuboid':
        #     return Cuboid(doc, self.dimension, self.matrixPos)
        return [shapeType, None]

    def deepCopyWithDifferentRotation(self, doc):
        return SemiCircle(doc, self.dimension, self.matrixPos, self.getRandomRotationIndexWithException(self.rotationIndex))
