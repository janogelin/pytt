# linked_list_queue.py
#
# Simple queue implementation in Python using a singly linked list.
# Adapted from a Jupyter notebook. Includes extensive comments and a test block.
#
# Author: (your name)
#

class LinkedNode:
    """
    Node in a singly linked list for use in the queue.
    """
    def __init__(self, value, tail=None):
        """
        Initialize a node with a value and optional next node.
        Args:
            value: The value to store in the node.
            tail: The next node in the list (default: None).
        """
        self.value = value
        self.next = tail

class LinkedListQueue:
    """
    Queue data structure (FIFO) implemented using a singly linked list.
    Supports append (enqueue) and pop (dequeue) operations.
    """
    def __init__(self, *start):
        """
        Initialize an empty queue, optionally with initial values.
        Args:
            *start: Optional initial values to enqueue.
        """
        self.head = None
        self.tail = None
        for value in start:
            self.append(value)

    def append(self, value):
        """
        Add (enqueue) a value to the end of the queue. O(1) time.
        Args:
            value: The value to add.
        """
        new_node = LinkedNode(value)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def is_empty(self):
        """
        Return True if the queue is empty.
        """
        return self.head is None

    def pop(self):
        """
        Remove and return the value at the front of the queue.
        Returns:
            The value at the front of the queue.
        Raises:
            IndexError: If the queue is empty.
        """
        if self.head is None:
            raise IndexError("pop from empty queue")
        val = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return val

    def __iter__(self):
        """
        Iterate over the values in the queue in FIFO order.
        """
        n = self.head
        while n is not None:
            yield n.value
            n = n.next

    def __repr__(self):
        """
        Return a string representation of the queue.
        """
        if self.head is None:
            return 'LinkedListQueue([])'
        return f'LinkedListQueue([{", ".join(map(str, self))}])'

    def __len__(self):
        """
        Return the number of items in the queue.
        """
        n = self.head
        count = 0
        while n is not None:
            count += 1
            n = n.next
        return count

if __name__ == "__main__":
    # Test block demonstrating queue operations
    q = LinkedListQueue()
    print("Initial queue:", q)
    q.append("Mon")
    q.append("Fri")
    q.append("Tue")
    q.append("Thu")
    print("Queue after enqueuing elements:", q)
    print(f'First front of queue: {q.head.value if not q.is_empty() else None}')
    q.append("Sat")
    print("Queue after enqueuing 'Sat':", q)
    print(f'Second front of queue: {q.head.value if not q.is_empty() else None}')
    print(f'Dequeued: {q.pop()}')
    print("Queue after dequeue:", q)
    print(f'Current front: {q.head.value if not q.is_empty() else None}')
    print(f'Queue size: {len(q)}') 