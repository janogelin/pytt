# Add Numbers as Linked Lists (LeetCode Style)

A Python script (`add_numbers.py`) that adds two numbers represented as singly linked lists, where each node contains a single digit and the digits are stored in reverse order (1's digit at the head). This is a classic LeetCode-style problem.

## Features
- Implements a `ListNode` class for singly linked lists.
- Adds two numbers represented as linked lists and returns the sum as a linked list.
- Includes helper functions to convert between Python lists and linked lists.
- Contains a test block demonstrating usage and printing results.
- Handles numbers of different lengths and carry-over.

## Usage Example
```python
from add_numbers import list_to_linked, add_two_numbers, linked_to_list

l1 = list_to_linked([2, 4, 3])  # Represents 342
l2 = list_to_linked([5, 6, 4])  # Represents 465
result = add_two_numbers(l1, l2)  # Should represent 807
print(linked_to_list(result))  # Output: [7, 0, 8]
```

**Command-line/test block output:**
```
Input 1: 2 -> 4 -> 3
Input 2: 5 -> 6 -> 4
Sum: 7 -> 0 -> 8
Sum as list: [7, 0, 8]
```

---

# Image Resizer

A Python program that resizes images to a target size of 640x480 pixels using different interpolation methods.

## Features

- Supports multiple image formats (JPEG, PNG, etc.)
- Maintains aspect ratio while resizing
- Three interpolation methods:
  - Nearest Neighbor
  - Bilinear
  - Bicubic
- Detailed error handling and validation
- Command-line interface with options

## Requirements

- Python 3.6 or higher
- Pillow library (PIL)

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Basic usage:
```bash
python image_resizer.py input_image.jpg
```

Specify interpolation methods:
```bash
python image_resizer.py input_image.jpg --methods nearest bilinear
```

## Output

The program creates resized versions of the input image with the following naming convention:
- `input_thumbnail_nearest.jpg`
- `input_thumbnail_bilinear.jpg`
- `input_thumbnail_bicubic.jpg`

## Error Handling

The program handles various error cases:
- Invalid input file
- Unsupported image format
- File permission issues
- Invalid interpolation method
- Output file creation failures 