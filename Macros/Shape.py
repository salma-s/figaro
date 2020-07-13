import random

class Shape:
    def __init__(self, id, dimension, rotations):
        self.id = id
        self.dimension = dimension
        self.rotations = rotations

    def getRandomRotation(self):
        n = random.randint(0, len(self.rotations) - 1)
        return self.rotations[n]
