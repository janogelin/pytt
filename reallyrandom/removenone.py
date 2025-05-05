# removenone.py
#
# Remove None values from a 2D list (matrix), returning only non-empty rows.
# Adapted from a Jupyter notebook. Includes extensive comments and a test block.
#
# Author: (your name)
#

def remove_none_from_2d(two_dim):
    """
    Remove None values from each row of a 2D list. Only non-empty rows are kept.
    Args:
        two_dim (list of list): The input 2D list (matrix) possibly containing None values.
    Returns:
        list of list: A new 2D list with None values removed and only non-empty rows.
    """
    cleaned = []
    for row in two_dim:
        # Filter out None values from the row
        filtered = [x for x in row if x is not None]
        if filtered:  # Only add non-empty rows
            cleaned.append(filtered)
    return cleaned

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