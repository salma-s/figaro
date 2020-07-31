from Cuboid import Cuboid
import FreeCAD
import random
class SetABaseShapeGenerator():
    def __init__(self, doc, unit):
        self.doc = doc
        self.unit = unit

    def getRandomBaseShape(self, matrixPos):
        n = random.randint(0, 4)
        shape = None

        if n == 0:
            shape = "Empty"
        else:
            shape = Cuboid(self.doc, self.unit, matrixPos)

        return shape