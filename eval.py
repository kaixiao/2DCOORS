from Coors2D import *
from cache.memory import Memory
import random as rd
from benchmark import *

XBST_non_veb = lambda memory, points: XBST(memory, points, veb_order=False)
XBST_non_veb.__name__ = 'XBST_non_veb'
RangeTree_non_veb = lambda memory, points: RangeTree(memory, points, veb_order=False)
RangeTree_non_veb.__name__ = 'RangeTree_non_veb'


# test with different memory configs
# different point and box distributions
# different data structures
SMALL_BOX_SIZE=100
LARGE_BOX_SIZE=10000
NUM_POINTS=1000



def generate_memory():
    # MBpairs = [(128, 8), (1024, 8), (16384, 64)]
    MBpairs = [(32, 8)]
    return [Memory(x[0], x[1]) for x in MBpairs]

def generate_points():
    points_sets = []
    points_1 = [(rd.uniform(-SMALL_BOX_SIZE, SMALL_BOX_SIZE), 
                rd.uniform(-SMALL_BOX_SIZE, SMALL_BOX_SIZE)) for \
                x in range(NUM_POINTS)]
    points_2 = [(rd.uniform(-LARGE_BOX_SIZE, LARGE_BOX_SIZE),
                rd.uniform(-LARGE_BOX_SIZE, LARGE_BOX_SIZE)) for \
                x in range(NUM_POINTS)]

    # points_sets.append(points_1)
    points_sets.append(points_2)
    return points_sets

def generate_boxes(num_boxes=100):
    boxes = []
    # Regular boxes
    BIG_SIZE = LARGE_BOX_SIZE/4
    for i in range(num_boxes):
        x_min = rd.uniform(-BIG_SIZE, BIG_SIZE)
        x_max = rd.uniform(-BIG_SIZE, BIG_SIZE)
        x_min = min(x_min, x_max)
        x_max = max(x_min, x_max)
        y_min = rd.uniform(-BIG_SIZE, BIG_SIZE)
        y_max = rd.uniform(-BIG_SIZE, BIG_SIZE)
        y_min = min(y_min, y_max)
        y_max = max(y_min, y_max)
        boxes.append([x_min, x_max, y_min, y_max])
    return boxes

def generate_small_boxes(num_boxes=100):
    boxes = []
    # Small boxes
    SMALL_SIZE = SMALL_BOX_SIZE/2
    for i in range(num_boxes):
        x_min = rd.uniform(-SMALL_SIZE, SMALL_SIZE-1)
        x_max = x_min + rd.uniform(1, SMALL_SIZE-x_min)
        y_min = rd.uniform(-SMALL_SIZE, SMALL_SIZE-1)
        y_max = y_min + rd.uniform(1, SMALL_SIZE-y_min)
        boxes.append([x_min, x_max, y_min, y_max])
    return boxes

def evaluation(points, boxes, memory, ds_builder):
    print("\n-----Running tests for {}-----".format(ds_builder.__name__))
    print("\nConfiguration: {} points, {} queries, B={}, M={}".format(
            len(points), 
            len(boxes), 
            memory.block_size, 
            memory.memory_size))

    # Construct data structure
    ds = ds_builder(memory, points)

    # Reset memory
    memory.reset_stats()
    assert(memory.get_disk_accesses() == 0)
    assert(memory.get_cell_probes() == 0)

    # Perform queries
    for box in boxes:
        ds.query(box[0], box[1], box[2], box[3])

    print("Queries: {}, Disk accesses: {}, Cell probes: {}".format(
            len(boxes), 
            memory.get_disk_accesses(), 
            memory.get_cell_probes()))

def main():
    # Ideally, also want to test for COORS2D4Sided with different
    # alpha and base_case parameters
    data_structures = [ NaiveStruct, 
                        XBST, 
                        XBST_non_veb,
                        RangeTree,
                        RangeTree_non_veb,
                        Coors]

    boxes = generate_boxes(1000)
    small_boxes = generate_small_boxes(1000)

    points_sets = generate_points()
    memories = generate_memory()
    
    # i = 1
    trials = 10

    for points in points_sets:
        for memory in memories:
            for data_structure in data_structures:
                evaluation(points, small_boxes, memory, data_structure)
            # i += 1

    print("Completed eval")

      
if __name__ == '__main__':
    # import cProfile
    # cProfile.run('main()')
    main()
    
