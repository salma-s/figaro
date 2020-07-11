from Shape import Shape
from Cylinder import Cylinder
from Cuboid import Cuboid
from Wedge import Wedge
from Position import Position
import FreeCAD

class HoleInWedge(Shape):
    NEXT_ID = 1

    def __init__(self, doc, dimension):
        n = dimension[0]
        id = "HoleInWedge" + str(HoleInWedge.NEXT_ID)
        super().__init__(id, dimension)
        
        cube1 = Cuboid(doc, [n, n, n])
        cube2 = Cuboid(doc, [n*1.5, n*1.5, n*1.5], Position([0,0,0], [45, 0, 0]))
        hole = Cylinder(doc, [n/4, n, 360], Position([n/2, 0, n/2], [0,0, -90]))
	
        # Wedge
        partialId = "PartialWedge" + str(HoleInWedge.NEXT_ID)
        doc.addObject("Part::Cut", partialId)
        doc.getObject(partialId).Base = doc.getObject(cube1.id)
        doc.getObject(partialId).Tool = doc.getObject(cube2.id)
        
        # Cut hole from wedge
        doc.addObject("Part::Cut", id)
        doc.getObject(id).Base = doc.getObject(partialId)
        doc.getObject(id).Tool = doc.getObject(hole.id)

        HoleInWedge.NEXT_ID += 1
