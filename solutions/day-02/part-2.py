import re

input = open('input.txt', 'r')

depth = 0
forward = 0
aim = 0

for line in input.readlines():
    find = re.search(r"(\w*) (\d)", line)
    word = find[1]
    number = int(find[2])

    if word == "forward":
        forward += number
        depth += number * aim
    elif word == "down":
        aim += number
    elif word == "up":
        aim -= number

print(depth * forward)
