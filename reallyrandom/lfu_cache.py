# lfu_cache.py
#
# LFU (Least Frequently Used) Cache implementation in Python.
# Adapted from a Jupyter notebook. Includes extensive comments and a test block.
#
# Author: (your name)
#

import collections

class LFUCache:
    """
    LFU (Least Frequently Used) Cache implementation.
    Supports get and put operations in O(1) time on average.
    """
    def __init__(self, capacity: int):
        """
        Initialize the LFU cache with a given capacity.
        Args:
            capacity (int): Maximum number of items the cache can hold.
        """
        self.cap = capacity
        self.key2val = {}  # Maps key to value
        self.key2freq = {}  # Maps key to its frequency
        self.freq2key = collections.defaultdict(collections.OrderedDict)  # Maps frequency to keys (OrderedDict for LRU within same freq)
        self.minf = 0  # Tracks the minimum frequency in the cache

    def get(self, key: int) -> int:
        """
        Retrieve the value for the given key if present, else return -1.
        Updates the frequency of the key.
        Args:
            key (int): The key to retrieve.
        Returns:
            int: The value associated with the key, or -1 if not found.
        """
        if key not in self.key2val:
            return -1
        oldfreq = self.key2freq[key]
        # Remove key from current frequency's OrderedDict
        self.freq2key[oldfreq].pop(key)
        if not self.freq2key[oldfreq]:
            del self.freq2key[oldfreq]
        # Add key to next frequency's OrderedDict
        self.freq2key[oldfreq + 1][key] = 1
        self.key2freq[key] = oldfreq + 1
        # Update minf if needed
        if self.minf not in self.freq2key:
            self.minf += 1
        return self.key2val[key]

    def put(self, key: int, value: int) -> None:
        """
        Insert or update the value for the given key.
        If the cache exceeds capacity, evict the least frequently used key.
        Args:
            key (int): The key to insert or update.
            value (int): The value to associate with the key.
        """
        if self.cap <= 0:
            return
        if key in self.key2val:
            # Update value and frequency
            self.key2val[key] = value
            self.get(key)  # Update frequency using get logic
            return
        if len(self.key2val) >= self.cap:
            # Evict the least frequently used and least recently used key
            k, _ = self.freq2key[self.minf].popitem(last=False)
            del self.key2val[k]
            del self.key2freq[k]
            if not self.freq2key[self.minf]:
                del self.freq2key[self.minf]
        # Insert new key
        self.key2val[key] = value
        self.key2freq[key] = 1
        self.freq2key[1][key] = 1
        self.minf = 1  # Reset minf to 1 for new key

if __name__ == "__main__":
    # Test block demonstrating LFU cache operations
    cache = LFUCache(2)
    print("Put (1, 1)")
    cache.put(1, 1)
    print("Put (2, 2)")
    cache.put(2, 2)
    print("Get 1:", cache.get(1))    # returns 1
    print("Put (3, 3)")
    cache.put(3, 3)                  # evicts key 2
    print("Get 2:", cache.get(2))    # returns -1 (not found)
    print("Get 3:", cache.get(3))    # returns 3
    print("Put (4, 4)")
    cache.put(4, 4)                  # evicts key 1
    print("Get 1:", cache.get(1))    # returns -1 (not found)
    print("Get 3:", cache.get(3))    # returns 3
    print("Get 4:", cache.get(4))    # returns 4 