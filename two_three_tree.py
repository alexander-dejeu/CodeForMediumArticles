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
                print(level_end_node)
        return result_str

    def find_node_value_belongs(self, value, node):
        if len(node.children) == 0:
            return node
        else:
            data_count = len(node.data)
            if data_count == 1:
                if value < node.data[0]:
                    print("go left")
                    return self.find_node_value_belongs(value, node.children[0])
                else:
                    print("go right")
                    return self.find_node_value_belongs(value, node.children[1])
            else:
                # Is it less than any value we have in children?
                if value < node.data[0]:
                    return self.find_node_value_belongs(value, node.children[0])
                elif value > node.data[data_count - 1]:
                    return self.find_node_value_belongs(value, node.children[len(node.children) - 1])
                else:
                    print("mmm")
                    for index in range(data_count - 1):
                        print(index)
                        if value >= node.data[index] and value < node.data[index + 1]:
                            return self.find_node_value_belongs(value, node.children[index+1])
                    return self.find_node_value_belongs(value, node.children[data_count - 1])

    def split_node(self, value, node):
        if node == self.root:
            if len(node.children) == 4:
                # this means there are child relationships to worry about
                # if node.data[0] > value:
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
                # TODO: This doesnt actually work?
                node.add_data(value)
                data_to_promote = node.data[1]
                new_root = Node(data_to_promote)
                node_left = Node(node.data[0])
                node_right = Node(node.data[2])

                node_left.parent_node = new_root
                node_right.parent_node = new_root

                new_root.children = [node_left, node_right]

                self.root = new_root

                print("got to make a new root")
        else:
            print(node)
            node.add_data(value)
            data_to_promote = node.data[1]
            node.data.remove(node.data[1])

            if len(node.parent_node.data) == 1:
                if data_to_promote >= node.parent_node.data[0]:
                    print("new data goes on right")
                    print("AEX")
                    print(len(node.children))
                    node_middle, node_right = Node(node.data[0]), Node(node.data[1])
                    node_right.parent_node = node.parent_node
                    node_middle.parent_node = node.parent_node
                    if len(node.children) != 0:
                        node.children[0].parent_node = node_middle
                        node.children[1].parent_node = node_middle
                        node.children[2].parent_node = node_right
                        node.children[3].parent_node = node_right

                        node_middle.children = [node.children[0], node.children[1]]
                        node_right.children = [node.children[2], node.children[3]]

                    new_children = [node.parent_node.children[0], node_middle, node_right]
                    node.parent_node.children = new_children

                    node.parent_node.add_data(data_to_promote)
                else:

                    node_left, node_middle = Node(node.data[0]), Node(node.data[1])
                    node_left.parent_node = node.parent_node
                    node_middle.parent_node = node.parent_node
                    if len(node.children) != 0:
                        node.children[0].parent_node = node_left
                        node.children[1].parent_node = node_left
                        node.children[2].parent_node = node_middle
                        node.children[3].parent_node = node_middle

                        node_left.children = [node.children[0], node.children[1]]
                        node_middle.children = [node.children[2], node.children[3]]

                    new_children = [node_left, node_middle, node.parent_node.children[1]]

                    node.parent_node.children = new_children
                    node.parent_node.add_data(data_to_promote)
            else:
                if data_to_promote >= node.parent_node.data[0]:
                    print("new data goes on right")
                    print("here we fuck up?")
                    print(node)
                    new_m_node = Node(node.data[0])
                    new_r_node = Node(node.data[1])
                    new_m_node.parent_node = node.parent_node
                    new_r_node.parent_node = node.parent_node

                    node.parent_node.children.remove(node)
                    node.parent_node.children.append(new_m_node)
                    node.parent_node.children.append(new_r_node)

                    print("Do we break the chuldren here?")
                    print(node)
                    # #TODO: I think I can delete the original node :O
                    # print("UPDATEd NODE ", node)
                    # print("UPDATED PAR ", node.parent_node)
                    # print("R Child", new_r_node)
                    # Split current node into two (no middle element)
                    # delete old child connection and replace with 2 new
                    self.split_node(data_to_promote, node.parent_node)
                else:
                    # Split the current node into 2 and push up the middle?
                    print("NODE ", node)
                    print("PAR ", node.parent_node)
                    new_l_node = Node(node.data[0])
                    new_r_node = Node(node.data[1])
                    new_l_node.parent_node = node.parent_node
                    new_r_node.parent_node = node.parent_node

                    node.parent_node.children.remove(node)
                    node.parent_node.children.insert(0, new_r_node)
                    node.parent_node.children.insert(0, new_l_node)

                    #TODO: I think I can delete the original node :O
                    print("UPDATEd NODE ", node)
                    print("UPDATED PAR ", node.parent_node)
                    print("R Child", new_r_node)
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
        print("INSERT: " + str(value))
        # 1. If the tree is empty
        if self.root is None:
            self.root = Node(value)
            return

        # 2. Find leaf where value belongs
        add_to_leaf = self.find_node_value_belongs(value, self.root)
        print(add_to_leaf)

        # 3. If leaf only has one value put the new value there!
        if len(add_to_leaf.data) == 1:
            add_to_leaf.add_data(value)
            return

        # 4. If leaf has more than 2 elements. Split and promote median to parent
        else:
            # 5. Repeat on the parent - worse case form a new root.
            self.split_node(value, add_to_leaf)

    def search(self, value):
        pass


test_tree = TwoThreeTree()

test_tree.insert(4)
test_tree.insert(30)
test_tree.insert(7)
test_tree.insert(5)
test_tree.insert(3)
test_tree.insert(6)
test_tree.insert(2)
test_tree.insert(36)
# print("***********Proof it can fill up 2 depth*************")
# print(test_tree.root)
# print(test_tree.root.children[0])
# print(test_tree.root.children[1])
# print(test_tree.root.children[2])

test_tree.insert(1)
# print("***********Proof it can move right up 3 depth*************")
# print(test_tree.root)
# print(test_tree.root.children[0])
# print(test_tree.root.children[1])
# print("*******************")
# print(test_tree.root.children[0].children[0])
# print(test_tree.root.children[0].children[1])
# print(test_tree.root.children[1].children[0])
# print(test_tree.root.children[1].children[1])
test_tree.insert(40)
# print("***********Proof it can move right up 3 depth*************")
# print(test_tree.root)
# print(test_tree.root.children[0])
# print(test_tree.root.children[1])
# print(test_tree.root.children[1].children[0])
# print(test_tree.root.children[1].children[1])
# print(test_tree.root.children[1].children[2])

test_tree.insert(0)
test_tree.insert(3)
test_tree.insert(25)
test_tree.insert(41)

test_tree.insert(1)
test_tree.insert(0)
test_tree.insert(2)
test_tree.insert(45)



print("***********Proof it can fill up 3 depth*************")
print(test_tree)
# print(test_tree.root)
# print(test_tree.root.children[0])
# print(test_tree.root.children[1])
# print(test_tree.root.children[0].children[0])
print(test_tree.root.children[2])
# print(test_tree.root.children[0].children[2])
