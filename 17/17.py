import numpy as np

from utils import read_input


def probe_shot(probe, target_area, p_map=False):
    x, y = probe
    min_x, max_x, min_y, max_y = target_area
    trajectory = {probe}
    not_in_target_or_missed = True
    step = 1
    new_x, new_y = x, y
    while not_in_target_or_missed:
        if step > 1:
            x_change = 0
            if new_x > 0:
                x_change = -1
            elif new_x < 0:
                x_change = 1
            new_x += x_change
            x += new_x

            new_y += -1
            y += new_y

        if x in range(min_x, max_x + 1) and y in range(min_y, max_y + 1):
            # In target area
            not_in_target_or_missed = False
            in_target = True

        if x > max_x + 1 or y < min_y - 1:
            # Missed target area
            not_in_target_or_missed = False
            in_target = False

        trajectory.add((x, y))
        step += 1

    if p_map:
        print_map(trajectory, target_area)

    return in_target, trajectory


def print_map(trajectory, target_area):
    min_x, max_x, min_y, max_y = target_area
    x_values = [0]
    y_values = [0]
    for pos in trajectory:
        x_values.append(pos[0])
        y_values.append(pos[1])

    a = np.full((max(y_values + [max_y]) - min(y_values + [min_y]) + 1,
                 max(x_values + [max_x]) - min(x_values + [min_x]) + 1),
                dtype=str, fill_value='.')

    y_offset = max(y_values + [max_y])

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if y >= 0:
                y_pos = y_offset - y
            elif y < 0:
                y_pos = y_offset + abs(y)
            a[y_pos][x] = 'T'

    for x, y in zip(x_values, y_values):
        if y >= 0:
            y_pos = y_offset - y
        elif y < 0:
            y_pos = y_offset + abs(y)
        sign = '#'
        if x == 0 and y == 0:
            sign = 'S'
        a[y_pos][x] = sign

    print(trajectory)
    for x in range(a.shape[0]):
        print("".join(a[x]))


def get_highest_y(trajectory):
    y_vals = set()
    for t in trajectory:
        y_vals.add(t[1])
    return max(y_vals)


debug = False
files = ['example.txt', 'input.txt', 'input2.txt']

for f in files:

    input = read_input(f)

    y = input[0].split(',')[1].split('=')[1].replace('..',',').split(',')
    min_y = int(y[0])
    max_y = int(y[1])
    x = input[0].split(',')[0].split('=')[1].replace('..', ',').split(',')
    min_x = int(x[0])
    max_x = int(x[1])

    target = (min_x, max_x, min_y, max_y)

    if f == 'example.txt':
        highest_y = None
        for probe, expected_match in zip([(7, 2), (6, 3), (9, 0), (17, -4)],
                                          [True, True, True, False]):
            print(f"\n{input}")
            actual_match, t = probe_shot(probe, target, p_map=True)
            assert actual_match == expected_match
            if actual_match:
                current_highest_y = get_highest_y(t)
                if highest_y is None or current_highest_y > highest_y:
                    highest_y = current_highest_y

        print(f"Highest in y in examples: {highest_y}")

    highest_probe = None
    probe_match_count = 0
    for x in range(max_x + 1):
        for y in range(min_y, max_x):
            match, t = probe_shot((x, y), target)
            if match:
                probe_match_count += 1
                current_highest_y = get_highest_y(t)
                if highest_y is None or current_highest_y > highest_y:
                    highest_y = current_highest_y
                    highest_probe = (x, y)

    print(f"{f} - Part 1: {highest_y} {highest_probe}")
    print(f"{f} - Part 2: {probe_match_count}")
