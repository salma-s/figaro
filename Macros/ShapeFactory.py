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

        pMatrix = [0.05, 0.25, 0.15, 0.125, 0.125, 0.10, 0.10, 0.04, 0.04, 0.02]
        # pMatrix = [0.05, 0.15, 0.15, 0.1, 0.1, 0.1, 0.10, 0.04, 0.04, 0.02]
        cumulativeMatrix = []
        sum = 0.00
        for i in range(len(pMatrix)):
            sum = sum + pMatrix[i]
            cumulativeMatrix.append(sum)

        n = random.uniform(0, 1)
        print(n)
        shape = None

        if n <= cumulativeMatrix[0]:
            shape = "Empty"
        elif n <= cumulativeMatrix[1]:
            shape = Cuboid(self.doc, self.unit, matrixPos)
        elif n <= cumulativeMatrix[2]:
            shape = Wedge(self.doc, self.unit, matrixPos)
        elif n <= cumulativeMatrix[3]:
            shape = QuarterCircle(self.doc, self.unit, matrixPos)
        elif n <= cumulativeMatrix[4]:
            shape = SemiCircle(self.doc, self.unit, matrixPos)
        elif n <= cumulativeMatrix[5]:
            shape = HoleInBox(self.doc, self.unit, matrixPos)
        elif n <= cumulativeMatrix[6]:
            shape = HoleInDoor(self.doc, self.unit, matrixPos)
        elif n <= cumulativeMatrix[7]:
            shape = QuarterHoleInCuboid(self.doc, self.unit, matrixPos)
        elif n <= cumulativeMatrix[8]:
            shape = SemiHoleInCuboid(self.doc, self.unit, matrixPos)
        elif n <= cumulativeMatrix[9]:
            shape = HoleInWedge(self.doc, self.unit, matrixPos)
        return shape
