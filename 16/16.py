import math

from utils import read_input


def calc_sub_package_value(t, values):
    if t == 0:  # sum
        res = sum(values)
    elif t == 1:  # prod
        res = math.prod(values)
    elif t == 2:  # min
        res = min(values)
    elif t == 3:  # max
        res = max(values)
    elif t in [5, 6, 7]:
        res = -1
        if len(values) == 2:
            if t == 5:
                res = 1 if values[0] > values[1] else 0
            elif t == 6:  # lt
                res = 1 if values[0] < values[1] else 0
            elif t == 7:  # eq
                res = 1 if values[0] == values[1] else 0
    #print(res)
    return res


def process_operator(b, ltid, t):
    if ltid == 1:
        length = 11
    elif ltid == 0:
        length = 15
    lb = b[:length]
    ld = int(lb, 2)
    #print(lb, ld)
    start_pos = length
    total = 0
    inner_lit_vs = []
    while total < ld:
        ep_sub, lit_value = process_package(b[start_pos:])
        #print("lit", lit_value)
        inner_lit_vs.append(lit_value)
        #print(inner_lit_vs)
        inner_lit_v = calc_sub_package_value(t, inner_lit_vs)
        if ltid == 1:
            total += 1
        elif ltid == 0:
            total += ep_sub
        start_pos += ep_sub
        #print(total, ld)
    return start_pos, inner_lit_v


def process_literal_value(b):
    search_last = True
    lit_b = ""
    start_pos = 0
    while search_last:
        end_pos = start_pos + 5
        lit_b += b[start_pos + 1:end_pos]
        if b[start_pos] == '0':
            search_last = False
        start_pos = end_pos
        #print(start_pos)
    lit_d = int(lit_b, 2)
    #print(lit_b, lit_d)
    return end_pos, lit_d


def get_version_type(b):
    #print(b)
    vb = b[:3]
    tb = b[3:6]
    vd = int(vb, 2)
    td = int(tb, 2)
    #print(vb, vd)
    #print(tb, td)
    return vd, td


def process_package(b, init=False):
    global sum_versions
    v, t = get_version_type(b)
    sum_versions += v
    start_pos = 6
    if t == 4:
        ep, lit_v = process_literal_value(b[start_pos:])
        ep += start_pos
    else:
        i = b[start_pos]
        ep, lit_v = process_operator(b[start_pos+1:], int(i), t)
        ep += start_pos + 1
    return ep, lit_v


debug = False
files = ['example.txt', 'example2.txt', 'input.txt', 'input2.txt']

for f in files:
    hex_strings = read_input(f)
    for hs in hex_strings:
        sum_versions = 0
        print(hs)
        b = bin(int(hs, 16))[2:].zfill(len(hs)*4)
        ep, p2 = process_package(b)
        print(f"{f} - Part 1: {sum_versions}")
        print(f"{f} - Part 2: {p2}")
