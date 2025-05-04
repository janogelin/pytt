# climbing_stairs_leet.py
#
# Solution to the 'Climbing Stairs' problem (LeetCode).
# This version uses dynamic programming with a sliding window of 2 (classic problem).
#
# Author: (your name)
#

class Solution:
    """
    Climbing Stairs (LeetCode):
    Given n stairs, you can climb 1 or 2 steps at a time.
    How many distinct ways can you climb to the top?
    """
    def count_ways_util(self, stairs, sliding_window):
        """
        Dynamic programming utility to count ways to climb stairs.
        Args:
            stairs (int): Number of steps (including 0th step for DP base case).
            sliding_window (int): Maximum steps you can take at once (2 for classic problem).
        Returns:
            int: Number of ways to reach the top.
        """
        res = [0 for _ in range(stairs)]
        res[0], res[1] = 1, 1  # Base cases: 1 way to reach step 0 and 1

        for i in range(2, stairs):
            j = 1
            while j <= sliding_window and j <= i:
                res[i] += res[i - j]
                j += 1
        return res[stairs - 1]

    def climb_stairs(self, stairs: int) -> int:
        """
        Main API: Returns the number of ways to climb 'stairs' steps.
        Args:
            stairs (int): Number of stairs (1 <= stairs <= 45)
        Returns:
            int: Number of ways to reach the top.
        """
        if 1 <= stairs <= 45:
            sliding_window = 2  # You can take 1 or 2 steps at a time
            # Add 1 to stairs to account for base case at step 0
            return self.count_ways_util(stairs + 1, sliding_window)
        else:
            raise ValueError("stairs must be between 1 and 45 inclusive.")

if __name__ == "__main__":
    mystair = 10
    climb = Solution()
    print(f"Ways to climb {mystair} stairs: {climb.climb_stairs(mystair)}") 