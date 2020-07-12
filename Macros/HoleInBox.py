from Shape import Shape
from Cuboid import Cuboid
from Cylinder import Cylinder
from Position import Position
import random
import FreeCAD

class HoleInBox(Shape):
    NEXT_ID = 1
    ROTATIONS = [FreeCAD.Rotation(90, 0, 0), FreeCAD.Rotation(0, 90, 0), FreeCAD.Rotation(0, 0, 90)]

    def __init__(self, doc, dimension, matrixPos):
        id = "HoleInBox" + str(HoleInBox.NEXT_ID)
        super().__init__(id, dimension)
        
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

        # Translate block to actual position
        doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(matrixPos[0] * dimension, matrixPos[1] * dimension, matrixPos[2] * dimension), 
            HoleInBox.getRandomRotation(), FreeCAD.Vector(dimension/2, dimension/2, dimension/2))	

        HoleInBox.NEXT_ID += 1
            
    def getRandomRotation():
        n = random.randint(0, len(HoleInBox.ROTATIONS) - 1)
        return HoleInBox.ROTATIONS[n]

