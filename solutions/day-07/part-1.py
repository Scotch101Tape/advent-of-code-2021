import re
import statistics

input = open('input.txt', 'r')

# Get the positions of the crab
positions = list(map(lambda x: int(x),
    re.split(r",", input.read())))

# Get the median, this is the best spot
median = statistics.median(positions)

# Count up how much it will cost
cost = 0
for position in positions:
    cost += abs(position - median)

# Print the cost
print(cost)
