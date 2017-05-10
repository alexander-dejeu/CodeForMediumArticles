import queue  # Uses queue for BFS of printing tree


class Node(object):
    # Node(a,b,c, children)
    def __init__(self, *data, children=None, parent=None):
        self.data = list(data)

        if children is not None:
            self.children = list(children)
        else:
            self.children = []

        self.parent = parent

    def add_data(self, value):
        self.data.append(value)
        self.data.sort()

    def is_full(self):
        return len(self.data) >= 3

    def has_space(self):
        return len(self.data) < 2

    def is_leaf(self):
        return len(self.children) == 0

    def is_internal(self):
        return len(self.children) > 0

    # Use __repr__ for printing the code that a programer could use
    # def __repr__(self):
    #     repr_str = "Node()"
    #     return "Alex should make the programer looking code"
    # Put this for the pretty side
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

        level_end_node = node
        while not level_q.empty():
            node = level_q.get()
            result_str += str(node.data) + ", "
            for i in range(len(node.children)):
                child = node.children[i]
                level_q.put(child)
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
        data_to_promote = node.data[1]
        node.data.remove(node.data[1])
        new_l_node = Node(node.data[0])
        new_r_node = Node(node.data[1])

        if node == self.root:
            new_root = Node(data_to_promote)
            new_l_node.parent = new_root
            new_r_node.parent = new_root

            if node.is_internal():
                # this means there are child relationships to worry about
                # Basically NOT Spliting the intial root
                node.children[0].parent = new_l_node
                node.children[1].parent = new_l_node
                node.children[2].parent = new_r_node
                node.children[3].parent = new_r_node

                new_l_node.children = [node.children[0], node.children[1]]
                new_r_node.children = [node.children[2], node.children[3]]

            new_root.children = [new_l_node, new_r_node]
            self.root = new_root

        else:
            # Not dealing with creating a new root
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

                # There are only two cases becasue we are dealing with 2-3 trees
                if data_to_promote >= node.parent.data[0]:
                    # The split impacted the right Node so leave left alone
                    node.parent.children.insert(1, new_l_node)
                    node.parent.children.insert(2, new_r_node)
                else:
                    # The split impacted the left Node so leave right alone
                    node.parent.children.insert(0, new_l_node)
                    node.parent.children.insert(1, new_r_node)

                node.parent.add_data(data_to_promote) # TODO may want to return index placement
            else:
                # Far right
                if data_to_promote >= node.parent.data[-1]:
                    # Insertion here is to append
                    node.parent.children.insert(2, new_l_node)
                    node.parent.children.insert(3, new_r_node)
                # Far Left
                elif data_to_promote < node.parent.data[0]:
                    node.parent.children.insert(0, new_l_node)
                    node.parent.children.insert(1, new_r_node)
                # Middle element assuming 2-3 tree
                else:
                    node.parent.children.insert(1, new_l_node)
                    node.parent.children.insert(2, new_r_node)
                # Split current node into two (no middle element)
                # delete old child connection and replace with 2 new
                node.parent.add_data(data_to_promote)
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
            if value in cur_node.data:
                return True
            elif len(cur_node.children) == 0:
                return False
            else:
                if value < cur_node.data[0]:
                    cur_node = cur_node.children[0]
                elif value > cur_node.data[-1]:
                    cur_node = cur_node.children[len(cur_node.data)]
                else:
                    for index in range(len(cur_node.data) - 1):
                        if value >= cur_node.data[index] and value < cur_node.data[index + 1]:
                            cur_node = cur_node.children[index+1]
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
