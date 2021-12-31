import os
import shutil

import numpy as np


up = (-1, 0)
down = (1, 0)
left = (0, -1)
right = (0, 1)
up_left = (-1, -1)
up_right = (-1, 1)
down_left = (1, -1)
down_right = (1, 1)


def get_2d_arr(input, dtype):
    a = np.array(list(map(dtype, input[0])))
    a = np.expand_dims(a, axis=0)
    for n in input[1:]:
        len_diff = len(input[0]) - len(n)
        if len_diff:
            n = n.ljust(len(input[0]))
        a = np.append(a, [list(map(dtype, list(n)))], axis=0)
    return a


def get_directions_possible_of_xy(x, y, x_max, y_max, diag=True):
    directions_possible = []
    if x == 0 and y == 0:  # Top left corner
        if diag:
            directions_possible += [right, down, down_right]
        else:
            directions_possible += [right, down]
    elif x + 1 == x_max and y + 1 == y_max:  # Bottom right corner
        if diag:
            directions_possible += [up, left, up_left]
        else:
            directions_possible += [up, left]
    elif x == 0 and y + 1 == y_max:  # Top right corner
        if diag:
            directions_possible += [down, left, down_left]
        else:
            directions_possible += [down, left]
    elif x + 1 == x_max and y == 0:  # Bottom left corner
        if diag:
            directions_possible += [up, right, up_right]
        else:
            directions_possible += [up, right]
    elif x == 0:  # Top row
        if diag:
            directions_possible += [right, down, left, down_left, down_right]
        else:
            directions_possible += [right, down, left]
    elif y == 0:  # Lef column
        if diag:
            directions_possible += [up, right, down, down_right, up_right]
        else:
            directions_possible += [up, right, down]
    elif x + 1 == x_max:  # Bottom row
        if diag:
            directions_possible += [up, right, left, up_left, up_right]
        else:
            directions_possible += [up, right, left]
    elif y + 1 == y_max:  # Right column
        if diag:
            directions_possible += [up, down, left, up_left, down_left]
        else:
            directions_possible += [up, down, left]
    else:
        if diag:
            directions_possible += [up, right, down, left, down_left, down_right, up_right, up_left]
        else:
            directions_possible += [up, right, down, left]
    return directions_possible


def read_input(filename='example.txt', sep='\n'):
    with open(filename) as f:
        inputs = f.read().strip().split(sep)
    return inputs


def create_dirs_and_templates():
    for i in range(8, 25):
        d_f_name = str(i).zfill(2)
        os.makedirs(d_f_name, exist_ok=True)
        py_file = os.path.join(d_f_name, d_f_name + '.py')
        ex_file = os.path.join(d_f_name, 'example.txt')
        for s, d in zip(['template.py', 'example.txt'], [py_file, ex_file]):
            if not os.path.isfile(d):
                shutil.copyfile(s, d)


if __name__ == "__main__":
    create_dirs_and_templates()
