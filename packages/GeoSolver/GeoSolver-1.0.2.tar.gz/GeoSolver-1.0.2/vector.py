from .point import Point


class Vec:
    def __init__(self, a: Point, b: Point):
        self.a = a
        self.b = b

    def length(self):
        return ((self.a.x - self.b.x) ** 2 + (self.a.y - self.b.y) ** 2 + (self.a.z - self.b.z) ** 2) ** 0.5

    def coordinate(self):
        return self.b.x - self.a.x, self.b.y - self.a.y, self.b.z - self.a.z

    def dot(self, other):
        return self.coordinate()[0] * other.coordinate()[0] + self.coordinate()[1] * other.coordinate()[1] + self.coordinate()[2] * other.coordinate()[2]

    def cross(self, other):
        return Vec(Point(self.coordinate()[1] * other.coordinate()[2] - self.coordinate()[2] * other.coordinate()[1],
                         self.coordinate()[2] * other.coordinate()[0] - self.coordinate()[0] * other.coordinate()[2],
                         self.coordinate()[0] * other.coordinate()[1] - self.coordinate()[1] * other.coordinate()[0]),
                   Point(self.coordinate()[2] * other.coordinate()[1] - self.coordinate()[1] * other.coordinate()[2],
                         self.coordinate()[0] * other.coordinate()[2] - self.coordinate()[2] * other.coordinate()[0],
                         self.coordinate()[1] * other.coordinate()[0] - self.coordinate()[0] * other.coordinate()[1]))

    def add(self, other):
        return Vec(self.a, Point(self.b.x + other.coordinate()[0], self.b.y + other.coordinate()[1], self.b.z + other.coordinate()[2]))