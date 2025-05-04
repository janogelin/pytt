# stack.py
#
# Simple stack implementation in Python using a list.
# Adapted from a Jupyter notebook. Includes extensive comments and a test block.
#
# Author: (your name)
#

class Stack:
    """
    Stack data structure (LIFO) implemented using a Python list.
    Supports add (push) and peek (top) operations.
    Prevents duplicate entries (for demonstration).
    """
    def __init__(self):
        """
        Initialize an empty stack.
        """
        self.stack = []

    def add(self, data):
        """
        Add (push) an item to the stack if not already present.
        Args:
            data: The item to add.
        Returns:
            bool: True if added, False if already present.
        """
        if data not in self.stack:
            self.stack.append(data)
            return True
        else:
            return False

    def peek(self):
        """
        Return the item at the top of the stack without removing it.
        Returns:
            The top item of the stack.
        Raises:
            IndexError: If the stack is empty.
        """
        if not self.stack:
            raise IndexError("peek from empty stack")
        return self.stack[-1]

    def pop(self):
        """
        Remove and return the item at the top of the stack.
        Returns:
            The top item of the stack.
        Raises:
            IndexError: If the stack is empty.
        """
        if not self.stack:
            raise IndexError("pop from empty stack")
        return self.stack.pop()

    def __len__(self):
        """
        Return the number of items in the stack.
        """
        return len(self.stack)

    def __repr__(self):
        """
        Return a string representation of the stack.
        """
        return f"Stack({self.stack})"

if __name__ == "__main__":
    # Test block demonstrating stack operations
    st = Stack()
    print("Initial stack:", st)
    st.add("Mon")
    st.add("Fri")
    st.add("Tue")
    st.add("Thu")
    print("Stack after adding elements:", st)
    print(f'First top of stack: {st.peek()}')
    st.add("Sat")
    st.add("Thu")  # Duplicate, should not be added
    print("Stack after attempting to add duplicate 'Thu':", st)
    print(f'Second top of stack: {st.peek()}')
    print(f'Popped: {st.pop()}')
    print("Stack after pop:", st)
    print(f'Current top: {st.peek()}')
    print(f'Stack size: {len(st)}') 