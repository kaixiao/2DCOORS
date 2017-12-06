from veb import *
from Node import NodeItem, Node
from xarray import XArray
from cache.memory import Memory
from Ors2D import ORS2D
import time

x_coord = lambda x: x[0]
y_coord = lambda x: x[1]

class COORS2D2Sided(object):

    def __init__(self, memory, points, x_upper_bound=True, y_upper_bound=True):
        assert len(points) > 0

        self.memory = memory
        self.x_upper_bound = x_upper_bound
        self.y_upper_bound = y_upper_bound

        # Points are stored in yveb sorted by y coordinate
        self.points = sorted(points, key=y_coord)
        node_items = [NodeItem(y, x) for x, y in points]
        self.yveb = VEB2Sided(self.memory, node_items)

        # Construct the xarray, must pass in pre-sorted (by y) points
        self.alpha = 2
        self.base_case_length = 10
        self.xarray = XArray(self.memory, self.points, self.alpha, \
                self.base_case_length, self.x_upper_bound, self.y_upper_bound)

        # initialize xarray_index field in each Node2Sided object
        self.link_nodes_to_xarray()

    def link_nodes_to_xarray(self):
        # iterate through yveb, uses hashmap to update self.xarray_index for each node
        for node in self.yveb.veb_ordered_nodes:
            node.xarray_index = self.xarray.y_to_xarray_chunk_map[node.key]

    def query(self, x_bound, y_bound):
        """
        Returns list of point tuples in closed query quadrant
        Only supports points with distinct x values
        """
        if self.y_upper_bound:
            rep_node = self.yveb.successor(y_bound)
            if rep_node is None:
                rep_node = self.yveb.predecessor(y_bound)
        else:
            rep_node = self.yveb.predecessor(y_bound)
            if rep_node is None:
                rep_node = self.yveb.successor(y_bound)

        solutions = [] 
        if self.x_upper_bound:
            prev_x = -float('inf')
        else:
            prev_x = float('inf')

        for i in range(rep_node.xarray_index, len(self.xarray.xarray)):
            point = self.xarray.xarray[i].read().key

            if self.x_upper_bound and point[0] > x_bound:
                break
            if not self.x_upper_bound and point[0] < x_bound:
                break
            if self.x_upper_bound and point[0] <= prev_x:
                continue
            if not self.x_upper_bound and point[0] >= prev_x:
                continue
            prev_x = point[0]

            if self.y_upper_bound and point[1] <= y_bound:
                solutions.append(point)
                self.memory.update_buffer()

            if not self.y_upper_bound and point[1] >= y_bound:
                solutions.append(point)
                self.memory.update_buffer()

        return solutions


class COORS2D3Sided(object):

    def __init__(self, memory, points, y_upper_bound=True):
        assert len(points) > 0
        self.memory = memory
        self.y_upper_bound = y_upper_bound

        self.points = sorted(points, key=x_coord)
        node_items = [NodeItem(x, y) for x, y in points]
        self.xveb = VEB3Sided(memory, node_items)

        self.link_nodes_to_2Sided()

    def link_nodes_to_2Sided(self):
        # store 2Sided structs on points in subtrees for every node in xveb
        for node in self.xveb.veb_ordered_nodes:
            points = [(v.key, v.data) for v in self.xveb.subtree(node, leaves=True)]
            node.x_upper_struct = COORS2D2Sided(self.memory, points, \
                    x_upper_bound=True, y_upper_bound=self.y_upper_bound)
            node.x_lower_struct = COORS2D2Sided(self.memory, points, \
                    x_upper_bound=False, y_upper_bound=self.y_upper_bound)

    def query(self, x_min, x_max, y_bound):
        assert x_min <= x_max

        solutions = []
        lca = self.xveb.fast_LCA(x_min, x_max)

        if lca.is_leaf():
            x, y = lca.point()
            if x_min <= x <= x_max and (self.y_upper_bound and y <= y_bound \
                    or not self.y_upper_bound and y >= y_bound):
                solutions.append(lca.point())
        else:
            solutions.extend(lca.left.x_lower_struct.query(x_min, y_bound))
            solutions.extend(lca.right.x_upper_struct.query(x_max, y_bound))

        return solutions

class COORS2D4Sided(ORS2D):
    """
    We will use the natural O(n log^2 n) space implementation instead of 
    the O(n log^2 n / log log n) space implementation given in class
    (query time bounds are the same)
    """

    def __init__(self, memory, points):
        assert len(points) > 0

        self.memory = memory

        self.points = sorted(points, key=y_coord)
        node_items = [NodeItem(y, x) for x, y in points]
        self.yveb = VEB4Sided(memory, node_items)

        self.link_nodes_to_3Sided()

    def link_nodes_to_3Sided(self):
        counter = 0
        target = 1
        start_time = time.time()
        for node in self.yveb.veb_ordered_nodes:
            cur_time = time.time()
            if counter == target:
                target *= 2
                print("Constructed %s nodes in %s time" % (counter, cur_time - start_time))
            points = [(v.data, v.key) for v in self.yveb.subtree(node, leaves=True)]
            node.y_upper_struct = COORS2D3Sided(self.memory, points, \
                    y_upper_bound=True)
            node.y_lower_struct = COORS2D3Sided(self.memory, points, \
                    y_upper_bound=False)
            counter += 1

    def query(self, x_min, x_max, y_min, y_max):
        assert x_min <= x_max and y_min <= y_max

        solutions = []
        lca = self.yveb.fast_LCA(y_min, y_max)

        if lca.is_leaf():
            x, y = lca.point()
            if x_min <= x <= x_max and y_min <= y <= y_max:
                solutions.append((x, y))
        else:
            solutions.extend(lca.left.y_lower_struct.query(x_min, x_max, y_min))
            solutions.extend(lca.right.y_upper_struct.query(x_min, x_max, y_max))

        return solutions

