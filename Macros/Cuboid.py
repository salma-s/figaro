from Shape import Shape
import FreeCAD

class Cuboid(Shape):
    NEXT_ID = 1

    def __init__(self, doc, dimension, matrixPos):
        id = "Cuboid" + str(Cuboid.NEXT_ID)
        super().__init__(id, dimension)
        doc.addObject("Part::Box", id)
        doc.getObject(id).Length = dimension
        doc.getObject(id).Width = dimension
        doc.getObject(id).Height = dimension

        doc.getObject(id).Placement = FreeCAD.Placement(FreeCAD.Vector(matrixPos[0] * dimension, matrixPos[1] * dimension, matrixPos[2] * dimension), 
            FreeCAD.Rotation(0, 0, 0))	

        Cuboid.NEXT_ID += 1