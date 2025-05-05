# Python Algorithms and Data Structures - reallyrandom Directory

This directory contains a collection of Python scripts implementing classic algorithms, data structures, and utility functions. Most scripts are adapted from Jupyter notebooks, include extensive comments, and feature a test block under `if __name__ == "__main__"` for demonstration and verification.

---

## Script Descriptions (with Algorithmic Details, Edge Cases, and Example Outputs)

### stack.py
**Algorithmic Explanation:**
- Implements a stack (Last-In-First-Out, LIFO) using a Python list. The `add` method pushes unique elements (prevents duplicates for demonstration), `pop` removes the top, and `peek` returns the top without removing it. The stack is a fundamental data structure used for parsing, backtracking, and function call management.
- **Time Complexity:** All operations are O(1) except duplicate checking in `add`, which is O(n).
- **Design Choice:** Preventing duplicates is not standard for stacks, but is included here for demonstration.

**Edge Case Handling:**
- Popping or peeking from an empty stack raises `IndexError`.
- Adding a duplicate returns `False` and does not modify the stack.

**Example Output:**
```
Initial stack: Stack([])
Stack after adding elements: Stack(['Mon', 'Fri', 'Tue', 'Thu'])
First top of stack: Thu
Stack after attempting to add duplicate 'Thu': Stack(['Mon', 'Fri', 'Tue', 'Thu', 'Sat'])
Second top of stack: Sat
Popped: Sat
Stack after pop: Stack(['Mon', 'Fri', 'Tue', 'Thu'])
Current top: Thu
Stack size: 4
```

### linked_list_queue.py
**Algorithmic Explanation:**
- Implements a queue (First-In-First-Out, FIFO) using a singly linked list. The `append` method enqueues at the tail, and `pop` dequeues from the head. Maintains head/tail pointers for O(1) enqueue/dequeue. Useful for scheduling, buffering, and breadth-first search.
- **Time Complexity:** O(1) for enqueue and dequeue.
- **Design Choice:** Linked list avoids resizing overhead of array-based queues.

**Edge Case Handling:**
- Popping from an empty queue raises `IndexError`.
- Handles queue initialization with or without starting values.

**Example Output:**
```
Initial queue: LinkedListQueue([])
Queue after enqueuing elements: LinkedListQueue([Mon, Fri, Tue, Thu])
First front of queue: Mon
Queue after enqueuing 'Sat': LinkedListQueue([Mon, Fri, Tue, Thu, Sat])
Second front of queue: Mon
Dequeued: Mon
Queue after dequeue: LinkedListQueue([Fri, Tue, Thu, Sat])
Current front: Fri
Queue size: 4
```

### quicksort.py
**Algorithmic Explanation:**
- Implements recursive quicksort (not in-place). Selects the first element as pivot, partitions into less, equal, and greater sublists, recursively sorts sublists, and concatenates results. Quicksort is efficient for large, unsorted lists and is widely used in practice.
- **Time Complexity:** Average O(n log n), worst-case O(n^2) (rare with good pivots).
- **Design Choice:** Not in-place for clarity; in-place versions are more space-efficient but more complex.

**Edge Case Handling:**
- Handles empty and single-element lists (returns as-is).

**Example Output:**
```
Original array: [12, 4, 5, 6, 7, 3, 1, 15]
Sorted array: [1, 3, 4, 5, 6, 7, 12, 15]
```

### remove_elements.py
**Algorithmic Explanation:**
- Provides two in-place algorithms for removing all instances of a value from a list:
  - `remove_element`: Preserves order by shifting non-targets forward.
  - `remove_element2`: Swaps target with end, does not preserve order, but is more efficient if the value is rare.
- **Time Complexity:** O(n) time, O(1) space.
- **Design Choice:** Both methods are standard for in-place removal; the second is optimal for rare removals.

**Edge Case Handling:**
- Handles empty lists, lists with all/none/only the target value.

**Example Output:**
```
After remove_element (Alt 1): [1, 2, 3, 5] Length: 4
After remove_element2 (Alt 2): [5, 1, 2, 3] Length: 4
```

### rabinkarp_needles.py
**Algorithmic Explanation:**
- Implements Rabin-Karp substring search using a rolling hash. Computes hash for the needle and sliding windows in the haystack, compares hashes, and checks for matches. Efficient for multiple pattern searches.
- **Time Complexity:** O(n + m) average, O(nm) worst-case (rare hash collisions).
- **Design Choice:** Uses base 26 and modulus to avoid overflow; assumes lowercase a-z.

