from os import path
import re

class Graph:
    def __init__(self, nodes):
        self.nodes = nodes

#    def copy(self):
#        new_nodes = []
#        for node in self.nodes:
#            new_nodes.append(Node(node.value, node.final_value))#
#
#        for i in range(len(new_nodes)):
#            new_node = new_nodes[i]
#            node = self.nodes[i]
#
#
#
#        return Graph(new_nodes)

class Connection:
    def __init__(self, path):
        self.path = path

    def total(self):
        return len(self.path) - 1

    def start(self):
        return self.path[0]

    def end(self):
        return self.path[-1]

class Node:
    def __init__(self, value, final_value):
        self.value = value
        self.final_value = final_value
        self.nodes = []

    def connect(self, node):
        self.nodes.append(node)

    def all_connections(self, path = []):
        connections = [Connection(path + [self])]
        for node in self.nodes:
            if node not in path:
                connections.extend(node.all_connections(path + [self]))
        return connections

    def __str__(self):
        return self.value if self.value is not None else "."

# Immutable slice of heaven
class Board:
    fish_cost = {
        "A": 1,
        "B": 10,
        "C": 100,
        "D": 1000
    }

    def __init__(self, graph, total):
        self.graph = graph
        self.total = total

    def __str__(self):
        return f"""
#############
#{self.graph.nodes[0]}{self.graph.nodes[1]}{self.graph.nodes[2]}{self.graph.nodes[3]}{self.graph.nodes[4]}{self.graph.nodes[5]}{self.graph.nodes[6]}{self.graph.nodes[7]}{self.graph.nodes[8]}{self.graph.nodes[9]}{self.graph.nodes[10]}#
###{self.graph.nodes[11]}#{self.graph.nodes[15]}#{self.graph.nodes[19]}#{self.graph.nodes[23]}###
  #{self.graph.nodes[12]}#{self.graph.nodes[16]}#{self.graph.nodes[20]}#{self.graph.nodes[24]}#
  #{self.graph.nodes[13]}#{self.graph.nodes[17]}#{self.graph.nodes[21]}#{self.graph.nodes[25]}#
  #{self.graph.nodes[14]}#{self.graph.nodes[18]}#{self.graph.nodes[22]}#{self.graph.nodes[26]}#
  #########"""

    # This is not nessicarily the correct usage of hash, but...
    def hash_positions(self):
        return hash(tuple(map(lambda x: x.value, self.graph.nodes)))

    def valid_moves(self):
        moves = []
        fish_nodes = list(filter(lambda x: x.value is not None and (len(list(filter(lambda y: y.value is not None and y.value != x.value, x.nodes))) != 0 if x.final_value == x.value else True), self.graph.nodes))
        for fish in fish_nodes:
            valid_connections = list(
                filter(lambda x: (True if len(x.end().nodes) == 1 else len(list(filter(lambda y: y.value is not None, x.end().nodes))) == 1) if fish.value == x.end().final_value else True,
                filter(lambda x: x.end() != fish,
                filter(lambda x: len(x.end().nodes) != 3,
                filter(lambda x: x.end().final_value is None or x.end().final_value == fish.value,
                filter(lambda x: len(list(filter(lambda y: y.value is not None and y.value != fish.value, x.end().nodes))) == 0 if x.end().final_value == fish.value else True,
                filter(lambda x: x.end().final_value is not None if x.start().final_value is None else True,
                filter(lambda x: len(list(filter(lambda y: y.value is not None, x.path))) == 1,
                fish.all_connections()
            ))))))))

            for connection in valid_connections:
                new_board = self.copy()
                new_board.total += connection.total() * Board.fish_cost[fish.value]
                end_index = self.graph.nodes.index(connection.end())
                start_index = self.graph.nodes.index(connection.start())

                new_board.graph.nodes[end_index].value = fish.value
                new_board.graph.nodes[start_index].value = None

                moves.append(new_board)

        return moves

    def from_fish(fish):
        nodes = []
        for i in range(11):
            nodes.append(Node(None, None))

        for i in range(len(nodes)):
            node = nodes[i]
            if i - 1 >= 0:
                node.connect(nodes[i - 1])
            
            if i + 1 < len(nodes):
                node.connect(nodes[i + 1])

        nodes.append(Node(fish[0], "A"))
        nodes.append(Node(fish[4], "A"))
        nodes.append(Node(fish[8], "A"))
        nodes.append(Node(fish[12], "A"))
        nodes[-4].connect(nodes[2])
        nodes[2].connect(nodes[-4])
        nodes[-4].connect(nodes[-3])
        nodes[-3].connect(nodes[-4])
        nodes[-3].connect(nodes[-2])
        nodes[-2].connect(nodes[-3])
        nodes[-2].connect(nodes[-1])
        nodes[-1].connect(nodes[-2])

        nodes.append(Node(fish[1], "B"))
        nodes.append(Node(fish[5], "B"))
        nodes.append(Node(fish[9], "B"))
        nodes.append(Node(fish[13], "B"))
        nodes[-4].connect(nodes[4])
        nodes[4].connect(nodes[-4])
        nodes[-4].connect(nodes[-3])
        nodes[-3].connect(nodes[-4])
        nodes[-3].connect(nodes[-2])
        nodes[-2].connect(nodes[-3])
        nodes[-2].connect(nodes[-1])
        nodes[-1].connect(nodes[-2])

        nodes.append(Node(fish[2], "C"))
        nodes.append(Node(fish[6], "C"))
        nodes.append(Node(fish[10], "C"))
        nodes.append(Node(fish[14], "C"))
        nodes[-4].connect(nodes[6])
        nodes[6].connect(nodes[-4])
        nodes[-4].connect(nodes[-3])
        nodes[-3].connect(nodes[-4])
        nodes[-3].connect(nodes[-2])
        nodes[-2].connect(nodes[-3])
        nodes[-2].connect(nodes[-1])
        nodes[-1].connect(nodes[-2])

        nodes.append(Node(fish[3], "D"))
        nodes.append(Node(fish[7], "D"))
        nodes.append(Node(fish[11], "D"))
        nodes.append(Node(fish[15], "D"))
        nodes[-4].connect(nodes[8])
        nodes[8].connect(nodes[-4])
        nodes[-4].connect(nodes[-3])
        nodes[-3].connect(nodes[-4])
        nodes[-3].connect(nodes[-2])
        nodes[-2].connect(nodes[-3])
        nodes[-2].connect(nodes[-1])
        nodes[-1].connect(nodes[-2])

        return Board(Graph(nodes), 0)

    def copy(self):
        nodes = []
        for i in range(11):
            nodes.append(Node(None, None))

        for i in range(len(nodes)):
            node = nodes[i]
            if i - 1 >= 0:
                node.connect(nodes[i - 1])
            
            if i + 1 < len(nodes):
                node.connect(nodes[i + 1])

        nodes.append(Node(None, "A"))
        nodes.append(Node(None, "A"))
        nodes.append(Node(None, "A"))
        nodes.append(Node(None, "A"))
        nodes[-4].connect(nodes[2])
        nodes[2].connect(nodes[-4])
        nodes[-4].connect(nodes[-3])
        nodes[-3].connect(nodes[-4])
        nodes[-3].connect(nodes[-2])
        nodes[-2].connect(nodes[-3])
        nodes[-2].connect(nodes[-1])
        nodes[-1].connect(nodes[-2])

        nodes.append(Node(None, "B"))
        nodes.append(Node(None, "B"))
        nodes.append(Node(None, "B"))
        nodes.append(Node(None, "B"))
        nodes[-4].connect(nodes[4])
        nodes[4].connect(nodes[-4])
        nodes[-4].connect(nodes[-3])
        nodes[-3].connect(nodes[-4])
        nodes[-3].connect(nodes[-2])
        nodes[-2].connect(nodes[-3])
        nodes[-2].connect(nodes[-1])
        nodes[-1].connect(nodes[-2])

        nodes.append(Node(None, "C"))
        nodes.append(Node(None, "C"))
        nodes.append(Node(None, "C"))
        nodes.append(Node(None, "C"))
        nodes[-4].connect(nodes[6])
        nodes[6].connect(nodes[-4])
        nodes[-4].connect(nodes[-3])
        nodes[-3].connect(nodes[-4])
        nodes[-3].connect(nodes[-2])
        nodes[-2].connect(nodes[-3])
        nodes[-2].connect(nodes[-1])
        nodes[-1].connect(nodes[-2])

        nodes.append(Node(None, "D"))
        nodes.append(Node(None, "D"))
        nodes.append(Node(None, "D"))
        nodes.append(Node(None, "D"))
        nodes[-4].connect(nodes[8])
        nodes[8].connect(nodes[-4])
        nodes[-4].connect(nodes[-3])
        nodes[-3].connect(nodes[-4])
        nodes[-3].connect(nodes[-2])
        nodes[-2].connect(nodes[-3])
        nodes[-2].connect(nodes[-1])
        nodes[-1].connect(nodes[-2])

        for i in range(len(self.graph.nodes)):
            nodes[i].value = self.graph.nodes[i].value

        return Board(Graph(nodes), self.total)

        

