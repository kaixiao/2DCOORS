from Ors2D import ORS2D
from veb import VEBTree
from Node import NodeItem, Node

# Naive in O(n)
# sort by x coordinate
# sort by x coordinate and y coordinate, and pick min via segment tree?
# if we have an implementation of simple 2D range trees log^2n

class NaiveStruct(ORS2D):
    def __init__(self, memory, points):
        self.memory = memory
        self.points = points
        nodes = 
        self.memory.add_array_to_disk(self.points)

    def query(self, x_min, x_max, y_min, y_max):
        solutions = []
        for i in range(len(disk)):
            point = next_thing.read() # a node

            if x_min <= p[0] and p[0] <= x_max and \
                y_min <= p[1] and p[1] <= y_max:
                solutions.append(p)
                self.memory.update_buffer()
        return solutions

class XBST(ORS2D):
    def __init__(self, memory, points, veb_order=False):
        # Use VeB tree for make_BST
        # if veb_order is False, store the nodes random order
        self.memory = memory
        self.points = points

    def query_xrange(x_min, x_max):
        pass

    def query(self, x_min, x_max, y_min, y_max):
        return None


class RangeTreeNode(VEBNode):
    def __init__(self, memory, node_item):
        VEBNode.__init__(self, memory, node_item)
        self.xbst = None

class RangeTree(ORS2D):
    def __init__(self, memory, points, veb_order=False):
        # if veb_order is False, store the nodes random order
        self.memory = memory
        self.points = points
        self.veb_order = veb_order

        node_items = [NodeItem(y, x) for x, y in points]
        self.ybst = VEBTree(node_items, data_at_leaves=True, veb_order=veb_order)
        self.link_nodes_to_XBST()

    def link_nodes_to_x_BST():
        if self.veb_order:
            nodes = self.ybst.veb_ordered.nodes
        else:
            nodes = self.ybst.nodes

        for node in nodes:
            points = [(v.data, v.key) for v in self.ybst.subtree(node, leaves=True)]
            node.xbst = XBST(self.memory, points, self.veb_order)

    def query(self, x_min, x_max, y_min, y_max):
        # path to pred of y_min
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



