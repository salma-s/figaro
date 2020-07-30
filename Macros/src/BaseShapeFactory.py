from SetABaseShapeGenerator import SetABaseShapeGenerator
from SetBBaseShapeGenerator import SetBBaseShapeGenerator
from SetCBaseShapeGenerator import SetCBaseShapeGenerator
import random

class BaseShapeFactory():
    def __init__(self, doc, unit, numBaseShapes, shapeComplexity):
        self.doc = doc
        self.unit = unit
        self.shapeComplexity = shapeComplexity
        self.setABaseShapeGenerator = SetABaseShapeGenerator(doc, unit)
        self.setBBaseShapeGenerator = SetBBaseShapeGenerator(doc, unit)
        self.setCBaseShapeGenerator = SetCBaseShapeGenerator(doc, unit)

        if shapeComplexity == 'SIMPLE':
            self.setA = numBaseShapes - 2
            self.setB = 2
            self.setC = 0
        elif shapeComplexity == 'NORMAL':
            self.setA = numBaseShapes - 3
            self.setB = 3
            self.setC = 0
        elif shapeComplexity == 'COMPLEX':
            self.setA = numBaseShapes - 3
            self.setB = 1
            self.setC = 2

    def generateRandomShape(self, matrixPos):
        # Get the sets of base shapes to generate
        complexitySets = []
        if self.setA > 0:
            complexitySets.append(0)
        if self.setB > 0:
            complexitySets.append(1)
        if self.setC > 0:
            complexitySets.append(2)
        if self.setA == 0 and self.setB == 0 and self.setC == 0:
            return

        # Get a random set (A, B or C)) and generate a base shape 
        n = random.choice(complexitySets)
        if n == 0:
            shape = self.setABaseShapeGenerator.getRandomBaseShape(matrixPos)
            self.setA = self.setA - 1
        elif n == 1:
            shape = self.setBBaseShapeGenerator.getRandomBaseShape(matrixPos)
            self.setB = self.setB - 1
        elif n == 2:
            shape = self.setCBaseShapeGenerator.getRandomBaseShape(matrixPos)
            self.setC = self.setC - 1
        return shape