**Edge Case Handling:**
- Handles empty needle, needle longer than haystack, and hash collisions.

**Example Output:**
```
Searching for 'def' in 'abcdefghijklmno' -> Index: 3
Searching for 'xyz' in 'abcdefghijklmno' -> Index: -1
```

### prefix_tree_typeahead.py
**Algorithmic Explanation:**
- Implements a Prefix Tree (Trie) for fast prefix search and typeahead. Each node is a dict; words are added character by character. Supports add, remove, membership, iteration, and word count. Tries are used in autocomplete, spell-checking, and IP routing.
- **Time Complexity:** O(L) for add/search/remove (L = word length).
- **Design Choice:** Uses a special key to mark word ends; counts nodes for stats.

**Edge Case Handling:**
- Handles empty trie, duplicate adds, removing non-existent words.

**Example Output:**
```
Initial trie: prefix: 0 entries in 1 dicts
Trie after adding words: prefix: 5 entries in 13 dicts
'inch' in trie? True
'input' in trie? True
'inside' in trie? False
Trie after removing 'inch': prefix: 4 entries in 13 dicts
'inch' in trie? False
All words in trie: ['in', 'inn', 'input', 'into']
prefix: 4 entries in 13 dicts
```

### lfu_cache.py
**Algorithmic Explanation:**
- LFU (Least Frequently Used) cache with O(1) average `get`/`put`. Uses dicts for key-value, key-frequency, and frequency-to-keys (OrderedDict for LRU within frequency). Evicts least frequently and least recently used key on overflow. Used in memory management and caching systems.
- **Time Complexity:** O(1) average for all operations.
- **Design Choice:** Combines LFU and LRU for fair eviction.

**Edge Case Handling:**
- Handles zero/negative capacity, updating existing keys, and eviction when full.

**Example Output:**
```
Put (1, 1)
Put (2, 2)
Get 1: 1
Put (3, 3)
Get 2: -1
Get 3: 3
Put (4, 4)
Get 1: -1
Get 3: 3
Get 4: 4
```

### reverse_integer.py
**Algorithmic Explanation:**
- Reverses a 32-bit signed integer by converting to string, reversing, and checking for overflow. Handles negative numbers and strips trailing zeros. Used in digit manipulation problems.
- **Time Complexity:** O(d) where d is the number of digits.
- **Design Choice:** String manipulation for clarity; checks for overflow after reversal.

**Edge Case Handling:**
- Handles zero, negative numbers, and overflow (returns 0 if out of 32-bit range).

**Example Output:**
```
reverse(120) = 21
reverse(-123) = -321
reverse(1534236469) = 0
reverse(0) = 0
reverse(1000) = 1
reverse(-100) = -1
reverse(2147483647) = 0
reverse(-2147483648) = 0
```

### rotate_image_90.py
**Algorithmic Explanation:**
- Rotates an n x n matrix 90 degrees clockwise in-place, layer by layer, moving four elements at a time. Used in image processing and games.
- **Time Complexity:** O(n^2) time, O(1) space.
- **Design Choice:** Index manipulation for in-place rotation.

**Edge Case Handling:**
- Handles 2x2, 3x3, 4x4 matrices; does not support non-square matrices.

**Example Output:**
```
Rotated 2x2: [[3, 1], [4, 2]]
Rotated 3x3: [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
Rotated 4x4: [[13, 9, 5, 1], [14, 10, 6, 2], [15, 11, 7, 3], [16, 12, 8, 4]]
```

### rotatearray.py
**Algorithmic Explanation:**
- Rotates an array k steps to the right in-place by shifting elements one by one, k times. Handles k > n by modulo. Used in cyclic buffer and scheduling problems.
- **Time Complexity:** O(n*k) time, O(1) space.
- **Design Choice:** Simple, clear implementation; not optimal for large k.

**Edge Case Handling:**
- Handles k > n, empty arrays, and k = 0.

**Example Output:**
```
After rotating [1, 2, 3, 4] by 3: [2, 3, 4, 1]
After rotating [1, 2, 3, 4, 5, 6, 7] by 2: [6, 7, 1, 2, 3, 4, 5]
After rotating [1, 2, 3] by 5: [2, 3, 1]
```

