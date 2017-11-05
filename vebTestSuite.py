import unittest
import veb
import math

class TestVEB(unittest.TestCase):
    points_1 = [(0, x) for x in range(15)]
    points_2 = [(0, x) for x in range(32)]
    points_3 = [(0, x) for x in range(50000)]

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
            if node.left is not None:
                frontier.append(node.left)
                self.assertTrue(node.left.key <= node.key)
                self.assertEqual(node.left.depth, node.depth + 1)
            if node.right is not None:
                frontier.append(node.right)
                self.assertTrue(node.right.key >= node.key)
                self.assertEqual(node.right.depth, node.depth + 1)
            max_depth = max(max_depth, node.depth)
            if printout:
                print(str(node) + ', ' + str(node.depth))
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
            # checks local structure besides for root and leaves
            if nodes[i].parent is not None and nodes[i].left is not None:
                self.assertTrue(nodes[i-1] is nodes[i].parent
                    or nodes[i-2] is nodes[i].parent
                    or nodes[i+1] is nodes[i].left)
            if printout:
                print(str(nodes[i]) + ', ' + str(nodes[i].depth))

    def test_make_veb_order_1(self, printout=False):
        self.verify_veb_order(self.points_1, printout)

    def test_make_veb_order_2(self, printout=False):
        self.verify_veb_order(self.points_2, printout)

    def test_make_veb_order_3(self, printout=False):
        self.verify_veb_order(self.points_3, printout)


def main():
    t = TestVEB()
    print('Printout values are (node, depth)')
    print('--------BFS on 15 nodes--------')
    t.test_make_BST_1(True)
    print('--------BFS on 28 nodes--------')
    t.test_make_BST_2(True)
    print('-----VEB order on 15 nodes-----')
    t.test_make_veb_order_1(True)
    print('-----VEB order on 28 nodes-----')
    t.test_make_veb_order_2(True)

if __name__ == '__main__':
    # main()
    unittest.main()
