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