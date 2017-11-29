# Assumes each node + all its fields are stored in one memory cell
import math

class VEBTree(object):

    def __init__(self, nodes):
        """
        Vanilla VEB tree constructed from list of Node objects
        """
        assert len(nodes) > 0

        self._root = self.make_BST(nodes)
        max_depth = int(math.log(len(nodes), 2))
        self.veb_ordered_nodes = self.make_veb_order(self._root, max_depth)
        self.initialize_node_back_pointers(self.veb_ordered_nodes)

    def make_BST(self, nodes, parent=None, srted=False):
        # make a perfect BST from a list of NodeItems
        # initializes depth of each node
        # returns root node of BST
        if not srted:
            nodes.sort(key=lambda x: x.key)

        mid = len(nodes) // 2
        left_items = nodes[:mid]
        right_items = nodes[mid+1:]

        root = nodes[mid]
        root._parent = parent
        if parent is None:
            root._depth = 0
        else:
            root._depth = parent._depth + 1

        if len(left_items):
            root._left = self.make_BST(left_items, root, True)
            root._left._parent = root
            root._left._depth = root._depth + 1

        if len(right_items):
            root._right = self.make_BST(right_items, root, True)
            root._right._parent = root
            root._right._depth = root._depth + 1

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

    def predecessor(self, key):
        # start search from root, returns searched node
        # memory transfers from reading nodes are accounted for by Node class
        candidate = None
        current_node = self.root
        while current_node is not None:
            if key == current_node.key:
                return current_node
            elif key > current_node.key:
                if candidate is None:
                    candidate = current_node
                else:
                    if candidate.key < current_node.key:
                        candidate = current_node
                current_node = current_node.right
            elif key < current_node.key:
                current_node = current_node.left
        return candidate

    def successor(self, key):
        # similar to predecessor
        candidate = None
        current_node = self.root
        while current_node is not None:
            if key == current_node.key:
                return current_node
            elif key < current_node.key:
                if candidate is None:
                    candidate = current_node
                else:
                    if candidate.key > current_node.key:
                        candidate = current_node
                current_node = current_node.left
            elif key > current_node.key:
                current_node = current_node.right
        return candidate

    def __str__(self):
        return str(veb_ordered_nodes)


class VEB2Sided(VEBTree):

    def __init__(self, memory, node_items):
        VEBTree.__init__(self, self.make_nodes(node_items))
        self.memory = memory
        self.offset = memory.add_array_to_disk(self.veb_ordered_nodes)
        self.initialize_node_memory_pointer(self.veb_ordered_nodes)

    def make_nodes(self, node_items):
        return [Node2Sided(x) for x in node_items]

    def initialize_node_memory_pointer(self, nodes):
        for node in nodes:
            node.memory = self.memory

    @property
    def root(self):
        r = self.memory.read(self.offset)
        assert self._root == r
        return r


class NodeItem(object):

    def __init__(self, key, data):
        self.key = key
        self.data = data

    def __str__(self):
        return str((self.key, self.data))

class Node(object):
    
    def __init__(self, node_item):
        # Constructor takes in NodeItem object
        self.key = node_item.key
        self.data = node_item.data
        self._left = None
        self._right = None
        self._parent = None
        self._depth = None

    def is_root(self):
        return self._parent is None

    def is_leaf(self):
        return self._left is None and self._right is None

    def __str__(self):
        return str((self.key, self.data))

class Node2Sided(Node):
    """
    Extends Node class to support veb_index, xarray_index, veb, memory
    Assumes every node + all its fields take up one memory slot in our model
    """

    def __init__(self, node_item):
        Node.__init__(self, node_item)
        self.xarray_index = None # index in xarray
        self.veb_index = None # index in VEB order
        self.veb = None # pointer to veb object it belongs to
        self.memory = None # pointer to memory structure

    def read(self):
        # accesses self through memory model
        return self.memory.read(self.veb.offset + self.veb_index)

    @property
    def left(self):
        # Enforces access through the cache/disk model
        if self._left is None:
            return None
        return self._left.read()

    @left.setter
    def left(self, node):
        # dynamic updates not supported yet
        self._left = node

    @property
    def right(self):
        if self._right is None:
            return None
        return self._right.read()

    @right.setter
    def right(self, node):
        self._right = node

    @property
    def parent(self):
        if self._parent is None:
            return None
        return self._parent.read()

    @parent.setter
    def parent(self, node):
        self._parent = node

