# TODO: Make a veB tree that sorts by element.key
# Or should we take this one from somewhere else

import numpy as np

class VEBTree(object):
	def __init__(self, node_items):
        self.root = make_BST(node_items)
        # TODO: make log work
        self.veb_ordered_nodes = make_veb_order(self.root, np.log(len(points)))
        self.set_veb_indices()

    def make_BST(self, node_items):
        # make a perfect BST from a list of tuples
        # returns root node
        pass

    def make_veb_order(self, node, depth):
        # returns a list
        # recurse
        pass

    def set_veb_indices(self):
        # iterates through veb_ordered_nodes, set indices from node to veb ordered list
        pass

    def predecessor(self, key):
        # start from root, returns node, use get_left()/get_right()!


    def successor(self, key):
        # same as above

class NodeItem(object):
    def __init__(self, data, key):
        self.data = data
        self.key = key

class Node(object):
    def __init__(self, node_item, left=None, right=None, parent=None):
        self.node_item = node_item
        self.left = left
        self.right = right
        self.parent = parent
        self.veb_index = None
        self.xarray_index = None

    def get_left():
        # find index of left in disk, and read it, don't directly access self.left
        pass

    def get_right():
        # same as above
        pass
