from Shape import Shape
from Cuboid import Cuboid
from Cylinder import Cylinder
from Position import Position
import FreeCAD

class SemiHoleInCuboid(Shape):
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
        id = "SemiHoleInCuboid" + str(SemiHoleInCuboid.NEXT_ID)
        super().__init__(id, dimension)
        
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

        # Translate block to actual position
        doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(matrixPos[0] * dimension, matrixPos[1] * dimension, matrixPos[2] * dimension), 
            SemiHoleInCuboid.getRandomRotation(), FreeCAD.Vector(dimension/2, dimension/2, dimension/2))

        SemiHoleInCuboid.NEXT_ID += 1

    def getRandomRotation():
        n = random.randint(0, len(SemiHoleInCuboid.ROTATIONS) - 1)
        return SemiHoleInCuboid.ROTATIONS[n]



