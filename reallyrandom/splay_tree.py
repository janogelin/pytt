# splay_tree.py
#
# Splay Tree implementation in Python.
# Adapted from a Jupyter notebook. Includes extensive comments and a test block.
#
# Author: (your name)
#

import sys

class Node:
    """
    Node for Splay Tree.
    Each node has a value, and pointers to parent, left, and right children.
    """
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.left = None
        self.right = None

class SplayTree:
    """
    Splay Tree data structure.
    Supports insert, search (with splaying), and pretty print.
    """
    def __init__(self):
        self.root = None

    def _left_rotate(self, x):
        """Left rotate at node x."""
        y = x.right
        if y:
            x.right = y.left
            if y.left:
                y.left.parent = x
            y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        if y:
            y.left = x
        x.parent = y

    def _right_rotate(self, x):
        """Right rotate at node x."""
        y = x.left
        if y:
            x.left = y.right
            if y.right:
                y.right.parent = x
            y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        if y:
            y.right = x
        x.parent = y

    def _splay(self, x):
        """
        Splay the node x to the root of the tree.
        """
        while x.parent:
            if not x.parent.parent:
                # Zig step
                if x.parent.left == x:
                    self._right_rotate(x.parent)
                else:
                    self._left_rotate(x.parent)
            elif x.parent.left == x and x.parent.parent.left == x.parent:
                # Zig-zig step
                self._right_rotate(x.parent.parent)
                self._right_rotate(x.parent)
            elif x.parent.right == x and x.parent.parent.right == x.parent:
                # Zig-zig step
                self._left_rotate(x.parent.parent)
                self._left_rotate(x.parent)
            elif x.parent.left == x and x.parent.parent.right == x.parent:
                # Zig-zag step
                self._right_rotate(x.parent)
                self._left_rotate(x.parent)
            else:
                # Zig-zag step
                self._left_rotate(x.parent)
                self._right_rotate(x.parent)

    def insert(self, data):
        """
        Insert a value into the splay tree and splay the inserted node to the root.
        Args:
            data: The value to insert.
        """
        node = Node(data)
        y = None
        x = self.root
        while x:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right
        node.parent = y
        if not y:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node
        self._splay(node)

    def search(self, data):
        """
        Search for a value in the splay tree. If found, splay it to the root.
        Args:
            data: The value to search for.
        Returns:
            Node if found, else None.
        """
        x = self.root
        while x:
            if data == x.data:
                self._splay(x)
                return x
            elif data < x.data:
                x = x.left
            else:
                x = x.right
        return None

    def print_tree(self):
        """
        Pretty print the splay tree structure.
        """
        def _print_helper(currPtr, indent, last):
            if currPtr:
                sys.stdout.write(indent)
                if last:
                    sys.stdout.write("R----")
                    indent += "     "
                else:
                    sys.stdout.write("L----")
                    indent += "|    "
                print(f'{currPtr.data}')
                _print_helper(currPtr.left, indent, False)
                _print_helper(currPtr.right, indent, True)
        _print_helper(self.root, "", True)

if __name__ == "__main__":
    # Test block demonstrating splay tree operations
    tree = SplayTree()
    # Insert values
    for val in [10, 20, 30, 40, 50, 25]:
        tree.insert(val)
    print("Tree after insertions:")
    tree.print_tree()
    # Search for a value (should splay to root)
    print("\nSearch for 30 (should splay 30 to root):")
    found = tree.search(30)
    if found:
        print(f"Found: {found.data}")
    else:
        print("Not found")
    tree.print_tree()
    # Search for a value not in the tree
    print("\nSearch for 99 (not in tree):")
    found = tree.search(99)
    if found:
        print(f"Found: {found.data}")
    else:
        print("Not found")
    tree.print_tree() 