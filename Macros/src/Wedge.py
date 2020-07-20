from Shape import Shape
import FreeCAD

class Wedge(Shape):
    NEXT_ID = 1
    ROTATIONS = [
        FreeCAD.Rotation(0, 0, 0), FreeCAD.Rotation(0, 90, 0), FreeCAD.Rotation(0, 180, 0), FreeCAD.Rotation(0, 270, 0), 
        FreeCAD.Rotation(0, 0, 90), FreeCAD.Rotation(0, 90, 90), FreeCAD.Rotation(0, 180, 90), FreeCAD.Rotation(0, 270, 90), 
        FreeCAD.Rotation(0, 0, 180), FreeCAD.Rotation(0, 90, 180), FreeCAD.Rotation(0, 180, 180), FreeCAD.Rotation(0, 270, 180), 
    ]

    def __init__(self, doc, dimension, matrixPos):
        id = "Wedge" + str(Wedge.NEXT_ID)
        super().__init__(id, dimension, Wedge.ROTATIONS)
        
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
        doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(matrixPos[0] * dimension, matrixPos[1] * dimension, matrixPos[2] * dimension), 
            self.getRandomRotation(), FreeCAD.Vector(dimension/2, dimension/2, dimension/2))

        Wedge.NEXT_ID += 1