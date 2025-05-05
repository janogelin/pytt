# findzerorectangles.py
#
# Find all rectangles of zeros in a 2D binary matrix.
# Adapted from a Jupyter notebook. Includes extensive comments and a test block.
#
# Author: (your name)
#

def findend(row, col, field, output, index):
    """
    Find the bottom-right corner of a rectangle of zeros starting at (row, col).
    Mark all cells in the rectangle as processed (-99).
    Args:
        row, col: Top-left coordinates of the rectangle.
        field: The 2D matrix (modified in-place).
        output: List to store rectangle coordinates.
        index: Index in output for this rectangle.
    """
    total_rows = len(field)
    total_columns = len(field[0])
    column_flag = 0  # Set if we hit a 1 or boundary in columns
    row_flag = 0     # Set if we hit a 1 or boundary in rows

    for this_row in range(row, total_rows):
        # Stop if we hit a 1 in the first column of the rectangle
        if field[this_row][col] == 1:
            row_flag = 1
            break
        # Skip already processed cells
        if field[this_row][col] == -99:
            pass
        for this_col in range(col, total_columns):
            # Stop if we hit a 1 in this row
            if field[this_row][this_col] == 1:
                column_flag = 1
                break
            # Mark cell as processed
            field[this_row][this_col] = -99
    # Record the bottom row of the rectangle
    if row_flag == 1:
        output[index].append(this_row - 1)
    else:
        output[index].append(this_row)
    # Record the rightmost column of the rectangle
    if column_flag == 1:
        output[index].append(this_col - 1)
    else:
        output[index].append(this_col)


def get_rectangle_coordinates(field):
    """
    Find all rectangles of zeros in the given 2D binary matrix.
    Args:
        field: 2D list of 0s and 1s.
    Returns:
        List of rectangles, each as [row_start, col_start, row_end, col_end].
    """
    size_of_field = len(field)
    output = []
    index = -1
    for row in range(size_of_field):
        for col in range(len(field[0])):
            if field[row][col] == 0:
                output.append([row, col])
                index += 1
                findend(row, col, field, output, index)
    return output

if __name__ == "__main__":
    # Example test matrix
    tests = [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1]
    ]
    # Deep copy to avoid modifying the original for repeated tests
    import copy
    field = copy.deepcopy(tests)
    rectangles = get_rectangle_coordinates(field)
    print("Rectangles of zeros (as [row_start, col_start, row_end, col_end]):")
    for rect in rectangles:
        print(rect) 