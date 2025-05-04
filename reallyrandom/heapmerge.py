# heapmerge.py
#
# Demonstrates merging multiple sorted lists using heapq.merge in Python.
# Adapted from a Jupyter notebook. Includes extensive comments and a test block.
#
# Author: (your name)
#

import heapq
import random

# Set a fixed random seed for reproducibility
random.seed(2016)

def generate_sorted_lists(num_lists, list_size, value_range):
    """
    Generate a list of sorted lists with random integers.
    Args:
        num_lists (int): Number of lists to generate.
        list_size (int): Number of elements in each list.
        value_range (tuple): Range of values (inclusive lower, exclusive upper).
    Returns:
        List[List[int]]: List of sorted integer lists.
    """
    data = []
    for i in range(num_lists):
        # Generate unique random numbers, sort, and append
        new_data = list(random.sample(range(*value_range), list_size))
        new_data.sort()
        data.append(new_data)
    return data

def print_lists(lists):
    """
    Print each list with its index.
    Args:
        lists (List[List[int]]): The lists to print.
    """
    for i, d in enumerate(lists):
        print(f'List {i}: {d}')

if __name__ == "__main__":
    # Generate 4 sorted lists of 5 random integers each, values 1-100
    data = generate_sorted_lists(num_lists=4, list_size=5, value_range=(1, 101))
    print("Generated sorted lists:")
    print_lists(data)

    # Merge all lists into a single sorted iterator
    print("\nMerged:")
    merged = list(heapq.merge(*data))
    print(merged) 