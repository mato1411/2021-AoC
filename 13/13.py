import numpy as np

from utils import read_input

debug = False
files = ['example.txt', 'input.txt', 'input2.txt']

for f in files:

    input = read_input(f)
    coords = [list(map(int, reversed(c.split(',')))) for c in input if not c.startswith('fold') and c != '']
    fold_instructions = [c.split('=') for c in input if c.startswith('fold')]
    fold_instructions = [[fi[0][-1], int(fi[1])] for fi in fold_instructions]

    a = np.full((max([c[0] for c in coords])+1, max([c[1] for c in coords])+1), '.')
    for c in coords:
        a[c[0]][c[1]] = '#'

    for i, fi in enumerate(fold_instructions):
        ax, v = fi[0], fi[1]
        if ax == 'x':
            for x in range(a.shape[0]):
                a[x][v] = '|'
                # fold right to left
                for y in range(v, a.shape[1]):
                    if a[x][y] == '#':
                        new_y = (a.shape[1] - 1) - y
                        a[x][new_y] = '#'
            a = a[:, :v]
        elif ax == 'y':
            for y in range(a.shape[1]):
                a[v][y] = '-'
                # fold bottom half up
                for x in range(v, a.shape[0]):
                    if a[x][y] == '#':
                        new_x = (a.shape[0] - 1) - x
                        a[new_x][y] = '#'
            a = a[:v]

        hash_count = a[a == '#'].shape[0]
        if i == 0:
            p1 = hash_count

    print(f"{f} - Part 1: {p1}")
    print(f"{f} - Part 2:")
    for x in range(a.shape[0]):
        print("".join(a[x]))
