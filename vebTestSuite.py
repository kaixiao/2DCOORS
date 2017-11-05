import unittest
import veb
import math
import random

class TestVEB(unittest.TestCase):
    points_1 = [(random.randint(-10, 10), x) for x in range(15)]
    points_2 = [(random.randint(-100, 100), x) for x in range(32)]
    points_3 = [(random.randint(-10000, 10000), x) for x in range(50000)]

    # verifies BST invariant at every node
    # checks if depths are correctly assigned
    # checks if tree depth is perfect
    def verify_BST(self, points, printout):
        node_items = [veb.NodeItem(key=y, data=x) for x, y in points]
        tree = veb.VEBTree(node_items)
        frontier = [tree.root]
        max_depth = 0
        # runs BFS and check invariant holds at every node
        for node in frontier:
            if printout:
                print(str(node) + ', ' + str(node.depth))

            if node.left is not None:
                frontier.append(node.left)
                self.assertTrue(node.left.key <= node.key)
                self.assertEqual(node.left.depth, node.depth + 1)
            if node.right is not None:
                frontier.append(node.right)
                self.assertTrue(node.right.key >= node.key)
                self.assertEqual(node.right.depth, node.depth + 1)
            max_depth = max(max_depth, node.depth)
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
        tree = veb.VEBTree(node_items)
        nodes = list(tree.veb_ordered_nodes)
        for i in range(len(nodes)):
            if printout:
                print(str(nodes[i]) + ', ' + str(nodes[i].depth))

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
        tree = veb.VEBTree(node_items)
        nodes = sorted(tree.veb_ordered_nodes, key=lambda z: -z.key)
        epsilon = 1e-5
        for i in range(len(nodes)):
            if printout:
                print(nodes[i])

            next_node = tree.predecessor(nodes[i].key - epsilon)
            if i < len(nodes) - 1:
                self.assertEqual(next_node.key, nodes[i+1].key)
                self.assertEqual(next_node.data, nodes[i+1].data)
            else:
                self.assertEqual(next_node, None)

    # verifier symmetric to predecessor
    def verify_successor(self, points, printout):
        node_items = [veb.NodeItem(key=y, data=x) for x, y in points]
        tree = veb.VEBTree(node_items)
        nodes = sorted(tree.veb_ordered_nodes, key=lambda z: z.key)
        epsilon = 1e-5
        for i in range(len(nodes)):
            if printout:
                print(nodes[i])

            next_node = tree.successor(nodes[i].key + epsilon)
            if i < len(nodes) - 1:
                self.assertEqual(next_node.key, nodes[i+1].key)
                self.assertEqual(next_node.data, nodes[i+1].data)
            else:
                self.assertEqual(next_node, None)

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
    main()
    # unittest.main()
