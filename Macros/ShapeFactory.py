from Cuboid import Cuboid
from Cylinder import Cylinder
from HoleInBox import HoleInBox
from HoleInDoor import HoleInDoor
from HoleInWedge import HoleInWedge
from QuarterCircle import QuarterCircle
from QuarterHoleInCuboid import QuarterHoleInCuboid
from SemiCircle import SemiCircle
from SemiHoleInCuboid import SemiHoleInCuboid
from Wedge import Wedge
import FreeCAD
import random

class ShapeFactory():
    def __init__(self, doc, unit):
        self.doc = doc
        self.unit = unit

    def generateRandomShape(self, matrixPos):
        n = random.randint(1,11)

        shape = None
        if n == 1:
            shape = Cuboid(self.doc, self.unit, matrixPos)
        elif n == 2:
            shape = Wedge(self.doc, self.unit, matrixPos)
        elif n == 3:
            shape = HoleInBox(self.doc, self.unit, matrixPos)
        elif n == 4:
            shape = SemiCircle(self.doc, self.unit, matrixPos)
        elif n == 5:
            shape = QuarterCircle(self.doc, self.unit, matrixPos)
        elif n == 6:
            shape = QuarterHoleInCuboid(self.doc, self.unit, matrixPos)
        elif n == 7:
            shape = SemiHoleInCuboid(self.doc, self.unit, matrixPos)
        elif n == 8:
            shape = HoleInWedge(self.doc, self.unit, matrixPos)
        elif n == 9:
            shape = HoleInDoor(self.doc, self.unit, matrixPos)
        elif n == 10:
            shape = "Empty"
        # elif n == 11:
        #     shape = Cylinder(self.doc, self.unit, matrixPos)
        
        return shape
