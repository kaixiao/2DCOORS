from veb import VEBTree, NodeItem
from xarray import XArray
from cache.memory import Memory

xcoord = lambda x: x[0]
ycoord = lambda x: x[1]

class COORS2D2Sided(object):

    def __init__(self, points, x_upper_bound=True, y_upper_bound=True):

        self.memory = Memory()
        self.x_upper_bound = x_upper_bound
        self.y_upper_bound = y_upper_bound

        # Points are stored sorted by y coordinate
        self.points = sorted(points, key = ycoord)

        self.yveb = VEBTree(self.memory, self.make_node_items(points))

        # self.xarray_disk_offset = len(self.memory.disk)

        # Construct the xarray, must pass in pre-sorted (by y) points
        self.alpha = 2
        self.base_case_length = 10
        self.xarray = XArray(self.memory, self.points,
                        self.alpha, self.base_case_length,
                        self.x_upper_bound, self.y_upper_bound)
        # initialize xarray_index field in each node
        self.connect_nodes_to_xarray()

    def make_node_items(self, points):
        return [NodeItem(y, x) for x, y in points]

    def connect_nodes_to_xarray(self):
        # iterate through yveb, uses hashmap to update self.xarray_index for each node
        for node in self.yveb.veb_ordered_nodes:
            node.xarray_index = self.xarray.y_to_xarray_chunk_map[node.key]

    def query(self, x_bound, y_bound):
        """
        Returns list of points in closed quadrant
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
        # read_counter = 0
        if self.x_upper_bound:
            prev_x = -float('inf')
        else:
            prev_x = float('inf')

        for i in range(rep_node.xarray_index, len(self.xarray.xarray)):
            point = self.xarray.get(i)
            # read_counter += 1
            # point = self.xarray.xarray[i]

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
            if not self.y_upper_bound and point[1] >= y_bound:
                solutions.append(point)

        # print("Read %s" % (read_counter))
        # print("Disk accesses %s" % (self.memory.disk_accesses))

        # just making sure there are no duplicates so logic is correct
        assert len(solutions) == len(list(set(solutions)))
        return solutions


class COORS2D3Sided(object):

    def __init__(self, points):
        # TODO: This whole thing
        pass

    def query(self, x_min, x_max, y_max):
        # TODO: This whole thing
        pass


class COORS2D4Sided(object):

    def __init__(self, points):
        # TODO: This whole thing
        pass

    def query(self, x_min, x_max, y_min, y_max):
        # TODO: This whole thing
        pass
