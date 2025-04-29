#!/usr/bin/env python3

import sys
import os
from PIL import Image
from typing import Tuple, List
import argparse

# Target dimensions
TARGET_WIDTH = 640
TARGET_HEIGHT = 480

def get_image_info(image_path: str) -> Tuple[str, str]:
    """Get image format and extension."""
    try:
        with Image.open(image_path) as img:
            format = img.format
            if format is None:
                raise ValueError("Could not determine image format")
            return format, img.format.lower()
    except Exception as e:
        raise ValueError(f"Error reading image: {str(e)}")

def resize_image(input_path: str, output_path: str, method: str) -> None:
    """Resize image using specified interpolation method."""
    try:
        with Image.open(input_path) as img:
            # Get current dimensions
            width, height = img.size
            
            # Calculate aspect ratio
            aspect_ratio = width / height
            target_ratio = TARGET_WIDTH / TARGET_HEIGHT
            
            # Calculate new dimensions while maintaining aspect ratio
            if aspect_ratio > target_ratio:
                new_width = TARGET_WIDTH
                new_height = int(TARGET_WIDTH / aspect_ratio)
            else:
                new_height = TARGET_HEIGHT
                new_width = int(TARGET_HEIGHT * aspect_ratio)
            
            # Choose interpolation method
            if method == 'nearest':
                resample = Image.NEAREST
            elif method == 'bilinear':
                resample = Image.BILINEAR
            elif method == 'bicubic':
                resample = Image.BICUBIC
            else:
                raise ValueError(f"Unknown interpolation method: {method}")
            
            # Resize image
            resized_img = img.resize((new_width, new_height), resample)
            
            # Save the resized image
            resized_img.save(output_path, quality=95)
            
    except Exception as e:
        raise RuntimeError(f"Error processing image: {str(e)}")

def create_output_filename(input_path: str, method: str) -> str:
    """Create output filename with method suffix."""
    base, ext = os.path.splitext(input_path)
    return f"{base}_thumbnail_{method}{ext}"

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Resize images using different interpolation methods')
    parser.add_argument('input_image', help='Path to the input image file')
    parser.add_argument('--methods', nargs='+', default=['nearest', 'bilinear', 'bicubic'],
                       choices=['nearest', 'bilinear', 'bicubic'],
                       help='Interpolation methods to use (default: all methods)')
    args = parser.parse_args()

    try:
        # Validate input file
        if not os.path.exists(args.input_image):
            raise FileNotFoundError(f"Input file not found: {args.input_image}")
        
        if not os.path.isfile(args.input_image):
            raise ValueError(f"Input path is not a file: {args.input_image}")
        
        # Get image format
        format, ext = get_image_info(args.input_image)
        print(f"Input image format: {format}")
        
        # Process image with each method
        for method in args.methods:
            output_path = create_output_filename(args.input_image, method)
            print(f"\nProcessing with {method} interpolation...")
            resize_image(args.input_image, output_path, method)
            print(f"Saved resized image to: {output_path}")
            
            # Verify output file
            if not os.path.exists(output_path):
                raise RuntimeError(f"Output file was not created: {output_path}")
            
            # Print output image info
            with Image.open(output_path) as img:
                print(f"Output dimensions: {img.size}")
                print(f"Output format: {img.format}")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 