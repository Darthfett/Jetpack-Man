import math

class Vector:

    def __add__(self, vec):
        return Vector(self.x + vec.x, self.y + vec.y)

    def __sub__(self, vec):
        return Vector(self.x - vec.x, self.y - vec.y)

    def __iadd__(self, vec):
        self.x += vec.x
        self.y += vec.y

    def __isub__(self, vec):
        self.x -= vec.x
        self.y -= vec.y

    def size(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __str__(self):
        return "<" + str(self.x) + ", " + str(self.y) + ">"

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        raise Exception("Vector " + str(self) + ": Index out of bound: " + str(item))

    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
