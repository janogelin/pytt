import sys
import math

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
            # Test case 1: Adding two integers
            result1 = add_numbers(5, 3)
            print(f"5 + 3 = {result1}")
            
            # Test case 2: Adding two floats
            result2 = add_numbers(2.5, 3.7)
            print(f"2.5 + 3.7 = {result2}")
            
            # Test case 3: Adding integer and float
            result3 = add_numbers(4, 2.5)
            print(f"4 + 2.5 = {result3}")
            
            # Test case 4: Large numbers
            result4 = add_numbers(1e300, 1e300)
            print(f"1e300 + 1e300 = {result4}")
            
            # Test case 5: Invalid input (string)
            result5 = add_numbers("5", 3)  # This will raise TypeError
            print(f"5 + 3 = {result5}")
            
        except (TypeError, OverflowError, ValueError) as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main() 