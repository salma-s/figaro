from Shape import Shape
from Cuboid import Cuboid
from Cylinder import Cylinder
import random
import FreeCAD

class HoleInDoor(Shape):
    NEXT_ID = 1
    ROTATIONS = [
        FreeCAD.Rotation(0, 0, 0), FreeCAD.Rotation(0, 90, 0), 
        FreeCAD.Rotation(90, 0, 0), FreeCAD.Rotation(90, 90, 0), 
        FreeCAD.Rotation(180, 0, 0), FreeCAD.Rotation(180, 90, 0),
        FreeCAD.Rotation(270, 0, 0), FreeCAD.Rotation(270, 90, 0),
        FreeCAD.Rotation(0, 0, 90), FreeCAD.Rotation(90, 0, 90),
        FreeCAD.Rotation(0, 0, 270), FreeCAD.Rotation(90, 0, 270) 
    ]

    def __init__(self, doc, dimension, matrixPos):
        id = "HoleInDoor" + str(HoleInDoor.NEXT_ID)
        super().__init__(id, dimension)
        
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

        # Translate block to actual position
        doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(matrixPos[0] * dimension, matrixPos[1] * dimension, matrixPos[2] * dimension), 
            HoleInDoor.getRandomRotation(), FreeCAD.Vector(dimension/2, dimension/2, dimension/2))

        HoleInDoor.NEXT_ID += 1

    def getRandomRotation():
        n = random.randint(0, len(HoleInDoor.ROTATIONS) - 1)
        return HoleInDoor.ROTATIONS[n]

