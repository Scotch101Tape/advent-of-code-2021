from os import error

input = open('input.txt', 'r')

def list_to_int(l):
    num = 0
    for i in range(12):
        num += int(l[i]) * pow(2, 11 - i)
    return num

lines = input.readlines()

# Oxygen
oxygen_lines = lines.copy()

for i in range(12):
    count = 0
    for line in oxygen_lines:
        if line[i] == "1":
            count += 1
        elif line[i] == "0":
            count -= 1

    chosen_bit = "1" if count >= 0 else "0"
    oxygen_lines = list(filter(lambda x: x[i] == chosen_bit, oxygen_lines))

    if len(oxygen_lines) == 1:
        oxygen = list_to_int(oxygen_lines[0])
        break

# CO2
co2_lines = lines.copy()

for i in range(12):
    count = 0
    for line in co2_lines:
        if line[i] == "1":
            count += 1
        elif line[i] == "0":
            count -= 1

    chosen_bit = "1" if count < 0 else "0"
    co2_lines = list(filter(lambda x: x[i] == chosen_bit, co2_lines))

    if len(co2_lines) == 1:
        co2 = list_to_int(co2_lines[0])
        break

print(oxygen * co2)
