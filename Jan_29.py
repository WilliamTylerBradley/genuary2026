'''
GENUARY 2026 JAN. 29
Genetic evolution and mutation.

Three polygons that grows to maximum size until one reaches the edge.
'''
from collections import namedtuple

import numpy as np
import svg

WIDTH = 100
HEIGHT = 100

rng = np.random.default_rng(20260129)


Point = namedtuple('Point', ['x', 'y', 'angle'])


class Shape:
    def __init__(self, color):
        self.color = color

        r = 5 * np.sqrt(rng.uniform(0, 1, 3))
        theta = rng.uniform(0, 1, 3) * 2 * np.pi

        x = r[0] * np.cos(theta[0])
        y = r[0] * np.sin(theta[0])

        self.max_radius = np.sqrt(x**2 + y**2)

        self.base_point = Point(x, y, 0)

        self.points = []
        self.points.append(self.base_point)
        for i in np.arange(1, 3):
            x = r[i] * np.cos(theta[i])
            y = r[i] * np.sin(theta[i])

            self.points.append(Point(x,
                                     y,
                                     self.calculate_angle(x, y)))

            radius = np.sqrt(x**2 + y**2)
            if radius >= self.max_radius:
                self.max_radius = radius

        self.sort_points(self.points)
        self.area = self.calculate_area(self.points)

    def sort_points(self, points):
        points.sort(key=lambda x: x.angle)

    def calculate_area(self, points):
        a1 = 0
        a2 = 0
        for p0, p1 in zip(points[:-1], points[1:]):
            a1 += p0.x * p1.y
            a2 += p0.y * p1.x

        a1 += points[-1].x * points[0].y
        a2 += points[-1].y * points[0].x

        return (a1 - a2) / 2

    def calculate_angle(self, x, y):
        return np.atan2(y - self.base_point.y, x - self.base_point.x)

    def determine_svg(self):
        polygon = []
        for p in self.points:
            polygon.extend([p.x, p.y])
        return svg.Polygon(points=polygon,
                           stroke=self.color,
                           fill=self.color,
                           stroke_linejoin="round",
                           opacity="1%",
                           transform=svg.Translate(WIDTH/2, HEIGHT/2))

    # now choose between add_midpoint and move_point
    def evolve(self):
        # test out add new point
        evolve_points = self.points.copy()

        point_location = rng.integers(len(self.points))
        point = evolve_points[point_location]

        # Move away from base point, not center?
        distance = np.sqrt(point.x**2 + point.y**2)
        move_point_x = point.x + (point.x / distance * 5)
        move_point_y = point.y + (point.y / distance * 5)

        evolve_points[point_location] = Point(move_point_x,
                                              move_point_y,
                                              self.calculate_angle(move_point_x,
                                                                   move_point_y))

        evolve_area = self.calculate_area(evolve_points)

        evolve_prop = evolve_area / (self.area + evolve_area)

        evolve_prob = rng.uniform()
        if evolve_prob < evolve_prop:
            self.points[point_location] = evolve_points[point_location]

            radius = np.sqrt(move_point_x**2 + move_point_y**2)
            if radius >= self.max_radius:
                self.max_radius = radius

        else:
            next_point_location = (point_location + 1) % len(self.points)
            point = self.points[point_location]
            next_point = self.points[next_point_location]

            midpoint_x = (point.x + next_point.x) / 2
            midpoint_y = (point.y + next_point.y) / 2

            self.points.append(Point(midpoint_x,
                                    midpoint_y,
                                    self.calculate_angle(midpoint_x,
                                                        midpoint_y)))

            radius = np.sqrt(midpoint_x**2 + midpoint_y**2)
            if radius >= self.max_radius:
                self.max_radius = radius

        self.sort_points(self.points)
        self.area = self.calculate_area(self.points)


def draw() -> svg.SVG:
    '''
    Actually adds the shapes to the SVG.
    '''

    # Start with a background rectangle.
    elements: list[svg.Element] = list()
    elements.append(svg.Rect(x=0,
                             y=0,
                             width=WIDTH,
                             height=HEIGHT,
                             fill="#D3D3D3"))

    elements.append(svg.Circle(cx=WIDTH / 2,
                               cy=HEIGHT / 2,
                               r=50,
                               fill="#FFFFFF"))

    elements.append(svg.Circle(cx=WIDTH / 2,
                               cy=HEIGHT / 2,
                               r=5,
                               fill="#A9A9A9"))

    creature_1 = Shape(color="#FFFF00")
    creature_2 = Shape(color="#FF00FF")
    creature_3 = Shape(color="#00FFFF")
    max_radius = 0

    elements.append(creature_1.determine_svg())
    elements.append(creature_2.determine_svg())
    elements.append(creature_3.determine_svg())

    while max_radius <= 50:
        creature_1.evolve()
        creature_2.evolve()
        creature_3.evolve()

        elements.append(creature_1.determine_svg())
        elements.append(creature_2.determine_svg())
        elements.append(creature_3.determine_svg())

        if max_radius <= creature_1.max_radius:
            max_radius = creature_1.max_radius
        if max_radius <= creature_2.max_radius:
            max_radius = creature_2.max_radius
        if max_radius <= creature_3.max_radius:
            max_radius = creature_3.max_radius

    return svg.SVG(
        width=WIDTH,
        height=HEIGHT,
        elements=elements)


if __name__ == '__main__':
    with open('Jan_29.svg', 'w') as f:
        print(draw(), file=f)
