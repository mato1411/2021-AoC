import numpy as np

from utils import read_input


def get_directions_possible_of_xy(x, y, x_max, y_max):
    directions_possible = []
    if x == 0 and y == 0:  # Top left corner
        directions_possible += [right, down]
    elif x + 1 == x_max and y + 1 == y_max:  # Bottom right corner
        directions_possible += [up, left]
    elif x == 0 and y + 1 == y_max:  # Top right corner
        directions_possible += [down, left]
    elif x + 1 == x_max and y == 0:  # Bottom left corner
        directions_possible += [up, right]
    elif x == 0:  # Top row
        directions_possible += [right, down, left]
    elif y == 0:  # Lef column
        directions_possible += [up, right, down]
    elif x + 1 == x_max:  # Bottom row
        directions_possible += [up, right, left]
    elif y + 1 == y_max:  # Right column
        directions_possible += [up, down, left]
    else:
        directions_possible += [up, right, down, left]
    return directions_possible


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
        adja_coords_processed = []
        adja_coords_processed.append((x, y))
        basin_size = process_adjacent_locations(a, x, y, 1, adja_coords_processed)
        basin_sizes.append(basin_size)
    return basin_sizes


def process_adjacent_locations(a, x, y, count, adja_coords_processed):
    border = 9
    curr_coord_h = a[x][y]
    dirs = get_directions_possible_of_xy(x, y, a.shape[0], a.shape[1])
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
    input = read_input(f)
    arr = np.array(list(map(int, input[0])))
    arr = np.expand_dims(arr, axis=0)
    for n in input[1:]:
        arr = np.append(arr, [list(map(int, list(n)))], axis=0)

    # Top left = 0,0
    # Bottom right 4,9
    up = (-1, 0)
    down = (1, 0)
    left = (0, -1)
    right = (0, 1)

    low_point_coords = []
    low_point_n = []

    for x in range(arr.shape[0]):
        for y in range(arr.shape[1]):
            directions_possible = get_directions_possible_of_xy(x, y, arr.shape[0], arr.shape[1])
            determine_low_point(arr, x, y, directions_possible)

    p1 = len(low_point_n) * 1 + sum(low_point_n)
    basin_sizes = determine_basin_size(arr, low_point_coords)
    top_3_basin_sizes = sorted(basin_sizes)[-3:]
    p2 = np.prod(np.array(top_3_basin_sizes))

    print(f"{f} - Part 1: {p1}")
    print(f"{f} - Part 2: {p2}")
