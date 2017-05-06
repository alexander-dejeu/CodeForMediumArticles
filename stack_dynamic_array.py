class Stack_Dynamic_Array(object):
    def __init__(self, iterable_data=None):
        self.data = list()
        if iterable_data is not None:
            for data in iterable_data:
                self.push(data)

    def __repr__(self):
        """Return a string representation of this stack"""
        return 'Stack({})'.format(self.length())

    def is_empty(self):
        """Return True if this stack is empty, or False otherwise"""
        return not self.data

    def length(self):
        """Return the number of items in this stack"""
        return len(self.data)

    def push(self, item):
        """Push the given item onto this stack"""
        self.data.insert(0, item)

    def pop(self):
        """Return the top item and remove it from this stack,
        or raise ValueError if this stack is empty"""
        if self.is_empty():
            raise ValueError, 'Stack is empty'
        head = self.peek()
        del self.data[0]
        return head

    def peak(self):
        """Return the top item on this stack without removing it,
        or None if this stack is empty"""
        if self.is_empty():
            return None
        return self.data[0]
