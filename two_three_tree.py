class Node(object):
    def __init__(self, data, children=None, parent_node=None):
        if type(data) is list:
            self.data = data
        else:
            data_list = [data]
            self.data = data_list

        if children is not None:
            self.children = list(children)
        else:
            self.children = []
        self.parent_node = parent_node


class TwoThreeTree(object):
    def __init__(self):
        self.root = None

    def __str__(self):
        self.inorder_print(self.root)
        return "representation"

    def inorder_print(self, node):
        child_count = len(node.children)
        if child_count == 0:
            for value in node.data:
                print(value)
        else:
            for index in xrange(child_count - 1):
                # There is one more child than data so we need to skip
                if index == child_count - 1:
                    self.inorder_print(node.children[index])
                else:
                    self.inorder_print(node.children[index])
                    print(node.data[index])

    def add_node(self, node, value):
        pass

    def insert(self, value):
        ''' 1. If the tree is empty, create a node and put value into the node
            2. Otherwise find the leaf node where the value belongs.
            3. If the leaf node has only one value, put the new value into the
                node
            4. If the leaf node has more than two values, split the node and
                promote the median of the three values to parent.
            5. If the parent then has three values, continue to split and
                promote, forming a new root node if necessary
        '''
        # 1. If the tree is empty
        if self.root is None:
            self.root = Node(value)

        # 2. Find leaf where value belongs

        # 3. If leaf only has one value put the new value there!

        # 4. If leaf has more than 2 elements. Split and promote median to parent

        # 5. Repeat on the parent - worse case form a new root.
        pass

    def search(self, value):
        pass




test_tree = TwoThreeTree()
test_tree.insert(4)
print(test_tree)
