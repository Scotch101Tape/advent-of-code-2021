from functools import reduce
import math

def parse(i):
    if isinstance(i, list):
        node = Node()

        l = parse(i[0])
        r = parse(i[1])

        node.add_items(l, r)
        l.add_parent(node)
        r.add_parent(node)

        return node
    elif isinstance(i, int):
        return End(i)
    elif isinstance(i, str):
        # Very evil
        return parse(eval(i))

class Item:
    def nested(self):
        nested = 0
        parent = self.parent
        while parent is not None:
            nested += 1
            parent = parent.parent
        return nested

    def top(self):
        parent = self
        while parent.parent:
            parent = parent.parent
        return parent

class End(Item):
    def __init__(self, value):
        self.value = value

    def add_parent(self, parent):
        self.parent = parent

    def __str__(self):
        return f"V{self.value}"

    def split(self):
        #print(f"splitting {self}")

        node = Node()
        node.add_parent(self.parent)

        l = End(math.floor(self.value / 2))
        r = End(math.ceil(self.value / 2))

        node.add_items(l, r)
        l.add_parent(node)
        r.add_parent(node)

        if self.parent.l == self:
            self.parent.l = node
        else:
            self.parent.r = node

        #print(f"After Split {self.top()}")

    def reduce_split(self):
        if self.should_split():
            self.split()
            return True
        return False
        
    def reduce_explode(self):
        return False

    def should_split(self):
        return self.value >= 10

    def magnitude(self):
        return self.value

class Node(Item):
    def __init__(self):
        self.parent = None

    def add_items(self, l, r):
        self.l = l
        self.r = r

    def add_parent(self, parent):
        self.parent = parent

    def __str__(self):
        return f"[{str(self.l)}, {str(self.r)}]"

    def magnitude(self):
        return self.l.magnitude() * 3 + self.r.magnitude() * 2

    def reduce_explode(self):
        if self.parent is not None:
            if self.should_explode():
                self.explode()
                return True

            return self.l.reduce_explode() or self.r.reduce_explode()

    def reduce_split(self):
        return self.l.reduce_split() or self.r.reduce_split()

    def reduce(self):
        if self.parent is None:
            while self.l.reduce_explode() or self.r.reduce_explode() or self.l.reduce_split() or self.r.reduce_split():
                pass
            return self

    def __add__(self, other):
        node = Node()

        node.add_items(self, other)
        self.add_parent(node)
        other.add_parent(node)

        #print(f"plain node {node}")

        node.reduce()

        return node

    def should_explode(self):
        return self.nested() >= 4

    def explode(self):
        #print(f"exploding {self}")
        l_parent = self
        l_down = None
        while l_parent.parent is not None:
            if l_parent.parent.l == l_parent:
                l_parent = l_parent.parent
            else:
                l_down = l_parent.parent.l
                while isinstance(l_down, Node):
                    l_down = l_down.r
                break
        
        r_parent = self
        r_down = None
        while r_parent.parent is not None:
            if r_parent.parent.r == r_parent:
                r_parent = r_parent.parent
            else:
                r_down = r_parent.parent.r
                while isinstance(r_down, Node):
                    r_down = r_down.l
                break

        if l_down is not None:
            #print(f"l_down {l_down}")
            l_down.value += self.l.value

        if r_down is not None:
            #print(f"r_down {r_down}")
            r_down.value += self.r.value

        # Replace yourself with 0
        end = End(0)
        end.add_parent(self.parent)

        if self.parent.l == self:
            self.parent.l = end
        else:
            self.parent.r = end

        #print(f"after explode {self.top()}")

# Parse input
input = open("input.txt", "r")
nodes = []
for line in input.readlines():
    nodes.append(parse(line))

# Now add all the lines
node_sum = reduce(lambda a, b: a + b, nodes)

# Print the magnitude
print(node_sum.magnitude())