import random

class Shape:
    def __init__(self, id, dimension, rotations, centrelines = None):
        self.id = id
        self.dimension = dimension
        self.rotations = rotations
        self.CENTRELNIES = centrelines
        self.centrelineInfo = None

    def getRandomRotationIndex(self):
        n = random.randint(0, len(self.rotations) - 1)
        self.rotationIndex = n
        if self.CENTRELNIES != None:
            self.centrelineInfo = self.CENTRELNIES[n]
        return n

    def getRandomRotationIndexWithException(self, rotationToIgnore):
        rotationIndexesToChooseFrom = []
        for i in range(len(self.rotations)):
            if i != rotationToIgnore:
                rotationIndexesToChooseFrom.append(i)
        
        randomRotationIndex = random.choice(rotationIndexesToChooseFrom)
        print('getRandomRotationIndexWithException()')
        print(rotationToIgnore)
        print(rotationIndexesToChooseFrom)
        print(randomRotationIndex)
        self.rotationIndex = randomRotationIndex
        return randomRotationIndex