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

class Board:
    def __init__(self, board):
        self.board = board

    def safe_get(self, point):
        if point.x >= 0 and point.y >= 0 and point.x < len(self.board) and point.y < len(self.board[0]):
            return self.board[point.x][point.y]
        else:
            return None

    def end_point(self):
        return Point(len(self.board) - 1, len(self.board[0]) - 1)

# Parse the input
input = open("input.txt", "r")
lines = input.readlines()

board = []
for x in range(5):
    for line in lines:
        board.append([])
        for y in range(5):
            for char in line:
                if char == "\n":
                    continue
                board[-1].append((int(char) + x + y - 1) % 9 + 1)

board = Board(board)

fastest = [] 
for x in range(len(board.board)):
    fastest.append([])
    for y in range(len(board.board[0])):
        fastest[-1].append(None)

fastest[0][0] = 0

class Path:
    def __init__(self, point, total = 0):
        self.point = point
        self.total = total
    
    def continue_path(self, new_point):
        value = board.safe_get(new_point)
        if value != None:
            return Path(new_point, self.total + value)

    def __str__(self):
        return f"p: {str(self.point)}, t: {str(self.total)}" 

# Find the path

# Adj tiles
offsets = [Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1)]

# Check how far a point is from the end
def distance_from_end(point):
    dis_point = board.end_point() - point
    return dis_point.x + dis_point.y

# Starts at top left
paths = [Path(Point(0, 0))]

# Until we break
while len(paths) > 0:
    new_paths = []

    for path in paths:
        for offset in offsets:
            new_path = path.continue_path(offset + path.point)

            if new_path != None:
                # Check if the new_path is a new fastest way to get somewhere
                fastest_total = fastest[new_path.point.x][new_path.point.y]

                if fastest_total != None:
                    if new_path.total > fastest_total:
                        continue
                
                fastest[new_path.point.x][new_path.point.y] = new_path.total
                new_paths.append(new_path)

    paths = new_paths
    new_paths = []

    # Prune all the paths that have faster ways to get there
    special = []
    for x in range(len(fastest)):
        special.append([])
        for y in range(len(fastest[0])):
            special[-1].append(None)
    
    for path in paths:
        fastest_total = fastest[path.point.x][path.point.y]
        if fastest_total >= path.total and special[path.point.x][path.point.y] == None:
            fastest[path.point.x][path.point.y] = path.total
            special[path.point.x][path.point.y] = True
            new_paths.append(path)

    paths = new_paths

# Print the min
print(fastest[board.end_point().x][board.end_point().y])
