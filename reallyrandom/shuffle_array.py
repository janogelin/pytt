# shuffle_array.py
#
# Shuffle array (LeetCode style solution).
# Adapted from a Jupyter notebook. Includes extensive comments and a test block.
#
# Author: (your name)
#

import random

class Solution:
    """
    Solution for shuffling an array and resetting it to its original configuration.
    Implements the Fisher-Yates shuffle algorithm for uniform randomness.
    """
    def __init__(self, nums):
        """
        Initialize the object with the array nums.
        Args:
            nums (list[int]): The array to shuffle and reset.
        """
        self.arr = nums  # Current state of the array
        self.original = list(nums)  # Store a copy of the original array

    def reset(self):
        """
        Reset the array to its original configuration and return it.
        Returns:
            list[int]: The original array.
        """
        self.arr = self.original
        self.original = list(self.original)  # Ensure a new copy is used
        return self.arr

    def shuffle(self):
        """
        Return a random shuffling of the array using Fisher-Yates algorithm.
        Returns:
            list[int]: The shuffled array.
        """
        aux = list(self.arr)  # Make a copy to shuffle
        for idx in range(len(self.arr)):
            remove_idx = random.randrange(len(aux))  # Pick a random index
            self.arr[idx] = aux.pop(remove_idx)      # Place the random element
        return self.arr

if __name__ == "__main__":
    # Test block demonstrating the solution
    nums = [1, 2, 3, 4, 5]
    sol = Solution(nums)
    print("Original array:", sol.reset())
    print("Shuffled array:", sol.shuffle())
    print("Reset array:", sol.reset())
    print("Shuffled again:", sol.shuffle()) 