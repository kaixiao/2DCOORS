import unittest
import veb
from cache.memory import Memory
import math
import random

class TestVEB(unittest.TestCase):
    points_1 = [(-2, -8), (-1, -8), (1, -8), (10, -7), (-2, -6), (-3, -6), \
                (6, -5), (-10, -3), (-6, -2), (8, -1), (-2, 1), (3, 2), \
                (4, 3), (-4, 7), (-6, 9)]

    points_2 = [(-84, -80), (92, -75), (-56, -74), (-35, -70), (-34, -67), \
                (11, -65), (39, -63), (-78, -61), (-75, -46), (-33, -42), \
                (-37, -38), (-72, -11), (29, -9), (-94, -8), (22, 2), \
                (-74, 10), (-73, 13), (-47, 17), (85, 26), (57, 32), (21, 38), \
                (67, 38), (85, 52), (-85, 52), (-32, 59), (-91, 67), (21, 71), \
                (19, 73), (24, 85), (58, 86), (41, 96), (43, 97)]

    points_3 = [(random.randint(-1000, 1000), random.randint(-1000, 1000)) for \
                x in range(5000)]

    # verifies BST invariant at every node
    # checks if depths are correctly assigned
    # checks if tree depth is perfect BST depth
    def verify_BST(self, points, printout):
        node_items = [veb.NodeItem(key=y, data=x) for x, y in points]
        memory = Memory()
        tree = veb.VEB2Sided(memory, node_items)
        frontier = [tree.root]
        max_depth = 0
        # runs BFS and check invariant holds at every node
        for node in frontier:
            if printout:
                print(str(node) + ', ' + str(node._depth))

            if node.left is not None:
                frontier.append(node.left)
                self.assertTrue(node.left.key <= node.key)
                self.assertEqual(node.left._depth, node._depth + 1)
            if node.right is not None:
                frontier.append(node.right)
                self.assertTrue(node.right.key >= node.key)
                self.assertEqual(node.right._depth, node._depth + 1)
            max_depth = max(max_depth, node._depth)
        self.assertEqual(max_depth, int(math.log(len(points), 2)))

    def test_make_BST_1(self, printout=False):
        self.verify_BST(self.points_1, printout)

    def test_make_BST_2(self, printout=False):
        self.verify_BST(self.points_2, printout)

    def test_make_BST_3(self, printout=False):
        self.verify_BST(self.points_3, printout)

    # verifies local depth-1 VEB structure; necessary but not sufficient
    def verify_veb_order(self, points, printout):
        node_items = [veb.NodeItem(key=y, data=x) for x, y in points]
        memory = Memory()
        tree = veb.VEB2Sided(memory, node_items)
        nodes = list(tree.veb_ordered_nodes)
        for i in range(len(nodes)):
            if printout:
                print(str(nodes[i]) + ', ' + str(nodes[i]._depth))

            # checks local structure besides for root and leaves
            if not nodes[i].is_root() and not nodes[i].is_leaf():
                self.assertTrue(nodes[i-1] is nodes[i].parent
                    or nodes[i-2] is nodes[i].parent
                    or nodes[i+1] is nodes[i].left)

    def test_make_veb_order_1(self, printout=False):
        self.verify_veb_order(self.points_1, printout)

    def test_make_veb_order_2(self, printout=False):
        self.verify_veb_order(self.points_2, printout)

    def test_make_veb_order_3(self, printout=False):
        self.verify_veb_order(self.points_3, printout)

    # verifies that predecessor visits nodes in order when shifted by epsilon
    # each time; again, necessary but not sufficient
    def verify_predecessor(self, points, printout):
        node_items = [veb.NodeItem(key=y, data=x) for x, y in points]
        memory = Memory()
        tree = veb.VEB2Sided(memory, node_items)
        nodes = sorted(tree.veb_ordered_nodes, key=lambda z: -z.key)
        epsilon = 1e-5
        
        if printout:
            for i in range(len(nodes)):
                print(nodes[i])

        for i in range(len(nodes)):
            access_node = tree.predecessor(nodes[i].key)
            self.assertEqual(nodes[i].key, access_node.key)

            curr_node = tree.predecessor(nodes[i].key + epsilon)
            self.assertEqual(nodes[i].key, curr_node.key)
            
        self.assertEqual(tree.predecessor(nodes[-1].key - epsilon), None)

    # verifier symmetric to predecessor
    def verify_successor(self, points, printout):
        node_items = [veb.NodeItem(key=y, data=x) for x, y in points]
        memory = Memory()
        tree = veb.VEB2Sided(memory, node_items)
        nodes = sorted(tree.veb_ordered_nodes, key=lambda z: z.key)
        epsilon = 1e-5
        if printout:
            for i in range(len(nodes)):
                print(nodes[i])

        for i in range(len(nodes)):
            access_node = tree.successor(nodes[i].key)
            self.assertEqual(nodes[i].key, access_node.key)

            curr_node = tree.successor(nodes[i].key - epsilon)
            self.assertEqual(nodes[i].key, curr_node.key)
            
        self.assertEqual(tree.successor(nodes[-1].key + epsilon), None)

    def test_predecessor_1(self, printout=False):
        self.verify_predecessor(self.points_1, printout)

    def test_predecessor_2(self, printout=False):
        self.verify_predecessor(self.points_2, printout)

    def test_predecessor_3(self, printout=False):
        self.verify_predecessor(self.points_3, printout)

    def test_successor_1(self, printout=False):
        self.verify_successor(self.points_1, printout)

    def test_successor_2(self, printout=False):
        self.verify_successor(self.points_2, printout)

    def test_successor_3(self, printout=False):
        self.verify_successor(self.points_3, printout)

def main():
    t = TestVEB()
    print('--------BFS on 32 nodes--------')
    print('Values: (y, x), depth')
    t.test_make_BST_2(True)
    print('-----VEB order on 32 nodes-----')
    print('Values: (y, x), depth')
    t.test_make_veb_order_2(True)
    print('----Predecessor on 15 nodes----')
    print('Values: (y, x)')
    t.test_predecessor_1(True)
    print('----Successor on 15 nodes----')
    print('Values: (y, x)')
    t.test_successor_1(True)

if __name__ == '__main__':
    # main()
    unittest.main()
