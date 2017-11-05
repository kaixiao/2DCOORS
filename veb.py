# Assumes each node + all its fields are stored in one memory slot
import math

class VEBTree(object):

    def __init__(self, node_items):
        # Takes in a nonempty list of NodeItems
        assert len(node_items) > 0

        self.root = self.make_BST(node_items)
        max_depth = int(math.log(len(node_items), 2))
        self.veb_ordered_nodes = self.make_veb_order(self.root, max_depth)
        self.set_veb_indices()

    def make_BST(self, node_items, parent=None, unsorted=True):
        # make a perfect BST from a list of NodeItems
        # returns root node of BST
        if unsorted:
            node_items.sort(key=lambda z: z.key)

        mid = len(node_items) // 2
        left_items = node_items[:mid]
        right_items = node_items[mid+1:]

        root = Node(node_items[mid])
        root.parent = parent
        if parent is None:
            root.depth = 0
        else:
            root.depth = parent.depth + 1

        if len(left_items):
            root.left = self.make_BST(left_items, root, False)

        if len(right_items):
            root.right = self.make_BST(right_items, root, False)
            root.right.parent = root
            root.right.depth = root.depth + 1

        return root

    def make_veb_order(self, start, depth):
        # given a starting node and max exploration depth, return
        # the list of nodes in the subtree in VEB order
        assert depth >= 0

        if depth == 0:
            return [start]

        lower_depth = depth // 2
        upper_depth = depth - lower_depth - 1

        depth_cutoff = start.depth + upper_depth
        frontier = [start]
        recurse_nodes = []

        for node in frontier:
            if node.depth == depth_cutoff + 1:
                recurse_nodes.append(node)
            if node.depth > depth_cutoff + 1:
                break
            if node.left is not None:
                frontier.append(node.left)
            if node.right is not None:
                frontier.append(node.right)
        
        veb_order = self.make_veb_order(start, upper_depth)
        for node in recurse_nodes:
            veb_order += self.make_veb_order(node, lower_depth)

        return veb_order

    def set_veb_indices(self):
        # iterates through veb_ordered_nodes to set veb_index of each node
        for i, node in enumerate(self.veb_ordered_nodes):
            node.veb_index = i

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


class NodeItem(object):

    def __init__(self, key, data):
        self.key = key
        self.data = data

    def __str__(self):
        return str((self.key, self.data))


class Node(object):
    """
    Node class supports basic attributes: key, data, left child 
    pointer, right child pointer, parent pointer
    Augmented with: depth, veb_index, xarray_index
    Assumes every node + all its fields take up one memory slot in our model
    """

    def __init__(self, node_item):
        # Constructor takes in a NodeItem object
        self.key = node_item.key
        self.data = node_item.data
        self._left = None
        self._right = None
        self._parent = None
        self.depth = None
        self.veb_index = None # index in VEB order
        self.xarray_index = None # pointer to solution xarray

    @property
    def left(self):
        # Enforces access through the cache/disk model
        # TODO: find index of left in disk, and read it
        return self._left

    @left.setter
    def left(self, node):
        self._left = node

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, node):
        self._right = node

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, node):
        self._parent = node

    def is_root(self):
        return self.parent is None

    def is_leaf(self):
        return self.left is None and self.right is None

    def __str__(self):
        return str((self.key, self.data))
