from veb import VEBTree

class COORS2D2Sided(object):

	def __init__(self, points):
		# TODO: make veb indexed by ycoord
		self.points = points
		self.yveb = VEBTree(make_node_items(points))

		# Also the yveb stuff needs to point to stuff in the array
		self.xarray = []
		construct_xarray()

	def make_node_items(points):
		# make list of node items with y as key and x as data
		pass

	def construct_xarray(self):
		# TODO: This whole thin
		# Main preprocessing step
		# computes xarray and connect nodes to correct index in xarray
		pass

	def connect_nodes_to_xarray(self, point_to_index_map):
		# iterate through yveb, uses hashmap to update self.xarray_index for each node
		pass

	# Support query for not just xmax/ymax, but also xmin/ymin/etc.?

	def query(self, x_max, y_max):
		# TODO: read from xarray via memory model, perhaps should create array 
		# class specifically for accessing and writing xarray
		# Returns list of points in the quadrant (<= xmax, <= ymax)
		rep = yveb.successor(y_max)
		if rep is None:
			rep = yveb.predecessor(y_max)

		solutions = []
		for i in range(rep.xarray_index, len(self.xarray)):
			node = self.xarray[i]
			if node.data > x_max:
				break
			if node.key <= y_max:
				solutions.append((node.data, node.key))

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
