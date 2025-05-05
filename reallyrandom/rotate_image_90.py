# rotate_image_90.py
#
# Rotate image (matrix) 90 degrees in-place (LeetCode style solution).
# Adapted from a Jupyter notebook. Includes extensive comments and a test block.
#
# Author: (your name)
#

from typing import List

class Solution:
    """
    Solution for rotating an n x n 2D matrix (image) by 90 degrees clockwise in-place.
    The rotation is performed layer by layer, moving four elements at a time.
    """
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Rotate the matrix 90 degrees clockwise in-place.
        Args:
            matrix (List[List[int]]): The n x n matrix to rotate.
        Returns:
            None. The matrix is modified in-place.
        """
        width = len(matrix) - 1  # The last index in the matrix
        cur_y = 0  # Start with the outermost layer

        # Process each layer from outermost to innermost
        while cur_y < width:
            cur_x = cur_y  # Start at the diagonal element for this layer
            pos_y = width - cur_y  # The corresponding row at the bottom of the layer
            while cur_x < pos_y:
                pos_x = width - cur_x  # The corresponding column at the right of the layer
                # Save the top-left value
                temp = matrix[cur_y][cur_x]
                # Move bottom-left to top-left
                matrix[cur_y][cur_x] = matrix[pos_x][cur_y]
                # Move bottom-right to bottom-left
                matrix[pos_x][cur_y] = matrix[pos_y][pos_x]
                # Move top-right to bottom-right
                matrix[pos_y][pos_x] = matrix[cur_x][pos_y]
                # Move saved top-left to top-right
                matrix[cur_x][pos_y] = temp
                cur_x += 1  # Move to the next element in the layer
            cur_y += 1  # Move to the next inner layer

if __name__ == "__main__":
    # Test block demonstrating the solution
    sol = Solution()
    # Test case 1: 2x2 matrix
    mx1 = [[1, 2], [3, 4]]
    sol.rotate(mx1)
    print("Rotated 2x2:", mx1)
    # Test case 2: 3x3 matrix
    mx2 = [[1,2,3],[4,5,6],[7,8,9]]
    sol.rotate(mx2)
    print("Rotated 3x3:", mx2)
    # Test case 3: 4x4 matrix
    mx3 = [[ 1, 2, 3, 4], [ 5, 6, 7, 8], [ 9,10,11,12], [13,14,15,16]]
    sol.rotate(mx3)
    print("Rotated 4x4:", mx3) 