from dataclasses import dataclass
from math import sqrt

@dataclass
class Point:
    x: int
    y: int

    def dst(self, other):
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def __rmul__(self, other):
        return Point(self.x * other, self.y * other)
