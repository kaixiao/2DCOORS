from Coors2D import *
from cache.memory import Memory
import random as rd
from benchmark import *
import numpy as np
import pandas as pd
import pickle


XBST_non_veb = lambda memory, points: XBST(memory, points, veb_order=False)
XBST_non_veb.__name__ = 'XBST_non_veb'
RangeTree_non_veb = lambda memory, points: RangeTree(memory, points, veb_order=False)
RangeTree_non_veb.__name__ = 'RangeTree_non_veb'


POINT_BOX_SIZE=10000
SMALL_QUERY_BOX_SIZE=100
LARGE_QUERY_BOX_SIZE=POINT_BOX_SIZE*1.2
DEFAULT_NUM_POINTS=1000


def get_default_memory():
    return Memory(32, 8)

def generate_all_memories():
    MBpairs = [(32, 8), (64, 8), (128, 8), (256, 16), (1024, 32)]
    return [Memory(x[0], x[1]) for x in MBpairs]

def generate_points(num_points=DEFAULT_NUM_POINTS):
    points = [(rd.uniform(-POINT_BOX_SIZE, POINT_BOX_SIZE), 
                rd.uniform(-POINT_BOX_SIZE, POINT_BOX_SIZE)) for \
                x in range(num_points)]

    return points

def get_default_points():
    return generate_points(5000)

def generate_all_points():
    all_points = [  generate_points(1000), 
                    generate_points(2000),
                    generate_points(5000),
                    generate_points(10000),
                    generate_points(20000)]
    return all_points

def generate_large_boxes(num_boxes=1000):
    boxes = []
    for i in range(num_boxes):
        x_min = rd.uniform(-LARGE_QUERY_BOX_SIZE, LARGE_QUERY_BOX_SIZE)
        x_max = rd.uniform(-LARGE_QUERY_BOX_SIZE, LARGE_QUERY_BOX_SIZE)
        x_min = min(x_min, x_max)
        x_max = max(x_min, x_max)
        y_min = rd.uniform(-LARGE_QUERY_BOX_SIZE, LARGE_QUERY_BOX_SIZE)
        y_max = rd.uniform(-LARGE_QUERY_BOX_SIZE, LARGE_QUERY_BOX_SIZE)
        y_min = min(y_min, y_max)
        y_max = max(y_min, y_max)
        boxes.append([x_min, x_max, y_min, y_max])
    return boxes

def generate_small_boxes(num_boxes=1000):
    boxes = []
    MAX_OFFSET = POINT_BOX_SIZE - SMALL_QUERY_BOX_SIZE
    # Small boxes
    for i in range(num_boxes):
        x_min = rd.uniform(-SMALL_QUERY_BOX_SIZE, SMALL_QUERY_BOX_SIZE)
        x_max = rd.uniform(-SMALL_QUERY_BOX_SIZE, SMALL_QUERY_BOX_SIZE)
        x_min = min(x_min, x_max)
        x_max = max(x_min, x_max)
        y_min = rd.uniform(-SMALL_QUERY_BOX_SIZE, SMALL_QUERY_BOX_SIZE)
        y_max = rd.uniform(-SMALL_QUERY_BOX_SIZE, SMALL_QUERY_BOX_SIZE)
        y_min = min(y_min, y_max)
        y_max = max(y_min, y_max)
        # Make the box anywhere in the space
        x_offset = rd.uniform(-MAX_OFFSET, MAX_OFFSET)
        y_offset = rd.uniform(-MAX_OFFSET, MAX_OFFSET)
        x_min += x_offset
        x_max += x_offset
        y_min += y_offset
        y_max += y_offset
        boxes.append([x_min, x_max, y_min, y_max])
    return boxes

def generate_all_boxes(num_boxes=1000):
    boxes = dict()
    boxes['smallBoxes'] = generate_small_boxes(num_boxes)
    boxes['bigBoxes'] = generate_large_boxes(num_boxes)
    return boxes

