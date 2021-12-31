import numpy as np

from utils import read_input, get_directions_possible_of_xy, get_2d_arr


def process_adjacent_coords(a, x, y, flashed):
    a[x][y] = 0
    dirs = get_directions_possible_of_xy(x, y, a.shape[0], a.shape[1], diag=True)
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

    arr = get_2d_arr(read_input(f), int)

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
