# remove_elements.py
#
# Solutions for removing elements from a list in-place.
# Adapted from a Jupyter notebook. Includes extensive comments and a test block.
#
# Author: (your name)
#

# This script demonstrates two different algorithms for removing all instances
# of a specific value from a list in-place, returning the new length of the list.
# Both methods operate in O(n) time and O(1) space, but differ in their approach
# and whether they preserve the order of elements.

class Solution:
    """
    Remove all instances of a value from a list in-place (Alternative 1).
    This method preserves the order of the remaining elements.
    """
    def remove_element(self, nums: list[int], val: int) -> int:
        """
        Remove all instances of val in nums in-place and return the new length.
        Args:
            nums (list[int]): The list of integers.
            val (int): The value to remove.
        Returns:
            int: The new length of the list after removal.
        """
        i = 0  # Pointer for the next position to write a non-val element
        # Iterate through all elements in the list
        for j in range(len(nums)):
            if nums[j] != val:
                # If current element is not val, write it at index i
                nums[i] = nums[j]
                i += 1  # Move write pointer forward
        # After loop, first i elements are those not equal to val
        return i

class Solution2:
    """
    Remove all instances of a value from a list in-place (Alternative 2).
    This method does not preserve the order of elements, but may be more efficient
    if the value to remove is rare, as it minimizes the number of writes.
    """
    def remove_element2(self, nums: list[int], val: int) -> int:
        """
        Remove all instances of val in nums in-place and return the new length.
        This method may change the order of elements.
        Args:
            nums (list[int]): The list of integers.
            val (int): The value to remove.
        Returns:
            int: The new length of the list after removal.
        """
        i = 0  # Current index
        n = len(nums)  # Effective length of the list
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
    # Test block demonstrating both solutions
    # Example input list and value to remove
    nums1 = [4, 1, 2, 3, 5]
    val1 = 4
    nums2 = [4, 1, 2, 3, 5]
    val2 = 4

    # Using Solution (Alternative 1)
    sol1 = Solution()
    new_len1 = sol1.remove_element(nums1, val1)
    # Print the modified list up to the new length and the new length
    print("After remove_element (Alt 1):", nums1[:new_len1], "Length:", new_len1)

    # Using Solution2 (Alternative 2)
    sol2 = Solution2()
    new_len2 = sol2.remove_element2(nums2, val2)
    # Print the modified list up to the new length and the new length
    print("After remove_element2 (Alt 2):", nums2[:new_len2], "Length:", new_len2) 