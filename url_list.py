#!/usr/bin/env python3

import sys
from typing import Optional, List
import re

class URLNode:
    def __init__(self, url: str):
        self.url = url
        self.next: Optional['URLNode'] = None

class URLLinkedList:
    def __init__(self):
        self.head: Optional[URLNode] = None
        self.size = 0

    def append(self, url: str) -> None:
        """Append a URL to the end of the list."""
        new_node = URLNode(url)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self.size += 1

    def print_list(self) -> None:
        """Print all URLs in the list with numbering."""
        if self.head is None:
            print("The list is empty.")
            return

        current = self.head
        count = 1
        while current is not None:
            print(f"{count}. {current.url}")
            current = current.next
            count += 1

    def validate_url(self, url: str) -> bool:
        """Validate if the string is a proper URL."""
        # Basic URL validation regex
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return bool(url_pattern.match(url))

def read_urls_from_file(filename: str) -> List[str]:
    """Read URLs from a file with error handling."""
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied when trying to read '{filename}'.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    # Check if filename is provided as command line argument
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "urls.txt"

    # Read URLs from file
    urls = read_urls_from_file(filename)
    
    # Create linked list and validate URLs
    url_list = URLLinkedList()
    invalid_urls = []
    
    for url in urls:
        if url_list.validate_url(url):
            url_list.append(url)
        else:
            invalid_urls.append(url)

    # Print results
    print("\nValid URLs in the list:")
    url_list.print_list()
    
    if invalid_urls:
        print("\nInvalid URLs (not added to list):")
        for i, url in enumerate(invalid_urls, 1):
            print(f"{i}. {url}")

if __name__ == "__main__":
    main() 