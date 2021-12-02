import re

input = open('input.txt', 'r')

depth = 0
forward = 0

for line in input.readlines():
    find = re.search(r"(\w*) (\d)", line)
    word = find[1]
    number = int(find[2])

    if word == "forward":
        forward += number
    elif word == "down":
        depth += number
    elif word == "up":
        depth -= number

print(depth * forward)
