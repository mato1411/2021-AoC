from utils import read_input


def get_neighbors(n):
    uniq_bs = set()
    for i in range(2):
        if i == 0:
            c_a = conn_a
            c_b = conn_b
        else:
            c_a = conn_b
            c_b = conn_a
        last_index = 0
        for j in range(c_a.count(n)):
            idx = c_a[last_index:].index(n) + last_index
            b = c_b[idx]
            last_index = idx + 1
            uniq_bs.add(b)
    return uniq_bs


def dfs(start, end, path=None, visited=None, allow_twice=None):
    global paths

    if visited is None:
        visited = {}
    if path is None:
        path = []

    path.append(start)

    if start == end:
        paths.add(",".join(path))
        return path

    neighbors = get_neighbors(start)

    if 'start' in neighbors:
        neighbors.remove('start')

    for n in neighbors:

        if n == end and ",".join(path + [end]) in paths:
            continue

        if n in path and n in uniq_lower_dest:
            if (allow_twice is not None and path.count(allow_twice) == 2) or \
                    (allow_twice is not None and n != allow_twice) or allow_twice is None:
                continue

        visited_path = ",".join(path)

        if n not in visited.get(visited_path, set()):
            n_v_set = visited.get(visited_path, set())
            n_v_set.update([n])
            visited[visited_path] = n_v_set

            dfs(n, end, path, visited, allow_twice)

            path.pop()

    return None


debug = False
files = ['example.txt', 'example2.txt', 'example3.txt', 'input.txt', 'input2.txt']

for f in files:

    input = read_input(f)
    conn_a = [c.split('-')[0] for c in input]
    conn_b = [c.split('-')[1] for c in input]

    uniq_dest = set(conn_a)
    uniq_dest.update(conn_b)

    uniq_lower_dest = set([c for c in conn_a if c.islower() and c != 'start' and c != 'end'])
    uniq_lower_dest.update([c for c in conn_b if c.islower() and c != 'start' and c != 'end'])

    uniq_upper_dest = uniq_dest.difference(uniq_lower_dest)
    uniq_upper_dest.remove('start')
    uniq_upper_dest.remove('end')

    n_dest = len(uniq_dest)
    conns_processed = set()

    counter = 0

    paths = set()
    dfs('start', 'end')
    print(f"{f} - Part 1: {len(paths)}")
    paths = set()
    for uld in uniq_lower_dest:
        dfs('start', 'end', allow_twice=uld)
    print(f"{f} - Part 2: {len(paths)}")
