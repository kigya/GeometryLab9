import random
import math
from matplotlib import pyplot as plt
from celluloid import Camera
from Point import Point
from Vector import Vector

fig = plt.figure()
camera = Camera(fig)
ax = fig.gca


def init_points():
    points = []
    xs = [random.randint(0, 100) for _ in range(10)]
    ys = [random.randint(0, 100) for _ in range(10)]
    for i in range(len(xs)):
        x = Point(xs[i], ys[i])
        points.append(x)
    return points


# Получить список координат по x из списка точек
def get_x_coords(points: list):
    return [point.x for point in points]


# Получить список координат по y из списка точек
def get_y_coords(points: list):
    return [point.y for point in points]


class Polygon:
    def __init__(self, points, name):
        self.points = points
        self.name = name

        self.points.append(self.points[0])

    def draw_polygon(self, color):
        # Вывод точки
        for i in range(len(self.points) - 1):
            plt.plot(self.points[i].x, self.points[i].y, marker="o", color=color)

        plt.plot(get_x_coords(self.points), get_y_coords(self.points), color=color)




def init_vectors_of_moving(points: list):
    vectors = []
    xs = [random.randint(-1, 1) for _ in range(len(points))]
    ys = [random.randint(-1, 1) for _ in range(len(points))]
    for i in range(len(xs)):
        p = Point(xs[i], ys[i])
        while p.x == 0 and p.y == 0:
            p = Point(random.randint(-1, 1), random.randint(-1, 1))
        vectors.append(p)
    return vectors


def opposite_vectors_of_moving(vector: Point):
    vector = Point(-vector.x, -vector.y)
    return vector


def det(a, b, c, d):
    return a * d - b * c


def sort_by_x(points: list):
    sorted_points = []
    sorted_points.extend(points[0: len(points)])
    for i in range(len(sorted_points)):
        min_idx = i
        for j in range(i + 1, len(sorted_points)):
            if sorted_points[min_idx].x >= sorted_points[j].x:
                min_idx = j
        sorted_points[i], sorted_points[min_idx] = sorted_points[min_idx], sorted_points[i]
    return sorted_points


def sort_by_y(points: list):
    sorted_points = []
    sorted_points.extend(points[0: len(points)])
    for i in range(len(sorted_points)):
        min_idx = i
        for j in range(i + 1, len(sorted_points)):
            if sorted_points[min_idx].y >= sorted_points[j].y:
                min_idx = j
        sorted_points[i], sorted_points[min_idx] = sorted_points[min_idx], sorted_points[i]
    return sorted_points


def get_middle_point_by_x(points_sorted_by_x: list):
    return points_sorted_by_x[math.floor(len(points_sorted_by_x) / 2)]


def point_distance(p1: Point, p2: Point):
    return math.sqrt(abs((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y)))


def min_set_distance(points: list):
    min_distance = point_distance(points[0], points[1])
    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            if point_distance(points[i], points[j]) <= min_distance:
                min_distance = point_distance(points[i], points[j])
    return min_distance


def closest_pair(points_sorted_by_x: list, points_sorted_by_y: list):
    if 1 < len(points_sorted_by_x) <= 3:
        min_distance = min_set_distance(points_sorted_by_x)
        return min_distance

    x_sep_point = get_middle_point_by_x(points_sorted_by_x)
    sep_index = points_sorted_by_x.index(x_sep_point)
    x_left_set = points_sorted_by_x[0: sep_index]
    x_right_set = points_sorted_by_x[sep_index: len(points_sorted_by_x)]

    y_left_set = []
    y_right_set = []
    for i in range(len(points_sorted_by_y)):
        if points_sorted_by_y[i].x < x_sep_point.x:
            y_left_set.append(points_sorted_by_y[i])
        else:
            y_right_set.append(points_sorted_by_y[i])

    min_distance_left = closest_pair(x_left_set, y_left_set)
    min_distance_right = closest_pair(x_right_set, y_right_set)
    min_distance = min(min_distance_left, min_distance_right)

    delta_set = []
    for i in range(len(points_sorted_by_y)):
        if abs(points_sorted_by_y[i].x - x_sep_point.x) <= min_distance:
            delta_set.append(points_sorted_by_y[i])

    mythical_number = 7
    n = len(delta_set) if len(delta_set) <= mythical_number else mythical_number
    for i in range(n - 1):
        for j in range(i + 1, n):
            if point_distance(delta_set[i], delta_set[j]) < min_distance:
                min_distance = point_distance(delta_set[i], delta_set[j])

    return min_distance


