from Shape import Shape
from Cuboid import Cuboid
from Cylinder import Cylinder
from Position import Position
import FreeCAD

class QuarterHoleInCuboid(Shape):
    NEXT_ID = 1

    def __init__(self, doc, dimension, matrixPos):
        id = "QuarterHoleInCuboid" + str(QuarterHoleInCuboid.NEXT_ID)
        super().__init__(id, dimension)
        
        cubeID = "QuarterHoleInCuboidCube" + str(QuarterHoleInCuboid.NEXT_ID)
        doc.addObject("Part::Box", cubeID)
        doc.getObject(cubeID).Length = dimension
        doc.getObject(cubeID).Width = dimension
        doc.getObject(cubeID).Height = dimension

        quarterHoleID = "QuarterHoleInCuboidCylinder" + str(QuarterHoleInCuboid.NEXT_ID)
        doc.addObject("Part::Cylinder", quarterHoleID)
        doc.getObject(quarterHoleID).Radius = dimension
        doc.getObject(quarterHoleID).Height = dimension
        doc.getObject(quarterHoleID).Angle = 360
        doc.getObject(quarterHoleID).Placement = FreeCAD.Placement(FreeCAD.Vector(0, dimension, 0), FreeCAD.Rotation(0, 0, 0))	
        
        # Cut hole from cube
        doc.addObject("Part::Cut", id)
        doc.getObject(id).Base = doc.getObject(cubeID)
        doc.getObject(id).Tool = doc.getObject(quarterHoleID)

        QuarterHoleInCuboid.NEXT_ID += 1
