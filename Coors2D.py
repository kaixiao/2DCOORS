from veb import VEBTree, NodeItem

xcoord = lambda x: x[0]
ycoord = lambda x: x[1]

class COORS2D2Sided(object):

	def __init__(self, points):
		# TODO: make veb indexed by ycoord

		# Points are stored sorted by y coordinate
		self.points = sorted(points, key = ycoord)
		self.yveb = VEBTree(self.make_node_items(points))

		print('starting xarray construction')
		# Also the yveb stuff needs to point to stuff in the array
		self.xarray = []
		self.y_to_xarray_chunk_map = dict()
		self.alpha = 2
		self.construct_xarray()

	def make_node_items(self, points):
        return [NodeItem(y, x) for x, y in points]

	# if the y is sparse, returns the max x for which (<=x, <=y)
	# is sparse. Otherwise, returns None
	def is_sparse_x_value(self, y, points):
		ps = sorted(points, key = xcoord)
		points_below = 0
		total_points = 0
		x_max = None
		for i in range(len(ps)):
			if ps[i][1] <= y:
				points_below += 1
			# i+1 is the total number of points examined so far
			if i+1 > self.alpha * points_below:
				x_max = ps[i][0]
		return x_max

	# Main preprocessing step
	# computes xarray and connect nodes to correct index in xarray
	def construct_xarray(self):
		# Sort yvals from largest to smallest
		all_yvals = [p[1] for p in self.points]
		all_yvals.reverse()

		# Base case
		o1_length = 2

		# Intialize S_0
		i = 0
		S_i = sorted(self.points, key = xcoord)
		start_i = 0
		xarr_start_i = 0
		base_case_termination = False

		for j in range(len(all_yvals)):
			if j % 500 == 0:
				print(j)
			y = all_yvals[j]
			x = self.is_sparse_x_value(y, S_i)

			if x:
				i += 1
				x_i, y_i = x, y
				print ("%s, %s is sparse!" % (x_i, y_i))
				print("mapping y values in the range (%s,%s) to %s" % \
						(all_yvals[start_i], y_i, xarr_start_i))

				# map all y values strictly greater than y_i to xarr_start_i
				# the index of the first element of P_i
				for k in range(start_i, j):
					self.y_to_xarray_chunk_map[all_yvals[k]] = xarr_start_i
					start_i = j

				# In next line, S_i refers to S_{i-1} because it has not been updated yet
				p_i_minus_1 = [s for s in S_i if s[0] <= x_i]
				self.xarray = self.xarray + p_i_minus_1
				xarr_start_i += len(p_i_minus_1)

				# Update S_i from S_{i-1}
				S_i = [s for s in S_i if s[0] > x_i or s[1] <= y_i]

			# Base case. Map all remaining elements to the last chunk, S_i
			if len(S_i) < o1_length:
				print('BASE CASE!')
				base_case_termination = True

				for k in range(start_i, len(all_yvals)):
					self.y_to_xarray_chunk_map[all_yvals[k]] = xarr_start_i
				self.xarray = self.xarray + S_i
				break

		# It is also possible that the final block is larger than the
		# base case and is also dense.
		if not base_case_termination:
			print("Final block is dense!")
			for k in range(start_i, len(all_yvals)):
				self.y_to_xarray_chunk_map[all_yvals[k]] = xarr_start_i
			self.xarray = self.xarray + S_i

	# def connect_nodes_to_xarray(self, point_to_index_map):
		# iterate through yveb, uses hashmap to update self.xarray_index for each node


	# Support query for not just xmax/ymax, but also xmin/ymin/etc.?
	def query(self, x_max, y_max):
		# TODO: read from xarray via memory model, perhaps should create array
		# class specifically for accessing and writing xarray
		# Returns list of points in the quadrant (<= xmax, <= ymax)
		lead = self.yveb.successor(y_max)
		if lead is None:
			lead = yveb.predecessor(y_max)

		solutions = []
		for i in range(self.y_to_xarray_chunk_map[lead.key], len(self.xarray)):
			point = self.xarray[i]
			if point[0] > x_max:
				break
			if point[1] <= y_max:
				solutions.append(point)

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
