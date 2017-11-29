import unittest
import Coors2D
import random
from cache.memory import Memory
import time

class TestCoors2D(unittest.TestCase):

    memory = Memory()
    points_1 = [(random.uniform(-1000, 1000), random.uniform(-1000, 1000)) \
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

    def verify_2Sided_randomized_queries(self, dirc, suppressed=True):
        x_upper_bound = bool(dirc//2)
        y_upper_bound = bool(dirc%2)

        obj = Coors2D.COORS2D2Sided(self.memory, self.points_1, \
                                    x_upper_bound, y_upper_bound)
        
        if not suppressed:
            print("x_upper_bound:", x_upper_bound)
            print("y_upper_bound:", y_upper_bound)

        for i in range(20):
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
        return True

    def verify_3Sided_randomized_queries(self, dirc, suppressed=True):
        y_upper_bound = bool(dirc % 2)
        
        obj = Coors2D.COORS2D3Sided(self.memory, self.points_1, y_upper_bound)

        if not suppressed:
            print('y_upper_bound:', y_upper_bound)

        for i in range(10):
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
        return True

    def verify_4Sided_randomized_queries(self, suppressed=True):
        print("Building 4Sided structure...")
        t1 = time.time()
        obj = Coors2D.COORS2D4Sided(self.memory, self.points_1)
        t2 = time.time()
        print("Preprocessing completed in {} seconds.".format(t2-t1))

        for i in range(10):
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
            print("Test Passed!\n")
        return True

    def test_2Sided_0(self):
        self.assertTrue(self.verify_2Sided_randomized_queries(0))

    def test_2Sided_1(self):
        self.assertTrue(self.verify_2Sided_randomized_queries(1))

    def test_2Sided_2(self):
        self.assertTrue(self.verify_2Sided_randomized_queries(2))

    def test_2Sided_3(self):
        self.assertTrue(self.verify_2Sided_randomized_queries(3))

    def test_3Sided_0(self):
        self.assertTrue(self.verify_3Sided_randomized_queries(0))

    def test_3Sided_1(self):
        self.assertTrue(self.verify_3Sided_randomized_queries(1))

    def test_4Sided(self):
        self.assertTrue(self.verify_4Sided_randomized_queries())

def main():
    t = TestCoors2D()
    t.test_4Sided()

if __name__ == '__main__':
    # unittest.main()
    main()

