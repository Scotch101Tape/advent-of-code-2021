input = open("input.txt", "r")

last = 0
count_up = 0

for line in input.readlines():
    if last != 0:
        if last < int(line):
            count_up += 1

    last = int(line)

print(count_up)