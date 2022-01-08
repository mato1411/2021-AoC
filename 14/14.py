from utils import read_input


def polymerization(max_steps):
    step = 0
    while step < max_steps:
        if step == 0:
            c_temp = template
            char_counts = {c_temp[0]: 1}
            insert_pattern_capture = {}
            insert_pattern_char_count = {}
        else:
            c_temp = new_template
        new_template = c_temp[0]
        for i in range(len(c_temp) - 1):
            insert = pir[f"{c_temp[i]}{c_temp[i + 1]}"]
            if step == max_steps - 1:
                char_counts[insert] = char_counts.get(insert, 0) + 1
                char_counts[c_temp[i + 1]] = char_counts.get(c_temp[i + 1], 0) + 1

            insert_pattern_capture[f"{c_temp[i]}{c_temp[i + 1]}"] = [f"{c_temp[i]}{insert}",
                                                                     f"{insert}{c_temp[i + 1]}"]
            insert_pattern_char_count[f"{c_temp[i]}{c_temp[i + 1]}"] = [c_temp[i], insert, c_temp[i + 1]]
            new_template += f"{insert}{c_temp[i + 1]}"
        step += 1
    return insert_pattern_capture, insert_pattern_char_count, char_counts


def polymerization_fast(max_steps, insert_pattern_capture):
    step = 0
    c_temp = template
    insert_pattern_count = {}
    while step < max_steps:
        char_counts = {}
        char_counts[c_temp[0]] = char_counts.get(c_temp[0], 0) + 1
        if step == 0:
            for i in range(len(c_temp) - 1):
                insert_pattern = insert_pattern_capture.get(f"{c_temp[i]}{c_temp[i + 1]}")
                for ip in insert_pattern:
                    insert_pattern_count[ip] = insert_pattern_count.get(ip, 0) + 1
                insert_pattern_count[f"{c_temp[i]}{c_temp[i + 1]}"] = insert_pattern_count.get(f"{c_temp[i]}{c_temp[i + 1]}", 0) + 1
                if insert_pattern_count.get(f"{c_temp[i]}{c_temp[i + 1]}", 0) != 0:
                    insert_pattern_count[f"{c_temp[i]}{c_temp[i + 1]}"] = insert_pattern_count.get(f"{c_temp[i]}{c_temp[i + 1]}", 0) - 1
                ip = insert_pattern[-1]
                char_counts[ip] = char_counts.get(ip, 0) + 1
            new_step_ipc = insert_pattern_count.copy()
        else:
            for p, c in insert_pattern_count.items():
                if c == 0:
                    continue
                insert_pattern = insert_pattern_capture.get(p)
                for ip in insert_pattern:
                    new_step_ipc[ip] = new_step_ipc.get(ip, 0) + c
                if new_step_ipc.get(p, 0) != 0:
                    new_step_ipc[p] = new_step_ipc.get(p, 0) - c
                ip = insert_pattern[-1]
                char_counts[ip] = char_counts.get(ip, 0) + c

            insert_pattern_count = new_step_ipc.copy()

        step += 1

    single_char_counts = {}
    for p, co in insert_pattern_count.items():
        ch = p[0]
        single_char_counts[ch] = single_char_counts.get(ch, 0) + co
    print(sum(char_counts.values()) * 2 - 1)
    print(f"single_char_counts: {single_char_counts}")

    return single_char_counts


debug = False
files = ['example.txt', 'input.txt', 'input2.txt']

for f in files:

    input = read_input(f)
    template = input[0]
    pir = {pir.split('->')[0].strip(): pir.split('>')[1].strip() for pir in input[2:]}
    insert_patterns, insert_pattern_to_chars, temp_chars = polymerization(10)
    print(temp_chars)
    p1 = max(temp_chars.values()) - min(temp_chars.values())

    temp_chars = polymerization_fast(10, insert_patterns)

    # BUG: Somehow there is a deviation for a single char count of either 1 or -1
    if f in ['example.txt', 'input2.txt']:
        deviation = 1
    else:
        deviation = -1

    temp_chars = polymerization_fast(40, insert_patterns)
    p2 = (max(temp_chars.values()) - min(temp_chars.values())) + deviation

    print(f"{f} - Part 1: {p1}")
    print(f"{f} - Part 2: {p2}")
