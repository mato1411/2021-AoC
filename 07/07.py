from scipy.spatial import distance

from utils import read_input
import numpy as np

debug = False
files = ['example.txt', 'input.txt', 'input2.txt']

for f in files:

    input = read_input(f)
    numbers = np.array(list(map(int, input[0].split(','))))

    results_p1 = {}
    results_p2 = {}
    for r in range(max(numbers), min(numbers) - 1, -1):
        d1 = 0
        d2 = 0
        for n in sorted(numbers):
            d_euc = int(distance.euclidean([r], [n]))
            #print(n, r, d_euc)
            d1 += d_euc
            if d_euc > 0:
                d2 += sum(range(1, d_euc + 1))
        results_p1[r] = d1
        results_p2[r] = d2

    print(f"{f} - Part 1: {min(results_p1.values())}")
    print(f"{f} - Part 2: {min(results_p2.values())}")
