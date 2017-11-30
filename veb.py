# Assumes each node + all its fields are stored in one memory cell
import math
from Node import Node, NodeItem


class VEBNode(Node):
    """
    Supports basic node features key, data, left, right, parent, depth
    Augmented with external memory model support when accessing fields
    Assumes every node + all its fields take up one memory slot in our model
    """
    def __init__(self, memory, node_item):
        # Constructor takes in NodeItem object
        Node.__init__(self, memory, node_item)
        self._left = None
        self._right = None
        self._parent = None
        self._depth = None
        self.original = self # pointer to original copy, applicable when data at disk

    @property
    def left(self):
        # Enforces access through the cache/disk model
        if self._left is None:
            return None
        return self._left.read()

    @left.setter
    def left(self, node):
        # dynamic updates not supported yet
        raise Exception("Writes not supported yet")
        self._left = node

    @property
    def right(self):
        if self._right is None:
            return None
        return self._right.read()

    @right.setter
    def right(self, node):
        raise Exception("Writes not supported yet")
        self._right = node

    @property
    def parent(self):
        if self._parent is None:
            return None
        return self._parent.read()

    @parent.setter
    def parent(self, node):
        raise Exception("Writes not supported yet")
        self._parent = node

    def is_root(self):
        return self._parent is None

    def is_leaf(self):
        return self._left is None and self._right is None

    def tuple(self):
        return (self.key, self.data)

    def copy(self):
        return type(self)(self.memory, NodeItem(self.key, self.data))

    def __str__(self):
        return str((self.key, self.data))

    def __hash__(self):
        return hash((self.key, self.data))


class Node2Sided(VEBNode):
    """
    Extends VEBNode class to support xarray index
    """

    def __init__(self, memory, node_item):
        VEBNode.__init__(self, memory, node_item)
        self.xarray_index = None # index in xarray


class Node3Sided(VEBNode):
    """
    Extends VEBNode class to support pointers to Coors2D2Sided objects
    """

    def __init__(self, memory, node_item):
        VEBNode.__init__(self, memory, node_item)
        self.x_upper_struct = None
        self.x_lower_struct = None


class Node4Sided(VEBNode):
    """
    Similar to Node3Sided class
    """

    def __init__(self, memory, node_item):
        VEBNode.__init__(self, memory, node_item)
        self.y_upper_struct = None
        self.y_lower_struct = None


