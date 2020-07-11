from Shape import Shape
from Cuboid import Cuboid
from Cylinder import Cylinder
from Position import Position
import FreeCAD

class HoleInBox(Shape):
    NEXT_ID = 1

    def __init__(self, doc, dimension):
        id = "HoleInBox" + str(HoleInBox.NEXT_ID)
        super().__init__(id, dimension)
        
        cube = Cuboid(doc, [dimension[0], dimension[1], dimension[2]])

        # TODO: make rotation random
        pos = Position([dimension[0]/2, dimension[1]/2, 0], [0, 0, 0])
        cylinder = Cylinder(doc, [0.3*dimension[0], dimension[2], 360], pos)
        
        # Cut cylinder
        doc.addObject("Part::Cut", id)
        doc.getObject(id).Base = doc.getObject(cube.id)
        doc.getObject(id).Tool = doc.getObject(cylinder.id)

        HoleInBox.NEXT_ID += 1
