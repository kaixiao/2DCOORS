from Coors2D import *
from cache.memory import Memory
import random as rd
from benchmark import *

# test with different memory configs
# different point and box distributions
# different data structures

def generate_memory():
    MBpairs = [(128, 8), (1024, 8), (16384, 64)]
    return [Memory(x[0], x[1]) for x in MBpairs]

def generate_points():
    points_sets = []
    points_1 = [(rd.uniform(-100, 100), rd.uniform(-100, 100)) for \
         x in range(1000)]
    points_2 = [(rd.uniform(-10000, 10000), rd.uniform(-10000, 10000)) for \
         x in range(1000)]

    points_sets.append(points_1)
    points_sets.append(points_2)
    return points_sets

def generate_boxes():
    boxes = []
    for i in range(5):
        x_min = rd.uniform(-1200, 1200)
        x_max = rd.uniform(-1200, 1200)
        x_min = min(x_min, x_max)
        x_max = max(x_min, x_max)
        y_min = rd.uniform(-1200, 1200)
        y_max = rd.uniform(-1200, 1200)
        y_min = min(y_min, y_max)
        y_max = max(y_min, y_max)
        boxes.append([x_min, x_max, y_min, y_max])
    return boxes

def evaluation(points, boxes, memory, data_structure):
    constructed_ds = data_structure(memory, points)
    for box in boxes:
        constructed_ds.query(box[0], box[1], box[2], box[3])
    print(" Datastructure: %s " % (data_structure))
    print(" Queries: {}, \
            Disk accesses: {}, \
            Cell probes: {}\n".format(
            len(boxes), 
            memory.get_disk_accesses(), 
            memory.get_cell_probes()))

def main():
    # Ideally, also want to test for COORS2D4Sided with different
    # alpha and base_case parameters
    data_structures = [ NaiveStruct, 
                        SortedXVEBTree, 
                        # SimpleRangeTree, 
                        COORS2D4Sided]

    boxes = generate_boxes()

    points_sets = generate_points()
    memories = generate_memory()
    
    i = 1
    for points in points_sets:
        for memory in memories:
            print("CONFIGURATION %s" % (i))
            for data_structure in data_structures:
                evaluation(points, boxes, memory, data_structure)
            i += 1
            
if __name__ == '__main__':
    main()

    