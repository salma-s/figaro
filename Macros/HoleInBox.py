from Shape import Shape
from Cuboid import Cuboid
from Cylinder import Cylinder
from Position import Position
import FreeCAD

class HoleInBox(Shape):
    NEXT_ID = 1

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

        HoleInBox.NEXT_ID += 1
