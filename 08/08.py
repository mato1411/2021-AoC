from utils import read_input


def decode_pattern(encoded, decoded_pattern, out):

    for n in [1, 4, 7, 8]:
        if len(encoded) == digits_len.get(n):
            decoded_pattern[n] = encoded
            if out:
                digits_counts[n] = digits_counts.get(n, 0) + 1
            return n

    if out:
        for d, p in decoded_pattern.items():
            if len(encoded) == len(p) and (set(encoded).intersection(set(p)) ==
                                           set(encoded)) and (0 == len(set(encoded).difference(set(p)))):
                return d

    if len(encoded) == 5:
        # 3 in 8, 3 in 9 but not needed
        if set(decoded_pattern[7]) and (set(decoded_pattern[7]) ==
                                        set(decoded_pattern[7]).intersection(set(encoded))):
            decoded_pattern[3] = encoded  # if 7 pattern in number_encrypted, then 3
            return 3

        # 5 in 8, 5 in 9 but not needed
        if set(decoded_pattern[6]) and (set(encoded) ==
                                        set(decoded_pattern[6]).intersection(set(encoded))):
            decoded_pattern[5] = encoded  # if number_encrypted in 6, then 5
            return 5

        if set(decoded_pattern[8]) and set(decoded_pattern[9]) and \
                (set(encoded) == set(decoded_pattern[8]).intersection(set(encoded))) and \
                (1 == len(set(encoded).difference(set(decoded_pattern[9])))):
            decoded_pattern[2] = encoded  # if 3 and 5 are determined only 2 is left
            return 2

    if len(encoded) == 6:
        if set(decoded_pattern[1]) and \
                (1 == len(set(decoded_pattern[1]).intersection(set(encoded)))) and \
                (5 == len(set(encoded).difference(set(decoded_pattern[1])))):
            decoded_pattern[6] = encoded  # if 1 pattern not in number_encrypted, then 6
            return 6

        if set(decoded_pattern[4]) and (3 == len(set(decoded_pattern[4]).intersection(set(encoded)))) and \
                (set(decoded_pattern[1]) == set(decoded_pattern[1]).intersection(set(encoded))):
            decoded_pattern[0] = encoded  # if 4 pattern not in number_encrypted, then 0
            return 0

        if set(decoded_pattern[4]) and (set(decoded_pattern[4]) ==
                                        set(decoded_pattern[4]).intersection(set(encoded))) and \
                (set(decoded_pattern[4]) == set(encoded).intersection(set(decoded_pattern[4]))):
            decoded_pattern[9] = encoded  # if 4 pattern in number_encrypted, then 9
            return 9

    return None


def decode_digits(encoded_digits, decoded_pattern, out=False):
    current_decoded = list('-' * len(encoded_digits))
    repeat = True
    while repeat:
        for j, d in enumerate(encoded_digits):
            n = decode_pattern(d, decoded_pattern, out)
            if n is not None:
                current_decoded[j] = n
                continue
        if "-" not in current_decoded:
            repeat = False
    return current_decoded


debug = False
files = ['example.txt', 'example2.txt', 'input.txt', 'input2.txt']

for f in files:

    input = read_input(f)

    signals = []
    signals_decoded = []

    digit_out = []
    digit_out_decoded = []

    digit_patterns = {0: 'abcefg', 1: 'cf', 2: 'acdeg', 3: 'acdfg', 4: 'bcdf',
                      5: 'abdfg', 6: 'abdfeg', 7: 'acf', 8: 'abcdefg', 9: 'abcdfg'}
    digits_len = {d: len(v) for d, v in digit_patterns.items()}
    digits_counts = {d: 0 for d, v in digit_patterns.items()}

    for n in input:
        signals.append(["".join(sorted(i)) for i in n.split('|')[0].split()])
        digit_out.append(["".join(sorted(i)) for i in n.split('|')[1].split()])

    for signal, output in zip(signals, digit_out):
        digits_decoded_pattern = {d: "" for d, v in digit_patterns.items()}

        d_signal = decode_digits(signal, digits_decoded_pattern)
        signals_decoded.append(d_signal)

        d_output = decode_digits(output, digits_decoded_pattern, out=True)
        digit_out_decoded.append(int("".join([str(n) for n in d_output])))

    print(f"{f} - Part 1: {sum(digits_counts.values())}")
    print(f"{f} - Part 2: {sum(digit_out_decoded)}")
