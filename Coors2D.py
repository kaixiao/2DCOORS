from veb import vebTree

def COORS2D2Sided(object):
	def __init__(self, points):
		# TODO: make veb indexed by ycoord
		self.yveb = vebTree(points, key = ycoord)

		# Also the yveb stuff needs to point to stuff in the array
		self.xarray = construct_array(points)

	def construct_array(self):
	# TODO: This whole thing

	# Support query for not just xmax/ymax, but also xmin/ymin/etc.?
	def query(self, xmax, ymax):
	# TODO: This whole thing 

def COORS2D3Sided(object):
	def __init__(self, points):
	# TODO: This whole thing 
		pass
	
	def query(self, xmin, xmax, ymax):
	# TODO: This whole thing 

def COORS2D4Sided(object):
	def __init__(self, points):
	# TODO: This whole thing 
		pass
	
	def query(self, xmin, xmax, ymin, ymax):
	# TODO: This whole thing 