def evaluation(points, boxes, memory, ds_builder):
    print("\n-----Running tests for {}-----".format(ds_builder.__name__))
    # print("\nConfiguration: {} points, {} queries, B={}, M={}".format(
    #         len(points), 
    #         len(boxes), 
    #         memory.block_size, 
    #         memory.memory_size))

    # Construct data structure
    ds = ds_builder(memory, points)

    # Reset memory
    memory.reset_stats()
    assert(memory.get_disk_accesses() == 0)
    assert(memory.get_cell_probes() == 0)

    # Perform queries
    # count = 0
    for box in boxes:
        sol = ds.query(box[0], box[1], box[2], box[3])

    print("Queries: {}, Disk accesses: {}, Cell probes: {}".format(
            len(boxes), 
            memory.get_disk_accesses(), 
            memory.get_cell_probes()))
    return len(boxes), memory.get_disk_accesses(), memory.get_cell_probes()

def main():


    for iteration in range(1,11):
        # Ideally, also want to test for COORS2D4Sided with different
        # alpha and base_case parameters
        data_structures = [ NaiveStruct, 
                            XBST, 
                            XBST_non_veb,
                            RangeTree,
                            RangeTree_non_veb,
                            Coors]

        boxes = generate_all_boxes(10000)
        
        all_num_points = []
        all_block_sizes = []
        all_memory_sizes = []
        all_box_types = []
        all_num_queries = []
        all_num_disk_accesses = []
        all_num_cell_probes = []
        all_data_structures = []


        # Case 1: Fix number of points, vary memory
        points = get_default_points()
        memories = generate_all_memories()
        for memory in memories:
            for box_type in boxes:
                for data_structure in data_structures:
                    queries, disk_accesses, cell_probes = evaluation(points, 
                        boxes[box_type], memory, data_structure)
                    all_num_points.append(len(points))
                    all_block_sizes.append(memory.block_size)
                    all_memory_sizes.append(memory.memory_size)
                    all_box_types.append(box_type)
                    all_num_queries.append(queries)
                    all_num_disk_accesses.append(disk_accesses)
                    all_num_cell_probes.append(cell_probes)
                    all_data_structures.append(data_structure.__name__)
        
        # Case 2: Fix memory config, vary number of points
        memory = get_default_memory()
        all_points = generate_all_points()
        for points in all_points:
            for box_type in boxes:
                for data_structure in data_structures:
                    queries, disk_accesses, cell_probes = evaluation(points, 
                        boxes[box_type], memory, data_structure)
                    all_num_points.append(len(points))
                    all_block_sizes.append(memory.block_size)
                    all_memory_sizes.append(memory.memory_size)
                    all_box_types.append(box_type)
                    all_num_queries.append(queries)
                    all_num_disk_accesses.append(disk_accesses)
                    all_num_cell_probes.append(cell_probes)
                    all_data_structures.append(data_structure.__name__)
        

        d = {   'num points': all_num_points,
                'block size': all_block_sizes,
                'memory size': all_memory_sizes,
                'box type': all_box_types, 
                'num queries': all_num_queries,
                'num disk accesses': all_num_disk_accesses,
                'num cell probes': all_num_cell_probes,
                'data structure': all_data_structures}
        df = pd.DataFrame(data=d)
        # print(df)
        # print(df[lambda df: df['data structure'] == 'Coors'])
        df.to_csv('results/results_%s.csv' % (iteration))
        df.to_pickle('results/results_%s.pkl' % (iteration))
        # So begin by fixing default (num_points, memory configs)
        # Step 1: Vary the memory configs
        # Step 2: Vary the num points
            # In each case, vary the query box sizes
        print("Completed iteration %s" % (iteration))
    print("======================Completed eval=======================")

      
if __name__ == '__main__':
    # import cProfile
    # cProfile.run('main()')
    main()
    
