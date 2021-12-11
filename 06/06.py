import numpy as np

from utils import read_input


def compute_growth_after_n_list(days, state):
    if debug:
        print(f"Initial state:{state}")
    for d in range(days):
        if d > 100 and d % 10 == 0:
            print(f"Day {d}")
        count_zeros = state.count(0)
        state = list(map(lambda x: x - 1 if x != 0 else 6, state))
        for c in range(count_zeros):
            state.append(8)
        if debug:
            print(f"{d + 1}: {state}")
    return len(state)


def compute_growth_after_n_np(days, state):
    if debug:
        print(f"Initial state:{state}")
    process_internal_time_nonzero = lambda x: x - 1
    process_internal_time_zero = lambda x: 6
    for d in range(days):
        if d > 100 and d % 10 == 0:
            print(f"Day {d}")
        #count_arr = np.bincount(state)
        #count_zeros = count_arr[0]
        zero_mask = state == 0
        count_zeros = (state == 0).sum()
        state = np.where(state > 0, process_internal_time_nonzero(state), state)
        state = np.where(zero_mask, process_internal_time_zero(state), state)
        for c in range(count_zeros):
            state = np.append(state, 8)
        if debug:
            print(f"{d + 1}: {state}")
    return len(state)


def compute_growth_after_n_dict(days, state):
    if debug:
        print(f"Initial state:{state}")
    for d in range(days):
        if d > 100 and d % 10 == 0:
            print(f"Day {d}")
        pos_zeros = {i for (i, s) in state.items() if s == 0}
        state = {i: s-1 for (i, s) in state.items() if s > 0}
        for pz in pos_zeros:
            state[pz] = 6
        for c in range(len(pos_zeros)):
            state[len(state)] = 8
        if debug:
            print(f"{d + 1}: {state}")
    return len(state)


def compute_occurrences(days, state):
    occ_prev = {i: 0 for i in range(10)}
    for n in state:
        occ_prev[n] = occ_prev.get(n, 0) + 1
    if debug:
        print(f"Initial state:{occ_prev}")
    occ_curr = occ_prev.copy()
    for d in range(days):
        if debug and d > 100 and d % 10 == 0:
            print(f"Day {d}")
        count_zeros = occ_prev.get(0, 0)
        occ_curr[0] = occ_prev.get(0, 0) - count_zeros
        for n in range(1, 10):
            if occ_prev.get(n, 0) != 0:
                occ_curr[n] = 0
                occ_curr[n - 1] = occ_curr.get(n - 1, 0) + occ_prev.get(n, 0)
        occ_curr[6] = occ_curr.get(6, 0) + count_zeros
        occ_curr[8] = occ_curr.get(8, 0) + count_zeros
        if debug:
            print(f"{d + 1}: {occ_curr}")
        occ_prev = occ_curr.copy()
    return sum(occ_curr.values())


debug = False
files = ['example.txt', 'input.txt', 'input2.txt']

for f in files:

    input = read_input(f)
    initial_state = [int(n) for n in input[0].split(',')]
    initial_state_np = np.array(initial_state)
    initial_state_dict = {i: initial_state[i] for i in range(len(initial_state))}

    print(f"{f} - Part 1: {compute_occurrences(80, initial_state)}")
    print(f"{f} - Part 2: {compute_occurrences(256, initial_state)}")
