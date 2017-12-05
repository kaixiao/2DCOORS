from veb import VEBTree, VEBNode
from Node import NodeItem, Node
from Ors2D import ORS2D
from Coors2D import COORS2D4Sided

# Naive in O(n)
# BST sorted by x coordinate
# simple 2D range trees with O(log^2n) query

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
            if x_min <= p[0] <= x_max and y_min <= p[1] <= y_max:
                solutions.append(p)
                self.memory.update_buffer()
        return solutions


class XLinkedListNode(Node):
    def __init__(self, memory, node_item):
        Node.__init__(self, memory, node_item)
        self._next = None

    def point(self):
        return (self.key, self.data)

    @property
    def next(self):
        if self._next is None:
            return None
        return self._next.read()


class XLinkedList(object):
    def __init__(self, memory, points):
        self.memory = memory
        self.points = sorted(points, key=x_coord)
        self.nodes = [XLinkedListNode(memory, NodeItem(*p)) \
                      for p in self.points]
        self.link_nodes()
        self.memory.add_array_to_disk(self.nodes)

    def link_nodes(self):
        prev = None
        for node in self.nodes:
            if prev is not None:
                prev._next = node
            prev = node


class XBSTNode(VEBNode):
    def __init__(self, memory, node_item):
        VEBNode.__init__(self, memory, node_item)
        self.linked_list_copy = None

    def point(self):
        return (self.key, self.data)


class XBST(ORS2D):
    def __init__(self, memory, points, veb_order=True):
        # if veb_order is True, store points in veb order
        # else store in sorted order

        self.memory = memory
        self.points = sorted(points, key=x_coord)
        self.veb_order = veb_order
        node_items = [NodeItem(x, y) for x, y in self.points]
        self.tree = VEBTree(self.memory, node_items, XBSTNode, 
                            data_at_leaves=False, veb_order=veb_order)
        self.linked_list = XLinkedList(memory, points)
        self.link_tree_to_linked_list()

    def link_tree_to_linked_list(self):
        for list_node in self.linked_list.nodes:
            tree_node = self.tree.find_in_subtree(self.tree._root, list_node.key,
                                                  list_node.data)
            tree_node.linked_list_copy = list_node

    def query(self, x_min, x_max, y_min, y_max):
        solutions = []
        curr = self.tree.successor(x_min)
        if curr is None:
            return solutions
        else:
            curr = curr.linked_list_copy

        while curr is not None and curr.key <= x_max:
            if y_min <= curr.data <= y_max:
                solutions.append(curr.point())
                self.memory.update_buffer()
            curr = curr.next

        return solutions


class RangeTreeNode(VEBNode):
    def __init__(self, memory, node_item):
        VEBNode.__init__(self, memory, node_item)
        self.xbst = None

    def point(self):
        return (self.data, self.key)


class RangeTree(ORS2D):
    def __init__(self, memory, points, veb_order=True):
        self.memory = memory
        self.points = points
        self.veb_order = veb_order

        node_items = [NodeItem(y, x) for x, y in points]
        self.ybst = VEBTree(memory, node_items, RangeTreeNode, data_at_leaves=True, 
                            veb_order=veb_order)
        self.link_nodes_to_XBST()

    def link_nodes_to_XBST(self):
        if self.veb_order:
            nodes = self.ybst.veb_ordered_nodes
        else:
            nodes = self.ybst.nodes

        for node in nodes:
            points = [(v.data, v.key) for v in self.ybst.subtree(node, leaves=True)]
            node.xbst = XBST(self.memory, points, self.veb_order)

    def query(self, x_min, x_max, y_min, y_max):
        solutions = []
        curr_left = curr_right = self.ybst.root
        split = False

        while not curr_left.is_leaf() or not curr_right.is_leaf():
            if not curr_left.is_leaf():
                if curr_left.key <= y_min:
                    curr_left = curr_left.right
                else:
                    if split and curr_left.right is not None:
                        solutions.extend(
                            curr_left.right.xbst.query(x_min, x_max, y_min, y_max))
                    curr_left = curr_left.left

            if not curr_right.is_leaf():
                if curr_right.key > y_max:
                    curr_right = curr_right.left
                else:
                    if split and curr_right.left is not None:
                        solutions.extend(
                            curr_right.left.xbst.query(x_min, x_max, y_min, y_max))
                    curr_right = curr_right.right

            if not split and not curr_left == curr_right:
                split = True

        solutions.extend(curr_left.xbst.query(x_min, x_max, y_min, y_max))
        solutions.extend(curr_right.xbst.query(x_min, x_max, y_min, y_max))

        return solutions


class Coors(COORS2D4Sided):
    def __init__(self, memory, points):
        COORS2D4Sided.__init__(self, memory, points)

