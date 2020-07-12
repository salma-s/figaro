from Shape import Shape
from Cuboid import Cuboid
from Cylinder import Cylinder
from Position import Position
import FreeCAD

class SemiHoleInCuboid(Shape):
    NEXT_ID = 1

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

        SemiHoleInCuboid.NEXT_ID += 1


