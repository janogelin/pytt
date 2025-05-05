# remove_elements_inplace_leet.py
#
# Remove elements from a list in-place (LeetCode style solution).
# Adapted from a Jupyter notebook. Includes extensive comments and a test block.
#
# Author: (your name)
#

from typing import List

class Solution:
    """
    Solution for removing all instances of a value from a list in-place.
    This method may change the order of elements, but is efficient for cases
    where the value to remove is rare, as it minimizes the number of writes.
    """
    def remove_elements(self, nums: List[int], val: int) -> int:
        """
        Remove all instances of val in nums in-place and return the new length.
        Args:
            nums (List[int]): The list of integers.
            val (int): The value to remove.
        Returns:
            int: The new length of the list after removal.
        """
        n = len(nums)  # Effective length of the list
        i = 0          # Current index
        # Loop until i reaches the effective end of the list
        while i < n:
            if nums[i] == val:
                # If current element is val, replace it with the last element
                nums[i] = nums[n - 1]
                n -= 1  # Reduce the effective length
                # Do not increment i, as the swapped-in element needs to be checked
            else:
                i += 1  # Move to next element
        # After loop, first n elements are those not equal to val
        return n

if __name__ == "__main__":
    # Test block demonstrating the solution
    nums = [3, 2, 2, 3, 4, 3, 5]
    val = 3
    sol = Solution()
    new_len = sol.remove_elements(nums, val)
    print("After remove_elements:", nums[:new_len], "Length:", new_len)
    # Additional test: no elements to remove
    nums2 = [1, 2, 4, 5]
    val2 = 3
    new_len2 = sol.remove_elements(nums2, val2)
    print("After remove_elements (no removal):", nums2[:new_len2], "Length:", new_len2)
    # Additional test: all elements to remove
    nums3 = [7, 7, 7]
    val3 = 7
    new_len3 = sol.remove_elements(nums3, val3)
    print("After remove_elements (all removed):", nums3[:new_len3], "Length:", new_len3) 