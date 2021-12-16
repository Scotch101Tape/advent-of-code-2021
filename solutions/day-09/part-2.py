from functools import reduce

input = open("input.txt", "r")

lines = input.read().splitlines()

# Stealing my basic utility Point class from day 5
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def scaler_mult(self, scaler):
        return Point(self.x * scaler, self.y * scaler)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

offsets = [Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)]

# Returns the number if in bounds, else returns a 9
def protected_check(point):
    if point.x < 0 or point.x >= len(lines):
        return 9

    if point.y < 0 or point.y >= len(lines[point.x]):
        return 9
    
    return int(lines[point.x][point.y])

def flow(point):
    num = protected_check(point)

    for offset in offsets:
        adj_point = offset + point
        if protected_check(adj_point) < num:
            return flow(adj_point)

    return point


# Basins are indexed by the point they flow into
basins = {}

# Iterate over the board, finding where each point flows.
# Then add it to basins
for x in range(len(lines)):
    line = lines[x]
    for y in range(len(line)):
        point = Point(x, y)

        # Don't count 9
        if protected_check(point) == 9:
            continue

        flow_point_str = str(flow(point))

        if not (flow_point_str in basins):
            basins[flow_point_str] = 1
        else:
            basins[flow_point_str] += 1

# Find the top three basins
top_three = sorted(basins.values(), reverse=True)[0:3]

# Multiply them together and print
print(reduce(lambda a, b: a * b, top_three))