class VEBTree(object):

    def __init__(self, memory, node_items, node_builder=None, data_at_leaves=False):
        """
        VEB tree constructed from list of NodeItem objects and node builder function
        Directly integrated with external memory module
        If data_at_leaves, each internal node stores the min of right subtree
        """
        assert len(node_items) > 0

        if node_builder is None:
            self.node_builder = VEBNode
        else:
            self.node_builder = node_builder
        self.data_at_leaves = data_at_leaves
        
        self.memory = memory
        self.nodes = [node_builder(memory, x) for x in node_items]
        self._root = self.make_BST(self.nodes, self.data_at_leaves)

        max_depth = int(math.log(len(node_items), 2) + data_at_leaves)
        self.veb_ordered_nodes = self.make_veb_order(self._root, max_depth)
        self.initialize_node_back_pointers(self.veb_ordered_nodes)

        self.offset = memory.add_array_to_disk(self.veb_ordered_nodes)

    def make_BST(self, nodes, data_at_leaves, parent=None, srted=False):
        # make a perfect BST from a list of NodeItems
        # initializes depth of each node
        # returns root node of BST
        if not srted:
            nodes.sort(key=lambda x: x.key)

        mid = len(nodes) // 2
        if len(nodes) == 1:
            left_nodes = []
            right_nodes = []
            root = nodes[0]
        elif data_at_leaves:
            left_nodes = nodes[:mid]
            right_nodes = nodes[mid:]
            root = nodes[mid].copy()
            root.original = nodes[mid]
        else:
            left_nodes = nodes[:mid]
            right_nodes = nodes[mid+1:]
            root = nodes[mid]

        root._parent = parent
        if parent is None:
            root._depth = 0
        else:
            root._depth = parent._depth + 1

        if len(left_nodes):
            root._left = self.make_BST(left_nodes, data_at_leaves, root, True)

        if len(right_nodes):
            root._right = self.make_BST(right_nodes, data_at_leaves, root, True)

        return root

    def make_veb_order(self, start, depth):
        # given a starting node and max exploration depth, return
        # the list of nodes in the subtree in VEB order
        if depth == 0:
            return [start]

        lower_depth = depth // 2
        upper_depth = depth - lower_depth - 1

        depth_cutoff = start._depth + upper_depth
        frontier = [start]
        recurse_nodes = []

        for node in frontier:
            if node._depth == depth_cutoff + 1:
                recurse_nodes.append(node)
            if node._depth > depth_cutoff + 1:
                break
            if node._left is not None:
                frontier.append(node._left)
            if node._right is not None:
                frontier.append(node._right)

        veb_order = self.make_veb_order(start, upper_depth)
        for node in recurse_nodes:
            veb_order += self.make_veb_order(node, lower_depth)

        return veb_order

    def initialize_node_back_pointers(self, nodes):
        # iterates through veb_ordered_nodes to set veb_index of each node
        for i, node in enumerate(nodes):
            node.veb_index = i
            node.veb = self

    def initialize_node_memory_pointer(self, nodes):
        for node in nodes:
            node.memory = self.memory

    def subtree_leaves(self, root):
        # returns list of leaves in a given subtree via BFS
        frontier = [root]
        res = []
        for node in frontier:
            if node.is_leaf():
                res.append(node)
            if node._left is not None:
                frontier.append(node._left)
            if node._right is not None:
                frontier.append(node._right)
        return res

    def predecessor(self, key):
        # start search from root, returns searched node
        # assumes O(1) extra space in cache
        # memory transfers from reading nodes are accounted for by VEBNode class
        candidate = None
        current_node = self.root
        while current_node is not None:
            if key >= current_node.key:
                if candidate is None or current_node.key >= candidate.key:
                    candidate = current_node
                current_node = current_node.right
            else:
                current_node = current_node.left
        if self.data_at_leaves and candidate is not None:
            candidate = candidate.original
            assert candidate.is_leaf()
        return candidate

    def successor(self, key):
        # symmetric to predecessor
        candidate = None
        current_node = self.root
        while current_node is not None:
            if key <= current_node.key:
                if candidate is None or current_node.key <= candidate.key:
                    candidate = current_node
                current_node = current_node.left
            else:
                current_node = current_node.right
        if self.data_at_leaves and candidate is not None:
            candidate = candidate.original
        return candidate

    def LCA(self, node_1, node_2):
        # we'll do lca naively in O(log n) instead of O(1)
        visited = set()
        while node_1 is not None or node_2 is not None:
            # print('node_1, node_2:', node_1, node_2)
            if node_1 in visited:
                return node_1
            else:
                visited.add(node_1)
            if node_2 in visited:
                return node_2
            else:
                visited.add(node_2)
            node_1 = node_1.parent
            node_2 = node_2.parent
            # print('node_1, node_2:', node_1, node_2)
        raise Exception('Did not find LCA.')

    @property
    def root(self):
        r = self.memory.read(self.offset)
        assert self._root == r
        return r

    def __str__(self):
        return str(veb_ordered_nodes)


class VEB2Sided(VEBTree):
    """
    Constructed from list of NodeItem objects
    """
    def __init__(self, memory, node_items):
        VEBTree.__init__(self, memory, node_items, Node2Sided, data_at_leaves=False)


class VEB3Sided(VEBTree):

    def __init__(self, memory, node_items):
        VEBTree.__init__(self, memory, node_items, Node3Sided, data_at_leaves=True)

class VEB4Sided(VEBTree):

    def __init__(self, memory, node_items):
        VEBTree.__init__(self, memory, node_items, Node4Sided, data_at_leaves=True)

