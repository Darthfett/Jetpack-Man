import math

class Vector:

    def __add__(self, vec):
        return Vector(self.x + vec[0], self.y + vec[1])

    def __sub__(self, vec):
        return Vector(self.x - vec[0], self.y - vec[1])

    def __iadd__(self, vec):
        self.x += vec[0]
        self.y += vec[1]
        return self

    def __isub__(self, vec):
        self.x -= vec[0]
        self.y -= vec[1]
        return self

    def __len__(self):
        return 2

    def __str__(self):
        return "V:(" + str(self.x) + ", " + str(self.y) + ")"

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        raise IndexError

    def size(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
