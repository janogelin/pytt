# reverse_integer.py
#
# Reverse integer (LeetCode style solution).
# Adapted from a Jupyter notebook. Includes extensive comments and a test block.
#
# Author: (your name)
#

class Solution:
    """
    Solution for reversing digits of a 32-bit signed integer.
    Handles negative numbers and overflow according to LeetCode constraints.
    """
    def reverse(self, x: int) -> int:
        """
        Reverse the digits of an integer, handling sign and overflow.
        Args:
            x (int): The integer to reverse.
        Returns:
            int: The reversed integer, or 0 if it overflows 32-bit signed int.
        """
        snum = str(x)  # Convert integer to string
        res = ''       # Result string to build the reversed number

        # Handle negative numbers
        if snum[0] == '-':
            res = '-'
            snum = snum[1:]  # Remove the negative sign for reversal

        # Remove trailing zeros (except for '0' itself)
        if len(snum) > 1:
            snum = snum.rstrip('0')

        # Reverse the string
        snum = snum[::-1]

        # Combine sign and reversed digits
        res = res + snum

        # Convert back to integer and check for 32-bit signed overflow
        if int(res) > 2**31 - 1 or int(res) < -2**31:
            return 0
        else:
            return int(res)

if __name__ == "__main__":
    # Test block demonstrating the solution
    sol = Solution()
    # Test cases
    test_cases = [120, -123, 1534236469, 0, 1000, -100, 2**31-1, -2**31]
    for val in test_cases:
        result = sol.reverse(val)
        print(f"reverse({val}) = {result}") 