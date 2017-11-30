from Ors2D import ORS2D
# Naive in O(n)
# sort by x coordinate
# sort by y coordinate
# sort by x coordinate and y coordinate, and pick min via segment tree
# if we have an implementation of simple 2D range trees log^2n
class naive_struct(ORS2D):
    def __init__(self, memory, points):
        self.memory = memory
        self.points = points
        nodes = 
        self.memory.add_array_to_disk(self.points)

    def query(self, x_min, x_max, y_min, y_max):
        solutions = []
        for i in range(len(disk)):
            point = next_thing.read() # a node

            if x_min <= p[0] and p[0] <= x_max and \
                y_min <= p[1] and p[1] <= y_max:
                solutions.append(p)
        return solutions

class x_coord_sorted(ORS2D):
    def __init__(self, memory, points):
        # Use VeB tree for make_BST
        self.memory = memory
        self.points = points

    def query(self, x_min, x_max, y_min, y_max):
        return None

class simple_range_tree(ORS2D):
    def __init__(self, memory, points):
        self.memory = memory
        self.points = points

    def query(self, x_min, x_max, y_min, y_max):
        return None

