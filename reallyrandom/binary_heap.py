# binary_heap.py
#
# A simple binary heap (min-heap) implementation in Python.
# This code is adapted from a Jupyter notebook and includes extensive comments.
#
# Author: (your name)
#

class Element:
    """
    Represents an element in the heap with an identifier and a priority value.
    """
    def __init__(self, ident, priority):
        self.ident = ident      # Unique identifier (e.g., vertex index)
        self.priority = priority  # Priority value (e.g., distance in Dijkstra)

    def __repr__(self):
        return f'[id={self.ident}, p={self.priority}]'

class BinaryHeap:
    """
    Min-heap implementation with support for decrease-key and position tracking.
    Useful for algorithms like Dijkstra's shortest path.
    """
    def __init__(self, size, src, infinity):
        """
        Initialize the heap with a given size, source index, and 'infinity' value.
        The heap is filled with Elements with priority 'infinity', except the source
        which is set to priority 0 and placed at the root.
        Args:
            size (int): Number of elements in the heap.
            src (int): Index of the source element (will have priority 0).
            infinity (numeric): Value representing 'infinity' for initial priorities.
        """
        self.ar = [None] * size  # The heap array (stores Element objects)
        self.pos = [None] * size # Maps element idents to their position in the heap
        for ident in range(size):
            self.ar[ident] = Element(ident, infinity)
            self.pos[ident] = ident
        self.n = size  # Current number of elements in the heap

        # Swap src with first one so it is root of heap
        self.pos[0], self.pos[src] = self.pos[src], self.pos[0]

        # Root of heap has distance zero (priority 0)
        self.ar[src] = self.ar[0]
        self.ar[0] = Element(src, 0)

    def isEmpty(self):
        """Return True if the heap is empty."""
        return self.n == 0

    def __len__(self):
        """Return the number of elements in the heap."""
        return self.n

    def pop(self):
        """
        Remove and return the identifier of the element with the smallest priority.
        Repairs the heap after removal.
        Returns:
            int: The identifier of the element with the smallest priority.
        Raises:
            ValueError: If the heap is empty.
        """
        if self.n == 0:
            raise ValueError("Heap is empty.")
        val = self.ar[0].ident
        self.pos[val] = None

        self.n -= 1
        last = self.ar[self.n]
        self.ar[0] = last
        pIdx = 0
        child = pIdx * 2 + 1
        while child < self.n:
            # Select the smaller of two children
            sm = self.ar[child]
            if child + 1 < self.n and sm.priority > self.ar[child + 1].priority:
                child += 1
                sm = self.ar[child]

            # Are we in the right spot?
            if last.priority <= sm.priority:
                break

            # Swap and move up
            self.ar[pIdx] = sm
            self.pos[sm.ident] = pIdx

            pIdx = child
            child = 2 * pIdx + 1

        # Insert into spot vacated by moved element or last one
        self.ar[pIdx] = last
        self.pos[last.ident] = pIdx
        return val

    def add(self, ident, priority):
        """
        Add a new element with the given identifier and priority to the heap.
        Args:
            ident (int): The identifier for the new element.
            priority (numeric): The priority value for the new element.
        """
        i = self.n
        self.n += 1

        # Bubble up to maintain heap property
        while i > 0:
            pIdx = (i - 1) // 2
            p = self.ar[pIdx]
            if priority > p.priority:
                break
            self.ar[i] = p
            self.pos[p.ident] = i
            i = pIdx

        self.ar[i] = Element(ident, priority)
        self.pos[ident] = i

    def decreaseKey(self, ident, newPriority):
        """
        Decrease the priority of an existing element in the heap.
        Caller must ensure newPriority is less than the current priority.
        Args:
            ident (int): The identifier of the element to update.
            newPriority (numeric): The new, lower priority value.
        """
        size = self.n
        # Remove the element from the heap by setting n to its position
        self.n = self.pos[ident]
        # Add it back with the new, lower priority
        self.add(ident, newPriority)
        # Restore the heap size
        self.n = size

    def __repr__(self):
        """
        Return a string representation of the heap (for debugging).
        """
        return 'heap:[' + ','.join(map(str, self.ar[:self.n])) + '], ' + str(self.pos)

# Example usage (uncomment to test):
# heap = BinaryHeap(5, 0, float('inf'))
# print(heap)
# heap.decreaseKey(2, 1)
# print(heap)
# print(heap.pop())
# print(heap) 