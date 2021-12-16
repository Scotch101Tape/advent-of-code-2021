input = open("input.txt", "r")

offsets = [[1, 0], [0, 1], [-1, 0], [0, -1]]

lines = input.read().splitlines()

total_risk = 0
for i in range(len(lines)):
    line = lines[i]
    for o in range(len(line)):
        worked = True
        num = int(line[o])

        for offset in offsets:
            new_i = offset[0] + i
            new_o = offset[1] + o

            if new_i < 0 or new_i >= len(lines):
                continue

            if new_o < 0 or new_o >= len(line):
                continue
                
            adj_num = int(lines[new_i][new_o])
            if num >= adj_num:
                worked = False

        if worked:
            total_risk += num + 1
        
print(total_risk)


