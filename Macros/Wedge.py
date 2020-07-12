from Shape import Shape
from Cuboid import Cuboid
from Position import Position
import FreeCAD

class Wedge(Shape):
    NEXT_ID = 1

    def __init__(self, doc, dimension, matrixPos):
        id = "Wedge" + str(Wedge.NEXT_ID)
        super().__init__(id, dimension)
        
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

        # Translate block to actual position
        doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(matrixPos[0] * dimension, matrixPos[1] * dimension, matrixPos[2] * dimension), FreeCAD.Rotation(0, 0, 0))

        Wedge.NEXT_ID += 1
