from veb import VEBTree, NodeItem
from xarray import XArray
from cache.memory import Memory

xcoord = lambda x: x[0]
ycoord = lambda x: x[1]

class COORS2D2Sided(object):

    def __init__(self, points):

        self.mem = Memory()

        # Points are stored sorted by y coordinate
        self.points = sorted(points, key = ycoord)
        self.yveb = VEBTree(self.make_node_items(points))
        self.mem.add_array_to_disk(self.yveb.veb_ordered_nodes)

        # Construct the xarray, must pass in pre-sorted (by y) points
        self.alpha = 2
        self.xarray = XArray(self.points, self.alpha)

        # offset measures how far from correct
        self.xarray_disk_offset = len(self.mem.disk)
        print('offset is', self.xarray_disk_offset)
        self.mem.add_array_to_disk(self.xarray.xarray)

    def make_node_items(self, points):
        return [NodeItem(y, x) for x, y in points]


    # def connect_nodes_to_xarray(self, point_to_index_map):
        # iterate through yveb, uses hashmap to update self.xarray_index for each node


    # Support query for not just xmax/ymax, but also xmin/ymin/etc.?
    def query(self, x_max, y_max):
        # TODO: read from xarray via memory model, perhaps should create array
        # class specifically for accessing and writing xarray
        # Returns list of points in the quadrant (<= xmax, <= ymax)
        
        # TODO: make yveb.successor/predecessor work with memory model
        # Maybe: Store reference to self.mem in self.yveb?
        lead = self.yveb.successor(y_max)
        if lead is None:
            lead = yveb.predecessor(y_max)

        solutions = []
        # I guess we can pretend we have the hashmap stored at the leaf nodes in the yveb
        # even though that's not how it's implemented here
        read_counter = 0
        for i in range(self.xarray.y_to_xarray_chunk_map[lead.key], len(self.xarray.xarray)):
            # This line here should incorporate the memory model
            ind = self.xarray_disk_offset + i
            point = self.mem.read(ind)
            read_counter += 1
            # point = self.xarray.xarray[i]
            if point[0] > x_max:
                break
            if point[1] <= y_max:
                solutions.append(point)
        print("Read %s" % (read_counter))
        print("Disk accesses %s" % (self.mem.disk_accesses))

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
