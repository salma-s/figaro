from Shape import Shape
from Placement import Placement
from Cuboid import Cuboid
from Cylinder import Cylinder
import FreeCAD

class SemiHoleInCuboid(Shape):
    NEXT_ID = 1

    def __init__(self, doc, dimension):
        id = "SemiHoleInCuboid" + str(SemiHoleInCuboid.NEXT_ID)
        super().__init__(id, dimension)
        
        cube = Cuboid(doc, [dimension[0], dimension[1], dimension[2]])
        cylinder = Cylinder(doc, [dimension[0]/2, dimension[2], 360], Placement([dimension[0]/2, dimension[1], 0], [0, 0, 0]))
        
        # Cut hole from cube
        doc.addObject("Part::Cut", id)
        doc.getObject(id).Base = doc.getObject(cube.id)
        doc.getObject(id).Tool = doc.getObject(cylinder.id)

        SemiHoleInCuboid.NEXT_ID += 1


