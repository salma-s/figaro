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

    def generateRandomShape(self):
        n = random.randint(1,10)

        if n == 1:
            shape = Cuboid(self.doc, [self.unit, self.unit, self.unit])
        elif n == 2:
            shape = Cylinder(self.doc, [self.unit, self.unit, self.unit])
        elif n == 3:
            shape = Wedge(self.doc, [self.unit, self.unit, self.unit])
        elif n == 4:
            shape = HoleInBox(self.doc, [self.unit, self.unit, self.unit])
        elif n == 5:
            shape = SemiCircle(self.doc, [self.unit, self.unit, self.unit])
        elif n == 6:
            shape = QuarterCircle(self.doc, [self.unit, self.unit, self.unit])
        elif n == 7:
            shape = QuarterHoleInCuboid(self.doc, [self.unit, self.unit, self.unit])
        elif n == 8:
            shape = SemiHoleInCuboid(self.doc, [self.unit, self.unit, self.unit])
        elif n == 9:
            shape = HoleInWedge(self.doc, [self.unit, self.unit, self.unit])
        elif n == 10:
            shape = HoleInDoor(self.doc, [self.unit, self.unit, self.unit])
        
        return shape


        
        

