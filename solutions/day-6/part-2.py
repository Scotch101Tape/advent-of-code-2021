from os import stat
import re

input = open("input.txt", "r")

# Each state contains the number of fishes in each state
fishes = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
}

# Add in the fishes from the input
for state in map(lambda x: int(x), re.split(r",", input.read())):
    fishes[state] += 1

# For 256 days
for day in range(256):
    # Create a new dictionary of fishes
    new_fishes = {}

    # For each state, shift it down one
    for state in fishes:
        new_fishes[state - 1] = fishes[state]

    # For each -1 fish create a new 8 fish
    new_fishes[8] = new_fishes[-1]

    # Add the -1 fishes to 6
    new_fishes[6] += new_fishes[-1]

    # Get rid of the -1 state
    del new_fishes[-1]
    
    # Set fishes to new fishes
    fishes = new_fishes

# Sum up all the fishes
sum = 0
for state in fishes:
    sum += fishes[state]

# Print the sum
print(sum)