if __name__ == "__main__":
    from Vector import Vector
else:
    from maths.Vector import Vector
from math import sqrt, pow

"""
Represents a point in 3d space
"""
class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
        