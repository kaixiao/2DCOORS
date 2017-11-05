from veb import VEBTree

class COORS2D2Sided(object):
	def __init__(self, points):
		# TODO: make veb indexed by ycoord
		self.points = points
		self.yveb = VEBTree(make_node_items(points))

		# Also the yveb stuff needs to point to stuff in the array
		self.xarray = None
		construct_xarray()

	def make_node_items(points):
		# make list of node items with y as key and x as data

	def construct_xarray(self):
		# TODO: This whole thing
		# Entire preprocessing step
		# takes in points (tuples)
		# returns xarray and hashmap from point to indices i, j 
		# 	corresponding to its set P_i and the index in the set

	def connect_nodes_to_xarray(self, point_to_index_map):
		# iterate through yveb, uses hashmap to update self.xarray_index for each node

	# Support query for not just xmax/ymax, but also xmin/ymin/etc.?

	def query(self, xmax, ymax):
	# TODO: This whole thing 

class COORS2D3Sided(object):
	def __init__(self, points):
	# TODO: This whole thing 
		pass
	
	def query(self, xmin, xmax, ymax):
	# TODO: This whole thing 

class COORS2D4Sided(object):
	def __init__(self, points):
	# TODO: This whole thing 
		pass
	
	def query(self, xmin, xmax, ymin, ymax):
	# TODO: This whole thing 


