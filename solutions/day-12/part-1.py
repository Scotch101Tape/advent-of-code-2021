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
def cave_search(cave, path = []):
    if path == []:
        paths = []
    else:
        paths = [path]
    
    for branch in cave.connections:
        if isinstance(branch, BigCave) or branch not in path:
            new_path = path + [cave]
            result_paths = cave_search(branch, new_path)
            paths.extend(result_paths)
    return paths

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

paths = cave_search(caves["start"])

# Filter out the paths that don't end with end
end_paths = list(filter(lambda p: p[-1].name == "end",
    paths))

# This is a stupid way to do it
# It removes duplicates
new_end_paths = []
for path in end_paths:
    if path not in new_end_paths:
        new_end_paths.append(path)
end_paths = new_end_paths

# Print the number of paths
print(len(end_paths))