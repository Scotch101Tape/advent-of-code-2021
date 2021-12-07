import re

input = open("input.txt", "r")

# Basic utility sign funciton
sign = lambda x: 1 if x > 0 else -1 if x < 0 else 0

# Basic utility Point class
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

# This dictionary contains each point that contains a hydrothermal vent and how many times it is overlapped
points = {}

# For each line
for line in input.readlines():
    # Parse line
    result = re.search(r"(\d*),(\d*) -> (\d*),(\d*)", line)

    # Get the beginning and ending of the line
    p1 = Point(int(result[1]), int(result[2]))
    p2 = Point(int(result[3]), int(result[4]))

    # Get the difference
    diff = p1 - p2

    if diff.y == 0:
        # If the line is horizontal
        step = Point(-sign(diff.x), 0)
    elif diff.x == 0:
        # If the line is vertical
        step = Point(0, -sign(diff.y))
    else:
        # If the line is diagonal
        step = Point(-sign(diff.x), -sign(diff.y))

    # While we are not at the end of the line
    i = 0
    while True:
        # Get the point on the line
        point = p1 + step.scaler_mult(i)

        # Add the point to the point
        point_str = str(point)
        if not (point_str in points):
            points[point_str] = 1
        else:
            points[point_str] += 1

        # If its the end of the line exit
        if point == p2:
            break

        # Increment i
        i += 1

# Find all points that overlap 2 or more
counter = 0
for key in points:
    if points[key] >= 2:
        counter += 1

# Print counter
print(counter)
