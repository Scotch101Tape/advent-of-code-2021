import re

input = open("input.txt", "r")

class Cave:
    def __init__(self, name):
        self.name = name
        self.connections = []

    def __str__(self):
        return self.name

    def add_connection(self, cave):
        self.connections.append(cave)

class SmallCave(Cave):
    def __str__(self):
        return self.name

class BigCave(Cave):
    def __str__(self):
        return self.name

# Search for paths in a cave
def cave_search(cave, total_path = [], doubled = False):
    # The paths in the search
    paths = 0

    # Edge case with end
    if cave.name == "end":
        return 1

    # Go through the caves connections
    has_connections = False
    for connection in cave.connections:
        # Whether this iteration was doubled
        new_double = doubled

        # Edge case with start
        if connection.name == "start":
            continue

        # Oh no your a small cave and have been visited
        if isinstance(connection, SmallCave) and (connection in total_path):
            # The special case of not being doubled and you want to visit a small cave
            if not doubled:
                # The cave is visited but doubled is off
                new_double = True
            else:
                continue
        
        # Add the number of paths
        has_connections = True
        paths += cave_search(connection, total_path + [cave], new_double)
    
    if has_connections:
        return paths
    else:
        return 0

# Parse the data and find all the caves
caves = {}

for line in input.readlines():
    result = re.search(r"(\w*)-(\w*)", line)

    cave_name_1 = result[1]
    cave_name_2 = result[2]

    if cave_name_1 not in caves:
        if cave_name_1[0].isupper():
            new_cave = BigCave(cave_name_1)
        else:
            new_cave = SmallCave(cave_name_1)
        caves[cave_name_1] = new_cave

    if cave_name_2 not in caves:
        if cave_name_2[0].isupper():
            new_cave = BigCave(cave_name_2)
        else:
            new_cave = SmallCave(cave_name_2)
        caves[cave_name_2] = new_cave

    caves[cave_name_1].add_connection(caves[cave_name_2])
    caves[cave_name_2].add_connection(caves[cave_name_1])

# Get the number of paths
paths = cave_search(caves["start"])

# Print the number of paths
print(paths)
