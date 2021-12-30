import re

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

    def __hash__(self):
        return hash((self.x, self.y))

class Bounds:
    def __init__(self, min_point, max_point):
        self.min_point = min_point
        self.max_point = max_point

    def contain(self, point):
        return point.x >= self.min_point.x and point.y >= self.min_point.y and point.x <= self.max_point.x and point.y <= self.max_point.y

class Probe:
    def __init__(self, vel):
        self.vel = vel
        self.pos = Point(0, 0)

    def step(self):
        self.pos = self.vel + self.pos

        self.vel.x = max(0, self.vel.x - 1)
        self.vel.y -= 1

# Parse input
input = open("input.txt", "r")
result = re.search(r"target area: x=(-?\d*)..(-?\d*), y=(-?\d*)..(-?\d*)", input.readline())
bounds = Bounds(
    Point(int(result[1]), int(result[3])),
    Point(int(result[2]), int(result[4]))
)

#print(bounds.contain(Point()))

# Do this 1000 times
total_in = 0
for i in range(1000):
    for xi in range(i + 1):
        if xi > 180:
            # Should make it faster
            continue
        yi = i - xi
        probe = Probe(Point(xi, yi + bounds.min_point.y))
        # Do the probe step 20 times
        for _ in range(1000):
            probe.step()
            #print(bounds.contain(probe.pos))
            #print(this_max_height)
            if bounds.contain(probe.pos):
                total_in += 1
                break
            if probe.pos.y < bounds.min_point.y:
                break


        
        #print(this_max_height)

# Print total_in
print(total_in)
