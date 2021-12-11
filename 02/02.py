from utils import read_input

files = ['example.txt', 'input.txt', 'input2.txt']

for f in files:

    h1 = 0
    d1 = 0
    h2 = 0
    d2 = 0
    a = 0

    cmds = read_input(f)

    for cmd in cmds:
        n_in_cmd = int(cmd.split()[1])

        if cmd.startswith('forward'):
            h1 += n_in_cmd
            h2 += n_in_cmd
            d2 += (a * n_in_cmd)

        elif cmd.startswith('down'):
            d1 += n_in_cmd
            a += n_in_cmd

        elif cmd.startswith('up'):
            d1 -= n_in_cmd
            a -= n_in_cmd

    print(f"{f} - Part 1: H = {h1}, d = {d1}, multiplied: {h1*d1}")
    print(f"{f} - Part 2: H = {h1}, d = {d2}, multiplied: {h2 * d2}")
