import re
import math

def add_to_dict(dic, key, num):
    if key in dic:
        dic[key] += num
    else:
        dic[key] = num

class Rule:
  def __init__(self, pattern, insertation):
    self.pattern = pattern
    self.insertation = insertation

input = open("input.txt", "r")

# Get the current poly
poly = list(input.readline())
input.readline()

# Get the rules
rules = []
for line in input.readlines():
  result = re.search(r"(\w\w) -> (\w)", line)

  pattern = result[1]
  insertation = result[2]

  rules.append(Rule(pattern, insertation))

patterns = list(map(lambda x: x.pattern, rules))

# Get the pairs
pairs = {}
for i in range(len(poly) - 2):
    pair = poly[i] + poly[i + 1]
    add_to_dict(pairs, pair, 1)

# Get the start and end of the poly
start_poly = poly[0]
end_poly = poly[-1]

# 10 times
for _ in range(40):
    new_pairs = {}
    for pair in pairs:
        if pair in patterns:
            rule = rules[patterns.index(pair)]
            add_to_dict(new_pairs, pair[0] + rule.insertation, pairs[pair])
            add_to_dict(new_pairs, rule.insertation + pair[1], pairs[pair])
        else:
            add_to_dict(new_pairs, pair, new_pairs[pair])
    pairs = new_pairs

# Find the number of letters
letters = {}
for pair in pairs:
    add_to_dict(letters, pair[0], pairs[pair])
    add_to_dict(letters, pair[1], pairs[pair])

# I need to find a map for dict
for letter in letters:
    letters[letter] = math.ceil(letters[letter] / 2)

# Print answer
print(max(letters.values()) - min(letters.values()))
