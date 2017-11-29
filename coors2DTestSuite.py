import unittest
import Coors2D
import random
from cache.memory import Memory
import time

class TestCoors2D(unittest.TestCase):

    memory = Memory()
    points_1 = [(random.uniform(-100, 100), random.uniform(-100, 100)) \
                for _ in range(100)]
    points_2 = [(random.uniform(-1000, 1000), random.uniform(-1000, 1000)) \
                for _ in range(1024)]
    
    def verify_2Sided_solutions(self, points, quadrant, solutions, \
                               x_upper_bound, y_upper_bound):
        sol = set(solutions)
        for x, y in points:
            if x_upper_bound:
                if y_upper_bound:
                    good_point = (x <= quadrant[0] and y <= quadrant[1])
                else:
                    good_point = (x <= quadrant[0] and y >= quadrant[1])
            else:
                if y_upper_bound:
                    good_point = (x >= quadrant[0] and y <= quadrant[1])
                else:
                    good_point = (x >= quadrant[0] and y >= quadrant[1])

            if good_point:
                if (x, y) not in sol:
                    print('Quadrant: {}'.format(quadrant))
                    print('Correct point (%s, %s) not in solution' % (x, y))
                    return False
            else:
                if (x, y) in sol:
                    print('Quadrant: {}'.format(quadrant))
                    print('Incorrect point (%s, %s) in solution' % (x, y))
                    return False
        return True

    def verify_3Sided_solution(self, points, solutions, x_min, x_max, \
                               y_bound, y_upper_bound):
        sol = set(solutions)
        for x, y in points:
            good_point = (x >= x_min and x <= x_max)
            if y_upper_bound:
                good_point = good_point and y <= y_bound
            else:
                good_point = good_point and y >= y_bound

            if good_point:
                if (x, y) not in sol:
                    print('(x_min, x_max, y_bound): {}'.format(
                            (x_min, x_max, y_bound)))
                    print('Correct point (%s, %s) not in solution' % (x, y))
                    return False
            else:
                if (x, y) in sol:
                    print('(x_min, x_max, y_bound): {}'.format(
                            (x_min, x_max, y_bound)))
                    print('Incorrect point (%s, %s) in solution' % (x, y))
                    return False
        return True

    def verify_4Sided_solution(self, points, solutions, x_min, x_max, \
                               y_min, y_max):
        sol = set(solutions)
        for x, y in points:
            good_point = (x >= x_min and x <= x_max and y >= y_min and y <= y_max)

            if good_point:
                if (x, y) not in sol:
                    print('(x_min, x_max, y_min, y_max): {}'.format(
                            (x_min, x_max, y_min, y_max)))
                    print('Correct point (%s, %s) not in solution' % (x, y))
                    return False
            else:
                if (x, y) in sol:
                    print('(x_min, x_max, y_min, y_max): {}'.format(
                            (x_min, x_max, y_min, y_max)))
                    print('Incorrect point (%s, %s) in solution' % (x, y))
                    return False
        return True

    def verify_2Sided_random_queries(self, dirc, num_queries=100, suppressed=True):
        x_upper_bound = bool(dirc//2)
        y_upper_bound = bool(dirc%2)

        obj = Coors2D.COORS2D2Sided(self.memory, self.points_1, \
                                    x_upper_bound, y_upper_bound)
        self.memory.reset_disk_accesses()
        self.memory.reset_cell_probes()
        
        if not suppressed:
            print("x_upper_bound:", x_upper_bound)
            print("y_upper_bound:", y_upper_bound)

        for i in range(num_queries):
            quadrant = (random.uniform(-1200, 1200), random.uniform(-1200, 1200))
            # print("Quadrant:", quadrant)
            # print("Len Solutions:", len(solutions))
            solutions = obj.query(*quadrant)
            if not self.verify_2Sided_solutions(self.points_1, quadrant, solutions, \
                         x_upper_bound, y_upper_bound):
                if not suppressed:
                    print("Test Failed.\n")
                return False

        if not suppressed:
            print("Test Passed!\n")
            print("Queries: {}, Disk accesses: {}, Cell probes: {}".format(
                                                num_queries, 
                                                self.memory.get_disk_accesses(), 
                                                self.memory.get_cell_probes()))
        return True

    def verify_3Sided_random_queries(self, dirc, num_queries=100, suppressed=True):
        y_upper_bound = bool(dirc % 2)
        
        obj = Coors2D.COORS2D3Sided(self.memory, self.points_1, y_upper_bound)
        self.memory.reset_disk_accesses()
        self.memory.reset_cell_probes()

        if not suppressed:
            print('y_upper_bound:', y_upper_bound)

        for i in range(num_queries):
            x_min = random.uniform(-1200, 1200)
            x_max = random.uniform(-1200, 1200)
            x_min = min(x_min, x_max)
            x_max = max(x_min, x_max)
            y_bound = random.uniform(-1200, 1200)

            solutions = obj.query(x_min, x_max, y_bound)
            if not self.verify_3Sided_solution(self.points_1, solutions, \
                    x_min, x_max, y_bound, y_upper_bound):
                if not suppressed:
                    print("Test Failed.\n")
                return False

        if not suppressed:
            print("Test Passed!\n")
            print("Queries: {}, Disk accesses: {}, Cell probes: {}".format(
                                                num_queries, 
                                                self.memory.get_disk_accesses(), 
                                                self.memory.get_cell_probes()))
        return True

    def verify_4Sided_random_queries(self, num_queries=100, suppressed=True):
        print("Started building 4Sided structure")
        t1 = time.time()
        obj = Coors2D.COORS2D4Sided(self.memory, self.points_1)
        self.memory.reset_disk_accesses()
        self.memory.reset_cell_probes()
        t2 = time.time()
        print("Preprocessing 4Sided completed in {:.2f}s.".format(t2-t1))

        for i in range(num_queries):
            x_min = random.uniform(-1200, 1200)
            x_max = random.uniform(-1200, 1200)
            x_min = min(x_min, x_max)
            x_max = max(x_min, x_max)
            y_min = random.uniform(-1200, 1200)
            y_max = random.uniform(-1200, 1200)
            y_min = min(y_min, y_max)
            y_max = max(y_min, y_max)

            solutions = obj.query(x_min, x_max, y_min, y_max)
            if not self.verify_4Sided_solution(self.points_1, solutions, \
                    x_min, x_max, y_min, y_max):
                if not suppressed:
                    print("Test Failed.\n")
                return False

        if not suppressed:
            print("Test Passed for 4Sided!\n")
            print("Queries: {}, Disk accesses: {}, Cell probes: {}".format(
                                                num_queries, 
                                                self.memory.get_disk_accesses(), 
                                                self.memory.get_cell_probes()))
        return True

    def test_2Sided_0(self, num_queries=100, suppressed=True):
        self.assertTrue(self.verify_2Sided_random_queries(0, num_queries, suppressed))

    def test_2Sided_1(self, num_queries=100, suppressed=True):
        self.assertTrue(self.verify_2Sided_random_queries(1, num_queries, suppressed))

    def test_2Sided_2(self, num_queries=100, suppressed=True):
        self.assertTrue(self.verify_2Sided_random_queries(2, num_queries, suppressed))

    def test_2Sided_3(self, num_queries=100, suppressed=True):
        self.assertTrue(self.verify_2Sided_random_queries(3, num_queries, suppressed))

    def test_3Sided_0(self, num_queries=100, suppressed=True):
        self.assertTrue(self.verify_3Sided_random_queries(0, num_queries, suppressed))

    def test_3Sided_1(self, num_queries=100, suppressed=True):
        self.assertTrue(self.verify_3Sided_random_queries(1, num_queries, suppressed))

    def test_4Sided(self, num_queries=100, suppressed=True):
        # this function takes a while to run when number of points is large
        self.assertTrue(self.verify_4Sided_random_queries(num_queries, suppressed))

def main():
    t = TestCoors2D()
    t._test_4Sided(num_queries=100, suppressed=False)

if __name__ == '__main__':
    unittest.main()
    # main()

