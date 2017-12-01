import unittest
import xarray
import math
import random
from cache.memory import Memory

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
                x in range(1000)]
    points_4 = [(random.uniform(-100, 100), random.uniform(-1000, 1000)) for \
                x in range(2000)]

    # points_3 = [(992, -930), (990, -489), (985, -668), (976, -81), (969, -110), (968, -245), (964, -224), (960, -87), (960, -153), (960, -990), (947, -861)]

    def verify(self, points, x_upper_bound=True, y_upper_bound=True, printout=False):
        # Construct xarray (this is the slowest part)
        alpha = 2
        base_case_length = 10
        memory = Memory()
        points = sorted(points, key = ycoord)

        print("x_upper_bound: ", x_upper_bound)
        print("y_upper_bound: ", y_upper_bound)

        xarr = xarray.XArray(memory, points, alpha, base_case_length, x_upper_bound, y_upper_bound)

        # Make sure all the points are in the xarray
        # diff = set(points)-set(xarr.xarray)
        # assert(len(diff) == 0)

        for k in range(1000):
            if k%1000 == 0 and k > 0:
                print('checked ', k)
            rand_index = random.randint(0, len(points)-1)
            # find a legitimate y value here to start - don't do veb tree search for now.
            randy = points[rand_index][1]

            # find a random xvalue in the range
            xmin = min(points, key = xcoord)[0]
            xmax = max(points, key = xcoord)[0]
            randx = random.uniform(xmin, xmax)
            
            if printout:       
                if x_upper_bound:
                    if y_upper_bound:    
                        print ('Query: x<=%s, y<=%s' %(randx, randy))
                    else:
                        print ('Query: x<=%s, y>=%s' %(randx, randy))
                else:
                    if y_upper_bound:
                        print ('Query: x>=%s, y<=%s' %(randx, randy))
                    else:
                        print ('Query: x>=%s, y>=%s' %(randx, randy))

            ind = xarr.y_to_xarray_chunk_map[randy]

            # Can ignore queries to the "base case" section
            # because those don't have to be dense
            if ind < len(xarr.xarray) - base_case_length:
            # if ind < len(xarr.xarray_points) - base_case_length:
                good_points = []
                all_points = []
                if x_upper_bound:
                    # x_condition = xarr.xarray_points[ind][0] <= randx
                    x_condition = xarr.xarray[ind].key[0] <= randx
                else:
                    # x_condition = xarr.xarray_points[ind][0] >= randx
                    x_condition = xarr.xarray[ind].key[0] >= randx


                # while ind < len(xarr.xarray_points) and x_condition:
                while ind < len(xarr.xarray) and x_condition:
                    if y_upper_bound:
                        # y_condition = xarr.xarray_points[ind][1] <= randy
                        y_condition = xarr.xarray[ind].key[1] <= randy
                    else:
                        # y_condition = xarr.xarray_points[ind][1] >= randy
                        y_condition = xarr.xarray[ind].key[1] >= randy

                    if y_condition:
                        # good_points.append(xarr.xarray_points[ind])
                    # all_points.append(xarr.xarray_points[ind])
                        good_points.append(xarr.xarray[ind].key)
                    all_points.append(xarr.xarray[ind].key)
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
                    # if ind < len(xarr.xarray_points):
                    if ind < len(xarr.xarray):
                        if x_upper_bound:
                            # x_condition = xarr.xarray_points[ind][0] <= randx
                            x_condition = xarr.xarray[ind].key[0] <= randx
                        else:
                            # x_condition = xarr.xarray_points[ind][0] >= randx
                            x_condition = xarr.xarray[ind].key[0] >= randx


            if printout:
                print ('Query verified!')
        print('Succeeded!')


    def test_1(self, x_upper_bound=True, y_upper_bound=True,
                 printout=False):
        self.verify(self.points_1, x_upper_bound, y_upper_bound, printout)

    def test_2(self, x_upper_bound=True, y_upper_bound=True,
                 printout=False):
        self.verify(self.points_2, x_upper_bound, y_upper_bound, printout)

    def test_3(self, x_upper_bound=True, y_upper_bound=True,
                 printout=False):
        self.verify(self.points_3, x_upper_bound, y_upper_bound, printout)
    
    def test_4(self, x_upper_bound=True, y_upper_bound=True,
                 printout=False):
        self.verify(self.points_4, x_upper_bound, y_upper_bound, printout)


def main():
    t = TestXarray()
    # print('--------TEST 1--------')
    # t.test_1(True, True, False)
    # t.test_1(True, False, False)
    # t.test_1(False, True, False)
    # t.test_1(False, False, False)
    # print('--------TEST 2--------')
    # t.test_2(True, True, False)
    # t.test_2(True, False, False)
    # t.test_2(False, True, False)
    # t.test_2(False, False, False)
    # print('--------TEST 3--------')
    # t.test_3(True, True, False)
    # t.test_3(True, False, False)
    # t.test_3(False, True, False)
    # t.test_3(False, False, False)
    print('--------TEST 4--------')
    t.test_4(True, True, False)
    t.test_4(True, False, False)
    t.test_4(False, True, False)
    t.test_4(False, False, True)

if __name__ == '__main__':
    main()

