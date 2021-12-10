input = open("input.txt", "r")

char_to_point = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

pairs = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}

opening = pairs.keys()
closing = pairs.values()

points = 0
for line in input.read().splitlines():
    stack = []
    for char in line:
        if char in opening:
            stack.append(char)
        elif char in closing:
            opening_char = stack.pop()
            if pairs[opening_char] != char:
                points += char_to_point[char]
                break

print(points)
