from Shape import Shape
import FreeCAD
import random

class Wedge(Shape):
    NEXT_ID = 1
    ROTATIONS = [
        FreeCAD.Rotation(0, 0, 0), FreeCAD.Rotation(0, 90, 0), FreeCAD.Rotation(0, 180, 0), FreeCAD.Rotation(0, 270, 0), 
        FreeCAD.Rotation(0, 0, 90), FreeCAD.Rotation(0, 90, 90), FreeCAD.Rotation(0, 180, 90), FreeCAD.Rotation(0, 270, 90), 
        FreeCAD.Rotation(0, 0, 180), FreeCAD.Rotation(0, 90, 180), FreeCAD.Rotation(0, 180, 180), FreeCAD.Rotation(0, 270, 180), 
    ]

    def __init__(self, doc, dimension, matrixPos, rotationIndex = None):
        self.baseShapeType = 'Wedge'
        self.matrixPos = matrixPos
        id = "Wedge" + str(Wedge.NEXT_ID)
        super().__init__(id, dimension, Wedge.ROTATIONS)
        
        mainCubeID = "WedgeMainCube" + str(Wedge.NEXT_ID)
        doc.addObject("Part::Box", mainCubeID)
        doc.getObject(mainCubeID).Length = dimension
        doc.getObject(mainCubeID).Width = dimension
        doc.getObject(mainCubeID).Height = dimension

        cutCubeID = "WedgeCutCube" + str(Wedge.NEXT_ID)
        doc.addObject("Part::Box", cutCubeID)
        doc.getObject(cutCubeID).Length = 1.5 * dimension
        doc.getObject(cutCubeID).Width = 1.5 * dimension
        doc.getObject(cutCubeID).Height = 1.5 * dimension
        doc.getObject(cutCubeID).Placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), FreeCAD.Rotation(45, 0, 0))
        
        # Cut cube1
        doc.addObject("Part::Cut", id)
        doc.getObject(id).Base = doc.getObject(mainCubeID)
        doc.getObject(id).Tool = doc.getObject(cutCubeID)

         # If a rotation is not given, generate a random rotation
        if rotationIndex is None:
            self.rotationIndex = self.getRandomRotationIndex()
        else:
            self.rotationIndex = rotationIndex

        # Translate block to actual position
        doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(matrixPos[0] * dimension, matrixPos[1] * dimension, matrixPos[2] * dimension), 
            Wedge.ROTATIONS[self.rotationIndex], FreeCAD.Vector(dimension/2, dimension/2, dimension/2))

        Wedge.NEXT_ID += 1

    # Returns [Wedge] a deep copy of the shape with the same dimension, matrix position,
    # but in a specified FreeCAD document
    def deepCopy(self, doc):
        return Wedge(doc, self.dimension, self.matrixPos, self.rotationIndex)

    def generateDissimilarShape(self, doc):
        shapes = ['Cuboid', 'HoleInDoor', 'HoleInBox', 'QuarterHoleInCuboid', 'SemiHoleInCuboid', 'QuarterCircle', 'SemiCircle']
        shapeType = shapes[random.randint(0, len(shapes) - 1)]
        return [shapeType, None]
        # if shapeType == 'Cuboid':
        #     return Cuboid(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'HoleInDoor':
        #     return HoleInDoor(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'HoleInBox':
        #     return HoleInBox(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'QuarterHoleInCuboid':
        #     return QuarterHoleInCuboid(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'SemiHoleInCuboid':
        #     return SemiHoleInCuboid(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'QuarterCircle':
        #     return QuarterCircle(doc, self.dimension, self.matrixPos)
        # elif shapeType == 'SemiCircle':
        #     return SemiCircle(doc, self.dimension, self.matrixPos)  

    def generateSimilarShape(self, doc):
        shapes = ['HoleInWedge']
        shapeType = shapes[random.randint(0, len(shapes) - 1)] 
        rotIdx = None
        if shapeType == 'HoleInWedge':
            rotIdx = random.randint(2 * self.rotationIndex, 2 * self.rotationIndex + 1)
        return [shapeType, rotIdx]

    def deepCopyWithDifferentRotation(self, doc):
        return Wedge(doc, self.dimension, self.matrixPos, self.getRandomRotationIndexWithException(self.rotationIndex))
