input = open("input.txt", "r")

# Once again stealing my point class >:)
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

offsets = [Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1), Point(1, 1), Point(-1, 1), Point(1, -1), Point(-1, -1)]

# I really want a pipe operator at this point
# This basicly parses it into a 2d list of ints
board = list(map(lambda x: list(map(lambda c: int(c), x)), 
    input.read().splitlines()))

# Number of flashes
flashes = 0

# For 100 steps
for step in range(100):
    # Part 1
    # Increase each octopus by one
    for x in range(10):
        for y in range(10):
            board[x][y] += 1
    
    # Part 2
    # Flash and increase

    # List of points that have been flashed
    flashed = []

    # Whether and octo flashed in an iteration
    octo_flashed = True

    while octo_flashed:
        octo_flashed = False

        # The board that gets modified
        new_board = board.copy()

        # For every point on the board
        for x in range(10):
            for y in range(10):
                point = Point(x, y)

                # Energy level greater than 9 and not flashed yet, then flash
                if board[x][y] > 9 and not (point in flashed):
                    flashes += 1

                    # Turn octo flashed to true
                    octo_flashed = True

                    # Add the point to flashed
                    flashed.append(point)

                    # Add to the adj_points, this is only dealt with in the next iteration
                    for offset in offsets:
                        adj_point = offset + point
                        if adj_point.x >= 0 and adj_point.x < 10 and adj_point.y >= 0 and adj_point.y < 10:
                            new_board[adj_point.x][adj_point.y] += 1

        # Set the board to new_board
        board = new_board
    
    # Part 3
    # Set all the flashed to 0
    for point in flashed:
        board[point.x][point.y] = 0

# Print the flashes
print(flashes)