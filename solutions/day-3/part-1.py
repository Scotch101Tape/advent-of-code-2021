input = open('input.txt', 'r')

# 12 long
count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def list_to_int(l):
    num = 0
    for i in range(12):
        num += int(l[i]) * pow(2, 11 - i)
    return num

for line in input.readlines():
    for i in range(12):
        digit = line[i]
        if digit == "1":
            count[i] += 1
        elif digit == "0":
            count[i] -= 1
    
gamma = list(map(lambda x: min(max(x, 0), 1), count.copy()))
elipson = list(map(lambda x: min(max(-x, 0), 1), count.copy()))

print(list_to_int(gamma) * list_to_int(elipson))
