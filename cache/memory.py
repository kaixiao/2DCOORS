# import numpy as np
from LRU import LRUCache, LRUCacheItem

DEFAULT_MEM_SIZE = 128
DEFAULT_BLOCK_SIZE = 8



class Block(object):

    # Takes in a list of length size
    def set_from_list(self, data):
        assert(len(data) == self.size)
        if data:
            self.data = data
        else:
            self.data = [None] * size

    def __init__(self, size=DEFAULT_BLOCK_SIZE, data=None):
        self.size = size
        self.set_from_list(data)

        
    def as_list(self):
        return self.data

    def __eq__(self, other):
        return (self.size == other.size) and (self.data == other.data)

    def __str__(self):
        return str(self.data)


class LRUBlock(LRUCacheItem):

    def __init__(self, index, block):
        LRUCacheItem.__init__(self, index, block)

    def as_list(self):
        return self.item.as_list()

    def __eq__(self, other):
        return (self.key == other.key) and (self.item == other.item)



class Memory(object):

    def set_cache(self, cache_size):
        self.cache = LRUCache(cache_size)

    def __init__(self, array, memory_size=DEFAULT_MEM_SIZE, 
                block_size=DEFAULT_BLOCK_SIZE):
        self.disk = array
        self.memory_size = memory_size
        self.block_size = block_size
        self.num_blocks = memory_size//block_size
        self.disk_accesses = 0

        if memory_size and block_size:
            self.set_cache(self.num_blocks)

    def read_block(self, index):
        disk_chunk = self.disk[index*self.block_size:(index+1)*self.block_size]

        if index not in self.cache.hash:
            self.disk_accesses += 1        
        block = LRUBlock(index, Block(self.block_size, disk_chunk))
        self.cache.insertItem(block)
        
        return disk_chunk

    # Takes in a Block()
    def write_block(self, index, block):
        self.disk_accesses += 1
        self.disk[index*self.block_size:(index+1)*self.block_size] = block.as_list()

def main():
    # test that disk_acceses is tracked correctly
    mem = Memory(list(range(1,1000)))
    for i in range(30):
        mem.read_block(i)
    print(mem.disk_accesses)
    for i in range(25,30):
        mem.read_block(i)
    mem.read_block(5)
    mem.read_block(6)
    mem.read_block(7)
    print(mem.disk_accesses)
    print(mem.cache.hash.keys())
    for i in range(8):
        mem.read_block(i)
        print(mem.cache.hash.keys())

    print(mem.num_blocks)
    print(mem.disk_accesses)

    pass

if __name__ == "__main__":
    main()
