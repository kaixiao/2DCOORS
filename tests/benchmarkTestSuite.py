import unittest
import benchmark
import random as rd
from cache.memory import Memory
import time

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
                    print('\n(x_min, x_max, y_min, y_max): ({:.2f}, {:.2f},' \
                          '{:.2f}, {:.2f})'.format(x_min, x_max, y_min, y_max))
                    print('Correct point (%.2f, %.2f) not in solution.\n' % (x, y))
                    return False
            else:
                if (x, y) in sol:
                    print('\n(x_min, x_max, y_min, y_max): ({:.2f}, {:.2f},' \
                          '{:.2f}, {:.2f})'.format(x_min, x_max, y_min, y_max))
                    print('Incorrect point (%.2f, %.2f) in solution.\n' % (x, y))
                    return False
        return True

    def verify_randomqueries(self, points, num_queries, obj, out=False):
        t1 = time.time()
        self.memory.reset_disk_accesses()
        self.memory.reset_cell_probes()
        t2 = time.time()
        if out:
            print("Preprocessing memory completed in {:.3f}s.".format(t2-t1))

        for i in range(num_queries):
            x_min = rd.uniform(-self.qbound, self.qbound)
            x_max = rd.uniform(-self.qbound, self.qbound)
            x_min = min(x_min, x_max)
            x_max = max(x_min, x_max)
            y_min = rd.uniform(-self.qbound, self.qbound)
            y_max = rd.uniform(-self.qbound, self.qbound)
            y_min = min(y_min, y_max)
            y_max = max(y_min, y_max)

            solutions = obj.query(x_min, x_max, y_min, y_max)
            if not self.verify_solution(points, solutions, \
                    x_min, x_max, y_min, y_max):
                if out:
                    print("Test Failed.\n")
                return False

        if out:
            print("Test Passed for 4Sided!")
            print("Queries: {}, Disk accesses: {}, Cell probes: {}\n".format(
                                                num_queries, 
                                                self.memory.get_disk_accesses(), 
                                                self.memory.get_cell_probes()))
        return True

    # @unittest.skip("This test is skipped")
    def test_queries_1(self, ds=None, trials=10, num_points=100, num_queries=1000, out=False):
        # this function takes a while to run when number of points is large
        for i in range(trials):
            points = [(rd.uniform(-self.pbound, self.pbound), 
                       rd.uniform(-self.pbound, self.pbound))
                       for _ in range(num_points)]
            datastruct = ds(self.memory, points)
            import pdb
            pdb.set_trace()
            self.assertTrue(self.verify_randomqueries(
                    points, num_queries, datastruct, out))
            print('Passed trial {} of {}.'.format(i+1, trials))

def main():
    t = TestBenchmark()
    ds1 = benchmark.NaiveStruct
    ds2 = benchmark.XBST
    t.test_queries_1(ds=ds1, trials=5, num_points=1000, num_queries=1000, out=True)
    t.test_queries_1(ds=ds2, trials=5, num_points=1000, num_queries=1000, out=True)

if __name__ == '__main__':
    # unittest.main()
    main()

