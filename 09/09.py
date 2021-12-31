import numpy as np

from utils import read_input, get_directions_possible_of_xy, get_2d_arr


def determine_low_point(a, x, y, dirs):
    low_point = a[x][y]
    dir_is_lower = []
    for d in dirs:
        if arr[x + d[0]][y + d[1]] > low_point:
            dir_is_lower.append(True)
        else:
            dir_is_lower.append(False)
    if sum(dir_is_lower) == len(dirs):
        low_point_coords.append((x, y))
        low_point_n.append(low_point)


def determine_basin_size(a, low_point_coords):
    basin_sizes = []
    for x, y in low_point_coords:
        adja_coords_processed = [(x, y)]
        basin_size = process_adjacent_locations(a, x, y, 1, adja_coords_processed)
        basin_sizes.append(basin_size)
    return basin_sizes


def process_adjacent_locations(a, x, y, count, adja_coords_processed):
    border = 9
    curr_coord_h = a[x][y]
    dirs = get_directions_possible_of_xy(x, y, a.shape[0], a.shape[1], diag=False)
    for d in dirs:
        x1 = x + d[0]
        y1 = y + d[1]
        if a[x1][y1] > curr_coord_h and a[x1][y1] != border and (x1, y1) not in adja_coords_processed:
            adja_coords_processed.append((x1, y1))
            count += 1
            count = process_adjacent_locations(a, x1, y1, count, adja_coords_processed)
    return count


debug = False
files = ['example.txt', 'input.txt', 'input2.txt']

for f in files:
    arr = get_2d_arr(read_input(f), int)

    low_point_coords = []
    low_point_n = []

    for x in range(arr.shape[0]):
        for y in range(arr.shape[1]):
            directions_possible = get_directions_possible_of_xy(x, y, arr.shape[0], arr.shape[1], diag=False)
            determine_low_point(arr, x, y, directions_possible)

    p1 = len(low_point_n) * 1 + sum(low_point_n)
    basin_sizes = determine_basin_size(arr, low_point_coords)
    top_3_basin_sizes = sorted(basin_sizes)[-3:]
    p2 = np.prod(np.array(top_3_basin_sizes))

    print(f"{f} - Part 1: {p1}")
    print(f"{f} - Part 2: {p2}")
