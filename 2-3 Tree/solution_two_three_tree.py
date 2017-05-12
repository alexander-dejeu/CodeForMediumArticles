import queue  # Uses queue for BFS of printing tree


class Node(object):
    def __init__(self, *data, children=None, parent=None):
        self.data = list(data)

        if children is not None:
            self.children = list(children)
        else:
            self.children = []

        self.parent = parent

    def add_data(self, value):
        '''Insert the value in the appropriate postition
        return the postition '''
        # We have to intialize with at least one peice of data
        # All nodes need to at least have 1 peice of data
        assert len(self.data) > 0

        # New value is less than anything in data
        if value < self.data[0]:
            self.data.insert(0, value)
            return 0

        # New value is greater than or equal to largest item in data
        elif value >= self.data[-1]:
            data_count = len(self.data)
            self.data.append(value)
            return data_count

        # New value is somewhere between the first and last element
        else:
            for i in range(len(self.data)-1):
                if value >= self.data[i] and value < self.data[i+1]:
                    self.data.insert(i+1, value)
                    return i+1

    def is_full(self):
        # 2-3 tree nodes are overflowing if they have 3 or more peices of data
        return len(self.data) >= 3

    def has_space(self):
        # 2-3 tree nodes only have an open space for data when they have less
        # than 2 nodes.
        return len(self.data) < 2

    def is_leaf(self):
        # Leaves do not have any children by definition
        return len(self.children) == 0

    def is_internal(self):
        # Interal nodes by definition have children
        return len(self.children) > 0

    # TODO: Use __repr__ for printing the code that a programer could use
    # def __repr__(self):

    def __str__(self):
        data_str = ""
        for item in self.data:
            data_str += str(item) + ","

        children_str = ""
        for item in self.children:
            children_str += str(item.data) + ","

        parent_str = str(self.parent)
        return "data: [\n" + data_str + "\n]\nchildren: [\n" + children_str + "\n]\nParent Node: " + parent_str


class TwoThreeTree(object):
    def __init__(self):
        self.root = None

    def __str__(self):
        return self.level_order_print(self.root)

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

    def level_order_print(self, node):
        result_str = ""
        level_q = queue.Queue()
        level_q.put(node)

        level_end_node = node  # variable for keeping track end of levels
        while not level_q.empty():
            node = level_q.get()
            result_str += str(node.data) + ", "

            # Add all children to queue
            for child in node.children:
                level_q.put(child)

            # If we reached the last child we need to print new line
            if node == level_end_node:
                result_str += '\n'
                if len(node.children) != 0:
                    level_end_node = node.children[-1]

        return result_str

    def find_node_value_belongs(self, value, node):
        if node.is_leaf():
            return node
        else:
            data_count = len(node.data)

            # Is value less than any existing value in children
            if value < node.data[0]:
                return self.find_node_value_belongs(value, node.children[0])

            # Is value greater than any existing value in children
            elif value > node.data[-1]:
                return self.find_node_value_belongs(value, node.children[-1])

            # Otherwise we have to ping through looking for a valid spot
            else:
                for index in range(data_count - 1):
                    if value >= node.data[index] and value < node.data[index + 1]:
                        return self.find_node_value_belongs(value, node.children[index+1])
                return self.find_node_value_belongs(value, node.children[data_count - 1])

    def split_node(self, node):
        # The second element is always the middle element because at this
        # point we know this is a leaf with 2 items and we just added another
        # 3 can be generalized to b
        assert len(node.data) == 3
        # Remeber data in the middle node and remove middle node to be promoted
        data_to_promote = node.data[1]
        node.data.remove(node.data[1])

        # Create new left and right nodes to be created from the current node
        new_l_node = Node(node.data[0])
        new_r_node = Node(node.data[1])

        if node == self.root:
            new_root = Node(data_to_promote)
            new_l_node.parent = new_root
            new_r_node.parent = new_root

            if node.is_internal():
                # this means there are child relationships to worry about
                # Basically NOT spliting the intial root
                node.children[0].parent = new_l_node
                node.children[1].parent = new_l_node
                node.children[2].parent = new_r_node
                node.children[3].parent = new_r_node

                new_l_node.children = [node.children[0], node.children[1]]
                new_r_node.children = [node.children[2], node.children[3]]

            new_root.children = [new_l_node, new_r_node]
            self.root = new_root
        # Not dealing with creating a new root
        else:
            # Create new left and right nodes to be created from the current node
            new_l_node.parent = node.parent
            new_r_node.parent = node.parent

            node.parent.children.remove(node)

            if node.parent.has_space():  # was len(parent.data) == 1
                if node.is_internal():  # was != 0
                    node.children[0].parent = new_l_node
                    node.children[1].parent = new_l_node
                    node.children[2].parent = new_r_node
                    node.children[3].parent = new_r_node

                    new_l_node.children = [node.children[0], node.children[1]]
                    new_r_node.children = [node.children[2], node.children[3]]

                inserted_at = node.parent.add_data(data_to_promote)
                # replaced deleted old child with the 2 new one
                node.parent.children.insert(inserted_at, new_l_node)
                node.parent.children.insert(inserted_at + 1, new_r_node)

            else:
                inserted_at = node.parent.add_data(data_to_promote)
                # replaced deleted old child with the 2 new one
                node.parent.children.insert(inserted_at, new_l_node)
                node.parent.children.insert(inserted_at + 1, new_r_node)

                self.split_node(node.parent)

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
            return

        # 2. Find leaf where value belongs
        add_to_leaf = self.find_node_value_belongs(value, self.root)

        # 3. If leaf only has one value put the new value there!
        if add_to_leaf.has_space():
            add_to_leaf.add_data(value)
            return

        # 4. If leaf has more than 2 elements. Split and promote median to parent
        else:
            # 5. Repeat on the parent - worse case form a new root.
            add_to_leaf.add_data(value)
            self.split_node(add_to_leaf)

    def search(self, value):
        cur_node = self.root

        while cur_node is not None:
            # We have found the value at some point in the tree
            if value in cur_node.data:
                return True

            # If we are at a leaf and the above conditional is False
            # then we know this value does not exist in this tree
        elif cur_node.is_leaf() == 0:
                return False

            # Figure out which node to travel to next
            else:
                if value < cur_node.data[0]:
                    cur_node = cur_node.children[0]
                elif value > cur_node.data[-1]:
                    cur_node = cur_node.children[len(cur_node.data)]
                else:
                    for index in range(len(cur_node.data) - 1):
                        if value >= cur_node.data[index] and value < cur_node.data[index + 1]:
                            cur_node = cur_node.children[index+1]
        # If the root is None then return False
        return False


if __name__ == '__main__':
    test_tree = TwoThreeTree()

    test_tree.insert(4)
    test_tree.insert(30)
    test_tree.insert(7)
    test_tree.insert(5)
    test_tree.insert(3)
    test_tree.insert(6)
    test_tree.insert(2)
    test_tree.insert(36)
    test_tree.insert(1)
    test_tree.insert(40)

    test_tree.insert(0)
    test_tree.insert(3)
    test_tree.insert(25)
    test_tree.insert(41)

    test_tree.insert(1)
    test_tree.insert(0)
    test_tree.insert(2)
    test_tree.insert(45)
    print(test_tree)
    print(test_tree.root.children[0].children[0])
    print(test_tree.search(41))
