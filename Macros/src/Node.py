#TODO: rename to base shape node
class Node:
    def __init__(self, x, y, z, shape = None):
        self.x = x
        self.y = y
        self.z = z
        self.reachable = False
        self.shape = shape