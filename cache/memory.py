# import numpy as np
from cache.LRU import LRUCache, LRUCacheItem

DEFAULT_MEM_SIZE = 128
DEFAULT_BLOCK_SIZE = 8



class Block(object):

    # Takes in a list of length size
    def set_from_list(self, data):
        assert(len(data) == self.size)
        if data:
            self.data = data
        else:
            self.data = [None] * self.size

    def __init__(self, size=DEFAULT_BLOCK_SIZE, data=None):
        self.size = size
        self.set_from_list(data)


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

    def set_cache(self, cache_size):
        self.cache = LRUCache(cache_size)

    # Zero pad to end of memory if it doesn't align
    def zero_pad(self):
        self.disk += [0] * (self.block_size - len(self.disk) % self.block_size)
        assert(len(self.disk) % self.block_size == 0)
        # print("Zero padded end of memory!")

    def __init__(self, array=None, memory_size=DEFAULT_MEM_SIZE,
                block_size=DEFAULT_BLOCK_SIZE):
        if array is None:
            self.disk = []
        else:
            self.disk = array
        self.memory_size = memory_size
        self.block_size = block_size
        self.num_blocks = memory_size//block_size
        self.disk_accesses = 0

        if memory_size and block_size:
            self.set_cache(self.num_blocks)

        if len(self.disk) % self.block_size != 0:
            self.zero_pad()


    def add_array_to_disk(self, array):
        # returns array offset in disk
        offset = len(self.disk)
        self.disk += array
        if len(self.disk) % self.block_size != 0:
            self.zero_pad()
        return offset


    # Read the element at the index on disk
    def read(self, index):
        self.update_cache(index//self.block_size)
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

    # Takes in a Block()
    # FOR NOW: This WILL NOT be used.
    def write_block(self, index, block):
        self.disk_accesses += 1
        self.disk[index*self.block_size:
            (index+1)*self.block_size] = block.as_list()

def main():
    # test that disk_acceses is tracked correctly
    mem = Memory(list(range(1,1000)))
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
