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
        self.pMatrix = None
        self.tMatrix = [
            [0.15, 0.200, 0.200, 0.200, 0.200, 0.20, 0.500, 0.30, 0.30, 0.1],
            [0.10, 0.150, 0.035, 0.035, 0.100, 0.06, 0.040, 0.05, 0.20, 0.1],
            [0.10, 0.050, 0.150, 0.150, 0.050, 0.06, 0.040, 0.10, 0.05, 0.1],
            [0.10, 0.050, 0.100, 0.150, 0.100, 0.15, 0.150, 0.10, 0.05, 0.1],
            [0.10, 0.150, 0.150, 0.125, 0.150, 0.15, 0.040, 0.15, 0.15, 0.1],
            [0.10, 0.050, 0.100, 0.100, 0.100, 0.15, 0.040, 0.05, 0.05, 0.1],
            [0.10, 0.025, 0.030, 0.030, 0.050, 0.06, 0.025, 0.05, 0.05, 0.1],
            [0.10, 0.125, 0.150, 0.125, 0.100, 0.06, 0.075, 0.10, 0.05, 0.1],
            [0.10, 0.150, 0.035, 0.035, 0.100, 0.06, 0.040, 0.05, 0.05, 0.1],
            [0.05, 0.050, 0.050, 0.050, 0.050, 0.05, 0.050, 0.05, 0.05, 0.1],
        ]

    def calculateProbabilityMatrix(self):
        if self.pMatrix is None:
            return [0.25, 0.15, 0.125, 0.125, 0.10, 0.10, 0.04, 0.04, 0.02, 0.05]
        
        pMatrixNew = []
        for i in range(len(self.pMatrix)):
            pMatrixNew.append(0)
            for j in range(len(self.pMatrix)):
                pMatrixNew[i] += self.tMatrix[i][j] * self.pMatrix[j]

        return pMatrixNew

    def generateRandomShape(self, matrixPos):
        pMatrix = self.calculateProbabilityMatrix()
        print(pMatrix)
        self.pMatrix = pMatrix
        cumulativeMatrix = []
        sum = 0.00
        for i in range(len(pMatrix)):
            sum = sum + pMatrix[i]
            cumulativeMatrix.append(sum)

        n = random.uniform(0, 1)
        shape = None

        if n <= cumulativeMatrix[0]:
            shape = Cuboid(self.doc, self.unit, matrixPos)
        elif n <= cumulativeMatrix[1]:
            shape = Wedge(self.doc, self.unit, matrixPos)
        elif n <= cumulativeMatrix[2]:
            shape = QuarterCircle(self.doc, self.unit, matrixPos)
        elif n <= cumulativeMatrix[3]:
            shape = SemiCircle(self.doc, self.unit, matrixPos)
        elif n <= cumulativeMatrix[4]:
            shape = HoleInBox(self.doc, self.unit, matrixPos)
        elif n <= cumulativeMatrix[5]:
            shape = HoleInDoor(self.doc, self.unit, matrixPos)
        elif n <= cumulativeMatrix[6]:
            shape = QuarterHoleInCuboid(self.doc, self.unit, matrixPos)
        elif n <= cumulativeMatrix[7]:
            shape = SemiHoleInCuboid(self.doc, self.unit, matrixPos)
        elif n <= cumulativeMatrix[8]:
            shape = HoleInWedge(self.doc, self.unit, matrixPos)
        else:
            shape = "Empty"
        return shape