# Найти положение точки P0 относительно прямой P1P2
def find_pos(p1: Point, p2: Point, p0: Point):
    d = det(p2.x - p1.x, p2.y - p1.y, p0.x - p1.x, p0.y - p1.y)
    if d > 0:
        return -1  # Точка левее прямой
    elif d < 0:
        return 1  # Точка правее прямой
    else:
        return 0  # Точка лежит на прямой


def get_point_position_binary_test(p0: Point, polygon: Polygon):

    if find_pos(polygon.points[0], polygon.points[1], p0) > 0 or \
       find_pos(polygon.points[0], polygon.points[len(polygon.points) - 1], p0) < 0:  # не попадает в сегмент Р1Р0Рn-1
        return False  # точка снаружи мн-ка

    start = 0
    end = len(polygon.points) - 1

    while end - start > 1:
        sep = math.floor((start + end) / 2)
        if find_pos(polygon.points[0], polygon.points[sep], p0) < 0:
            start = sep
        else:
            end = sep

    if find_pos(polygon.points[start], polygon.points[end], p0) < 0:
        return True  # точка внутри мн-ка
    else:
        return False  # точка снаружи мн-ка


def get_intersected_edge(p1: Point, p2: Point, polygon: Polygon):
    for i in range(len(polygon.points) - 1):
        if check_intersection(p1, p2, polygon.points[i], polygon.points[i + 1]):
            return [polygon.points[i], polygon.points[i + 1]]
    return []


def check_intersection(p1: Point, p2: Point, p3: Point, p4: Point):
    d1 = det(p4.x - p3.x, p4.y - p3.y, p1.x - p3.x, p1.y - p3.y)
    d2 = det(p4.x - p3.x, p4.y - p3.y, p2.x - p3.x, p2.y - p3.y)
    d3 = det(p2.x - p1.x, p2.y - p1.y, p3.x - p1.x, p3.y - p1.y)
    d4 = det(p2.x - p1.x, p2.y - p1.y, p4.x - p1.x, p4.y - p1.y)

    if d1 * d2 <= 0 and d3 * d4 <= 0:
        return True  # пересекаются
    else:
        return False  # не пересекаются



def draw_circle(point: Point, radius: int):
    circle = plt.Circle((point.x, point.y), radius, color="pink")
    plt.gcf().gca().add_artist(circle)


def draw_circles(points: list, radius: int):
    for i in range(len(points)):
        draw_circle(points[i], radius)


def get_closest_pair_indexes(points: list, closest_pair_diameter):
    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            if point_distance(points[i], points[j]) == closest_pair_diameter:
                return (i, j)
    print("not found")


def draw_min_distance(points: list, closest_pair_diameter):
    closest_pair_indexes = get_closest_pair_indexes(points, closest_pair_diameter)
    plt.plot([points[closest_pair_indexes[0]].x, points[closest_pair_indexes[1]].x],
             [points[closest_pair_indexes[0]].y, points[closest_pair_indexes[1]].y], "red")


def move(moving_points: list, vectors: list):
    for i in range(len(moving_points)):
        moving_points[i] = moving_points[i] + vectors[i]


def init_motion(points: list):
    radius = 5
    vectors = Vector.get_list_of_vectors(len(points))
    Q = Polygon([Point(0, 0), Point(0, 100), Point(100, 100), Point(100,0)], "Q")
    i = 0
    while i < 70:
        Q.draw_polygon("red")
        draw_circles(points, radius)

        points_sorted_by_x = sort_by_x(points)
        points_sorted_by_y = sort_by_y(points)

        closest_pair_diameter = closest_pair(points_sorted_by_x, points_sorted_by_y)
        closest_pair_indexes = get_closest_pair_indexes(points, closest_pair_diameter)
        draw_min_distance(points, closest_pair_diameter)
        camera.snap()

        for j in range(len(points)):
            next_point = Point(points[j].x + vectors[j].x, points[j].y + vectors[j].y)
            if not get_point_position_binary_test(next_point, Q):
                edges = get_intersected_edge(points[j], next_point, Q)
                if len(edges) == 0:
                    continue
                edge_p1 = edges[0]
                edge_p2 = edges[1]
                vectors[j] = Vector.get_reflected_vector(vectors[j], edge_p1, edge_p2)

        if closest_pair_diameter <= 2 * radius:
            vectors[closest_pair_indexes[0]] = opposite_vectors_of_moving(vectors[closest_pair_indexes[0]])
            vectors[closest_pair_indexes[1]] = opposite_vectors_of_moving(vectors[closest_pair_indexes[1]])
        move(points, vectors)

        i += 1


def init():
    points = init_points()
    init_motion(points)
    plt.grid(True)
    plt.gca().set_xlim((0, 100))
    plt.gca().set_ylim((0, 100))
    animation = camera.animate(blit=False, interval=300)
    animation.save("animation.gif")
    plt.show()


init()
