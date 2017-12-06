# This class is used for efficient construction of xarray
import random as rd
import math

class SkipListNode(object):
    def __init__(self, key, data, head=False):
        self.key = key
        self.data = data
        self.left = None
        self.right = None
        self.down = None
        self.up = None
        self.head = head
        self.skip = 0 # augmented with number of items skipped

    def tuple(self, flipped=False):
        if flipped:
            return (self.data, self.key)
        return (self.key, self.data)

    def copy(self):
        return SkipListNode(self.key, self.data, self.head)

    def __str__(self):
        return str(self.tuple())


class SkipListHead(SkipListNode):
    def __init__(self):
        SkipListNode.__init__(self, -float('inf'), None, head=True)


class SkipList(object):
    def __init__(self, tuples):
        self.root = SkipListHead()
        self.num_levels = 1
        self.num_nodes = 0

        for key, data in tuples:
            self.insert(key, data)
        
    def predecessors(self, key):
        # return list of tuples (predecessor, rank of predecessor) in each linked 
        # list ordered by level from bottom to top
        curr = self.root
        rank = 0
        res = []
        while curr.down is not None:
            if curr.right is not None and curr.right.key <= key:
                rank += curr.right.skip
                curr = curr.right
            else:
                res.append((curr, rank))
                curr = curr.down

        while curr.right is not None and curr.right.key <= key:
            assert curr.right.skip == 1
            rank += curr.right.skip
            curr = curr.right

        res.append((curr, rank))
        res.reverse()
        return res

    def insert(self, key, data):
        preds, ranks = zip(*self.predecessors(key))
        assert self.num_levels == len(preds)

        node = SkipListNode(key, data)
        prev = None
        i = 0
        while i < math.ceil(math.log(self.num_nodes+1, 2)):
            if i < self.num_levels:
                node.left = preds[i]
                node.right = preds[i].right
                node.skip = ranks[0] + 1 - ranks[i]
                node.left.right = node
                if node.right is not None:
                    node.right.left = node
                    node.right.skip = node.right.skip - node.skip + 1
            else:
                self.make_new_level()
                self.root.right = node
                node.left = self.root
                node.skip = ranks[0] + 1

            node.down = prev
            if prev is not None:
                prev.up = node
            prev = node
            node = node.copy()

            if rd.randint(0, 1) == 0:
                break
            else:
                i += 1

        self.num_nodes += 1

    def delete(self, key):
        node = self.predecessors(key)[0][0]
        assert key == node.key

        while node is not None:
            node.left.right = node.right
            if node.right is not None:
                node.right.left = node.left
                node.right.skip += node.skip
            else:
                if node.left.head and self.num_levels > 1:
                    self.root = node.left.down
                    self.num_levels -= 1
            node = node.up

        self.num_nodes -= 1

    def rank(self, key):
        # number of points less than or equal to key
        node, rank = self.predecessors(key)[0]
        return rank

    def to_list(self):
        curr = self.root
        res = []
        while curr.down is not None:
            curr = curr.down

        while curr is not None:
            if not curr.head:
                res.append(curr)
            curr = curr.right
        return res

    def to_lists(self):
        curr = self.root
        res = []
        while curr is not None:
            level = []
            while curr.right is not None:
                if not curr.head:
                    level.append(curr)
                curr = curr.right
            res.append(level)
            curr = curr.down
        return res

    def make_new_level(self):
        new_root = SkipListHead()
        new_root.down = self.root
        self.root.up = new_root
        self.root = new_root
        self.num_levels += 1

def main():
    s = SkipList([(x, x) for x in range(1, 21)])
    print('Expected', 0, 'Returned', s.rank(-1))
    print('Expected', 5, 'Returned', s.rank(5))
    print('Expected', 12, 'Returned', s.rank(12.5))
    print('Expected', 20, 'Returned',  s.rank(30))
    print('Num_levels', s.num_levels)
    print('Num_nodes', s.num_nodes)

if __name__ == '__main__':
    main()
