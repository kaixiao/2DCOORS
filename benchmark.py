from Ors2D import ORS2D
from Node import Node, NodeItem
from veb import VEBNode, VEBTree
# Naive in O(n)
# sort by x coordinate
# if we have an implementation of simple 2D range trees log^2n

x_coord = lambda x: x[0]
y_coord = lambda x: x[1]


class NaiveStruct(ORS2D):
    def __init__(self, memory, points):
        self.memory = memory
        self.points = points
        self.nodes = [Node(self.memory, NodeItem(point)) for point in self.points]
        self.memory.add_array_to_disk(self.nodes)

    def query(self, x_min, x_max, y_min, y_max):
        solutions = []
        for i in range(len(self.nodes)):
            p = self.nodes[i].read().key # a node
            if x_min <= p[0] and p[0] <= x_max and \
                y_min <= p[1] and p[1] <= y_max:
                solutions.append(p)
        return solutions

class SortedXVEBTree(ORS2D):
    def __init__(self, memory, points):

        self.memory = memory
        self.points = sorted(points, key=x_coord)
        node_items = [NodeItem(x, y) for x, y in self.points]
        self.tree = VEBTree(self.memory, node_items, VEBNode)

    def query(self, x_min, x_max, y_min, y_max):
        solutions = []

        current_node = self.tree.successor(x_min)
        if current_node is None:
            return solutions
        x = current_node.read().key
        y = current_node.read().data

        while x <= x_max:
            if x_min <= x and x <= x_max and \
                y_min <= y and y <= y_max:
                solutions.append((x,y))
            current_node = current_node.right

            if current_node is None:
                return solutions
            x = current_node.read().key
            y = current_node.read().data

        return solutions


class SimpleRangeTree(ORS2D):
    def __init__(self, memory, points):
        self.memory = memory
        self.points = points

    def query(self, x_min, x_max, y_min, y_max):
        return None


