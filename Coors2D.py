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

        self.yveb = VEBTree(self.make_node_items(points))

        # TODO: Fix how memory works with yveb
        self.memory.add_array_to_disk(self.yveb.veb_ordered_nodes)
        # self.xarray_disk_offset = len(self.memory.disk)

        # Construct the xarray, must pass in pre-sorted (by y) points
        self.alpha = 2
        self.base_case_length = 10
        self.xarray = XArray(self.memory, self.points,
                        self.alpha, self.base_case_length,
                        self.x_upper_bound, self.y_upper_bound)

    def make_node_items(self, points):
        return [NodeItem(y, x) for x, y in points]


    # def connect_nodes_to_xarray(self, point_to_index_map):
        # iterate through yveb, uses hashmap to update self.xarray_index for each node


    # Support query for not just xmax/ymax, but also xmin/ymin/etc.?
    def query(self, x_bound, y_bound):
        # Returns list of points in the quadrant (<= xmax, <= ymax)
        # Variables are improperly named but should work for other
        # types of queries (e.g. >= xmin, >= ymin)
        # TODO: make yveb.successor/predecessor work with memory model
        # Maybe: Store reference to self.memory in self.yveb?
        if self.y_upper_bound:
            rep_node = self.yveb.successor(y_bound)
            if rep_node is None:
                rep_node = self.yveb.predecessor(y_bound)
        else:
            rep_node = self.yveb.predecessor(y_bound)
            if rep_node is None:
                rep_node = self.yveb.successor(y_bound)

        solutions = []
        # I guess we can pretend we have the hashmap stored at the leaf nodes in the yveb
        # even though that's not how it's implemented here
        read_counter = 0
        for i in range(self.xarray.y_to_xarray_chunk_map[rep_node.key], len(self.xarray.xarray)):
            # This line here should incorporate the memory model
            point = self.xarray.get(i)
            # The next few lines can be deleted once we're sure this works
            # ind = self.xarray_disk_offset + i
            # point2 = self.memory.read(ind)
            # print('hey whatsup')
            # assert(point == point2)
            read_counter += 1
            # point = self.xarray.xarray[i]
            if self.x_upper_bound and point[0] > x_bound:
                break
            if not self.x_upper_bound and point[0] < x_bound:
                break

            if self.y_upper_bound and point[1] <= y_bound:
                solutions.append(point)
            if not self.y_upper_bound and point[1] >= y_bound:
                solutions.append(point)

        print("Read %s" % (read_counter))
        print("Disk accesses %s" % (self.memory.disk_accesses))

        # hacky way to remove duplicates; not sure how it fits in memory model
        return list(set(solutions))


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
