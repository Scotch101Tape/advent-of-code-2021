import re

input = open("input.txt", "r")

# At this point theres nothing more to say than that you've probably seen this before
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

# The paper class
class Paper:
    def __init__(self, points):
        self.points = points

    def fold_x(self, x):
        new_points = []

        for point in self.points:
            if point.x > x:
                new_point = Point(2 * x - point.x, point.y)
            elif point.x < x:
                new_point = point

            if new_point not in new_points:
                new_points.append(new_point)

        self.points = new_points

    def fold_y(self, y):
        new_points = []

        for point in self.points:
            if point.y > y:
                new_point = Point(point.x, 2 * y - point.y)
            elif point.y < y:
                new_point = point

            if new_point not in new_points:
                new_points.append(new_point)

        self.points = new_points

    def points_showing(self):
        return len(self.points)

# Parse the data to get the points
points = []

while True:
    # Consume the line
    # When it gets to it, this will consume the newline seperator between the folding instructions
    line = input.readline()

    result = re.search(r"(\d*),(\d*)", line)
    if result == None:
        break
    else:
        points.append(Point(int(result[1]), int(result[2])))

# Now we paper
paper = Paper(points)

# Follow the first instruction
for i in range(1):
    # Consume the line
    line = input.readline()

    result = re.search(r"fold along (x|y)=(\d*)", line)

    if result == None:
        break
    else:
        # Fold
        if result[1] == "x":
            paper.fold_x(int(result[2]))
        else:
            paper.fold_y(int(result[2]))

# print the number of points showing
print(paper.points_showing())
