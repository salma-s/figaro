from HoleInBox import HoleInBox
from QuarterCircle import QuarterCircle
from SemiCircle import SemiCircle
from Wedge import Wedge
import FreeCAD
import random

class MediumBaseShapeGenerator():
    def __init__(self, doc, unit):
        self.doc = doc
        self.unit = unit

    def getRandomBaseShape(self, matrixPos):
        n = random.randint(0, 3)
        shape = None

        if n == 0:
            shape = Wedge(self.doc, self.unit, matrixPos)
        elif n == 1:
            shape = QuarterCircle(self.doc, self.unit, matrixPos)
        elif n == 2:
            shape = SemiCircle(self.doc, self.unit, matrixPos)
        elif n == 3:
            shape = HoleInBox(self.doc, self.unit, matrixPos)

        return shape