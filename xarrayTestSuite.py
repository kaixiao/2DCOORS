import unittest
# import Coors2D
import xarray
import math
import random

xcoord = lambda x: x[0]
ycoord = lambda x: x[1]

class TestXarray(unittest.TestCase):

    # points_1 = [(random.randint(-10, 10), random.randint(-10, 10)) for \
    #             x in range(15)]
    points_1 = [(-2, -8), (-1, -8), (1, -8), (10, -7), (-2, -6), (-3, -6), (6, -5), (-10, -3), (-6, -2), (8, -1), (-2, 1), (3, 2), (4, 3), (-4, 7), (-6, 9)]
    # points_2 = [(random.randint(-100, 100), random.randint(-100, 100)) for \
    #             x in range(32)]
    points_2 = [(-84, -80), (92, -75), (-56, -74), (-35, -70), (-34, -67), (11, -65), (39, -63), (-78, -61), (-75, -46), (-33, -42), (-37, -38), (-72, -11), (29, -9), (-94, -8), (22, 2), (-74, 10), (-73, 13), (-47, 17), (85, 26), (57, 32), (21, 38), (67, 38), (85, 52), (-85, 52), (-32, 59), (-91, 67), (21, 71), (19, 73), (24, 85), (58, 86), (41, 96), (43, 97)]
    points_3 = [(random.randint(-1000, 1000), random.randint(-1000, 1000)) for \
                x in range(5000)]

    def verify(self, points, printout):
        # Construct xarray (this is the slowest part)
        alpha = 2
        base_case_length = 10
        points = sorted(points, key = ycoord)
        xarr = xarray.XArray(points, alpha, base_case_length)

        # Make sure all the points are in the xarray
        diff = set(points)-set(xarr.xarray)
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

            ind = xarr.y_to_xarray_chunk_map[randy]

            # Can ignore queries to the "base case" section
            # because those don't have to be dense
            if ind < len(xarr.xarray) - base_case_length:
                good_points = []
                all_points = []
                while ind < len(xarr.xarray) and xarr.xarray[ind][0] <= randx:
                    if xarr.xarray[ind][1] <= randy:
                        good_points.append(xarr.xarray[ind])
                    all_points.append(xarr.xarray[ind])
                    try:
                        self.assertTrue(len(all_points) <= alpha * len(good_points))
                    except:
                        print("ERROR")
                        print("Good points have length: % s" % (len(good_points)))
                        print("Total points: % s" % (len(all_points)))
                        # Stop the code so you can inspect what the error is
                        import pdb
                        pdb.set_trace()
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

