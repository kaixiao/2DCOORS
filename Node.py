class NodeItem(object):

    def __init__(self, key, data=None):
        self.key = key
        self.data = data

    def __eq__(self, other):
        return self.key == other.key and self.data == other.data

    def __str__(self):
        return str((self.key, self.data))


class Node(object):

    def __init__(self, memory, node_item):
        self.key = node_item.key
        self.data = node_item.data
        self.memory = memory
        self.memory_index = None 

    def read(self):
        # accesses self through memory model
        if self.memory_index is None:
            raise Exception("Node not added to disk yet.")

        return self.memory.read(self.memory_index)

    def point(self):
        raise Exception("Point() not supported for this Node class.")

