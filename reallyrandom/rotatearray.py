# rotatearray.py
#
# Rotate an array k steps to the right (LeetCode style solution).
# Adapted from a Jupyter notebook. Includes extensive comments and a test block.
#
# Author: (your name)
#

class Solution:
    """
    Solution for rotating an array k steps to the right in-place.
    This method rotates the array by shifting elements one by one, k times.
    """
    def rotate(self, nums: list[int], k: int) -> None:
        """
        Rotate the array to the right by k steps in-place.
        Args:
            nums (list[int]): The list of integers to rotate.
            k (int): Number of steps to rotate.
        Returns:
            None. The list is modified in-place.
        """
        size = len(nums)
        k %= size  # In case k is greater than the length of the array
        # Perform the rotation k times
        for i in range(k):
            previous = nums[-1]  # Store the last element
            # Shift all elements to the right by one
            for j in range(size):
                nums[j], previous = previous, nums[j]

if __name__ == "__main__":
    # Test block demonstrating the solution
    sol = Solution()
    # Test case 1
    nums1 = [1, 2, 3, 4]
    k1 = 3
    sol.rotate(nums1, k1)
    print(f"After rotating [1, 2, 3, 4] by 3: {nums1}")
    # Test case 2
    nums2 = [1, 2, 3, 4, 5, 6, 7]
    k2 = 2
    sol.rotate(nums2, k2)
    print(f"After rotating [1, 2, 3, 4, 5, 6, 7] by 2: {nums2}")
    # Test case 3: k greater than array length
    nums3 = [1, 2, 3]
    k3 = 5
    sol.rotate(nums3, k3)
    print(f"After rotating [1, 2, 3] by 5: {nums3}") 