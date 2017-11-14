xcoord = lambda x: x[0]
ycoord = lambda x: x[1]

class XArray(object):
    """An XArray structure that fits with the memory model
        Assumes that the points passed in are PRE-SORTED by y coordinate"""


    # if the y is sparse, returns the max x for which (<=x, <=y)
    # is sparse. Otherwise, returns None
    def is_sparse_x_value(self, y, points):
        ps = sorted(points, key = xcoord)
        points_below = 0
        x_max = None
        for i in range(len(ps)):
            if ps[i][1] <= y:
                points_below += 1
            # i+1 is the total number of points examined so far
            if i+1 > self.alpha * points_below:
                x_max = ps[i][0]
        return x_max

    def __init__(self, points, alpha=2, base_case_length=10):

        self.xarray=[]
        self.y_to_xarray_chunk_map=dict()
        self.alpha = alpha

        # Sort yvals from largest to smallest
        all_yvals = [p[1] for p in points]
        all_yvals.reverse()

        # Intialize S_0
        i = 0
        S_i = sorted(points, key = xcoord)
        start_i = 0
        xarr_start_i = 0
        base_case_termination = False

        for j in range(len(all_yvals)):
            if j % 500 == 0:
                print('preprocessed %s points' % (j))
            y = all_yvals[j]
            x = self.is_sparse_x_value(y, S_i)

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
                p_i_minus_1 = [s for s in S_i if s[0] <= x_i]
                self.xarray = self.xarray + p_i_minus_1
                xarr_start_i += len(p_i_minus_1)

                # Update S_i from S_{i-1}
                S_i = [s for s in S_i if s[0] > x_i or s[1] <= y_i]

            # Base case. Map all remaining elements to the last chunk, S_i
            if len(S_i) < base_case_length:
                # print('BASE CASE!')
                base_case_termination = True

                for k in range(start_i, len(all_yvals)):
                    self.y_to_xarray_chunk_map[all_yvals[k]] = xarr_start_i
                self.xarray = self.xarray + S_i
                break

        # It is also possible that the final block is larger than the
        # base case and is also dense.
        if not base_case_termination:
            # print("Final block is dense!")
            for k in range(start_i, len(all_yvals)):
                self.y_to_xarray_chunk_map[all_yvals[k]] = xarr_start_i
            self.xarray = self.xarray + S_i

