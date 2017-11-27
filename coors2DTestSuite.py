import unittest
import Coors2D
import random

class TestCoors2D:

    def verify_2sided(self, points, quadrant, solutions, x_upper_bound, y_upper_bound):
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

    def test_COORS2D2Sided(self, dir):
        points = [(random.randint(-1000, 1000), x) for x in range(1005)]
        quadrant = (random.randint(-100, 100), random.randint(-100, 100))
        
        x_upper_bound = bool(dir//2)
        y_upper_bound = bool(dir%2)

        obj = Coors2D.COORS2D2Sided(points, x_upper_bound, y_upper_bound)
        solutions = obj.query(*quadrant)
        # print("Points:", points)
        print("Quadrant:", quadrant)
        print("x_upper_bound: ", x_upper_bound)
        print("y_upper_bound: ", y_upper_bound)
        # print("Len Solutions:", len(solutions))
        
        if self.verify_2sided(points, quadrant, solutions, x_upper_bound, y_upper_bound):
            print("Test Passed!\n")
            return True
        else:
            print("Test Failed\n.")
            return False

def main():
    t = TestCoors2D()
    total = 5 
    passed = 0
    for i in range(total):
        for j in range(4):
            res = t.test_COORS2D2Sided(j)
            if res:
                passed += 1
    print('Passed {} / {} Randomized Tests.'.format(passed, total * 4))

if __name__ == '__main__':
    main()
