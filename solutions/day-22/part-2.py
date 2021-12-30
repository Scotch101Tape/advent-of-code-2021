import re

class StartFlag:
    def __init__(self, value, order):
        self.value = value
        self.order = order

class EndFlag:
    def __init__(self, value, order):
        self.value = value
        self.order = order

input = open("input.txt", "r")

order_to_on = []
x_flags = []
y_flags = []
z_flags = []

lines = input.readlines()
for i in range(len(lines)):
    line = lines[i]
    result = re.search(r"(on|off) x=(-?\d*)\.\.(-?\d*),y=(-?\d*)\.\.(-?\d*),z=(-?\d*)\.\.(-?\d*)", line)

    on = result[1] == "on"
    x_min = int(result[2])
    x_max = int(result[3])
    y_min = int(result[4])
    y_max = int(result[5])
    z_min = int(result[6])
    z_max = int(result[7])

    order_to_on.append(on)

    x_flags.append(StartFlag(x_min, i))
    x_flags.append(EndFlag(x_max + 1, i))

    y_flags.append(StartFlag(y_min, i))
    y_flags.append(EndFlag(y_max + 1, i))

    z_flags.append(StartFlag(z_min, i))
    z_flags.append(EndFlag(z_max + 1, i))


def group_same(l):
    l = sorted(l, key = lambda x: x.value)
    new_l = []
    for element in l:
        if len(new_l) > 0:
            if element.value in list(map(lambda x: x.value, new_l[-1])):
                new_l[-1] = sorted(new_l[-1] + [element], reverse = True, key = lambda x: x.order)
            else:
                new_l.append([element])
        else:
            new_l.append([element])

    return new_l

x_flags = group_same(x_flags)
y_flags = group_same(y_flags)
z_flags = group_same(z_flags)

def is_on(order):
    return order_to_on[order]

total = 0
on_x = set()
for xi in range(len(x_flags) - 1):
    x_group = x_flags[xi]
    x_spread = x_flags[xi + 1][-1].value - x_flags[xi][-1].value
    for x in x_group:
        if isinstance(x, StartFlag):
            on_x.add(x.order)
        elif isinstance(x, EndFlag):
            on_x.remove(x.order)

    on_y = set()
    for yi in range(len(y_flags) - 1):
        y_group = y_flags[yi]
        y_spread = y_flags[yi + 1][-1].value - y_flags[yi][-1].value
        for y in y_group:
            if isinstance(y, StartFlag):
                on_y.add(y.order)
            elif isinstance(y, EndFlag):
                on_y.remove(y.order)

        on_z = set()
        for zi in range(len(z_flags) - 1):
            z_group = z_flags[zi]
            z_spread = z_flags[zi + 1][-1].value - z_flags[zi][-1].value
            for z in z_group:
                if isinstance(z, StartFlag):
                    on_z.add(z.order)
                elif isinstance(z, EndFlag):
                    on_z.remove(z.order)
            
            total_intersection = on_z.intersection(on_y).intersection(on_x)
            if len(total_intersection) > 0:
                highest_order = max(total_intersection)
                if is_on(highest_order):
                    total += z_spread * y_spread * x_spread

print(total)