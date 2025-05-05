# rabinkarp_needles.py
#
# Rabin-Karp substring search implementation in Python.
# Adapted from a Jupyter notebook. Includes extensive comments and a test block.
#
# Author: (your name)
#

class Solution:
    """
    Implements Rabin-Karp substring search algorithm for finding the first occurrence
    of a substring (needle) in a string (haystack) using rolling hash.
    """
    def strStr(self, haystack: str, needle: str) -> int:
        """
        Return the index of the first occurrence of needle in haystack, or -1 if not found.
        Args:
            haystack (str): The string to search in.
            needle (str): The substring to search for.
        Returns:
            int: The index of the first occurrence, or -1 if not found.
        """
        L, n = len(needle), len(haystack)
        if L > n:
            # If needle is longer than haystack, it can't be found
            return -1

        # Base value for the rolling hash function (number of possible characters)
        a = 26
        # Modulus value for the rolling hash to avoid integer overflow
        modulus = 2**31

        # Helper lambdas to convert characters to integers (assuming lowercase a-z)
        h_to_int = lambda i: ord(haystack[i]) - ord('a')
        needle_to_int = lambda i: ord(needle[i]) - ord('a')

        # Compute the hash of the first window of haystack and the needle
        h = ref_h = 0
        for i in range(L):
            h = (h * a + h_to_int(i)) % modulus
            ref_h = (ref_h * a + needle_to_int(i)) % modulus
        if h == ref_h:
            # If the initial hashes match, return 0
            return 0

        # Precompute a^L % modulus for use in rolling hash
        aL = pow(a, L, modulus)
        # Slide the window over haystack, updating the hash in O(1) time
        for start in range(1, n - L + 1):
            # Remove the leftmost character and add the new rightmost character
            h = (h * a - h_to_int(start - 1) * aL + h_to_int(start + L - 1)) % modulus
            if h == ref_h:
                # If the hash matches, return the current start index
                return start

        # If no match is found, return -1
        return -1

if __name__ == "__main__":
    # Test block demonstrating Rabin-Karp substring search
    haystack = "abcdefghijklmno"
    needle = "def"
    sol = Solution()
    result = sol.strStr(haystack, needle)
    print(f"Searching for '{needle}' in '{haystack}' -> Index: {result}")

    # Additional test: needle not present
    needle2 = "xyz"
    result2 = sol.strStr(haystack, needle2)
    print(f"Searching for '{needle2}' in '{haystack}' -> Index: {result2}") 