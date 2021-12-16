input = open("input.txt", "r")

lines = input.readlines()

last = 0

count_up = 0

for i in range(0, (len(lines) - 2)):
    window_sum = sum(map(lambda x: int(x), lines[i:i + 3]))

    if last != 0:
        if window_sum > last:
            count_up += 1

    last = window_sum

print(count_up)