### shuffle_array.py
**Algorithmic Explanation:**
- Fisher-Yates shuffle for uniform randomization. `shuffle` randomly permutes the array; `reset` restores the original. Used in games, simulations, and randomized algorithms.
- **Time Complexity:** O(n) time, O(n) space for copies.
- **Design Choice:** Ensures unbiased shuffling; stores original for reset.

**Edge Case Handling:**
- Handles empty arrays, repeated shuffles, and reset after shuffle.

**Example Output:**
```
Original array: [1, 2, 3, 4, 5]
Shuffled array: [3, 2, 1, 5, 4]
Reset array: [1, 2, 3, 4, 5]
Shuffled again: [2, 4, 1, 5, 3]
```

### splay_tree.py
**Algorithmic Explanation:**
- Splay Tree (self-adjusting BST). On access, splay operation brings node to root via rotations (zig, zig-zig, zig-zag). Supports insert, search, and pretty print. Splay trees optimize for locality of reference.
- **Time Complexity:** Amortized O(log n) for insert/search; worst-case O(n) for a single operation.
- **Design Choice:** Splaying improves performance for frequently accessed elements.

**Edge Case Handling:**
- Handles search for missing values, duplicate inserts, and empty tree.

**Example Output:**
```
Tree after insertions:
R----25
     L----20
     |    L----10
     |    R----null
     R----40
          L----30
          R----50

Search for 30 (should splay 30 to root):
Found: 30
...
Search for 99 (not in tree):
Not found
...
```

### validanagram_twostrings.py
**Algorithmic Explanation:**
- Checks if two strings are anagrams using a fixed-size count array for ASCII. Increments for s, decrements for t, checks all zero. Used in string comparison and cryptography.
- **Time Complexity:** O(n) time, O(1) space (fixed array size).
- **Design Choice:** Array-based counting is faster than sorting for fixed alphabets.

**Edge Case Handling:**
- Handles empty strings, different lengths, and non-ASCII chars (may not work for Unicode).

**Example Output:**
```
isAnagram('anagram', 'nagaram') = True (expected: True)
isAnagram('rat', 'car') = False (expected: False)
...
```

### binary_heap.py
**Algorithmic Explanation:**
- Min-heap with decrease-key and position tracking. Used for Dijkstra's algorithm. Maintains heap property on add/pop/decreaseKey. Supports efficient priority updates.
- **Time Complexity:** O(log n) for add/pop/decreaseKey.
- **Design Choice:** Position tracking allows O(log n) decrease-key, which is essential for graph algorithms.

**Edge Case Handling:**
- Handles empty heap, decreaseKey for non-existent elements.

**Example Output:**
```
heap:[[id=0, p=0],[id=1, p=inf],[id=2, p=inf],[id=3, p=inf],[id=4, p=inf]], [0, 1, 2, 3, 4]
...
```

### findzerorectangles.py
**Algorithmic Explanation:**
- Finds all rectangles of zeros in a 2D binary matrix. Scans for zeros, marks processed cells, and records rectangle coordinates. Useful in image processing and matrix analysis.
- **Time Complexity:** O(n*m) for n x m matrix.
- **Design Choice:** Marks processed cells to avoid double-counting.

**Edge Case Handling:**
- Handles overlapping rectangles, no zeros, and all zeros.

**Example Output:**
```
Rectangles of zeros (as [row_start, col_start, row_end, col_end]):
[2, 3, 3, 5]
[4, 1, 6, 1]
[6, 3, 7, 6]
```

### heapmerge.py
**Algorithmic Explanation:**
- Uses `heapq.merge` to merge multiple sorted lists into one sorted iterator. Demonstrates efficient k-way merge, as used in external sorting and database systems.
- **Time Complexity:** O(N log k) where N is total elements, k is number of lists.
- **Design Choice:** Uses Python's built-in heapq for efficiency and clarity.

**Edge Case Handling:**
- Handles empty lists, lists of different lengths.

**Example Output:**
```
Generated sorted lists:
List 0: [2, 17, 34, 56, 89]
List 1: [3, 18, 35, 57, 90]
...
Merged:
[2, 3, 17, 18, 34, 35, 56, 57, 89, 90]
```

### heapsort.py
**Algorithmic Explanation:**
- In-place heap sort. Builds max-heap, repeatedly extracts max and heapifies remainder. Used for in-place, comparison-based sorting.
- **Time Complexity:** O(n log n) time, O(1) space.
- **Design Choice:** Heap sort is stable and does not require extra memory.

**Edge Case Handling:**
- Handles empty arrays, already sorted, and reverse-sorted arrays.

