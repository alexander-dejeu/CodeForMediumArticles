# 2-3 Tree
>**TLDR:** “A **2–3 tree** is a **tree data structure**, where every **node** with **children** (internal node) has either two children (2-node) and one data element or three children (3-nodes) and two data elements. According to Knuth, “a B-tree of order 3 is a 2–3 tree.” Nodes on the outside of the tree (leaf nodes) have no children and one or two data elements”
###### Source: https://en.wikipedia.org/wiki/2%E2%80%933_tree

### Still hazy on what a 2-3 tree is or how / why it works?
** Insert shameless plug - ** I wrote a super [in depth article](https://medium.com/@alexdejeu/2-3-trees-9b50e3484a47) with fun gifs, illustrative pictures, and quality emoji use 🔌 💯  Definitely would recommend checking it out!


## Classes
```python
class Node(object):
  def __init__(self, *data, children=None, parent=None):  # ⭐️ Required
    pass

  def __str__(self):  # 🔷 Optional
    pass

  def add_data(self, value):  # ⛑ Helper
    pass

  def is_full(self):  # 🔷 Optional
    pass

  def has_space(self):  # 🔷 Optional
    pass

  def is_leaf(self):  # 🔷 Optional
    pass

  def is_internal(self):  # 🔷 Optional
    pass

```

```python
class TwoThreeTree(object):
  def __init__(self):  # ⭐️ Required
    pass

  def __str__(self):  # 🔷 Optional
    pass

  def level_order_print(self, node):  # 🔷 Optional
    pass

  def find_node_value_belongs(self, value, node):  # ⛑ Helper
    pass

  def split_node(self, node):  # ⛑ Helper
    pass

  def insert(self, value):  # ⭐️ Required
    pass

  def search(self, value):  # ⭐️ Required
    pass
```

## Functions
#### Node
``init`` Going to want to store the nodes data, children, and parent.  May want to consider also having the ability to initialize with multiple pieces of data

``add_data(self, value)`` Insert a given value in the appropriate position and return that position

May want to consider - to write helpers for if the node is full, has space, is a leaf, or is an internal node 🤔

#### TwoThreeTree
``__init__`` May just want to initialize the root here, or maybe handle iterable data and add to the Tree from the start

``level_order_print(self, node)`` Might be useful to implement this function so you can visualize the tree.  **Hint** : Think about using a queue 🎞

``find_node_value_belongs(self, value, node)`` Determine where a value belongs in a tree and return that node.

``split_node(self, node)`` Handle splitting a node when it is overfilled. Rather complicated --> Definitely recommend drawing it out or visualizing what it should be doing using this [awesome website](https://www.cs.usfca.edu/~galles/visualization/BTree.html "Visualizing B-Trees").  Just make sure to handle all of those cases 😼

``insert(self, value)`` Definitely one of the core functions.  It will use split_node and find_node_value_belongs.  The general idea of inserting into a 2-3 tree is:

1️⃣ If the tree is empty, create a node and put value into the node

2️⃣ Otherwise find the leaf node where the value belongs

3️⃣ If the leaf node has only one value, put the new value into the node

4️⃣ If the lead node has more than two values, split the node and promote the median of the three values to parent

5️⃣ If the parent then has tree values, continue to split and promote, forming a new root node if necessary

``search(self, value)`` Very similar to searching through a binary search tree.  See if the data is in the current node otherwise determine which child of the current node *could* have the value being searched for and then move to that node.  Return True if it is found, otherwise return False.
