import unittest
import Coors2D
import random

class TestCoors2D:
    points_1 = [(random.randint(-10, 10), x) for x in range(16)]

    def verify_2sided(self, points, quadrant, solutions):
        sol = set(solutions)
        for x, y in points:
            if x <= quadrant[0] and y <= quadrant[1]:
                if (x, y) not in sol:
                    print(x, y)
                    return False
            else:
                if (x, y) in sol:
                    return False
        return True

    def test_COORS2D2Sided(self):
        points = [(random.randint(-1000, 1000), x) for x in range(1005)]
        quadrant = (random.randint(-100, 100), random.randint(-100, 100))
        obj = Coors2D.COORS2D2Sided(points)
        # import pdb
        # pdb.set_trace()
        solutions = obj.query(*quadrant)
        # print("Points:", points)
        # print("Quadrant:", quadrant)
        # print("Solutions:", solutions)
        if self.verify_2sided(points, quadrant, solutions):
            return "Test Passed!"
        return "Test Failed."

def main():
    t = TestCoors2D()
    print(t.test_COORS2D2Sided())

if __name__ == '__main__':
    main()
