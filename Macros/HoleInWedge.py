from Shape import Shape
from Cylinder import Cylinder
from Cuboid import Cuboid
from Wedge import Wedge
from Position import Position
import FreeCAD

class HoleInWedge(Shape):
    NEXT_ID = 1

    def __init__(self, doc, dimension, matrixPos):
        id = "HoleInWedge" + str(HoleInWedge.NEXT_ID)
        super().__init__(id, dimension)

        mainCubeID = "HoleInWedgeMainCube" + str(HoleInWedge.NEXT_ID)
        doc.addObject("Part::Box", mainCubeID)
        doc.getObject(mainCubeID).Length = dimension
        doc.getObject(mainCubeID).Width = dimension
        doc.getObject(mainCubeID).Height = dimension

        cutCubeID = "HoleInWedgeCutCube" + str(HoleInWedge.NEXT_ID)
        doc.addObject("Part::Box", cutCubeID)
        doc.getObject(cutCubeID).Length = 1.5 * dimension
        doc.getObject(cutCubeID).Width = 1.5 * dimension
        doc.getObject(cutCubeID).Height = 1.5 * dimension
        doc.getObject(cutCubeID).Placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), FreeCAD.Rotation(45, 0, 0))

        cylinderID = "HoleInWedgeCylinder" + str(HoleInWedge.NEXT_ID)
        doc.addObject("Part::Cylinder", cylinderID)
        doc.getObject(cylinderID).Radius = dimension/4
        doc.getObject(cylinderID).Height = dimension
        doc.getObject(cylinderID).Angle = 360
        doc.getObject(cylinderID).Placement = FreeCAD.Placement(FreeCAD.Vector(dimension/2, 0, dimension/2), FreeCAD.Rotation(0, 0, -90))
	
        # Wedge
        partialId = "PartialWedge" + str(HoleInWedge.NEXT_ID)
        doc.addObject("Part::Cut", partialId)
        doc.getObject(partialId).Base = doc.getObject(mainCubeID)
        doc.getObject(partialId).Tool = doc.getObject(cutCubeID)
        
        # Cut hole from wedge
        doc.addObject("Part::Cut", id)
        doc.getObject(id).Base = doc.getObject(partialId)
        doc.getObject(id).Tool = doc.getObject(cylinderID)

        HoleInWedge.NEXT_ID += 1
