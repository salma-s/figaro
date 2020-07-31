from Shape import Shape
import FreeCAD
import random

class Cuboid(Shape):
    NEXT_ID = 1
    ROTATIONS = [FreeCAD.Rotation(0, 0, 0)]

    def __init__(self, doc, dimension, matrixPos):
        self.matrixPos = matrixPos
        self.baseShapeType = 'Cuboid'
        self.matrixPos = matrixPos

        id = "Cuboid" + str(Cuboid.NEXT_ID)
        super().__init__(id, dimension, Cuboid.ROTATIONS)
        doc.addObject("Part::Box", id)
        doc.getObject(id).Length = dimension
        doc.getObject(id).Width = dimension
        doc.getObject(id).Height = dimension

        doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(matrixPos[0] * dimension, matrixPos[1] * dimension, matrixPos[2] * dimension), 
            Cuboid.ROTATIONS[0])	

        Cuboid.NEXT_ID += 1
    
    def generateDissimilarShape(self, doc):
        shapes = ['QuarterCircle', 'SemiCircle', 'Wedge', 'HoleInWedge', 'QuarterHoleInCuboid', 'SemiHoleInCuboid', 'HoleInDoor']
        shapeType = shapes[random.randint(0, len(shapes) - 1)]

        return [shapeType, None]

    def generateSimilarShape(self, doc):
        shapes = ['HoleInBox']
        shapeType = shapes[random.randint(0, len(shapes) - 1)]
        return [shapeType, None]

    # Arguments:
    # - doc: The FreeCAD document to create the deep copy in
    # Returns [Cuboid] a deep copy of the shape with the same dimension, matrix position,
    # but in a specified FreeCAD document
    def deepCopy(self, doc):
        return Cuboid(doc, self.dimension, self.matrixPos)
