from typing import Dict


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

class Board:
    around_offsets = [Point(-1, -1), Point(-1, 0), Point(-1, 1), Point(0, -1), Point(0, 0), Point(0, 1), Point(1, -1), Point(1, 0), Point(1, 1)]

    def __init__(self, default, board):
        self.board = board
        self.default = default

    def get(self, point):
        if self.is_in(point):
            return self.board[point.x][point.y]
        return self.default

    def set(self, point, value):
        if point.x not in self.board:
            self.board[point.x] = {}
        
        self.board[point.x][point.y] = value

    def is_in(self, point):
        if point.x in self.board:
            if point.y in self.board[point.x]:
                return True
        return False

    def copy(self):
        return Board(self.default, self.board.copy())

    def value_of_around(self, point):
        value = 0
        for (i, offset) in enumerate(Board.around_offsets):
            value += pow(2, 8 - i) * (1 if self.get(point + offset) else 0)
        return value

    def __str__(self):
        string = ""
        for x in range(-50, 50):
            string = string + "\n"
            for y in range(-50, 50):
                string =  string + ("#" if self.get(Point(x, y)) else ".")

        return string



input = open("input.txt", "r")
image_changer = input.readline()
input.readline()

board = Board(False, dict())
for (x, line) in enumerate(input.readlines()):
    for (y, char) in enumerate(line):
        if char == "#":
            board.set(Point(x, y), True)

#print(board.board)

# for 2 times
#print(board)
for i in range(2):
    # Because special
    new_board = Board(not board.default, dict())
    for x in board.board:
        #print(x)
        for y in board.board[x]:
            #print(board.board[x])
            for offset in Board.around_offsets:
                point = offset + Point(x, y)
                if not new_board.is_in(point):
                    #print("not in")
                    changer_value = image_changer[board.value_of_around(point)]
                    new_board.set(point, True if changer_value == "#" else False)
                #print(point)
                #print(board.board[x])
            #print(board.board[x])

    board = new_board
    #print(board)

# Print the number of on
total = 0
for x in board.board:
    for y in board.board[x]:
        if board.get(Point(x, y)) == True:
            total += 1

print(total)