import re
import numpy as np

rotatations = [
    np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]),
    np.array([
        [-1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ]),
    np.array([
        [-1, 0, 0],
        [0, 1, 0],
        [0, 0, -1]
    ]),
    np.array([
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, -1]
    ]),
    np.array([
        [0, 1, 0],
        [-1, 0, 0],
        [0, 0, 1]
    ]),
    np.array([
        [0, -1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ]),
    np.array([
        [0, 0, -1],
        [0, 1, 0],
        [1, 0, 0]
    ]),
    np.array([
        [0, 0, 1],
        [0, 1, 0],
        [-1, 0, 0]
    ]),
    np.array([
        [1, 0, 0],
        [0, 0, 1],
        [0, -1, 0]
    ]),
    np.array([
        [1, 0, 0],
        [0, 0, -1],
        [0, 1, 0]
    ]),
    np.array([
        [0, 0, -1],
        [-1, 0, 0],
        [0, 1, 0]
    ]),
    np.array([
        [0, 0, 1],
        [-1, 0, 0],
        [0, -1, 0]
    ]),
    np.array([
        [0, 0, -1],
        [0, -1, 0],
        [-1, 0, 0]
    ]),
    np.array([
        [0, 0, 1],
        [0, -1, 0],
        [1, 0, 0]
    ]),
    np.array([
        [0, 1, 0],
        [0, 0, -1],
        [-1, 0, 0]
    ]),
    np.array([
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0]
    ]),
    np.array([
        [0, -1, 0],
        [-1, 0, 0],
        [0, 0, -1]
    ]),
    np.array([
        [0, -1, 0],
        [0, 0, -1],
        [1, 0, 0]
    ]),
    np.array([
        [-1, 0, 0],
        [0, 0, 1],
        [0, 1, 0]
    ]),
    np.array([
        [-1, 0, 0],
        [0, 0, -1],
        [0, -1, 0]
    ]),
    np.array([
        [0, -1, 0],
        [0, 0, 1],
        [-1, 0, 0]
    ]),
    np.array([
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0]
    ]),
    np.array([
        [0, 0, 1],
        [1, 0, 0],
        [0, -1, 0]
    ]),
    np.array([
        [0, 1, 0],
        [1, 0, 0],
        [0, 0, -1]
    ]),
]

class Scanner:
    def __init__(self, points):
        self.points = points

    def add_point(self, point):
        self.points.append(point)

# Parse inputs
input = open("input.txt", "r")
scanners = []
origins = []
for line in input.readlines():
    if re.match(r"--- scanner \d* ---\n", line) or line == "\n":
        scanners.append(Scanner([]))
    elif line == "\n":
        continue
    else:
        result = re.search(r"(-?\d*),(-?\d*),(-?\d*)", line)
        point = np.array([int(result[1]), int(result[2]), int(result[3])])

        scanners[-1].add_point(point)

scanners = list(filter(lambda x: len(x.points) > 0, scanners))
for i in range(len(scanners)):
    origins.append([np.array([0, 0, 0])])

while len(scanners) > 1:
    print("next")
    correct = list(map(lambda x: list(x), scanners.pop(0).points))
    correct_origin = origins.pop(0)
    any_overlap = True
    while any_overlap:
        print(" next")
        #print("scanners", len(scanners))
        any_overlap = False
        new_scanners = []
        new_origins = []

        for si in range(len(scanners)):
            scanner = scanners[si]
            origin = origins[si]
            found_overlap = False
            for rot in rotatations:
                rot_points = list(map(lambda x: rot.dot(x), scanner.points))
                for rot_point in rot_points:
                    for correct_list in correct:
                        trans = np.array(correct_list) - rot_point
                        trans_lists = list(map(lambda x: list(x + trans), rot_points))
                        #print(trans)

                        total_in = 0
                        for trans_list in trans_lists:
                            if trans_list in correct:
                                total_in += 1
                        
                        if total_in >= 12:
                            found_overlap = True
                            any_overlap = True
                            correct_origin.extend(list(map(lambda x: rot.dot(x) + trans, origin)))
                            for trans_list in trans_lists:
                                if trans_list not in correct:
                                    correct.append(trans_list)
                            break
                    if found_overlap:
                        break
                if found_overlap:
                    break
            if not found_overlap:
                new_scanners.append(scanner)
                new_origins.append(origin)
        
        scanners = new_scanners
        origins = new_origins
    scanners.append(
        Scanner(list(map(lambda x: np.array(x), correct)))
    )
    origins.append(
        correct_origin
    )

max_distance = 0
for point_1 in origins[0]:
    for point_2 in origins[0]:
        if np.array_equal(point_1, point_2):
            continue
        else:
            distance = abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1]) + abs(point_1[2] - point_2[2])
            if max_distance < distance:
                max_distance = distance

print(max_distance)
