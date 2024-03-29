from Shape import Shape
from CentrelineInfo import CentrelineInfo
import FreeCAD
import random

class HoleInBox(Shape):
    NEXT_ID = 1
    ROTATIONS = [
        FreeCAD.Rotation(90, 0, 0), # Top 
        FreeCAD.Rotation(0, 90, 0), # Right
        FreeCAD.Rotation(0, 0, 90) # Front
    ]

    @staticmethod
    def generateCentrelines(dimension):
        return [
            CentrelineInfo(dimension/2, dimension/2, None, -10, dimension + 10, 0.3*dimension + 10),
            CentrelineInfo(None, dimension/2, dimension/2, -10, dimension + 10, 0.3*dimension + 10),
            CentrelineInfo(dimension/2, None, dimension/2, -10, dimension + 10, 0.3*dimension + 10),
        ]

    def __init__(self, doc, dimension, matrixPos, rotationIndex = None):
        self.baseShapeType = 'HoleInBox'
        self.matrixPos = matrixPos
        id = "HoleInBox" + str(HoleInBox.NEXT_ID)
        super().__init__(id, dimension, HoleInBox.ROTATIONS, HoleInBox.generateCentrelines(dimension))
        
        cubeID = "HoleInBoxCuboid" + str(HoleInBox.NEXT_ID)
        doc.addObject("Part::Box", cubeID)
        doc.getObject(cubeID).Length = dimension
        doc.getObject(cubeID).Width = dimension
        doc.getObject(cubeID).Height = dimension

        cylinderID = "HoleInBoxCylinder" + str(HoleInBox.NEXT_ID)
       	doc.addObject("Part::Cylinder", cylinderID)
        doc.getObject(cylinderID).Radius = 0.3 * dimension
        doc.getObject(cylinderID).Height = dimension
        doc.getObject(cylinderID).Angle = 360
        doc.getObject(cylinderID).Placement = FreeCAD.Placement(FreeCAD.Vector(dimension/2, dimension/2, 0), FreeCAD.Rotation(0, 0, 0))
        
        # Cut cylinder
        doc.addObject("Part::Cut", id)
        doc.getObject(id).Base = doc.getObject(cubeID)
        doc.getObject(id).Tool = doc.getObject(cylinderID)

        # If a rotation is not given, generate a random rotation
        if rotationIndex is None:
            self.rotationIndex = self.getRandomRotationIndex()
        else:
            self.rotationIndex = rotationIndex
            self.centrelineInfo = self.CENTRELNIES[rotationIndex]

        # Translate block to actual position
        doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(matrixPos[0] * dimension, matrixPos[1] * dimension, matrixPos[2] * dimension), 
            HoleInBox.ROTATIONS[self.rotationIndex], FreeCAD.Vector(dimension/2, dimension/2, dimension/2))	

        HoleInBox.NEXT_ID += 1
    
    # Returns [HoleInBox] a deep copy of the shape with the same dimension, matrix position,
    # but in a specified FreeCAD document
    def deepCopy(self, doc):
        return HoleInBox(doc, self.dimension, self.matrixPos, self.rotationIndex)

    def generateDissimilarShape(self, doc):
        shapes = ['QuarterCircle','Wedge', 'HoleInWedge', 'QuarterHoleInCuboid', 'SemiHoleInCuboid', 'SemiCircle']
        shapeType = shapes[random.randint(0, len(shapes) - 1)]
        return [shapeType, None]

    def generateSimilarShape(self, doc):
        shapes = ['HoleInDoor', 'Cuboid']
        shapeType = shapes[random.randint(0, len(shapes) - 1)]
        rotIdx = None
        if shapeType == 'HoleInDoor':
            rotIdx = random.randint(4 * self.rotationIndex, 4 * self.rotationIndex + 3)
            print(self.rotationIndex)
            print(rotIdx)
        return [shapeType, rotIdx]

    def deepCopyWithDifferentRotation(self, doc):
        return HoleInBox(doc, self.dimension, self.matrixPos, self.getRandomRotationIndexWithException(self.rotationIndex))

    