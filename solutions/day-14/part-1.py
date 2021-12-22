import re

class Rule:
    def __init__(self, pattern, insertation):
        self.pattern = pattern
        self.insertation = insertation


input = open('input.txt', 'r')

# Get the current poly

poly = list(input.readline())
input.readline()

# Get the rules

rules = []
for line in input.readlines():
    result = re.search(r"(\w\w) -> (\w)", line)

    pattern = list(result[1])
    insertation = result[2]

    rules.append(Rule(pattern, insertation))

# For 10 steps

for _ in range(10):

  # Get the inserts, these will be added in later

    inserts = [None] * (len(poly) - 1)

  # For each pair

    for i in range(len(poly) - 1):
        pair = [poly[i], poly[i + 1]]

    # For each rule

        for rule in rules:

      # Check if the rule matches the pair

            if rule.pattern == pair:

        # If it does add it to inserts

                inserts[i] = rule.insertation

  # Add the inserts into the poly

    new_poly = []

  # Alt between inserts and poly

    for i in range(len(poly) + len(inserts)):
        if i % 2 == 0:
            new_poly.append(poly[int(i / 2)])
        else:

      # If there is an insert here, add it in

            ins = inserts[int((i - 1) / 2)]
            if ins != None:
                new_poly.append(ins)

  # Update poly

    poly = new_poly

# Find the least and greatest values

values = {}
for char in poly:
    if char == '\n':
        continue

    if char in values:
        values[char] += 1
    else:
        values[char] = 0

# Print the max - min
print(max(values.values()) - min(values.values()))
