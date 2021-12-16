import re

# The lengths of the digits for 1, 7, 4, 8 respectivly
lengths = {2, 3, 4, 7}

input = open("input.txt", "r")

# The counter for the number of 1, 4, 7, 8 digits
counter = 0

# For each input line
for line in input.readlines():
    # Search the string for the last 4 digits
    result = re.search(r"\| (\w*) (\w*) (\w*) (\w*)", line)

    # Put the results into an array
    digits = [
        result[1],
        result[2],
        result[3],
        result[4]
    ]

    # For the digits
    for digit in digits:
        # Get the length
        length = len(digit)

        # If the digit is 1, 4, 7, 8 add to counter
        if length in lengths:
            counter += 1

# Print counter
print(counter)
    