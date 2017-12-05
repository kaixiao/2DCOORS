import unittest
import random as rd
from benchmark import *
from cache.memory import Memory

XBST_non_veb = lambda memory, points: XBST(memory, points, veb_order=False)
XBST_non_veb.__name__ = 'XBST_non_veb'
RangeTree_non_veb = lambda memory, points: RangeTree(memory, points, veb_order=False)
RangeTree_non_veb.__name__ = 'RangeTree_non_veb'

class TestBenchmark(unittest.TestCase):

    memory = Memory()

    pbound = 100
    qbound = 120
    
    def verify_solution(self, points, solutions, x_min, x_max, \
                               y_min, y_max):
        sol = set(solutions)
        for x, y in points:
            good_point = (x >= x_min and x <= x_max and y >= y_min and y <= y_max)

            if good_point:
                if (x, y) not in sol:
                    print('\n(x_min, x_max, y_min, y_max): ({:.2f}, {:.2f}, ' \
                          '{:.2f}, {:.2f})'.format(x_min, x_max, y_min, y_max))
                    print('Correct point (%.2f, %.2f) not in solution.\n' % (x, y))
                    return False
            else:
                if (x, y) in sol:
                    print('\n(x_min, x_max, y_min, y_max): ({:.2f}, {:.2f}, ' \
                          '{:.2f}, {:.2f})'.format(x_min, x_max, y_min, y_max))
                    print('Incorrect point (%.2f, %.2f) in solution.\n' % (x, y))
                    return False
        return True

    def verify_random_queries(self, points, num_queries, ors_ds, out=False):
        self.memory.reset_stats()

        for i in range(num_queries):
            x_min = rd.uniform(-self.qbound, self.qbound)
            x_max = rd.uniform(-self.qbound, self.qbound)
            x_min = min(x_min, x_max)
            x_max = max(x_min, x_max)
            y_min = rd.uniform(-self.qbound, self.qbound)
            y_max = rd.uniform(-self.qbound, self.qbound)
            y_min = min(y_min, y_max)
            y_max = max(y_min, y_max)

            solutions = ors_ds.query(x_min, x_max, y_min, y_max)
            if not self.verify_solution(points, solutions, \
                    x_min, x_max, y_min, y_max):
                if out:
                    print("\nTest Failed.\n")
                return False

        if out:
            print("Queries: {}, Disk accesses: {}, Cell probes: {}".format(
                                                num_queries, 
                                                self.memory.get_disk_accesses(), 
                                                self.memory.get_cell_probes()))
        return True

    def ors_test(self, ors_builder, trials=10, num_points=100, num_queries=1000, 
                 out=False):
        print("\n-----Running tests for {}-----".format(ors_builder.__name__))
        for i in range(trials):
            points = [(rd.uniform(-self.pbound, self.pbound), 
                       rd.uniform(-self.pbound, self.pbound))
                       for _ in range(num_points)]
            ds = ors_builder(self.memory, points)
            self.assertTrue(self.verify_random_queries(
                    points, num_queries, ds, out))
            print('Passed trial {}/{}.\n'.format(i+1, trials))

def main():
    t = TestBenchmark()
    ds1 = NaiveStruct
    ds2 = XBST
    ds2x = XBST_non_veb
    ds3 = RangeTree
    ds3x = RangeTree_non_veb
    ds4 = Coors
    t.ors_test(ds1, trials=5, num_points=100, num_queries=1000, out=True)
    t.ors_test(ds2, trials=5, num_points=100, num_queries=1000, out=True)
    t.ors_test(ds2x, trials=5, num_points=100, num_queries=1000, out=True)
    t.ors_test(ds3, trials=5, num_points=100, num_queries=1000, out=True)
    t.ors_test(ds3x, trials=5, num_points=100, num_queries=1000, out=True)
    t.ors_test(ds4, trials=5, num_points=100, num_queries=1000, out=True)

if __name__ == '__main__':
    main()

