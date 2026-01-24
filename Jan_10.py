# Random walk through polar coordinates (r and theta, starting at 1, 1), use arcs?
# figure out arc length to move 1 unit

import numpy as np
import svg

WIDTH = 100
HEIGHT = 100

rng = np.random.default_rng(20260110)


def create_paths(n_steps):

    new_elements = []

    current_r = 0
    current_theta = 0
    color_value = 0

    steps = rng.binomial(1, .5, (n_steps, 2))

    for step_number, s in enumerate(steps):
        if step_number <= n_steps / 2:
            color_value = 255 - (step_number * 2 / n_steps) * 255
        else:
            color_value = (step_number * 2 / n_steps) * 255 / 2

        path = [svg.M(current_r * np.cos(current_theta), current_r * np.sin(current_theta))]
        if s[0] == 0:
            # Use polar coordinates then convert, duh
            if current_r != 0:
                current_r = current_r - 1
            else:
                current_r = 1
                current_theta = current_theta + np.pi
        else:
            current_r = current_r + 1

        path.append(svg.L(current_r * np.cos(current_theta),
                          current_r * np.sin(current_theta)))  # move r

        large_arc_flag = 0
        sweep_flag = 0

        if current_r != 0:

            if s[1] == 1:
                # arc_length = current_r * (new_theta - current_theta)
                # 1 / current_r = new_theta - current_theta
                # current_theta + 1 / current_r = new_theta
                current_theta = current_theta + 1 / current_r
                sweep_flag = 1

            else:
                current_theta = current_theta - 1 / current_r

        else:

            current_theta = current_theta + np.pi  # I guess

        path.append(svg.Arc(current_r,
                            current_r,
                            0,
                            large_arc_flag,
                            sweep_flag,
                            current_r * np.cos(current_theta),
                            current_r * np.sin(current_theta)))  # move theta

        new_elements.append(svg.Path(
                d=path,
                transform=[svg.Translate(WIDTH / 2, HEIGHT / 2)],
                fill="none",
                stroke=f"rgb({color_value} {color_value} {color_value})",
                stroke_width=".25",
                stroke_linecap="square"))

    return new_elements


def draw() -> svg.SVG:

    # Start with a background rectangle.
    elements = [svg.Rect(x=0,
                         y=0,
                         width=WIDTH,
                         height=HEIGHT,
                         fill="#FFFFFF")]

    elements.append(create_paths(50000))

    return svg.SVG(
        width=WIDTH,
        height=HEIGHT,
        elements=elements)
 
if __name__ == '__main__':
    with open('Jan_10.svg', 'w') as f:
        print(draw(), file=f)