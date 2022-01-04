from heapq import heappop, heappush
from queue import PriorityQueue

import numpy as np

from utils import read_input, get_2d_arr, get_directions_possible_of_xy, get_adjacent_data


# Use manhattan distance as optimization for a star
def h(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


#  A* algorithm
def get_distance_a_star(a, start, end):
    not_visited = PriorityQueue()
    not_visited.put((0, start))
    distances = {start: 0}
    parents = {start: start}

    while not not_visited.empty():
        d, node = not_visited.get()
        if node == end:
            break

        for neighbor, distance in get_adjacent_data(a, node).items():
            new_dist = distances[node] + distance
            if neighbor not in parents or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                priority = new_dist + h(neighbor, end)
                not_visited.put((priority, neighbor))
                parents[neighbor] = node
    return distances[end]


def get_lowest_risk_path(a):
    start = (0, 0)
    end = (a.shape[0] - 1, a.shape[1] - 1)
    return get_distance_a_star(a, start, end)


def get_increased_map(a):
    d = 5
    o_shape = a.shape
    xl_a = np.resize(a, (o_shape[0]*d, o_shape[1]*d))

    for x in range(xl_a.shape[0]):
        if x < o_shape[0]:
            new_x = a[x]
            new_y = a[x]
        else:
            x_mod = x % o_shape[0]
            if x_mod == 0:
                x_add = int(x / o_shape[0])
            new_x = a[x_mod] + x_add
            if new_x[new_x > 9].size > 0:
                new_x[new_x > 9] = new_x[new_x > 9] - 9
            new_y = new_x
        for y in range(1, d):
            t = new_x + y
            if t[t > 9].size > 0:
                t[t > 9] = t[t > 9] -9
            new_y = np.append(new_y, t)
        xl_a[x] = new_y
    return xl_a


debug = False
files = ['example.txt', 'input.txt', 'input2.txt']

for f in files:

    arr = get_2d_arr(read_input(f), int)
    print(f"{f} - Part 1: {get_lowest_risk_path(arr)}")
    xl_arr = get_increased_map(arr)
    if f == 'example.txt':
        expected_xl_arr = get_2d_arr(read_input('example2.txt'), int)
        for x in range(xl_arr.shape[0]):
            for y in range(xl_arr.shape[1]):
                if expected_xl_arr[x][y] != xl_arr[x][y]:
                    print(f"ERROR: Diff for x {x} y {y}: {expected_xl_arr[x][y]} vs. {xl_arr[x][y]}")
    print(f"{f} - Part 2: {get_lowest_risk_path(xl_arr)}")
