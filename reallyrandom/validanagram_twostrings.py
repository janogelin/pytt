# validanagram_twostrings.py
#
# Check if two strings are anagrams (LeetCode style solution).
# Adapted from a Jupyter notebook. Includes extensive comments and a test block.
#
# Author: (your name)
#

class Solution:
    """
    Solution for checking if two strings are anagrams.
    Uses a fixed-size count array for all ASCII characters.
    """
    def isAnagram(self, s: str, t: str) -> bool:
        """
        Check if string t is an anagram of string s.
        Args:
            s (str): The first string.
            t (str): The second string.
        Returns:
            bool: True if t is an anagram of s, False otherwise.
        """
        if len(s) != len(t):
            # If lengths differ, they cannot be anagrams
            return False

        count = [0] * 256  # Array to count occurrences of each ASCII character

        # Count each character in s
        for character in s:
            count[ord(character)] += 1
        # Subtract count for each character in t
        for character in t:
            if count[ord(character)] == 0:
                # If a character in t is not in s or used up, not an anagram
                return False
            count[ord(character)] -= 1
        # If all counts are zero, it's an anagram
        return True

if __name__ == "__main__":
    # Test block demonstrating the solution
    sol = Solution()
    # Test cases
    tests = [
        ("anagram", "nagaram", True),
        ("rat", "car", False),
        ("listen", "silent", True),
        ("hello", "bello", False),
        ("aabbcc", "abcabc", True),
        ("", "", True),
        ("a", "a", True),
        ("a", "b", False),
        ("anagram", "ganaram", True),
    ]
    for s, t, expected in tests:
        result = sol.isAnagram(s, t)
        print(f"isAnagram({s!r}, {t!r}) = {result} (expected: {expected})") 