# Parse input
result = re.search(r"#############\n#...........#\n###(A|B|C|D)#(A|B|C|D)#(A|B|C|D)#(A|B|C|D)###\n  #(A|B|C|D)#(A|B|C|D)#(A|B|C|D)#(A|B|C|D)#\n  #(A|B|C|D)#(A|B|C|D)#(A|B|C|D)#(A|B|C|D)#\n  #(A|B|C|D)#(A|B|C|D)#(A|B|C|D)#(A|B|C|D)#\n  #########", """
#############
#...........#
###B#A#B#C###
  #D#C#B#A#
  #D#B#A#C#
  #C#D#D#A#
  #########
""")

fish = []
for i in range(16):
    fish.append(result[i + 1])
start_board = Board.from_fish(fish)

fastest_boards = {
    start_board.hash_positions(): 0
}
boards = [start_board]

goal_board = Board.from_fish(["A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D"])

thing_i = 0
while len(boards) > 0:
    thing_i += 1
    new_boards = []
    for board in boards:
        new_boards_soon = list(filter(lambda x: fastest_boards[x.hash_positions()] > x.total if x.hash_positions() in fastest_boards else True,
            board.valid_moves()))

        for new_board in new_boards_soon:
            fastest_boards[new_board.hash_positions()] = new_board.total

        new_boards.extend(new_boards_soon)

    boards = new_boards

print()
print(fastest_boards[goal_board.hash_positions()])

