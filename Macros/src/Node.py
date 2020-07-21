#TODO: rename to base shaoe node
class Node:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.reachable = False
        self.shape = None