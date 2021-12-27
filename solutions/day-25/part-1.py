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

class South():
    def next_move(point: Point) -> Point:
        return Point(1, 0) + point

class East():
    def next_move(point: Point) -> Point:
        return Point(0, 1) + point

def parse(s: str):
    if s == ">":
        return East()
    elif s == "v":
        return South()
    elif s == ".":
        return None

input = open("input.txt", "r")
board = []
for line in input.readlines():
    board.append([])
    for char in line:
        if char == "\n":
            continue
        has = parse(char)
        board[-1].append(has)

# Undefined behavior is point is neg coord
def get_point_on_board(point):
    if point.x < 0 or point.x >= len(board) or point.y < 0 or point.y >= len(board[0]):
        raise IndexError
    else:
        return board[point.x][point.y]

def get_wrapped_point(point):
    return Point(point.x % len(board), point.y % len(board[0]))

def print_board():
    for line in board:
        print("\n", end = "")
        for element in line:
            s = "v" if isinstance(element, South) else ">" if isinstance(element, East) else "."
            print(s, end = "")
    print()

herds = [East, South]

i = 0
moved = True
while moved:
    moved = False

    for herd in herds:
        new_board = []
        for line in board:
            new_board.append([])
            for element in line:
                new_board[-1].append(East() if isinstance(element, East) else South() if isinstance(element, South) else None)

        for x in range(len(board)):
            for y in range(len(board[0])):
                element = board[x][y]
                if isinstance(element, herd):
                    moved_point = get_wrapped_point(herd.next_move(Point(x, y)))
                    if get_point_on_board(moved_point) is None:
                        new_board[moved_point.x][moved_point.y] = element
                        new_board[x][y] = None
                        moved = True

        board = new_board
    
    i += 1
    
print(i)
