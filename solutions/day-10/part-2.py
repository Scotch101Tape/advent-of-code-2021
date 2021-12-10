from statistics import median

input = open("input.txt", "r")

char_to_point = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}

pairs = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}

opening = pairs.keys()
closing = pairs.values()

# The list of the points each line has
line_points = []
for line in input.read().splitlines():
    invalid = False
    stack = []
    for char in line:
        if char in opening:
            # Add opening characters to the stack
            stack.append(char)
        elif char in closing:
            # Check if closing characters are correct
            opening_char = stack.pop()
            if pairs[opening_char] != char:
                # The closing character is wrong, the line is invalid
                invalid = True
                break
        
    if not invalid:
        points = 0
        # Reverse the stack so it goes in autocomplete order
        for char in reversed(stack):
            # Multiply by five
            points *= 5

            # Add the score
            points += char_to_point[pairs[char]]
        
        # Add the points to line points
        line_points.append(points)

# Return the middle point
print(median(line_points))