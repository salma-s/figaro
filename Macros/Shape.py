import random

class Shape:
    def __init__(self, id, dimension, rotations, centrelines = None):
        self.id = id
        self.dimension = dimension
        self.rotations = rotations
        self.CENTRELNIES = centrelines
        self.centrelineInfo = None

    def getRandomRotation(self):
        n = random.randint(0, len(self.rotations) - 1)
        if self.CENTRELNIES != None:
            self.centrelineInfo = self.CENTRELNIES[n]
        return self.rotations[n]
