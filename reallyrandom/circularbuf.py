# circularbuf.py
#
# A simple circular buffer (ring buffer) implementation in Python.
# Adapted from a Jupyter notebook. Includes extensive comments and a test block.
#
# Author: (your name)
#

class CircularBuffer:
    """
    Circular buffer (ring buffer) with fixed size.
    Supports adding elements, deleting (FIFO), and iteration.
    When full, adding overwrites the oldest element.
    """
    def __init__(self, size):
        """
        Initialize the buffer with a fixed size.
        Args:
            size (int): The maximum number of elements the buffer can hold.
        """
        self.buffer = [None] * size  # Underlying storage
        self.low = 0                 # Index of the oldest element
        self.high = 0                # Index where the next element will be inserted
        self.size = size             # Fixed buffer size
        self.count = 0               # Number of elements currently in the buffer

    def isEmpty(self):
        """Return True if the buffer is empty."""
        return self.count == 0

    def isFull(self):
        """Return True if the buffer is full."""
        return self.count == self.size

    def __len__(self):
        """Return the number of elements in the buffer."""
        return self.count

    def add(self, value):
        """
        Add a value to the buffer. If the buffer is full, overwrite the oldest value.
        Args:
            value: The value to add.
        """
        if self.isFull():
            # Overwrite the oldest value (move low pointer forward)
            self.low = (self.low + 1) % self.size
        else:
            self.count += 1
        self.buffer[self.high] = value
        self.high = (self.high + 1) % self.size

    def delete(self):
        """
        Remove and return the oldest value from the buffer (FIFO).
        Raises:
            Exception: If the buffer is empty.
        Returns:
            The value removed from the buffer.
        """
        if self.count == 0:
            raise Exception("Buffer empty")
        value = self.buffer[self.low]
        self.low = (self.low + 1) % self.size
        self.count -= 1
        return value

    def __iter__(self):
        """
        Iterate over the elements in the buffer in FIFO order.
        """
        idx = self.low
        num = self.count
        while num > 0:
            yield self.buffer[idx]
            idx = (idx + 1) % self.size
            num -= 1

    def __repr__(self):
        """
        Return a string representation of the buffer contents.
        """
        if self.isEmpty():
            return 'circularbuf:[]'
        return 'circularbuf:[' + ','.join(map(str, self)) + ']'

if __name__ == "__main__":
    # Test block demonstrating buffer operations
    buf = CircularBuffer(5)
    print(buf)  # Should be empty
    # Add elements
    for val in [4, 4, 5, 15, 43, 65]:
        buf.add(val)
        print(f"After adding {val}: {buf}")
    print(f"Buffer storage: {buf.buffer}")
    print(f"Low index: {buf.low}, High index: {buf.high}")
    # Add another element to force overwrite
    buf.add(44)
    print(f"After adding 44 (overwrite): {buf}")
    print(f"Buffer storage: {buf.buffer}")
    print(f"Low index: {buf.low}, High index: {buf.high}")
    # Delete two elements
    print(f"Deleted: {buf.delete()}")
    print(f"Deleted: {buf.delete()}")
    print(f"Buffer after deletes: {buf}")
    print(f"Buffer storage: {buf.buffer}") 