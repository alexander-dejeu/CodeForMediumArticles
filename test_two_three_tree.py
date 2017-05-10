from two_three_tree import TwoThreeTree, Node
import unittest


class NodeTest(unittest.TestCase):

    def test_init(self):
        data = 1
        node = Node(data)
        assert node.data[0] == data
        assert len(node.data) == 1
        assert len(node.children) == 0
        assert node.parent is None

    def test_init_list_of_data(self):
        data = [2, 3, 4]
        node = Node(*data)
        assert node.data[2] == data[2]
        assert len(node.data) == 3
        assert len(node.children) == 0
        assert node.parent is None

    def test_init_with_args(self):
        node = Node(1, 2, 3)
        assert node.data[2] == 3
        assert len(node.data) == 3
        assert len(node.children) == 0
        assert node.parent is None

    def test_init_full(self):
        parent = Node(3)
        data = 1
        node_children = [Node(2), Node(4)]
        node = Node(data, children=node_children, parent=parent)
        parent.children.append(node)
        assert node.data[0] == 1
        assert node.parent == parent
        assert parent.children[0] == node
        assert len(parent.children) == 1
        assert len(node.children) == 2
        assert len(node.children[0].children) == 0


class TwoThreeTreeTest(unittest.TestCase):
    def test_init(self):
        ttt = TwoThreeTree()
        assert ttt.root is None

    def test_first_root(self):
        ttt = TwoThreeTree()
        ttt.insert(4)
        assert ttt.root is not None
        assert ttt.root.data[0] == 4
        assert len(ttt.root.data) == 1
        assert ttt.root.parent is None
        assert len(ttt.root.children) == 0

    def test_first_split(self):
        ttt = TwoThreeTree()
        ttt.insert(4)
        ttt.insert(30)
        # It is important that the values remain sorted so going to Check
        assert ttt.root.data[0] == 4
        assert ttt.root.data[1] == 30

        ttt.insert(7)
        assert len(ttt.root.data) == 1
        assert ttt.root.data[0] == 7
        assert len(ttt.root.children) == 2
        assert ttt.root.children[0].data[0] == 4
        assert ttt.root.children[0].parent is ttt.root

        assert ttt.root.children[1].data[0] == 30
        assert ttt.root.children[1].parent is ttt.root

    def test_split_leaf(self):
        ttt = TwoThreeTree()
        ttt.insert(4)
        ttt.insert(30)
        ttt.insert(7)
        ttt.insert(5)
        ttt.insert(3)

        assert len(ttt.root.children[0].data) == 1
        assert len(ttt.root.children[1].data) == 1
        assert len(ttt.root.children[2].data) == 1

        assert ttt.root.children[0].parent is ttt.root
        assert ttt.root.children[1].parent is ttt.root
        assert ttt.root.children[2].parent is ttt.root

        assert len(ttt.root.data) == 2
        assert ttt.root.data[0] == 4
        assert ttt.root.data[1] == 7

        assert len(ttt.root.children[0].data) == 1
        assert len(ttt.root.children[1].data) == 1
        assert len(ttt.root.children[2].data) == 1

        assert ttt.root.children[0].data[0] == 3
        assert ttt.root.children[1].data[0] == 5
        assert ttt.root.children[2].data[0] == 30

    def test_full_two_level(self):
        ttt = TwoThreeTree()
        ttt.insert(4)
        ttt.insert(30)
        ttt.insert(7)
        ttt.insert(5)
        ttt.insert(3)
        ttt.insert(6)
        ttt.insert(2)
        ttt.insert(36)
        assert len(ttt.root.children[0].data) == 2
        assert len(ttt.root.children[1].data) == 2
        assert len(ttt.root.children[2].data) == 2
        assert ttt.root.children[0].parent is ttt.root
        assert ttt.root.children[1].parent is ttt.root
        assert ttt.root.children[2].parent is ttt.root

        assert ttt.root.data[0] == 4
        assert ttt.root.data[1] == 7

    def test_full_two_level_split(self):
        ttt = TwoThreeTree()
        ttt.insert(4)
        ttt.insert(30)
        ttt.insert(7)
        ttt.insert(5)
        ttt.insert(3)
        ttt.insert(6)
        ttt.insert(2)
        ttt.insert(36)
        ttt.insert(1)
        assert len(ttt.root.children[0].children[0].data) == 1
        assert len(ttt.root.children[0].children[1].data) == 1
        assert len(ttt.root.children[1].children[0].data) == 2
        assert len(ttt.root.children[1].children[1].data) == 2
        assert len(ttt.root.data) == 1
        assert len(ttt.root.children) == 2
        assert len(ttt.root.children[1].data) == 1

        assert ttt.root.data[0] == 4
        assert ttt.root.children[0].data[0] == 2
        assert ttt.root.children[1].data[0] == 7

        assert ttt.root.children[0].parent is ttt.root
        assert ttt.root.children[1].parent is ttt.root

        assert ttt.root.children[0].children[0].parent is ttt.root.children[0]
        assert ttt.root.children[0].children[1].parent is ttt.root.children[0]

        assert ttt.root.children[1].children[0].parent is ttt.root.children[1]
        assert ttt.root.children[1].children[1].parent is ttt.root.children[1]

    def test_middle_split(self):
        ttt = TwoThreeTree()
        ttt.insert(10)
        ttt.insert(20)
        ttt.insert(30)
        ttt.insert(60)
        ttt.insert(70)
        ttt.insert(50)
        ttt.insert(40)

        assert len(ttt.root.children) == 2
        assert ttt.root.children[0].data[0] == 20
        assert ttt.root.children[1].data[0] == 60

        assert len(ttt.root.children[0].children) == 2
        assert ttt.root.children[0].children[0].data[0] == 10
        assert ttt.root.children[0].children[1].data[0] == 30

        assert len(ttt.root.children[1].children) == 2
        assert ttt.root.children[1].children[0].data[0] == 50
        assert ttt.root.children[1].children[1].data[0] == 70

    def test_fill_full_three_level(self):
        ttt = TwoThreeTree()
        ttt.insert(4)
        ttt.insert(30)
        ttt.insert(7)
        ttt.insert(5)
        ttt.insert(3)
        ttt.insert(6)
        ttt.insert(2)
        ttt.insert(36)
        ttt.insert(1)
        ttt.insert(3)
        ttt.insert(0)
        ttt.insert(1)
        ttt.insert(40)
        ttt.insert(0)
        ttt.insert(2)
        ttt.insert(25)
        ttt.insert(41)
        assert len(ttt.root.children[0].children[0].data) == 2
        assert len(ttt.root.children[0].children[1].data) == 2
        assert len(ttt.root.children[1].children[0].data) == 2
        assert len(ttt.root.children[1].children[1].data) == 2
        assert len(ttt.root.data) == 1
        assert len(ttt.root.children) == 2
        assert len(ttt.root.children[1].data) == 2
        assert ttt.root.children[0].data[0] == 1
        assert ttt.root.children[0].data[1] == 2
        assert ttt.root.children[0].children[0].parent == ttt.root.children[0]

    # At this point we are feeling better with the tests because we know
    # our split function can split a few times up the tree without fail
    def test_full_three_level_split(self):
        ttt = TwoThreeTree()
        ttt.insert(4)
        ttt.insert(30)
        ttt.insert(7)
        ttt.insert(5)
        ttt.insert(3)
        ttt.insert(6)
        ttt.insert(2)
        ttt.insert(36)
        ttt.insert(1)
        ttt.insert(3)
        ttt.insert(0)
        ttt.insert(1)
        ttt.insert(40)
        ttt.insert(0)
        ttt.insert(2)
        ttt.insert(25)
        ttt.insert(41)
        ttt.insert(45)
        # Pushed data up to the root correctly
        assert len(ttt.root.data) == 2
        assert ttt.root.data[0] == 4
        assert ttt.root.data[1] == 36

        # Make sure the 2nd layer data looks right
        assert len(ttt.root.children[0].data) == 2
        assert ttt.root.children[1].data[0] == 7
        assert ttt.root.children[2].data[0] == 41

        # Make sure the childen's parent relationships are correct
        assert ttt.root.children[2].parent is ttt.root
        assert ttt.root.children[2].children[0].parent is ttt.root.children[2]
        assert ttt.root.children[2].children[1].parent is ttt.root.children[2]

        assert ttt.root.children[1].children[0].parent is ttt.root.children[1]
        assert ttt.root.children[1].children[1].parent is ttt.root.children[1]

    def test_search(self):
        ttt = TwoThreeTree()
        ttt.insert(4)
        ttt.insert(30)
        ttt.insert(7)
        ttt.insert(5)
        ttt.insert(3)
        ttt.insert(6)
        ttt.insert(2)
        ttt.insert(36)
        ttt.insert(1)
        ttt.insert(3)
        ttt.insert(0)
        ttt.insert(1)
        ttt.insert(40)
        ttt.insert(0)
        ttt.insert(2)
        ttt.insert(25)
        ttt.insert(41)
        ttt.insert(45)

        assert ttt.search(4) is True
        assert ttt.search(30) is True
        assert ttt.search(7) is True
        assert ttt.search(5) is True
        assert ttt.search(3) is True
        assert ttt.search(6) is True
        assert ttt.search(2) is True
        assert ttt.search(36) is True
        assert ttt.search(1) is True
        assert ttt.search(0) is True
        assert ttt.search(40) is True
        assert ttt.search(25) is True
        assert ttt.search(41) is True
        assert ttt.search(45) is True

        assert ttt.search(12) is False
        assert ttt.search(-4) is False
        assert ttt.search(49) is False
        assert ttt.search(57) is False
        assert ttt.search(101) is False
        assert ttt.search(124) is False


    def test_search_empty_tree(self):
        ttt = TwoThreeTree()


if __name__ == '__main__':
    unittest.main()
