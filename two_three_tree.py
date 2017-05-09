import queue  # Uses queue for BFS of printing tree


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

    def add_data(self, value):
        self.data.append(value)
        self.data.sort()

    def __str__(self):
        data_str = ""
        for item in self.data:
            data_str += str(item) + ","

        children_str = ""
        for item in self.children:
            children_str += str(item.data) + ","

        parent_str = str(self.parent_node)
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
                    level_end_node = node.children[len(node.children) - 1]
        return result_str

    def find_node_value_belongs(self, value, node):
        if len(node.children) == 0:
            return node
        else:
            data_count = len(node.data)
            if value < node.data[0]:
                return self.find_node_value_belongs(value, node.children[0])
            # Is value greater than any existing value in children
            elif value > node.data[data_count - 1]:
                return self.find_node_value_belongs(value, node.children[len(node.children) - 1])
            # Otherwise we have to ping through looking for a valid spot
            else:
                for index in range(data_count - 1):
                    if value >= node.data[index] and value < node.data[index + 1]:
                        return self.find_node_value_belongs(value, node.children[index+1])
                return self.find_node_value_belongs(value, node.children[data_count - 1])

    def split_node(self, value, node):
        if node == self.root:
            if len(node.children) == 4:
                # this means there are child relationships to worry about
                node.add_data(value)
                data_to_promote = node.data[1]
                new_root = Node(data_to_promote)
                node_left, node_right = Node(node.data[0]), Node(node.data[2])
                node_left.parent_node, node_right.parent_node = new_root, new_root

                node.children[0].parent_node = node_left
                node.children[1].parent_node = node_left
                node.children[2].parent_node = node_right
                node.children[3].parent_node = node_right

                node_left.children = [node.children[0], node.children[1]]
                node_right.children = [node.children[2], node.children[3]]

                new_root.children = [node_left, node_right]
                self.root = new_root

            else:
                # Creating the intial root
                node.add_data(value)
                data_to_promote = node.data[1]
                new_root = Node(data_to_promote)
                node_left = Node(node.data[0])
                node_right = Node(node.data[2])

                node_left.parent_node = new_root
                node_right.parent_node = new_root

                new_root.children = [node_left, node_right]

                self.root = new_root

        else:
            # Not dealing with creating a new root
            node.add_data(value)
            data_to_promote = node.data[1]
            node.data.remove(node.data[1])

            if len(node.parent_node.data) == 1:
                    node_one, node_two = Node(node.data[0]), Node(node.data[1])
                    node_one.parent_node = node.parent_node
                    node_two.parent_node = node.parent_node
                    if len(node.children) != 0:
                        node.children[0].parent_node = node_one
                        node.children[1].parent_node = node_one
                        node.children[2].parent_node = node_two
                        node.children[3].parent_node = node_two

                        node_one.children = [node.children[0], node.children[1]]
                        node_two.children = [node.children[2], node.children[3]]

                    new_children = []
                    if data_to_promote >= node.parent_node.data[0]:
                        new_children = [node.parent_node.children[0], node_one, node_two]
                    else:
                        new_children = [node_one, node_two, node.parent_node.children[1]]
                    node.parent_node.children = new_children
                    node.parent_node.add_data(data_to_promote)
            else:
                new_l_node = Node(node.data[0])
                new_r_node = Node(node.data[1])
                new_l_node.parent_node = node.parent_node
                new_r_node.parent_node = node.parent_node

                node.parent_node.children.remove(node)
                if data_to_promote >= node.parent_node.data[0]:
                    node.parent_node.children.append(new_l_node)
                    node.parent_node.children.append(new_r_node)
                else:
                    node.parent_node.children.insert(0, new_r_node)
                    node.parent_node.children.insert(0, new_l_node)
                # Split current node into two (no middle element)
                # delete old child connection and replace with 2 new
                self.split_node(data_to_promote, node.parent_node)

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
        if len(add_to_leaf.data) == 1:
            add_to_leaf.add_data(value)
            return

        # 4. If leaf has more than 2 elements. Split and promote median to parent
        else:
            # 5. Repeat on the parent - worse case form a new root.
            self.split_node(value, add_to_leaf)

    # def search(self, value):
    #     cur_node = self.root
    #     while cur_node is not None:
    #         print(cur_node.data)
    #         if value in cur_node.data:
    #             return True
    #         elif len(cur_node.children) == 0:
    #             return False
    #         else:
    #             if value < cur_node.data[0]:
    #                 cur_node = cur_node.children[0]
    #             elif value > cur_node.data[len(cur_node.data) - 1]:
    #                 cur_node = cur_node.children[len(cur_node.data)]
    #             else:
    #                 for index in range(len(cur_node.data) - 1):
    #                     if value >= cur_node.data[index] and value < cur_node.data[index + 1]:
    #                         cur_node = cur_node.children[index+1]
    #
    #                 cur_node = cur_node.children[len(cur_node.data) - 1]



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
# print(test_tree.search(30))
