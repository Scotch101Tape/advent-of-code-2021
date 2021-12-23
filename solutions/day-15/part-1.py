class Board:
    def __init__(self, board):
        self.board = board

    def safe_get(self, x, y):
        if x >= 0 and y >= 0 and x < len(self.board) and y < len(self.board[0]):
            return self.board[x][y]
        else:
            return None

# Parse the input
input = open("input.txt", "r")

board = []
for line in input.readlines():
    board.append([])
    for char in line:
        if char == "\n":
            continue
        board[-1].append(int(char))

board = Board(board)

class Path:
    def __init__(self, position, total = 0):
        self.position = position
        self.total = total
    
    def continue_path(self, new_position):
        value = board.safe_get(*new_position)
        if value != None:
            return Path(new_position, self.total + value)

# Find the path
# Algorithem is 
# 1. For each possible path, expand it 5
# 2. Take the top 100 new possiblities (<32 for each possible path)
# 3. Repeat

# Adj tiles
offsets = [(1, 0), (0, 1)]

# expand funciton
def expand(path, n = 0):
    if n == 5 or path.position == (len(board.board) - 1, len(board.board[0]) - 1):
        return [path]
    else:
        paths = []
        for offset in offsets:
            new_position = (offset[0] + path.position[0], offset[1] + path.position[1])
            new_path = path.continue_path(new_position)
            if new_path != None:
                paths.extend(expand(new_path, n + 1))
        return paths


# Starts at top left
paths = [Path((0, 0))]

# Until we reach the end
while paths[0].position != (len(board.board) - 1, len(board.board[0]) - 1):
    new_paths = []
    for path in paths:
        new_paths.extend(expand(path))

    # Sorry for this
    new_new_paths = []
    new_new_paths_position = []
    for path in new_paths:
        if path.position in new_new_paths_position:
            i = new_new_paths_position.index(path.position)
            if path.total < new_new_paths[i].total:
                new_new_paths[i] = path
                new_new_paths_position[i] = path.position
        else:
            new_new_paths.append(path)
            new_new_paths_position.append(path.position)

    paths = sorted(new_new_paths, key = lambda x: x.total)[0:100]

# Print the min
print(min(list(map(lambda x: x.total, paths))))
