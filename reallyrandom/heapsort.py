# heapsort.py
#
# Implementation of the Heap Sort algorithm in Python.
# This code is adapted from a Jupyter notebook and includes extensive comments.
#
# Author: (your name)
#

def heapify(arr, n, i):
    """
    Ensure the subtree rooted at index i is a max heap.
    Args:
        arr (list): The array to heapify.
        n (int): Size of the heap (may be less than len(arr) during sort).
        i (int): Index of the root of the subtree.
    """
    largest = i         # Initialize largest as root
    left = 2 * i + 1    # left child index
    right = 2 * i + 2   # right child index

    # If left child exists and is greater than root
    if left < n and arr[largest] < arr[left]:
        largest = left

    # If right child exists and is greater than largest so far
    if right < n and arr[largest] < arr[right]:
        largest = right

    # If largest is not root, swap and continue heapifying
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        # Recursively heapify the affected subtree
        heapify(arr, n, largest)

def heap_sort(arr):
    """
    Perform heap sort on the input array in-place.
    Args:
        arr (list): The array to sort.
    """
    n = len(arr)

    # Build a max heap (rearrange array)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extract elements one by one from the heap
    for i in range(n - 1, 0, -1):
        # Move current root to end
        arr[i], arr[0] = arr[0], arr[i]
        # Call max heapify on the reduced heap
        heapify(arr, i, 0)

if __name__ == "__main__":
    # Example usage and test
    arr = [12, 11, 13, 5, 6, 7]
    print("Original array:")
    print(arr)
    heap_sort(arr)
    print("Sorted array is:")
    for num in arr:
        print(num) 