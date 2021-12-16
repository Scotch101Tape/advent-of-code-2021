import re

input = open("input.txt", "r")

sign = lambda x: 1 if x > 0 else -1 if x < 0 else 0

# List of x values
xs = list(map(lambda x: int(x),
    re.split(r",", input.read())))

n = len(xs)

def di(x, i):
    return abs(x - xs[i])

def dcdx(x):
    sum = 0
    for i in range(n):
        sum += sign(x - xs[i])*(di(x, i) + 1/2)
    return sum

def c(x):
    sum = 0
    for i in range(n):
        sum += (pow(di(x, i), 2) + di(x, i)) / 2
    return sum

x = 1
last = sign(dcdx(x))
while True:
    new = sign(dcdx(x))
    if sign(dcdx(x)) != last:
        x -= 1
        break

    x += 1

print(c(x))
