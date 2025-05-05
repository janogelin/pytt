# removenone_optimized.py
#
# Remove None values from a 2D list (matrix), returning only non-empty rows.
# Optimized and Pythonic version.
#
# Author: (your name)
#

from typing import List, Any

def remove_none_from_2d(two_dim: List[List[Any]]) -> List[List[Any]]:
    """
    Remove None values from each row of a 2D list. Only non-empty rows are kept.
    Args:
        two_dim: The input 2D list (matrix) possibly containing None values.
    Returns:
        A new 2D list with None values removed and only non-empty rows.
    """
    # Use a nested list comprehension for efficiency and clarity
    return [
        [x for x in row if x is not None]
        for row in two_dim
        if any(x is not None for x in row)
    ]

if __name__ == "__main__":
    # Example 2D list with None values
    two_dim = [
        [2.5, 2.5, 2.5, None, None, None],
        [None, 2.5, None, None, None, None],
        [None, None, None, 2.5, None, None],
        [None, None, 6.5, 8.5, None, None],
        [None, None, None, None, None, None],
        [None, None, None, 9.0, None, 2.5],
        [None, None, None, 8.9, 5.5, 8.5]
    ]

    print(f"Original 2D list (with None):\n{two_dim}\n")
    cleaned = remove_none_from_2d(two_dim)
    print(f"Cleaned 2D list (no None, only non-empty rows):\nc={cleaned}") 