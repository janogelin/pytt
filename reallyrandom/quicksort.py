# quicksort.py
#
# Simple quicksort implementation in Python.
# Adapted from a Jupyter notebook. Includes extensive comments and a test block.
#
# Author: (your name)
#

# Quicksort is a classic divide-and-conquer sorting algorithm.
# It works by selecting a 'pivot' element from the array and partitioning
# the other elements into two sub-arrays, according to whether they are
# less than or greater than the pivot. The sub-arrays are then sorted recursively.
# This implementation is not in-place and returns a new sorted list.

def quicksort(arr):
    """
    Sort an array using the quicksort algorithm (recursive, not in-place).
    Args:
        arr (list): The list of elements to sort.
    Returns:
        list: A new sorted list.
    """
    # Lists to hold elements less than, equal to, and greater than the pivot
    less = []
    equal = []
    greater = []

    # Base case: arrays with 0 or 1 element are already sorted
    if len(arr) > 1:
        # Select the first element as the pivot
        pivot = arr[0]
        # Partition the array into three lists
        for x in arr:
            if x < pivot:
                # Elements less than pivot go into 'less'
                less.append(x)
            elif x == pivot:
                # Elements equal to pivot go into 'equal'
                equal.append(x)
            else:
                # Elements greater than pivot go into 'greater'
                greater.append(x)
        # Recursively sort 'less' and 'greater', then concatenate
        return quicksort(less) + equal + quicksort(greater)
    else:
        # Return arrays with 0 or 1 element as-is
        return arr

if __name__ == "__main__":
    # Test block demonstrating quicksort usage
    # Define an unsorted array
    a = [12, 4, 5, 6, 7, 3, 1, 15]
    print("Original array:", a)
    # Sort the array using quicksort
    b = quicksort(a)
    # Print the sorted result
    print("Sorted array:", b) 