**Example Output:**
```
Original array:
[12, 11, 13, 5, 6, 7]
Sorted array is:
5
6
7
11
12
13
```

### removenone.py
**Algorithmic Explanation:**
- Removes `None` values from each row of a 2D list, keeping only non-empty rows. Used in data cleaning and preprocessing.
- **Time Complexity:** O(n*m) for n rows, m columns.
- **Design Choice:** Simple iteration and filtering for clarity.

**Edge Case Handling:**
- Handles all-None rows, empty matrix.

**Example Output:**
```
Original 2D list (with None):
...
Cleaned 2D list (no None, only non-empty rows):
c=[[2.5, 2.5, 2.5], [2.5], [2.5], [6.5, 8.5], [9.0, 2.5], [8.9, 5.5, 8.5]]
```

### removenone_optimized.py
**Algorithmic Explanation:**
- Optimized version of `removenone.py` using list comprehensions for efficiency and clarity. Suitable for large datasets.
- **Time Complexity:** O(n*m).
- **Design Choice:** Pythonic, concise, and efficient.

**Edge Case Handling:**
- Same as above.

**Example Output:**
```
Original 2D list (with None):
...
Cleaned 2D list (no None, only non-empty rows):
c=[[2.5, 2.5, 2.5], [2.5], [2.5], [6.5, 8.5], [9.0, 2.5], [8.9, 5.5, 8.5]]
```

### region.py
**Algorithmic Explanation:**
- Defines a rectangular region for KD-trees/Quad Trees. Supports union, overlap, containment, and point/region operations. Handles coordinate normalization. Used in spatial indexing and computational geometry.
- **Time Complexity:** O(1) for all operations.
- **Design Choice:** Flexible and robust for geometric algorithms.

**Edge Case Handling:**
- Handles degenerate (line/point) regions, negative coordinates.

**Example Output:**
```
(0,0 , 10,10)
...
```

### primecheck.py
**Algorithmic Explanation:**
- Checks if a number is prime using trial division up to sqrt(n). Skips even numbers > 2. Used in cryptography and number theory.
- **Time Complexity:** O(sqrt(n)).
- **Design Choice:** Efficient for small to moderate n; not suitable for very large numbers.

**Edge Case Handling:**
- Handles n < 2, even numbers, and large primes.

**Example Output:**
```
prime_check(2) = True
prime_check(9) = False
prime_check(17) = True
```

### climbing_stairs_leet.py
**Algorithmic Explanation:**
- Dynamic programming for the Climbing Stairs problem. Uses a sliding window to count ways to reach the top, similar to Fibonacci sequence. Used in combinatorics and optimization.
- **Time Complexity:** O(n) time, O(n) space.
- **Design Choice:** Sliding window reduces space for larger step sizes.

**Edge Case Handling:**
- Handles stairs = 1, stairs = 45 (upper bound), invalid input raises ValueError.

**Example Output:**
```
Ways to climb 10 stairs: 89
```

### removeduplicates_sortedarray.py
**Algorithmic Explanation:**
- Removes duplicates from a sorted array in-place, preserving order. Uses two pointers to overwrite duplicates. Used in data deduplication and preprocessing.
- **Time Complexity:** O(n) time, O(1) space.
- **Design Choice:** Efficient for sorted arrays; preserves first occurrence of each value.

**Edge Case Handling:**
- Handles empty arrays, all unique, all duplicates.

**Example Output:**
```
After removeDuplicates: [0, 1, 2, 3, 4] Length: 5
After removeDuplicates (all unique): [1, 2, 3, 4, 5] Length: 5
After removeDuplicates (all duplicates): [7] Length: 1
After removeDuplicates (empty): [] Length: 0
```

### remove_elements_inplace_leet.py
**Algorithmic Explanation:**
- In-place removal of all instances of a value from a list, possibly changing order. Swaps target with end and reduces length. Used in array filtering and memory management.
- **Time Complexity:** O(n) time, O(1) space.
- **Design Choice:** Efficient for rare removals; does not preserve order.

**Edge Case Handling:**
- Handles all/none/some elements to remove, empty list.

**Example Output:**
```
After remove_elements: [5, 2, 2, 4] Length: 4
After remove_elements (no removal): [1, 2, 4, 5] Length: 4
After remove_elements (all removed): [] Length: 0
```

---

Most scripts are self-contained and can be run directly to see example usage and test results. See each script's comments and test block for details. 