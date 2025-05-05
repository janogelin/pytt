import sys
import math

class ListNode:
    """
    Node of a singly linked list representing a single digit.
    """
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({self.val})"

    def __str__(self):
        # Print the list as a string of digits
        vals = []
        node = self
        while node:
            vals.append(str(node.val))
            node = node.next
        return ' -> '.join(vals)

def add_two_numbers(l1, l2):
    """
    Add two numbers represented as linked lists, where each node contains a single digit.
    The digits are stored in reverse order (1's digit at the head).
    Returns the sum as a new linked list in the same format.

    Args:
        l1 (ListNode): Head of the first linked list.
        l2 (ListNode): Head of the second linked list.
    Returns:
        ListNode: Head of the resulting linked list representing the sum.
    """
    dummy = ListNode(0)
    current = dummy
    carry = 0
    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        total = val1 + val2 + carry
        carry = total // 10
        current.next = ListNode(total % 10)
        current = current.next
        if l1:
            l1 = l1.next
        if l2:
            l2 = l2.next
    return dummy.next

def list_to_linked(lst):
    """
    Helper function to convert a list of digits to a linked list (reverse order).
    Args:
        lst (list[int]): List of digits (least significant digit first).
    Returns:
        ListNode: Head of the linked list.
    """
    dummy = ListNode(0)
    current = dummy
    for num in lst:
        current.next = ListNode(num)
        current = current.next
    return dummy.next

def linked_to_list(node):
    """
    Helper function to convert a linked list to a list of digits (reverse order).
    Args:
        node (ListNode): Head of the linked list.
    Returns:
        list[int]: List of digits (least significant digit first).
    """
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result

def add_numbers(a, b):
    """
    Add two numbers together with input validation and overflow protection.
    
    Args:
        a (int, float): First number
        b (int, float): Second number
        
    Returns:
        float: Sum of the two numbers
        
    Raises:
        TypeError: If either input is not a number
        OverflowError: If the result would be too large
        ValueError: If the input is invalid
    """
    # Input validation
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both inputs must be numbers")
    
    # Convert to float for consistent handling
    a_float = float(a)
    b_float = float(b)
    
    # Check for overflow
    if abs(a_float) > sys.float_info.max or abs(b_float) > sys.float_info.max:
        raise OverflowError("Input numbers are too large")
    
    result = a_float + b_float
    
    # Check for result overflow
    if abs(result) > sys.float_info.max:
        raise OverflowError("Result would be too large")
    
    return result

def parse_input(value):
    """
    Parse input string to number with validation.
    
    Args:
        value (str): Input string to parse
        
    Returns:
        float: Parsed number
        
    Raises:
        ValueError: If the input cannot be parsed to a number
    """
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"Invalid number: {value}")

def main():
    # Check if command line arguments are provided
    if len(sys.argv) == 3:
        try:
            num1 = parse_input(sys.argv[1])
            num2 = parse_input(sys.argv[2])
            result = add_numbers(num1, num2)
            print(f"{num1} + {num2} = {result}")
        except (TypeError, OverflowError, ValueError) as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        # Run example tests if no arguments provided
        try:
            # Example 1: (2 -> 4 -> 3) + (5 -> 6 -> 4) = 342 + 465 = 807 (7 -> 0 -> 8)
            l1 = list_to_linked([2, 4, 3])
            l2 = list_to_linked([5, 6, 4])
            result = add_two_numbers(l1, l2)
            print("Input 1:", l1)
            print("Input 2:", l2)
            print("Sum:", result)
            print("Sum as list:", linked_to_list(result))
            
            # Example 2: (0) + (0) = 0
            l1 = list_to_linked([0])
            l2 = list_to_linked([0])
            result = add_two_numbers(l1, l2)
            print("\nInput 1:", l1)
            print("Input 2:", l2)
            print("Sum:", result)
            print("Sum as list:", linked_to_list(result))
            
            # Example 3: (9 -> 9 -> 9 -> 9 -> 9 -> 9 -> 9) + (9 -> 9 -> 9 -> 9) = 9999999 + 9999 = 10009998
            l1 = list_to_linked([9,9,9,9,9,9,9])
            l2 = list_to_linked([9,9,9,9])
            result = add_two_numbers(l1, l2)
            print("\nInput 1:", l1)
            print("Input 2:", l2)
            print("Sum:", result)
            print("Sum as list:", linked_to_list(result))
            
        except (TypeError, OverflowError, ValueError) as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main() 