from Shape import Shape
from CentrelineInfo import CentrelineInfo
from CentreArcInfo import CentreArcInfo
import FreeCAD
import random

class QuarterCircle(Shape):
    NEXT_ID = 1
    ROTATIONS = [
        FreeCAD.Rotation(0, 0, 0), 
        FreeCAD.Rotation(0, 90, 0),
        FreeCAD.Rotation(0, 180, 0),
        FreeCAD.Rotation(0, 270, 0),

        FreeCAD.Rotation(0, 0, 90),
        FreeCAD.Rotation(0, 90, 90),
        FreeCAD.Rotation(0, 180, 90),
        FreeCAD.Rotation(0, 270, 90),

        FreeCAD.Rotation(0, 0, 180),
        FreeCAD.Rotation(0, 90, 180),
        FreeCAD.Rotation(0, 180, 180), 
        FreeCAD.Rotation(0, 270, 180), 
    ]

    @staticmethod
    def generateCentrelines(dimension):
        baseShapeType = 'QuarterShape'
        return [
            CentrelineInfo(0, 0, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, 0, 0, dimension)),
            CentrelineInfo(None, 0, dimension, -10, dimension + 10, None, CentreArcInfo(baseShapeType, 0, dimension, dimension)),
            CentrelineInfo(dimension, 0, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, dimension, 0, dimension)),
            CentrelineInfo(None, 0, 0, -10, dimension + 10, None, CentreArcInfo(baseShapeType, 0, 0, dimension)),

            CentrelineInfo(0, None, 0, -10, dimension + 10, dimension + 20, CentreArcInfo(baseShapeType, 0, 0, dimension)),
            CentrelineInfo(0, None, dimension, -10, dimension + 10, dimension + 20, CentreArcInfo(baseShapeType, 0, dimension, dimension)),
            CentrelineInfo(dimension, None, dimension, -10, dimension + 10, dimension + 20, CentreArcInfo(baseShapeType, dimension, dimension, dimension)),
            CentrelineInfo(dimension, None, 0, -10, dimension + 10, dimension + 20, CentreArcInfo(baseShapeType, dimension, 0, dimension)),

            CentrelineInfo(0, dimension, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, 0, dimension, dimension)),
            CentrelineInfo(None, dimension, dimension, -10, dimension + 10, None, CentreArcInfo(baseShapeType, dimension, dimension, dimension)),
            CentrelineInfo(dimension, dimension, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, dimension, dimension, dimension)),
            CentrelineInfo(None, dimension, 0, -10, dimension + 10, None, CentreArcInfo(baseShapeType, dimension, 0, dimension)),
        ]

    def __init__(self, doc, dimension, matrixPos, rotationIndex = None):
        self.baseShapeType = 'QuarterCircle'
        self.matrixPos = matrixPos
        id = "QuarterCircle" + str(QuarterCircle.NEXT_ID)
        super().__init__(id, dimension, QuarterCircle.ROTATIONS, QuarterCircle.generateCentrelines(dimension))

        doc.addObject("Part::Cylinder", id)
        doc.getObject(id).Radius = dimension
        doc.getObject(id).Height = dimension
        doc.getObject(id).Angle = 90
        
        # If a rotation is not given, generate a random rotation
        if rotationIndex is None:
            self.rotationIndex = self.getRandomRotationIndex()
        else:
            self.rotationIndex = rotationIndex
        
        # Translate block to actual position
        doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(matrixPos[0] * dimension, matrixPos[1] * dimension, matrixPos[2] * dimension), 
            QuarterCircle.ROTATIONS[self.rotationIndex], FreeCAD.Vector(dimension/2, dimension/2, dimension/2))
      
        QuarterCircle.NEXT_ID += 1

    # Returns [QuarterCircle] a deep copy of the shape with the same dimension, matrix position,
    # but in a specified FreeCAD document
    def deepCopy(self, doc):
        return QuarterCircle(doc, self.dimension, self.matrixPos, self.rotationIndex)

    def generateDissimilarShape(self, doc):
        shapes = ['HoleInDoor', 'HoleInBox', 'Wedge', 'HoleInWedge', 'QuarterHoleInCuboid', 'SemiHoleInCuboid']
        shapeType = shapes[random.randint(0, len(shapes) - 1)]
        return [shapeType, None]
        # if shapeType == 'HoleInDoor':
        #     return HoleInDoor(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'HoleInBox':
        #     return HoleInBox(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'Wedge':
        #     return Wedge(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'QuarterHoleInCuboid':
        #     return QuarterHoleInCuboid(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'HoleInWedge':
        #     return HoleInWedge(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'SemiHoleInCuboid':
        #     return SemiHoleInCuboid(doc, self.dimension, self.matrixPos)  

    def generateSimilarShape(self, doc):
        # TODO: confirm cuboid should be here
        shapes = ['SemiCircle', 'Cuboid']
        shapeType = shapes[random.randint(0, len(shapes) - 1)]
        return [shapeType, None]
        # if shapeType == 'SemiCircle':
        #     return SemiCircle(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'Cuboid':
        #     return Cuboid(doc, self.dimension, self.matrixPos)
    
    def deepCopyWithDifferentRotation(self, doc):
        return QuarterCircle(doc, self.dimension, self.matrixPos, self.getRandomRotationIndexWithException(self.rotationIndex))
