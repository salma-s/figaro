from EasyBaseShapeGenerator import EasyBaseShapeGenerator
from MediumBaseShapeGenerator import MediumBaseShapeGenerator
from HardBaseShapeGenerator import HardBaseShapeGenerator
import random

class BaseShapeFactory():
    def __init__(self, doc, unit, numBaseShapes, difficulty):
        self.doc = doc
        self.unit = unit
        self.difficulty = difficulty
        self.easyBaseShapeGenerator = EasyBaseShapeGenerator(doc, unit)
        self.mediumBaseShapeGenerator = MediumBaseShapeGenerator(doc, unit)
        self.hardBaseShapeGenerator = HardBaseShapeGenerator(doc, unit)

        if difficulty == 'Easy':
            self.easy = numBaseShapes - 2
            self.med = 2
            self.hard = 0
        elif difficulty == 'Medium':
            self.easy = numBaseShapes - 3
            self.med = 3
            self.hard = 0
        elif difficulty == 'Hard':
            self.easy = numBaseShapes - 3
            self.med = 1
            self.hard = 2

    def generateRandomShape(self, matrixPos):
        # Get the difficulties of base shapes to generate
        difficulties = []
        if self.easy > 0:
            difficulties.append(0)
        if self.med > 0:
            difficulties.append(1)
        if self.hard > 0:
            difficulties.append(2)
        if self.easy == 0 and self.med == 0 and self.hard == 0:
            return

        # Get a random difficulty and generate a base shape 
        n = random.choice(difficulties)
        if n == 0:
            shape = self.easyBaseShapeGenerator.getRandomBaseShape(matrixPos)
            self.easy = self.easy - 1
        elif n == 1:
            shape = self.mediumBaseShapeGenerator.getRandomBaseShape(matrixPos)
            self.med = self.med - 1
        elif n == 2:
            shape = self.hardBaseShapeGenerator.getRandomBaseShape(matrixPos)
            self.hard = self.hard - 1
        return shape