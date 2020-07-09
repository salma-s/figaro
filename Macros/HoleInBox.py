from Shape import Shape
from Placement import Placement

class HoleInBox(Shape):
    def __init__(self, id, dimension, placement):
        super().__init__(id, dimension, placement)