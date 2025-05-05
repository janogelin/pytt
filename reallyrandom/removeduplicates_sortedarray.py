# removeduplicates_sortedarray.py
#
# Remove duplicates from a sorted array in-place (LeetCode style solution).
# Adapted from a Jupyter notebook. Includes extensive comments and a test block.
#
# Author: (your name)
#

from typing import List

class Solution:
    """
    Solution for removing duplicates from a sorted array in-place.
    This method modifies the input array so that each element appears only once
    and returns the new length. The order of unique elements is preserved.
    """
    def removeDuplicates(self, nums: List[int]) -> int:
        """
        Remove duplicates in-place from a sorted array and return the new length.
        Args:
            nums (List[int]): The sorted list of integers.
        Returns:
            int: The new length of the array with unique elements at the start.
        """
        if not nums:
            return 0
        insertIndex = 1  # Position to insert the next unique element
        size = len(nums)
        # Start from the second element and compare with the previous
        for i in range(1, size):
            if nums[i - 1] != nums[i]:
                # If current element is different from previous, it's unique
                nums[insertIndex] = nums[i]
                insertIndex += 1  # Move insert position forward
        # After loop, first insertIndex elements are unique
        return insertIndex

if __name__ == "__main__":
    # Test block demonstrating the solution
    nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    sol = Solution()
    new_len = sol.removeDuplicates(nums)
    print("After removeDuplicates:", nums[:new_len], "Length:", new_len)
    # Additional test: all unique
    nums2 = [1, 2, 3, 4, 5]
    new_len2 = sol.removeDuplicates(nums2)
    print("After removeDuplicates (all unique):", nums2[:new_len2], "Length:", new_len2)
    # Additional test: all duplicates
    nums3 = [7, 7, 7, 7]
    new_len3 = sol.removeDuplicates(nums3)
    print("After removeDuplicates (all duplicates):", nums3[:new_len3], "Length:", new_len3)
    # Additional test: empty array
    nums4 = []
    new_len4 = sol.removeDuplicates(nums4)
    print("After removeDuplicates (empty):", nums4[:new_len4], "Length:", new_len4) 