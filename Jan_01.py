from itertools import product

import numpy as np
import opensimplex
import svg

# Set up global variables
WIDTH = 100
HEIGHT = 100
COLOR = "#3EB489"  # One Color


def create_hexagonal_grid(side_length, n_columns, n_rows):
    '''Used to create the hexagonal grid'''
    grid = np.array(list(product(np.arange(0, n_columns),
                                 np.arange(0, n_rows, 2) * np.sqrt(3) / 2)))
    grid_2 = grid.copy()
    move_array = np.array([.5, np.sqrt(3) / 2])
    grid_2 = grid_2 + move_array

    grid = np.vstack((grid, grid_2))
    grid = grid * side_length

    return grid


def base_shape(circle_radius):
    '''Used to create the base shape'''  # One Shape
    return [
            svg.M(circle_radius, 0),
            svg.L(circle_radius * np.cos(2 * np.pi / 3),
                  circle_radius * np.sin(2 * np.pi / 3)),
            svg.L(circle_radius * np.cos(2 * np.pi / 3) / 3,
                  circle_radius * np.sin(2 * np.pi / 3) / 3),
            svg.L(circle_radius * np.cos(np.pi),
                  circle_radius * np.sin(np.pi)),
            svg.L(circle_radius * np.cos(4 * np.pi / 3) / 3,
                  circle_radius * np.sin(4 * np.pi / 3) / 3),
            svg.L(circle_radius * np.cos(4 * np.pi / 3),
                  circle_radius * np.sin(4 * np.pi / 3)),
            svg.Z()]


def direction(x, y, h=1e-5):
    '''
    Determines the direction the shape is pointing.
    Based on open simplex noise, uses the gradient to rotate the shape.
    '''
    center = opensimplex.noise2(x / 100, y / 100)
    x_step = opensimplex.noise2(x / 100 + h, y / 100)
    y_step = opensimplex.noise2(x / 100, y / 100 + h)

    dx = (x_step - center) / h
    dy = (y_step - center) / h

    return np.atan2(dx, dy) / np.pi * 180


def draw() -> svg.SVG:
    '''
    Actually adds the shapes to the SVG.
    '''

    # Start with a background rectangle.
    elements = [svg.Rect(x=0,
                         y=0,
                         width=WIDTH,
                         height=HEIGHT,
                         fill=COLOR)]

    # Set up the hexagonal grid
    radius = 5
    grid = create_hexagonal_grid(radius,
                                 WIDTH / radius + 1,
                                 HEIGHT / (radius * np.sqrt(3) / 2))

    # Set up seed for the noise
    opensimplex.seed(20260101)

    # Create and rotate a shape for each spot in the grid
    for p in grid:
        this_shape = svg.Path(
            d=base_shape(radius / 2),
            transform=[svg.Rotate(direction(p[0], p[1]), p[0], p[1]),
                       svg.Translate(p[0], p[1])],
            fill="#FFFFFF",
            stroke="none"
            )
        elements.append(this_shape)

    return svg.SVG(
        width=WIDTH,
        height=HEIGHT,
        elements=elements)


if __name__ == '__main__':
    with open('Jan_01.svg', 'w') as f:
        print(draw(), file=f)