from LinkedList import LinkedList


class Stack_LinkedList(object):
    def __init__(self, iterable_data=None):
        pass
        # self.data = LinkedList()
        # if iterable_data is not None:
        #     for data in iterable_data:
        #         self.push(data)

    def __repr__(self):
        """Return a string representation of this stack"""
        return 'Stack({})'.format(self.length())

    def is_empty(self):
        """Return True if this stack is empty, or False otherwise"""
        pass

    def length(self):
        """Return the number of items in this stack"""
        pass

    def push(self, item):
        """Push the given item onto this stack"""
        pass

    def pop(self):
        """Return the top item and remove it from this stack,
        or raise ValueError if this stack is empty"""
        pass

    def peek(self):
        """Return the top item on this stack without removing it,
        or None if this stack is empty"""
        pass
