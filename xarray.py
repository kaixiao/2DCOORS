from cache.memory import Memory
from Node import Node, NodeItem

xcoord = lambda x: x[0]
ycoord = lambda x: x[1]

class XArray(object):
    """An XArray structure that fits with the memory model
        Assumes that the points passed in are PRE-SORTED by y coordinate"""

    def leq(self, a, b):
        return a <= b

    def geq(self, a, b):
        return a >= b

    # if the y is sparse, returns the opt x for which (<=x, <=y)
    # (or other quadrant) is sparse. Otherwise, returns None
    def is_sparse_x_value(self, y, points, x_upper_bound=True,
                            y_upper_bound=True):
        ps = sorted(points, key = xcoord)
        if not x_upper_bound:
            ps.reverse()

        points_good = 0
        x_opt = None
        if y_upper_bound:
            comparison = self.leq
        else:
            comparison = self.geq

        for i in range(len(ps)):
            if comparison(ps[i][1], y):
                points_good += 1
            # i+1 is the total number of points examined so far
            if i+1 > self.alpha * points_good:
                x_opt = ps[i][0]

        return x_opt

    def __init__(self, memory, points, alpha=2, base_case_length=10,
                    x_upper_bound=True, y_upper_bound=True):
        # print("inside: x_upper_bound: ", x_upper_bound)
        # print("inside: y_upper_bound: ", y_upper_bound)

        xarray_points=[]
        self.y_to_xarray_chunk_map=dict()
        self.alpha = alpha
        self.memory = memory

        # offset measures how far from the start of memory
        self.memory_disk_offset = len(self.memory.disk)
        # print('offset is', self.memory_disk_offset)

        # Sort yvals from largest to smallest
        all_yvals = [p[1] for p in points]
        if y_upper_bound:
            all_yvals.reverse()

        # Intialize S_0
        i = 0

        y_sorted_points = points

        # reverse y coordinates - strange condition
        # this only needs to be done for x_upper_bound = False
        # and y_upper_bound = True
        if not x_upper_bound and y_upper_bound:
            y_sorted_points.reverse()

        S_i = sorted(y_sorted_points, key = xcoord)
        if not x_upper_bound:
            S_i.reverse()

        start_i = 0
        xarr_start_i = 0
        base_case_termination = False

        for j in range(len(all_yvals)):
            if j % 500 == 0:
                pass
                # print('preprocessed %s points' % (j))
            y = all_yvals[j]
            x = self.is_sparse_x_value(y, S_i, x_upper_bound, y_upper_bound)

            if x:
                i += 1
                x_i, y_i = x, y
                # print("%s, %s is sparse!" % (x_i, y_i))
                # print("mapping y values in the range (%s,%s) to %s" % \
                #         (all_yvals[start_i], y_i, xarr_start_i))

                # map all y values strictly greater than y_i to xarr_start_i
                # the index of the first element of P_i
                for k in range(start_i, j):
                    self.y_to_xarray_chunk_map[all_yvals[k]] = xarr_start_i
                    start_i = j

                # In next line, S_i refers to S_{i-1} because it has not been updated yet
                if x_upper_bound:
                    p_i_minus_1 = [s for s in S_i if s[0] <= x_i]
                else:
                    p_i_minus_1 = [s for s in S_i if s[0] >= x_i]
                xarray_points = xarray_points + p_i_minus_1
                xarr_start_i += len(p_i_minus_1)

                # Update S_i from S_{i-1}
                if y_upper_bound:
                    if x_upper_bound:
                        S_i = [s for s in S_i if s[0] > x_i or s[1] <= y_i]
                    else:
                        S_i = [s for s in S_i if s[0] < x_i or s[1] <= y_i]
                else:
                    if x_upper_bound:
                        S_i = [s for s in S_i if s[0] > x_i or s[1] >= y_i]
                    else:
                        S_i = [s for s in S_i if s[0] < x_i or s[1] >= y_i]

            # Base case. Map all remaining elements to the last chunk, S_i
            if len(S_i) < base_case_length:
                # print('BASE CASE!')
                base_case_termination = True

                for k in range(start_i, len(all_yvals)):
                    self.y_to_xarray_chunk_map[all_yvals[k]] = xarr_start_i
                xarray_points = xarray_points + S_i
                break

        # It is also possible that the final block is larger than the
        # base case and is also dense.
        if not base_case_termination:
            # print("Final block is dense!")
            for k in range(start_i, len(all_yvals)):
                self.y_to_xarray_chunk_map[all_yvals[k]] = xarr_start_i
            xarray_points = xarray_points + S_i

        # Add to memory
        # self.xarray_points = xarray_points
        self.xarray = [Node(self.memory, NodeItem(xarr_point)) for xarr_point in xarray_points]
        self.memory.add_array_to_disk(self.xarray)

    # def get(self, index):
    #     return self.memory.read(self.memory_disk_offset + index)
