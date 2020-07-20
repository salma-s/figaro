from Shape import Shape
from CentrelineInfo import CentrelineInfo
from CentreArcInfo import CentreArcInfo
import FreeCAD

class QuarterCircle(Shape):
    NEXT_ID = 1
    ROTATIONS = [
        FreeCAD.Rotation(0, 0, 0), 
        FreeCAD.Rotation(0, 90, 0),
        FreeCAD.Rotation(0, 180, 0),
        FreeCAD.Rotation(0, 270, 0),

        FreeCAD.Rotation(0, 0, 90),
        FreeCAD.Rotation(0, 90, 90),
        FreeCAD.Rotation(0, 180, 90),
        FreeCAD.Rotation(0, 270, 90),

        FreeCAD.Rotation(0, 0, 180),
        FreeCAD.Rotation(0, 90, 180),
        FreeCAD.Rotation(0, 180, 180), 
        FreeCAD.Rotation(0, 270, 180), 
    ]

    @staticmethod
    def generateCentrelines(dimension):
        baseShapeType = 'QuarterShape'
        return [
            CentrelineInfo(0, 0, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, 0, 0, dimension)),
            CentrelineInfo(None, 0, dimension, -10, dimension + 10, None, CentreArcInfo(baseShapeType, 0, dimension, dimension)),
            CentrelineInfo(dimension, 0, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, dimension, 0, dimension)),
            CentrelineInfo(None, 0, 0, -10, dimension + 10, None, CentreArcInfo(baseShapeType, 0, 0, dimension)),

            CentrelineInfo(0, None, 0, -10, dimension + 10, dimension + 20, CentreArcInfo(baseShapeType, 0, 0, dimension)),
            CentrelineInfo(0, None, dimension, -10, dimension + 10, dimension + 20, CentreArcInfo(baseShapeType, 0, dimension, dimension)),
            CentrelineInfo(dimension, None, dimension, -10, dimension + 10, dimension + 20, CentreArcInfo(baseShapeType, dimension, dimension, dimension)),
            CentrelineInfo(dimension, None, 0, -10, dimension + 10, dimension + 20, CentreArcInfo(baseShapeType, dimension, 0, dimension)),

            CentrelineInfo(0, dimension, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, 0, dimension, dimension)),
            CentrelineInfo(None, dimension, dimension, -10, dimension + 10, None, CentreArcInfo(baseShapeType, dimension, dimension, dimension)),
            CentrelineInfo(dimension, dimension, None, -10, dimension + 10, None, CentreArcInfo(baseShapeType, dimension, dimension, dimension)),
            CentrelineInfo(None, dimension, 0, -10, dimension + 10, None, CentreArcInfo(baseShapeType, dimension, 0, dimension)),
        ]

    def __init__(self, doc, dimension, matrixPos):
        id = "QuarterCircle" + str(QuarterCircle.NEXT_ID)
        super().__init__(id, dimension, QuarterCircle.ROTATIONS, QuarterCircle.generateCentrelines(dimension))

        doc.addObject("Part::Cylinder", id)
        doc.getObject(id).Radius = dimension
        doc.getObject(id).Height = dimension
        doc.getObject(id).Angle = 90
        
        # Translate block to actual position
        doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(matrixPos[0] * dimension, matrixPos[1] * dimension, matrixPos[2] * dimension), 
            self.getRandomRotation(), FreeCAD.Vector(dimension/2, dimension/2, dimension/2))	

        QuarterCircle.NEXT_ID += 1
