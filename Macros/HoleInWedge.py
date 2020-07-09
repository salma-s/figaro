from Shape import Shape
from Placement import Placement
from Cylinder import Cylinder
from Cuboid import Cuboid
from Wedge import Wedge
import FreeCAD

class HoleInWedge(Shape):
    NEXT_ID = 1

    def __init__(self, doc, dimension):
        n = dimension[0]
        id = "HoleInWedge" + str(HoleInWedge.NEXT_ID)
        super().__init__(id, dimension)
        
        cube1 = Cuboid(doc, [n, n, n])
        cube2 = Cuboid(doc, [dimension[0]*1.5, dimension[1]*1.5, dimension[2]*1.5], Placement([0,0,0], [45, 0, 0]))
        hole = Cylinder(doc, [n/4, n, 360], Placement([n/2, 0, n/2], [0,0, -90]))
	
        # Wedge
        partialId = "partialWedgeId"
        doc.addObject("Part::Cut", partialId)
        doc.getObject(partialId).Base = doc.getObject(cube1.id)
        doc.getObject(partialId).Tool = doc.getObject(cube2.id)
        
        # Cut hole from wedge
        doc.addObject("Part::Cut", id)
        doc.getObject(id).Base = doc.getObject(partialId)
        doc.getObject(id).Tool = doc.getObject(hole.id)

        HoleInWedge.NEXT_ID += 1

doc = FreeCAD.newDocument()
HoleInWedge(doc, [100,100,100])
doc.recompute()


