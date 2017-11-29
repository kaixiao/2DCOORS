import unittest
import Coors2D
import random
from cache.memory import Memory

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
                    print('Correct point (%s, %s) not in solution' % (x, y))
                    return False
            else:
                if (x, y) in sol:
                    print('Incorrect point (%s, %s) in solution' % (x, y))
                    return False
        return True

    def verify_2Sided_randomized_queries(self, dirc, suppressed=True):
        x_upper_bound = bool(dirc//2)
        y_upper_bound = bool(dirc%2)

        obj = Coors2D.COORS2D2Sided(self.memory, self.points_1, \
                                    x_upper_bound, y_upper_bound)
        
        if not suppressed:
            print("x_upper_bound: ", x_upper_bound)
            print("y_upper_bound: ", y_upper_bound)

        for i in range(100):
            quadrant = (random.uniform(-1200, 1200), random.uniform(-1200, 1200))
            # print("Quadrant:", quadrant)
            # print("Len Solutions:", len(solutions))
            solutions = obj.query(*quadrant)
            if not self.verify_2Sided_solutions(self.points_1, quadrant, solutions, \
                         x_upper_bound, y_upper_bound):
                if not suppressed:
                    print("Test Failed.")
                return False

        if not suppressed:
            print("Test Passed!")
        return True

    def test_2Sided_1(self):
        self.assertTrue(self.verify_2Sided_randomized_queries(1))

    def test_2Sided_2(self):
        self.assertTrue(self.verify_2Sided_randomized_queries(2))

    def test_2Sided_3(self):
        self.assertTrue(self.verify_2Sided_randomized_queries(3))

    def test_2Sided_4(self):
        self.assertTrue(self.verify_2Sided_randomized_queries(4))

    def test_2Sided_total(self, total=10):
        passed = 0
        for i in range(total):
            dirc = random.randint(1,4)
            res = self.verify_2Sided_randomized_queries(dirc)
            if res:
                passed += 1
        print('Passed {} / {} Randomized Tests.'.format(passed, total))
        self.assertEqual(passed, total)

def main():
    t = TestCoors2D()
    t.test_2Sided_total()

if __name__ == '__main__':
    unittest.main()
