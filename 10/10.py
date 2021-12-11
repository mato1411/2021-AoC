from statistics import median

from utils import read_input


def is_last_closing_char_unexpected(idx, line, to_be_validated_idx):
    unexpected = False
    last_read_closing_char = line[idx]
    idx_closing_chars = closing_chars.index(last_read_closing_char)
    matching_start_char = start_chars[idx_closing_chars]
    if idx == 0: # First char is closing
        unexpected = True
    elif line[to_be_validated_idx[-1]] != matching_start_char:
        unexpected = True
    elif line[to_be_validated_idx[-1]] == matching_start_char:
        to_be_validated_idx.pop()
    if unexpected:
        illegal_counts[idx_closing_chars] += 1

    return unexpected, to_be_validated_idx


def get_autocomplete_closing_chars(line):
    to_be_validated_idx = []
    ac_closing_chars = ""
    for i in range(len(line) -1, -1, -1):
        if line[i] in closing_chars:
            to_be_validated_idx.append(i)
        elif line[i] in start_chars:
            idx_start_chars = start_chars.index(line[i])
            matching_closing_char = closing_chars[idx_start_chars]
            if not to_be_validated_idx: # First char is start
                ac_closing_chars += matching_closing_char
            else:
                if line[to_be_validated_idx[-1]] == matching_closing_char:
                    to_be_validated_idx.pop()
                elif line[to_be_validated_idx[-1]] != matching_closing_char:
                    to_be_validated_idx.append(i)
    return ac_closing_chars


def get_ac_total(ac_closing_chars):
    ac_total_score = 0
    for c in ac_closing_chars:
        idx_closing_chars = closing_chars.index(c)
        ac_total_score *= 5
        ac_total_score += autocomplete_points[idx_closing_chars]
    return ac_total_score


debug = False
files = ['example.txt', 'input.txt', 'input2.txt']

for f in files:

    input = read_input(f)

    start_chars = ['(', '[', '{', '<']
    closing_chars = [')', ']', '}', '>']

    illegal_counts = [0, 0, 0, 0]
    illegal_score = [3, 57, 1197, 25137]

    autocomplete_points = [1, 2, 3, 4]
    autocomplete_multiplier = 5
    autocomplete_results = []
    autocomplete_scores = []

    for line in input:
        to_be_validated_idx = []
        validated_idx = []
        for i in range(len(line)):
            if line[i] in closing_chars:
                unexpected, to_be_validated_idx = is_last_closing_char_unexpected(i, line, to_be_validated_idx)
                if unexpected:
                    break
            else:
                to_be_validated_idx.append(i)
        if unexpected:
            continue

        ac_closing_chars = get_autocomplete_closing_chars(line)
        ac_total_score = get_ac_total(ac_closing_chars)
        autocomplete_results.append(ac_closing_chars)
        autocomplete_scores.append(ac_total_score)

    total_syntax_error_score = 0
    for c, s in zip(illegal_counts, illegal_score):
        total_syntax_error_score += c * s

    for r, s in zip(autocomplete_results, autocomplete_scores):
        if debug:
            print(r, s)
    print(f"{f} - Part 1: {total_syntax_error_score}")
    print(f"{f} - Part 2: {median(autocomplete_scores)}")
