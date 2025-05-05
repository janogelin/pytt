# prefix_tree_typeahead.py
#
# Prefix Tree (Trie) implementation in Python for typeahead suggestions.
# Adapted from a Jupyter notebook. Includes extensive comments and a test block.
#
# Author: (your name)
#

# Special key to mark the end of a word in the trie
WordKey = '\n'  # Any character not 'a'..'z'

def traverse(d, prefix):
    """
    Recursively generate all words in the Prefix Tree (Trie).
    Args:
        d (dict): The current node in the trie.
        prefix (str): The prefix accumulated so far.
    Yields:
        str: Complete words found in the trie.
    """
    for k in d:
        if k == WordKey:
            yield prefix
        else:
            for _ in traverse(d[k], prefix + k):
                yield _

class PrefixTree:
    """
    Prefix Tree (Trie) data structure for efficient prefix-based search and typeahead.
    Supports add, remove, membership test, iteration, and length operations.
    """
    def __init__(self, *start):
        """
        Initialize an empty prefix tree, optionally with initial words.
        Args:
            *start: Optional initial words to add to the trie.
        """
        self.head = {}  # Root node of the trie
        self.count = 0  # Number of words in the trie
        self.numDictionaries = 1  # Number of dictionary nodes (for stats)
        for _ in start:
            self.add(_.lower())

    def add(self, value):
        """
        Add a word to the prefix tree. Returns True if the word was added, False if it was already present.
        Args:
            value (str): The word to add.
        Returns:
            bool: True if the word was added, False if it was already present.
        """
        d = self.head
        while len(value) > 0:
            if value[0] not in d:
                d[value[0]] = {}
                self.numDictionaries += 1
            d = d[value[0]]
            value = value[1:]
        if WordKey in d:
            return False  # Word already present
        d[WordKey] = True  # Mark end of word
        self.count += 1
        return True

    def remove(self, value):
        """
        Remove a word from the prefix tree. Returns True if removed, False if not found.
        Args:
            value (str): The word to remove.
        Returns:
            bool: True if the word was removed, False if not found.
        """
        d = self.head
        while len(value) > 0:
            if value[0] not in d:
                return False  # Word not found
            d = d[value[0]]
            value = value[1:]
        if WordKey not in d:
            return False  # Word not found
        del d[WordKey]
        self.count -= 1
        return True

    def __contains__(self, value):
        """
        Check if a word is contained in the prefix tree.
        Args:
            value (str): The word to check.
        Returns:
            bool: True if the word is present, False otherwise.
        """
        d = self.head
        while len(value) > 0:
            if value[0] not in d:
                return False
            d = d[value[0]]
            value = value[1:]
        return WordKey in d

    def __iter__(self):
        """
        Iterate over all words stored in the prefix tree.
        Yields:
            str: Each word in the trie.
        """
        for _ in traverse(self.head, ''):
            yield _

    def __repr__(self):
        """
        Return a string representation of the prefix tree (stats only).
        Returns:
            str: Stats about the trie.
        """
        return 'prefix: {0:d} entries in {1:d} dicts'.format(
           self.count, self.numDictionaries)

    def __len__(self):
        """
        Return the number of words in the prefix tree.
        Returns:
            int: Number of words.
        """
        return self.count

if __name__ == "__main__":
    # Test block demonstrating prefix tree operations
    trie = PrefixTree()
    print("Initial trie:", trie)
    # Add words
    trie.add('in')
    trie.add('inch')
    trie.add('input')
    trie.add('into')
    trie.add('inn')
    print("Trie after adding words:", trie)
    # Check membership
    print("'inch' in trie?", 'inch' in trie)
    print("'input' in trie?", 'input' in trie)
    print("'inside' in trie?", 'inside' in trie)
    # Remove a word
    trie.remove('inch')
    print("Trie after removing 'inch':", trie)
    print("'inch' in trie?", 'inch' in trie)
    # List all words
    print("All words in trie:", list(trie))
    # Trie stats
    print(repr(trie)) 