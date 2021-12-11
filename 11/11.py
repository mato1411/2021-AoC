import numpy as np

from utils import read_input


def get_directions_possible_of_xy(x, y, x_max, y_max):
    directions_possible = []
    if x == 0 and y == 0:  # Top left corner
        directions_possible += [right, down, down_right]
    elif x + 1 == x_max and y + 1 == y_max:  # Bottom right corner
        directions_possible += [up, left, up_left]
    elif x == 0 and y + 1 == y_max:  # Top right corner
        directions_possible += [down, left, down_left]
    elif x + 1 == x_max and y == 0:  # Bottom left corner
        directions_possible += [up, right, up_right]
    elif x == 0:  # Top row
        directions_possible += [right, down, left, down_left, down_right]
    elif y == 0:  # Lef column
        directions_possible += [up, right, down, down_right, up_right]
    elif x + 1 == x_max:  # Bottom row
        directions_possible += [up, right, left, up_left, up_right]
    elif y + 1 == y_max:  # Right column
        directions_possible += [up, down, left, up_left, down_left]
    else:
        directions_possible += [up, right, down, left, down_left, down_right, up_right, up_left]
    return directions_possible


def process_adjacent_coords(a, x, y, flashed):
    a[x][y] = 0
    dirs = get_directions_possible_of_xy(x, y, a.shape[0], a.shape[1])
    for d in dirs:
        x1 = x + d[0]
        y1 = y + d[1]
        if a[x1][y1] != 0 and (a[x1][y1] + 1) > 9 and (x1, y1) not in flashed:
            flashed.append((x1, y1))
            a, flashed = process_adjacent_coords(a, x1, y1, flashed)
        elif a[x1][y1] != 0:
            a[x1][y1] += 1
    return a, flashed


def get_number_of_flashes(a):
    coords_flashed = []
    coords_larger_9 = np.transpose((a > 9).nonzero())
    for coords in coords_larger_9:
        x, y = coords[0], coords[1]
        if (x, y) not in coords_flashed:
            coords_flashed.append((x, y))
            a, coords_flashed = process_adjacent_coords(a, x, y, coords_flashed)
    return a, len(coords_flashed)


debug = False
files = ['example.txt', 'example2.txt', 'input.txt', 'input2.txt']

for f in files:

    input = read_input(f)

    arr = np.array(list(map(int, input[0])))
    arr = np.expand_dims(arr, axis=0)
    for n in input[1:]:
        arr = np.append(arr, [list(map(int, list(n)))], axis=0)

    # Top left = 0,0
    # Bottom right 9,9
    up = (-1, 0)
    down = (1, 0)
    left = (0, -1)
    right = (0, 1)
    up_left = (-1, -1)
    up_right = (-1, 1)
    down_left = (1, -1)
    down_right = (1, 1)

    n_flashes = 0

    i = 0
    while True:
        arr, flashes = get_number_of_flashes(arr +1)
        if i < 100:
            n_flashes += flashes
        i += 1

        if (arr == 0).sum() == arr.shape[0] * arr.shape[1]:
            step_all_flash = i
            break

    # print(arr)

    print(f"{f} - Part 1: {n_flashes}")
    print(f"{f} - Part 2: {step_all_flash}")
