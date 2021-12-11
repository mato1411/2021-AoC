with open('input2.txt') as f:
    inputs = f.read().split('\n')[:-1]

inputs = [int(i) for i in inputs]
result_1 = ['N/A - no previous measurement']
result_2 = []
previous = 0
sums = []
for i in range(len(inputs) - 1):
    if inputs[i+1] > inputs[i]:
        result_1.append('increased')
    else:
        result_1.append('decreased')

    if i >= len(inputs) - 2:
        continue
    current = sum(inputs[i:i + 3])
    sums.append(current)
    if previous == 0:
        result_2.append(result_1[0])
    else:
        if current > previous:
            result_2.append('increased')
        else:
            result_2.append('decreased')
    previous = current
for i, r in zip(inputs, result_1):
    print(f"{i} ({r})")

for s, r in zip(sums, result_2):
    print(f"{s} ({r})")

print(f"Part 1: {result_1.count('increased')}")
print(f"Part 2: {result_2.count('increased')}")
