import unittest
import Coors2D
import random as rd
from cache.memory import Memory
import time

class TestCoors2D(unittest.TestCase):

    memory = Memory()

    pbound = 100
    qbound = 120
    
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
                    print('\nQuadrant: {}'.format(quadrant))
                    print('Correct point (%.2f, %.2f) not in solution.\n' % (x, y))
                    return False
            else:
                if (x, y) in sol:
                    print('\nQuadrant: {}'.format(quadrant))
                    print('Incorrect point (%.2f, %.2f) in solution.\n' % (x, y))
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
                    print('\n(x_min, x_max, y_bound):' \
                          '({:.2f}, {:.2f}, {:.2f})'.format(x_min, x_max, y_bound))
                    print('Correct point (%.2f, %.2f) not in solution.\n' % (x, y))
                    return False
            else:
                if (x, y) in sol:
                    print('\n(x_min, x_max, y_bound):' \
                          '({:.2f}, {:.2f}, {:.2f})'.format(x_min, x_max, y_bound))
                    print('Incorrect point (%.2f, %.2f) in solution.\n' % (x, y))
                    return False
        return True

    def verify_4Sided_solution(self, points, solutions, x_min, x_max, \
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

    def verify_2Sidedrandomqueries(self, dirc, points, num_queries, \
                                     out=False):
        x_upper_bound = bool(dirc//2)
        y_upper_bound = bool(dirc%2)

        obj = Coors2D.COORS2D2Sided(self.memory, points, \
                                    x_upper_bound, y_upper_bound)
        self.memory.reset_disk_accesses()
        self.memory.reset_cell_probes()
        
        if out:
            print("x_upper_bound:", x_upper_bound)
            print("y_upper_bound:", y_upper_bound)

        for i in range(num_queries):
            quadrant = (rd.uniform(-self.qbound, self.qbound), rd.uniform(-self.qbound, self.qbound))
            # print("Quadrant:", quadrant)
            # print("Len Solutions:", len(solutions))
            solutions = obj.query(*quadrant)
            if not self.verify_2Sided_solutions(points, quadrant, solutions, \
                         x_upper_bound, y_upper_bound):
                if out:
                    print("Test Failed.\n")
                return False

        if out:
            print("Test Passed!\n")
            print("Queries: {}, Disk accesses: {}, Cell probes: {}".format(
                                                num_queries, 
                                                self.memory.get_disk_accesses(), 
                                                self.memory.get_cell_probes()))
        return True

    def verify_3Sidedrandomqueries(self, dirc, points, num_queries, \
                                     out=False):
        y_upper_bound = bool(dirc % 2)
        
        obj = Coors2D.COORS2D3Sided(self.memory, points, y_upper_bound)
        self.memory.reset_disk_accesses()
        self.memory.reset_cell_probes()

        if out:
            print('y_upper_bound:', y_upper_bound)

        for i in range(num_queries):
            x_min = rd.uniform(-self.qbound, self.qbound)
            x_max = rd.uniform(-self.qbound, self.qbound)
            x_min = min(x_min, x_max)
            x_max = max(x_min, x_max)
            y_bound = rd.uniform(-self.qbound, self.qbound)

            solutions = obj.query(x_min, x_max, y_bound)
            if not self.verify_3Sided_solution(points, solutions, \
                    x_min, x_max, y_bound, y_upper_bound):
                if out:
                    print("Test Failed.\n")
                return False

        if out:
            print("Test Passed!")
            print("Queries: {}, Disk accesses: {}, Cell probes: {}\n".format(
                                                num_queries, 
                                                self.memory.get_disk_accesses(), 
                                                self.memory.get_cell_probes()))
        return True

    def verify_4Sidedrandomqueries(self, points, num_queries, out=False):
        if out:
            print("\nStarted building 4Sided structure on {} points...".format(
                                                                    len(points)))
        t1 = time.time()
        obj = Coors2D.COORS2D4Sided(self.memory, points)
        self.memory.reset_disk_accesses()
        self.memory.reset_cell_probes()
        t2 = time.time()
        if out:
            print("Preprocessing 4Sided completed in {:.3f}s.".format(t2-t1))

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
            if not self.verify_4Sided_solution(points, solutions, \
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

    def test_2Sided_1(self, trials=10, num_points=100, num_queries=1000, out=False):
        for i in range(trials):
            points = [(rd.uniform(-self.pbound, self.pbound), 
                       rd.uniform(-self.pbound, self.pbound))
                       for _ in range(num_points)]
            for dirc in range(4):
                self.assertTrue(self.verify_2Sidedrandomqueries(dirc, points, \
                        num_queries, out))

    def test_3Sided_1(self, trials=10, num_points=100, num_queries=1000, out=False):
        for i in range(trials):
            points = [(rd.uniform(-self.pbound, self.pbound), 
                       rd.uniform(-self.pbound, self.pbound))
                       for _ in range(num_points)]
            for dirc in range(2):
                self.assertTrue(self.verify_3Sidedrandomqueries(dirc, points, \
                        num_queries, out))

    def test_4Sided_1(self, trials=10, num_points=100, num_queries=1000, out=False):
        # this function takes a while to run when number of points is large
        for i in range(trials):
            points = [(rd.uniform(-self.pbound, self.pbound), 
                       rd.uniform(-self.pbound, self.pbound))
                       for _ in range(num_points)]
            self.assertTrue(self.verify_4Sidedrandomqueries(
                    points, num_queries, out))
            print('Passed trial {} of {} for 4Sided.'.format(i+1, trials))

def main():
    t = TestCoors2D()
    t.test_4Sided_1(trials=10, num_points=100, num_queries=1000, out=True)
    t.test_4Sided_1(trials=1, num_points=1000, num_queries=1000, out=True)

if __name__ == '__main__':
    unittest.main()
    # main()

