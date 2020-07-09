from Shape import Shape
from Placement import Placement
from Cuboid import Cuboid
from Cylinder import Cylinder
import FreeCAD

class HoleInDoor(Shape):
    NEXT_ID = 1

    def __init__(self, doc, dimension):
        n = dimension[0]
        id = "HoleInDoor" + str(HoleInDoor.NEXT_ID)
        super().__init__(id, dimension)
        
        cube = Cuboid(doc, [n, n/2, n])
        cylinder1 = Cylinder(doc, [n/2, n, 180], Placement([n/2, n/2, 0], [0, 0, 0]))
        cylinder2 = Cylinder(doc, [n/4, n, 360], Placement([n/2, n/2, 0], [0, 0, 0]))
        
        # Fuse cuboid and semicircle
        partialId = "PartialHoleInDoor" + str(HoleInDoor.NEXT_ID)
        doc.addObject("Part::Fuse", partialId)
        doc.getObject(partialId).Base = doc.getObject(cube.id)
        doc.getObject(partialId).Tool = doc.getObject(cylinder1.id)

        # Cut hole in partial fused part
        doc.addObject("Part::Cut", id)
        doc.getObject(id).Base = doc.getObject(partialId)
        doc.getObject(id).Tool = doc.getObject(cylinder2.id)

        HoleInDoor.NEXT_ID += 1
