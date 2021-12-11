import numpy as np

from utils import read_input


def read_line_coordinates(input):
    x1s, y1s, x2s, y2s = [], [], [], []

    x_pos, y_pos = 0, 1
    x_max = 0
    y_max = 0

    for l in input:
        for pos in [0, 2]:
            x = int(l.split()[pos].split(',')[x_pos])
            y = int(l.split()[pos].split(',')[y_pos])
            if pos == 0:
                x1s.append(x)
                y1s.append(y)
            else:
                x2s.append(x)
                y2s.append(y)
            x_max = x if x > x_max else x_max
            y_max = y if y > y_max else y_max

    x_max += 1
    y_max += 1
    arr = np.zeros((x_max, y_max), dtype=int)

    return arr, (x1s, y1s, x2s, y2s)


def add_lines(arr, line_coords, hv_only=True):
    x1, y1, x2, y2 = line_coords
    s = 1
    if hv_only:
        if x1 == x2:
            if y1 > y2:
                s = -1
                y2 += -1
            else:
                y2 += 1
            for y in range(y1, y2, s):
                arr[x1][y] += 1
                if debug:
                    print(x1, y)
        elif y1 == y2:
            if x1 > x2:
                s = -1
                x2 += -1
            else:
                x2 += 1
            for x in range(x1, x2, s):
                arr[x][y1] += 1
                if debug:
                    print(x, y1)
    elif x1 != x2 and y1 != y2:
        xs = 1
        ys = 1
        if x1 > x2:
            xs = -1
        if y1 > y2:
            ys = -1
        arr[x1][y1] += 1
        while x1 != x2 and y1 != y2:
            x1 += xs
            y1 += ys
            arr[x1][y1] += 1
    if debug:
        print(arr)
        print(line_coords)


def get_n_overlapping_lines(arr):
    return np.sum(arr > 1)


debug = False
files = ['example.txt', 'input.txt', 'input2.txt']

for f in files:

    input = read_input(f)

    arr, coords = read_line_coordinates(input)

    for x1, y1, x2, y2 in zip(*coords):
        add_lines(arr, (x1, y1, x2, y2))

    print(f"{f} - Part 1: {get_n_overlapping_lines(arr)}")
    for x1, y1, x2, y2 in zip(*coords):
        add_lines(arr, (x1, y1, x2, y2), hv_only=False)
    print(f"{f} - Part 2: {get_n_overlapping_lines(arr)}")
