'''
GENUARY 2026 JAN. 17
Wallpaper group.

pg group
'''

import numpy as np
import svg

WIDTH = 100
HEIGHT = 100


def create_row(start_y, width, height, fill):
    row = []

    slide_x = width * np.cos(np.pi/4) - height * np.sin(np.pi/4)
    slant_up_y = width * np.sin(np.pi/4) + height * np.cos(np.pi/4) + start_y

    step_x = slide_x + (width * np.cos(np.pi/4)) + (height * np.cos(np.pi/4))
    steps = np.ceil(WIDTH / step_x) * 2

    for count_x in np.arange(steps):
        if count_x % 2 == 0:
            transform = [svg.Translate(-slide_x + count_x / 2 * step_x,
                                       start_y),
                         svg.Rotate(45, 0, 0)]
        else:
            transform = [svg.Translate((count_x - 1) / 2 * step_x, slant_up_y),
                         svg.Rotate(-45, 0, 0)]

        base = svg.Rect(x=0,
                        y=0,
                        rx=width/8,
                        ry=width/8,
                        width=width,
                        height=height,
                        stroke="black",
                        fill=fill,
                        transform=transform)
        row.append(base)

    return row


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
                             fill="#000000"))

    rect_height = 5
    rect_width = 10

    slide_y = np.sqrt(2 * rect_height ** 2)
    steps = np.ceil(HEIGHT / slide_y)

    for count_y in np.arange(-1, steps):
        r, g, b = "FF", "FF", "FF"
        if count_y % 2 == 0:
            r = "88"
        else:
            g = "88"
        if count_y % 3 == 0:
            b = "88"
        elements.append(create_row(slide_y * count_y,
                                   rect_width,
                                   rect_height,
                                   f"#{r}{g}{b}"))

    return svg.SVG(
        width=WIDTH,
        height=HEIGHT,
        elements=elements)


if __name__ == '__main__':
    with open('Jan_17.svg', 'w') as f:
        print(draw(), file=f)
