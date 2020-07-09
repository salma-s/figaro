from Shape import Shape
from Placement import Placement
from Cuboid import Cuboid
from Cylinder import Cylinder
import FreeCAD

class QuarterCircle(Shape):
    NEXT_ID = 1

    def __init__(self, doc, dimension):
        n = dimension[0]
        id = "QuarterCircle" + str(QuarterCircle.NEXT_ID)
        super().__init__(id, dimension)
        
        Cylinder(doc, [n/2, n, 90], Placement([0, 0, 0], [0, 0, 0]))
        QuarterCircle.NEXT_ID += 1


