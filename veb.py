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
        self._original = self 

    # Enforces access through the cache/disk model
    @property
    def left(self):
        if self._left is None:
            return None
        return self._left.read()
        self._left = node

    @property
    def right(self):
        if self._right is None:
            return None
        return self._right.read()

    @property
    def parent(self):
        if self._parent is None:
            return None
        return self._parent.read()

    @property
    def original(self):
        return self._original.read()

    def is_root(self):
        return self._parent is None

    def is_leaf(self):
        return self._left is None and self._right is None

    def point(self):
        raise Exception("Point not implemented.")

    def copy(self):
        return type(self)(self.memory, NodeItem(self.key, self.data))

    def __str__(self):
        return str(self.point())

    def __hash__(self):
        return hash(self.point())


class Node2Sided(VEBNode):
    """
    Extends VEBNode class to support xarray index
    """

    def __init__(self, memory, node_item):
        VEBNode.__init__(self, memory, node_item)
        self.xarray_index = None # index in xarray

    def point(self):
        return (self.data, self.key)


class Node3Sided(VEBNode):
    """
    Extends VEBNode class to support pointers to Coors2D2Sided objects
    """

    def __init__(self, memory, node_item):
        VEBNode.__init__(self, memory, node_item)
        self.x_upper_struct = None
        self.x_lower_struct = None

    def point(self):
        return (self.key, self.data)

class Node4Sided(VEBNode):
    """
    Similar to Node3Sided class
    """

    def __init__(self, memory, node_item):
        VEBNode.__init__(self, memory, node_item)
        self.y_upper_struct = None
        self.y_lower_struct = None

    def point(self):
        return (self.data, self.key)


class VEBTree(object):
    """
    VEB tree constructed from list of NodeItem objects and node builder function
    If data_at_leaves is True, each internal node stores the min of right subtree
    """
    def __init__(self, memory, node_items, node_builder=None, data_at_leaves=False, \
                 veb_order=True):
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

        if veb_order:
            self.memory.add_array_to_disk(self.veb_ordered_nodes)
        else:
            self.memory.add_array_to_disk(self.nodes)

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
            root._original = nodes[mid]
            self.nodes.append(root)
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

    def subtree(self, root, leaves=False):
        # used during preprocessing
        # returns list of leaves in a given subtree via BFS
        frontier = [root]
        res = []
        for node in frontier:
            if leaves and node.is_leaf() or not leaves:
                res.append(node)
            if node._left is not None:
                frontier.append(node._left)
            if node._right is not None:
                frontier.append(node._right)
        return res

    def find_in_subtree(self, root, key, data):
        curr = root
        while not curr.is_leaf():
            if key > curr.key:
                curr = curr._right
            elif key < curr.key:
                curr = curr._left
            else:
                if data == curr.data:
                    return curr._original
                else:
                    return self.find_in_subtree(curr._left, key, data) or \
                           self.find_in_subtree(curr._right, key, data)
        if key == curr.key and data == curr.data:
            return curr
        return None

    def predecessor(self, key):
        # NOTE: algorithm assumes O(1) extra space in cache to store candidate
        # start search from root, returns searched node
        # memory transfers from reading nodes are accounted for by VEBNode class
        # note that internal stores store min of right subtree if data_at_leaves

        candidate = None
        current_node = self.root
        while current_node is not None:
            if key >= current_node.key:
                if candidate is None or current_node.key >= candidate.key:
                    candidate = current_node
                current_node = current_node.right
            else:
                current_node = current_node.left

        # kind of hacky way of doing predecessor when data_at_leaves is True
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
                # technically should traverse right in equality case if data_at_leaves
                # but correctness is taken care of by candidate variable
                if candidate is None or current_node.key <= candidate.key:
                    candidate = current_node
                current_node = current_node.left
            else:
                current_node = current_node.right
        if self.data_at_leaves and candidate is not None:
            candidate = candidate.original
        return candidate

    def fast_LCA(self, key_min, key_max):
        # does pred/succ search with LCA together
        # only makes sense when data_at_leaves is True
        assert self.data_at_leaves and key_min <= key_max
        
        current_node = self.root
        while not current_node.is_leaf():
            if key_min < current_node.key <= key_max:
                break
            elif key_min >= current_node.key:
                current_node = current_node.right 
            else:
                current_node = current_node.left
        return current_node

    @property
    def root(self):
        r = self._root.read()
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

