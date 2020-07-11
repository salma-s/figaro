from Shape import Shape
from Cuboid import Cuboid
from Position import Position
import FreeCAD

class Wedge(Shape):
    NEXT_ID = 1

    def __init__(self, doc, dimension):
        id = "Wedge" + str(Wedge.NEXT_ID)
        super().__init__(id, dimension)
        
        cube1 = Cuboid(doc, [dimension[0], dimension[1], dimension[2]])
        cube2 = Cuboid(doc, [dimension[0]*1.5, dimension[1]*1.5, dimension[2]*1.5], Position([0,0,0], [45, 0, 0]))
        
        # Cut cube1
        doc.addObject("Part::Cut", id)
        doc.getObject(id).Base = doc.getObject(cube1.id)
        doc.getObject(id).Tool = doc.getObject(cube2.id)

        Wedge.NEXT_ID += 1

doc = FreeCAD.newDocument()
w = Wedge(doc, [30,30,30])
doc.recompute()
