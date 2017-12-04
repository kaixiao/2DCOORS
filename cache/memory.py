# import numpy as np
from cache.LRU import LRUCache, LRUCacheItem
from Node import Node

DEFAULT_MEM_SIZE = 32
DEFAULT_BLOCK_SIZE = 8

class Block(object):

    def __init__(self, size=DEFAULT_BLOCK_SIZE, data=None):
        self.size = size
        self.set_from_list(data)

    # Takes in a list of length equal to block size
    def set_from_list(self, data):
        assert(len(data) == self.size)
        if data:
            self.data = data
        else:
            self.data = [None] * self.size

    def as_list(self):
        return self.data

    def __eq__(self, other):
        return (self.size == other.size) and \
            (self.data == other.data)

    def __str__(self):
        return str(self.data)


class LRUBlock(LRUCacheItem):

    def __init__(self, index, block):
        LRUCacheItem.__init__(self, index, block)

    def as_list(self):
        return self.item.as_list()

    def __eq__(self, other):
        return (self.key == other.key) and \
            (self.item == other.item)



class Memory(object):

    def __init__(self, memory_size=DEFAULT_MEM_SIZE,
                block_size=DEFAULT_BLOCK_SIZE, array=None):
        assert memory_size and block_size

        if array is None:
            self.disk = []
        else:
            self.disk = array

        self.memory_size = memory_size
        self.block_size = block_size
        self.num_blocks = memory_size//block_size
        self.disk_accesses = 0
        self.cell_probes = 0

        self.set_cache(self.num_blocks)
        self.set_buffer()

        if len(self.disk) % self.block_size != 0:
            self.zero_pad()

    def set_cache(self, cache_size):
        self.cache = LRUCache(cache_size)

    def set_buffer(self):
        # set buffer placeholder padded with zeros
        self.disk += [0] * self.block_size
        self.buffer_count = 0

    # Zero pad to end of memory if it doesn't align
    # NOTE: perhaps pad it with an empty node
    def zero_pad(self):
        self.disk += [0] * (self.block_size - len(self.disk) % self.block_size)

    # Should only be passed in an array of Nodes
    def add_array_to_disk(self, array):
        # initializes each node's memory_index
        assert(len(array) and isinstance(array[0], Node))

        offset = len(self.disk)
        self.disk += array
        for i in range(len(array)):
            array[i].memory_index = offset + i

        if len(self.disk) % self.block_size != 0:
            self.zero_pad()

    # Read the element at the index on disk
    def read(self, index):
        self.update_cache(index//self.block_size)
        self.cell_probes += 1
        return self.disk[index]

    # Figure out if block is already in LRU cache
    # Update cache and number of disk reads
    def update_cache(self, block_index):
        disk_chunk = self.disk[block_index*self.block_size:
                        (block_index+1)*self.block_size]
        if block_index not in self.cache.hash:
            self.disk_accesses += 1
            block = LRUBlock(block_index,
                    Block(self.block_size, disk_chunk))
            self.cache.insertItem(block)

    def update_buffer(self, num_of_items=1):
        self.update_cache(0)
        self.buffer_count += num_of_items 
        if self.buffer_count >= self.block_size:
            self.disk_accesses += self.buffer_count // self.block_size
            self.buffer_count = self.buffer_count % self.block_size

    def get_disk_accesses(self):
        return self.disk_accesses

    def get_cell_probes(self):
        return self.cell_probes

    def reset_stats(self):
        self.disk_accesses = 0
        self.cell_probes = 0

    def write_block(self, index, block):
        raise Exeception("Writes are not supported yet.")
        self.disk_accesses += 1
        self.disk[index*self.block_size:(index+1)*self.block_size] = block.as_list()

def main():
    # test that disk_accesses is tracked correctly
    mem = Memory(array=list(range(1,1000)))
    for i in range(240):
        mem.read(i)
    print(mem.disk_accesses)
    for i in range(25,30):
        mem.read(i)
    for i in range(5, 9):
        mem.read(i)
    print(mem.disk_accesses)
    print(mem.cache.hash.keys())
    for i in range(64):
        mem.read(i)
        if i % 8 == 0:
            print(mem.cache.hash.keys())
    print(mem.num_blocks)
    print(mem.disk_accesses)


if __name__ == "__main__":
    main()
