import unittest
import Coors2D
import math
import random

xcoord = lambda x: x[0]
ycoord = lambda x: x[1]

class TestXarray(unittest.TestCase):

    points_1 = [(random.randint(-10, 10), random.randint(-10, 10)) for \
                x in range(15)]
    points_1 = [(-2, -8), (-1, -8), (1, -8), (10, -7), (-2, -6), (-3, -6), (6, -5), (-10, -3), (-6, -2), (8, -1), (-2, 1), (3, 2), (4, 3), (-4, 7), (-6, 9)]
    points_2 = [(random.randint(-100, 100), random.randint(-100, 100)) for \
                x in range(32)]
    points_3 = [(random.randint(-1000, 1000), random.randint(-1000, 1000)) for \
                x in range(5000)]

    def verify(self, points, printout):
        # Construct coors2d (this is the slowest part)
        coors = Coors2D.COORS2D2Sided(points)
        points = sorted(points, key = ycoord)

        # Make sure all the points are in the xarray
        diff = set(points)-set(coors.xarray)
        assert(len(diff) == 0)

        for k in range(1000):
            rand_index = random.randint(0, len(points)-1)
            # find a legitimate y value here to start - don't do veb tree search for now.
            randy = points[rand_index][1]

            # find a random xvalue in the range
            xmin = min(points, key = xcoord)[0]
            xmax = max(points, key = xcoord)[0]
            randx = random.randint(xmin, xmax)
            
            if printout:           
                print ('Query: x<=%s, y<=%s' %(randx, randy))

            ind = coors.y_to_xarray_chunk_map[randy]
            good_points = []
            all_points = []
            while ind < len(coors.xarray) and coors.xarray[ind][0] <= randx:
                if coors.xarray[ind][1] <= randy:
                    good_points.append(coors.xarray[ind])
                all_points.append(coors.xarray[ind])
                try:
                    self.assertTrue(len(all_points) <= coors.alpha * len(good_points))
                except:
                    print("ERROR")
                    print("Good points have length: % s" % (len(good_points)))
                    print("Total points: % s" % (len(all_points)))

                ind += 1
            if printout:
                print ('Query verified!')


    def test_1(self, printout=False):
        self.verify(self.points_1, printout)

    def test_2(self, printout=False):
        self.verify(self.points_2, printout)

    def test_3(self, printout=False):
        self.verify(self.points_3, printout)


def main():
    t = TestXarray()
    print('--------TEST 1--------')
    t.test_1(True)
    print('--------TEST 2--------')
    t.test_2(True)
    print('--------TEST 3--------')
    t.test_3(True)

if __name__ == '__main__':
    main()

