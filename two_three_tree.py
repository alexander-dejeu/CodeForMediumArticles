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


    def split_node(self, value, node):
        if node == self.root:
            #TODO: This doesnt actually work?
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
                else:
                    node_left, node_middle = Node(node.data[0]), Node(node.data[1])
                    node_left.parent_node = node.parent_node
                    node_middle.parent_node = node.parent_node
                    new_children = [node_left, node_middle]
                    for item in node.parent_node.children:
                        new_children.append(item)
                    del new_children[2]
                    node.parent_node.children = new_children
                    node.parent_node.add_data(data_to_promote)
            else:
                self.split_node(data_to_promote, node.parent_node)
            print("yeah just push that shit up")


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
        print("INSERT: " +str(value))
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

        else:
            self.split_node(value, add_to_leaf)
        # 4. If leaf has more than 2 elements. Split and promote median to parent

        # 5. Repeat on the parent - worse case form a new root.
        pass

    def search(self, value):
        pass




test_tree = TwoThreeTree()
test_tree.insert(4)
# print(test_tree)

test_tree.insert(30)
# print(test_tree)
# print(test_tree.root)

test_tree.insert(7)
# print(test_tree)
# print(test_tree.root)


test_tree.insert(5)
# print("************************")
# print(test_tree.root.children[0])
test_tree.insert(3)

# print("************************")
# print(test_tree.root)
test_tree.insert(6)
# print("**********Proper Middle Element Finding**********")
# print(test_tree.root)

test_tree.insert(2)
test_tree.insert(36)
# print("***********Proof it can fill up 2 depth*************")
# print(test_tree.root)
print("1111111111111")
print(test_tree.root.children[0])
print("3333333333333")
print(test_tree.root.children[1])
print("222222222222")
print(test_tree.root.children[2])

test_tree.insert(1)
print("***********Proof it can move right up 3 depth*************")
print(test_tree.root)
print(test_tree.root.children[0])
