from functools import reduce
from itertools import permutations
import re

# Positions:   
#  1111 
# 2    3
# 2    3
#  4444 
# 5    6
# 5    6
#  0000 

# The digits with unique length and its length
lengths = {
    1: 2, 
    7: 3, 
    4: 4, 
    8: 7
}

number_from_length = lambda length: list(lengths.keys())[list(lengths.values()).index(length)]

# What segments are supposed to show with each number
correct_numbers = {
    0: {1, 2, 3, 5, 6, 0},
    1: {3, 6},
    2: {1, 3, 4, 5, 0},
    3: {1, 3, 4, 6, 0},
    4: {2, 4, 6, 3},
    5: {1, 2, 4, 6, 0},
    6: {1, 2, 4, 6, 5, 0},
    7: {6, 3, 1},
    8: {1, 2, 3, 4, 5, 6, 0},
    9: {2, 1, 3, 4, 6, 0}
}


input = open("input.txt", "r")

# Sum of the messages
sum = 0
for line in input.readlines():
    # parse the line into example_digits and message_digits
    result = re.search(r"(\w*) (\w*) (\w*) (\w*) (\w*) (\w*) (\w*) (\w*) (\w*) (\w*) \| (\w*) (\w*) (\w*) (\w*)", line)

    example_digits = {        
        result[1],
        result[2],
        result[3],
        result[4],
        result[5],
        result[6],
        result[7],
        result[8],
        result[9],
        result[10]
    }

    message_digits = [
        result[11],
        result[12],
        result[13],
        result[14]
    ]

    # Find 1, 4, 7, 8
    sorted_digits = [None] * 10
    for digit in example_digits:
        length = len(digit)
        # If the length is one of the special lengths
        if length in lengths.values():
            # Add it to sorted digits in the index of what it corresponds to
            sorted_digits[number_from_length(length)] = set(digit)

    #   1:      4:      7:      8:
    #  ....    ....    zzzz    zzzz 
    # .    x  y    x  .    x  y    x
    # .    x  y    x  .    x  y    x
    #  ....    yyyy    ....    yyyy 
    # .    x  .    x  .    x  a    x
    # .    x  .    x  .    x  a    x
    #  ....    ....    ....    aaaa 

    # contain positions 3, 6
    x_positions = [3, 6]
    x_digits = sorted_digits[1].intersection(sorted_digits[4])

    # contain positions 2, 4
    y_positions = [2, 4]
    y_digits = sorted_digits[4].difference(sorted_digits[1])

    # contains position 1
    # treated as multiple for consitancy
    z_positions = [1]
    z_digits = sorted_digits[7].difference(sorted_digits[1])

    # contains positon 5, 7
    a_positions = [5, 0]
    a_digits = sorted_digits[8].difference(sorted_digits[7].union(sorted_digits[4]))

    # find the sorted wires
    # the sorted wires are the char in the index the position corresponds to
    def find_sorted_wires():
        for test_x in permutations(x_digits):
            for test_y in permutations(y_digits):
                for test_z in permutations(z_digits):
                    for test_a in permutations(a_digits):
                        # Create a sorted wires test
                        test_sorted_wires = [None] * 7
                        for i, position in enumerate(x_positions):
                            test_sorted_wires[position] = test_x[i]
                        for i, position in enumerate(y_positions):
                            test_sorted_wires[position] = test_y[i]
                        for i, position in enumerate(z_positions):
                            test_sorted_wires[position] = test_z[i]
                        for i, position in enumerate(a_positions):
                            test_sorted_wires[position] = test_a[i]
                                                

                        worked = True
                        for digit in example_digits:
                            turned_on = set()
                            for char in digit:
                                turned_on.add(test_sorted_wires.index(char))

                            if not (turned_on in correct_numbers.values()):
                                worked = False
                                break
                            
                        
                        if worked == True:
                            return test_sorted_wires

    # Get the sorted wires
    sorted_wires = find_sorted_wires()

    # Update the sorted digits from the sorted wires
    for number in correct_numbers:
        digits_on = set()
        for position in correct_numbers[number]:
            digits_on.add(sorted_wires[position])
        sorted_digits[number] = digits_on

    # Using sorted digits, decode the message and add it to the sum
    num = 0    
    for i, int_digit in enumerate(list(map(lambda x: sorted_digits.index(set(x)), message_digits))):
        num += int_digit * pow(10, 3 - i)
    sum += num

    
# Print sum
print(sum)