from Ors2D import ORS2D
from veb import VEBTree
from Node import NodeItem, Node

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
                self.memory.update_buffer()
        return solutions

class XBSTNode(VEBNode):
    def __init__(self, memory, node_item):
        VEBNode.__init__(self, memory, node_item)
        self._next = None

    @property
    def next(self):
        return self._next.read()


class XBST(ORS2D):
    def __init__(self, memory, points, veb_order):
        # if veb_order is False, store points in sorted order 

        self.memory = memory
        self.points = sorted(points, key=x_coord)
        self.veb_order = veb_order
        node_items = [NodeItem(x, y) for x, y in self.points]
        self.tree = VEBTree(self.memory, node_items, XBSTNode, veb_order=veb_order)
        self.link_sorted_nodes()

    def link_sorted_nodes(self):
        # initializes next pointers in XBSTNode objects
        prev = None
        for node in self.tree.nodes:
            if prev is not None:
                assert prev.key <= node.key
                prev._next = node
            prev = node

    def query(self, x_min, x_max, y_min, y_max):
        solutions = []
        current_node = self.tree.successor(x_min)
        if current_node is None:
            return solutions
        x, y = current_node.point()

        while x <= x_max and current_node is not None:
            if y_min <= y <= y_max:
                solutions.append((x, y))
            current_node = current_node.next
            x, y = current_node.point()

        return solutions


class RangeTreeNode(VEBNode):
    def __init__(self, memory, node_item):
        VEBNode.__init__(self, memory, node_item)
        self.xbst = None


class RangeTree(ORS2D):
    def __init__(self, memory, points, veb_order):
        self.memory = memory
        self.points = points
        self.veb_order = veb_order

        node_items = [NodeItem(y, x) for x, y in points]
        self.ybst = VEBTree(node_items, data_at_leaves=True, veb_order=veb_order)
        self.link_nodes_to_XBST()

    def link_nodes_to_XBST():
        if self.veb_order:
            nodes = self.ybst.veb_ordered.nodes
        else:
            nodes = self.ybst.nodes

        for node in nodes:
            points = [(v.data, v.key) for v in self.ybst.subtree(node, leaves=True)]
            node.xbst = XBST(self.memory, points, self.veb_order)

    def query(self, x_min, x_max, y_min, y_max):
        solutions = []
        curr_left = curr_right = self.ybst.root
        split = False

        while curr_left is not None:
            if curr_left.key <= y_min:
                curr_left = curr_left.right
                if split:
                    solutions.extend(curr_left.right.xbst.query(
                                                x_min, x_max, y_min, y_max))
            else:
                curr_left = curr_left.left

            if curr_right.key > y_max:
                curr_right = curr_right.left
                if split:
                    solutions.extend(curr_right.left.xbst.query(
                                                x_min, x_max, y_min, y_max))
            else:
                curr_right = curr_right.right

            if not split and not curr_left == curr_right:
                split = True

        assert curr_right is None
        return solutions

