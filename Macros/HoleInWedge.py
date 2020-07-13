from Shape import Shape
from CentrelineInfo import CentrelineInfo
import FreeCAD

class HoleInWedge(Shape):
    NEXT_ID = 1
    ROTATIONS = [
        FreeCAD.Rotation(0, 0, 0), FreeCAD.Rotation(90, 180, 0), 
        FreeCAD.Rotation(0, 90, 0), FreeCAD.Rotation(-90, 0, 90), 
        FreeCAD.Rotation(0, 180, 0), FreeCAD.Rotation(-90, 0, 0),
        FreeCAD.Rotation(0, 270, 0), FreeCAD.Rotation(-90, 0, -90),
        FreeCAD.Rotation(0, 0, 90), FreeCAD.Rotation(90, 90, 0), 
        FreeCAD.Rotation(0, 90, 90), FreeCAD.Rotation(180, 0, 90), 
        FreeCAD.Rotation(0, 180, 90), FreeCAD.Rotation(-90, -90, 0), 
        FreeCAD.Rotation(0, 270, 90), FreeCAD.Rotation(0, 0, -90), 
        FreeCAD.Rotation(0, 0, 180), FreeCAD.Rotation(90, 0, 0), 
        FreeCAD.Rotation(0, 90, 180), FreeCAD.Rotation(90, 0, 90), 
        FreeCAD.Rotation(0, 180, 180), FreeCAD.Rotation(90, 0, 180), 
        FreeCAD.Rotation(0, 270, 180), FreeCAD.Rotation(90, 0, -90), 
    ]

    @staticmethod
    def generateCentrelines(dimension):
        return [
            CentrelineInfo(dimension/2, None, dimension/2, -10, 0.75 * dimension + 10, dimension/2 + 10),
            CentrelineInfo(None, dimension/2, dimension/2, 0.25 * dimension - 10, dimension + 10, dimension/2 + 10),
            CentrelineInfo(dimension/2, None, dimension/2, -10, 0.75 * dimension + 10, dimension/2 + 10),
            CentrelineInfo(dimension/2, dimension/2, None, -10, 0.75 * dimension + 10, dimension/2 + 10),
            CentrelineInfo(dimension/2, None, dimension/2, -10, 0.75 * dimension + 10, dimension/2 + 10),
            CentrelineInfo(None, dimension/2, dimension/2, -10, 0.75 * dimension + 10, dimension/2 + 10),
            CentrelineInfo(dimension/2, None, dimension/2, -10, 0.75 * dimension + 10, dimension/2 + 10),
            CentrelineInfo(dimension/2, dimension/2, None, 0.25 * dimension - 10, dimension + 10, dimension/2 + 10),
            CentrelineInfo(dimension/2, dimension/2, None, -10, 0.75 * dimension + 10, dimension/2 + 10),
            CentrelineInfo(None, dimension/2, dimension/2, 0.25 * dimension - 10, dimension + 10, dimension/2 + 10),
            CentrelineInfo(None, dimension/2, dimension/2, -10, 0.75 * dimension + 10, dimension/2 + 10),
            CentrelineInfo(dimension/2, dimension/2, None, -10, 0.75 * dimension + 10, dimension/2 + 10),
            CentrelineInfo(dimension/2, dimension/2, None, 0.25 * dimension - 10, dimension + 10, dimension/2 + 10),
            CentrelineInfo(None, dimension/2, dimension/2, -10, 0.75 * dimension + 10, dimension/2 + 10),
            CentrelineInfo(None, dimension/2, dimension/2, 0.25 * dimension - 10, dimension + 10, dimension/2 + 10),
            CentrelineInfo(dimension/2, dimension/2, None, 0.25 * dimension - 10, dimension + 10, dimension/2 + 10),
            CentrelineInfo(dimension/2, None, dimension/2, 0.25 * dimension - 10, dimension + 10, dimension/2 + 10),
            CentrelineInfo(None, dimension/2, dimension/2, 0.25 * dimension - 10, dimension + 10, dimension/2 + 10),
            CentrelineInfo(dimension/2, None, dimension/2, 0.25 * dimension - 10, dimension + 10, dimension/2 + 10),
            CentrelineInfo(dimension/2, dimension/2, None, -10, 0.75 * dimension + 10, dimension/2 + 10),
            CentrelineInfo(dimension/2, None, dimension/2, 0.25 * dimension - 10, dimension + 10, dimension/2 + 10),
            CentrelineInfo(None, dimension/2, dimension/2, -10, 0.75 * dimension + 10, dimension/2 + 10),
            CentrelineInfo(dimension/2, None, dimension/2, 0.25 * dimension - 10, dimension + 10, dimension/2 + 10),
            CentrelineInfo(dimension/2, dimension/2, None, 0.25 * dimension - 10, dimension + 10, dimension/2 + 10),
        ]

    def __init__(self, doc, dimension, matrixPos):
        id = "HoleInWedge" + str(HoleInWedge.NEXT_ID)
        super().__init__(id, dimension, HoleInWedge.ROTATIONS, HoleInWedge.generateCentrelines(dimension))

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

        # Translate block to actual position
        doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(matrixPos[0] * dimension, matrixPos[1] * dimension, matrixPos[2] * dimension), 
            self.getRandomRotation(), FreeCAD.Vector(dimension/2, dimension/2, dimension/2))

        HoleInWedge.NEXT_ID += 1
