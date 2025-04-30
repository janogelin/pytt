#!/usr/bin/env python3

"""
SumKeyValue - A utility to sum values by key from input data

This script reads key-value pairs from stdin or files and sums the values
for each unique key. The results are sorted by the summed values in descending
order and printed to stdout.

Usage:
    cat input.txt | ./sumkeyvalue.py
    ./sumkeyvalue.py < input.txt

Input format:
    Each line should contain a key and a value separated by whitespace.
    Example:
        apple 5
        banana 3
        apple 2

Output format:
    Each line contains a key and its summed value, sorted by value in descending order.
    Example:
        apple 7
        banana 3
"""

import sys
from collections import defaultdict
import argparse

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Sum values by key from input data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
    cat input.txt | ./sumkeyvalue.py
    ./sumkeyvalue.py < input.txt
        """)
    return parser.parse_args()

def process_input():
    """
    Process input data and return a dictionary of summed values.
    
    Returns:
        defaultdict: A dictionary with keys and their summed values
    """
    # Use defaultdict to automatically initialize new keys with 0
    src = defaultdict(int)
    
    # Read from stdin
    for line in sys.stdin:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
            
        # Split on whitespace and handle potential errors
        try:
            key, value = line.split()
            src[key] += int(value)
        except ValueError:
            print(f"Warning: Skipping malformed line: {line}", file=sys.stderr)
            continue
    
    return src

def print_results(src):
    """
    Print the results sorted by value in descending order.
    
    Args:
        src (defaultdict): Dictionary containing keys and their summed values
    """
    # Sort by value in descending order and print
    for key, value in sorted(src.items(), key=lambda x: x[1], reverse=True):
        print(f"{key} {value}")

def main():
    """Main function to orchestrate the program flow."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Process input and get results
    results = process_input()
    
    # Print results
    print_results(results)

if __name__ == "__main__":
    main() 