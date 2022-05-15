from Point import Point
import random

class Vector:
    def __init__(self, p1: Point, p2: Point):
        self.x = p2.x - p1.x
        self.y = p2.y - p1.y

    def get_length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y

    @staticmethod
    # вектор отражения
    def get_reflected_vector(a: Point, p1: Point, p2: Point):
        # reflectedVector = fallingVector - 2 * normalVector * ((fallingVector * normalVector) / ( normalVector^2))
        b = Point(p2.x - p1.x, p2.y - p1.y)
        result = b
        product = ((a * b) / (b * b)) * 2
        result.x *= product
        result.y *= product
        return result - a

    @staticmethod
    def get_list_of_vectors(length):
        vectors = []
        for i in range(length):
            p = Point(random.randint(-1, 1), random.randint(-1, 1))
            while p.x == 0 and p.y == 0:
                p = Point(random.randint(-1, 1), random.randint(-1, 1))
            vectors.append(p)
        return vectors