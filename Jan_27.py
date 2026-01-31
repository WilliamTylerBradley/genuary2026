from collections import namedtuple

import numpy as np
import svg

WIDTH = 100
HEIGHT = 100

DIVIDE_CUTOFF = HEIGHT * (4/5)
FLOWER_CUTOFF = HEIGHT / 5

rng = np.random.default_rng(20260127)

Point = namedtuple('Point', ['x', 'y'])

Segment = namedtuple('Segment', ['start_point',
                                 'start_control_point',
                                 'end_point',
                                 'end_control_point'])


def grow_segment(start_point, start_control_point):
    end_r = 10 * np.sqrt(rng.uniform())
    end_theta = rng.uniform() * np.pi

    end_point = Point(start_point.x + end_r * np.cos(end_theta),
                      start_point.y - end_r * np.sin(end_theta))

    end_control_r = 10 * np.sqrt(rng.uniform())
    end_control_theta = rng.uniform() * 2 * np.pi

    end_control_point = Point((end_point.x + end_control_r
                               * np.cos(end_control_theta)),
                              (end_point.y - end_control_r
                               * np.sin(end_control_theta)))

    return Segment(start_point,
                   start_control_point,
                   end_point,
                   end_control_point)


def grow_flower(start_point):

    flower = []

    for step in np.arange(10):
        petal_end_r = 5 * np.sqrt(rng.uniform())
        petal_end_theta = rng.uniform() * 2 * np.pi

        petal_end_point = Point((start_point.x + petal_end_r
                                 * np.cos(petal_end_theta)),
                                (start_point.y - petal_end_r
                                 * np.sin(petal_end_theta)))

        petal_width = rng.uniform(.25, 1.75)

        end_control_point = Point((-1 * (start_point.y - petal_end_point.y)
                                   * petal_width + petal_end_point.x),
                                  ((start_point.x - petal_end_point.x) *
                                   petal_width + petal_end_point.y))

        flower.append(svg.Path(d=[svg.M(start_point.x, start_point.y),
                                  svg.C(start_point.x, start_point.y,
                                        end_control_point.x,
                                        end_control_point.y,
                                        petal_end_point.x, petal_end_point.y),
                                  svg.S(start_point.x, start_point.y,
                                        start_point.x, start_point.y)],
                               fill="#a64ca6",
                               stroke="#800080",
                               stroke_width=.25))

    return flower


def create_growth():
    growth = []
    segments = []

    start_point = Point(WIDTH / 2,
                        HEIGHT)

    start_control_point = Point(start_point.x,
                                start_point.y)

    segments.append(grow_segment(start_point, start_control_point))

    while segments:

        s = segments.pop()

        segment = svg.Path(d=[svg.M(s.start_point.x, s.start_point.y),
                              svg.C(s.start_control_point.x,
                                    s.start_control_point.y,
                                    s.end_control_point.x,
                                    s.end_control_point.y,
                                    s.end_point.x,
                                    s.end_point.y)],
                           fill="none",
                           stroke="#2C4C3B",
                           stroke_linecap="butt",
                           stroke_width=(s.start_control_point.y / HEIGHT * 3))
        growth.append(segment)

        segment = svg.Path(d=[svg.M(s.start_point.x, s.start_point.y),
                              svg.C(s.start_control_point.x,
                                    s.start_control_point.y,
                                    s.end_control_point.x,
                                    s.end_control_point.y,
                                    s.end_point.x,
                                    s.end_point.y)],
                           fill="none",
                           stroke="#306844",
                           stroke_linecap="round",
                           stroke_width=((s.start_control_point.y / HEIGHT * 3)
                                         - .5))
        growth.append(segment)

        if s.end_point.y > 0:

            start_point = Point(s.end_point.x,
                                s.end_point.y)

            start_control_point = Point((-1 * (s.end_control_point.x
                                               - s.end_point.x)
                                         + s.end_point.x),
                                        (-1 * (s.end_control_point.y
                                               - s.end_point.y)
                                         + s.end_point.y))

            # Branching
            if start_point.y > DIVIDE_CUTOFF:
                segments.append(grow_segment(start_point, start_control_point))
            elif start_point.y > FLOWER_CUTOFF:
                branch = rng.uniform()

                if branch < .25:
                    segments.append(grow_segment(start_point,
                                                 start_control_point))
                elif branch < .75:
                    segments.append(grow_segment(start_point,
                                                 start_control_point))
                    segments.append(grow_segment(start_point,
                                                 start_control_point))
                else:
                    growth.append(grow_flower(start_point))
            else:
                growth.append(grow_flower(start_point))

    return growth


def draw() -> svg.SVG:
    # Start with a background rectangle.
    elements: list[svg.Element] = list()
    elements.append(svg.Rect(x=0,
                             y=0,
                             width=WIDTH,
                             height=HEIGHT,
                             fill="#FFB732"))

    elements.append(create_growth())

    return svg.SVG(
        width=WIDTH,
        height=HEIGHT,
        elements=elements)


if __name__ == '__main__':
    with open('Jan_27.svg', 'w') as f:
        print(draw(), file=f)