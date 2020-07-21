from Cuboid import Cuboid
import FreeCAD
import random
class EasyBaseShapeGenerator():
    def __init__(self, doc, unit):
        self.doc = doc
        self.unit = unit

    # TODO: refactor such that shape types arent hardcoded in the method (i.e. set in constructor)
    def getRandomBaseShape(self, matrixPos):
        n = random.randint(0, 3)
        shape = None

        if n == 0:
            shape = "Empty"
        else:
            shape = Cuboid(self.doc, self.unit, matrixPos)

        return shape