from HoleInDoor import HoleInDoor
from HoleInWedge import HoleInWedge
from QuarterHoleInCuboid import QuarterHoleInCuboid
from SemiHoleInCuboid import SemiHoleInCuboid
import FreeCAD
import random

class HardBaseShapeGenerator():
    def __init__(self, doc, unit):
        self.doc = doc
        self.unit = unit

    def getRandomBaseShape(self, matrixPos):
        n = random.randint(0, 3)
        shape = None

        if n == 0:
            shape = HoleInDoor(self.doc, self.unit, matrixPos)
        elif n == 1:
            shape = QuarterHoleInCuboid(self.doc, self.unit, matrixPos)
        elif n == 2:
            shape = SemiHoleInCuboid(self.doc, self.unit, matrixPos)
        elif n == 3:
            shape = HoleInWedge(self.doc, self.unit, matrixPos)
            
        return shape