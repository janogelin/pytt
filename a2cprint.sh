#!/usr/bin/env bash

# a2cprint.sh - Color print utility using a2ps
#
# This script allows printing files with different font sizes using a2ps.
# It provides a menu to select the font size and handles the printing process.
#
# Usage: ./a2cprint.sh <output_file> <input_file>
# Example: ./a2cprint.sh output.ps input.txt
#
# Dependencies:
#   - a2ps (GNU a2ps)
#   - bash

# Function to print usage information
print_usage() {
    echo "Usage: $0 <output_file> <input_file>"
    echo "Example: $0 output.ps input.txt"
    exit 1
}

# Function to check if a2ps is installed
check_dependencies() {
    if ! command -v a2ps &> /dev/null; then
        echo "Error: a2ps is not installed. Please install it first."
        echo "On Debian/Ubuntu: sudo apt-get install a2ps"
        exit 1
    fi
}

# Function to validate input parameters
validate_input() {
    if [ $# -ne 2 ]; then
        echo "Error: Incorrect number of arguments"
        print_usage
    fi

    if [ ! -f "$2" ]; then
        echo "Error: Input file '$2' does not exist or is not a regular file"
        exit 1
    fi

    # Check if output directory is writable
    output_dir=$(dirname "$1")
    if [ ! -w "$output_dir" ]; then
        echo "Error: Output directory '$output_dir' is not writable"
        exit 1
    fi
}

# Function to print with specified font size
printbig() {
    local font_size=$1
    echo "Printing with font size $font_size..."
    if ! a2ps --pro=color -R -f "$font_size" --columns=1 --output="$out" "$in"; then
        echo "Error: Failed to print with font size $font_size"
        exit 1
    fi
    echo "Successfully created output file: $out"
}

# Main script execution
main() {
    # Check dependencies
    check_dependencies

    # Validate input
    validate_input "$@"

    # Set variables
    out=$1
    in=$2

    # Show menu and get user input
    echo "Select font size:"
    select printt in 18 16 14 12 10 8; do
        if [ -n "$printt" ]; then
            PRINTT=$printt
            echo "Selected font size: $PRINTT"
            break
        else
            echo "Invalid choice. Please select a valid option."
        fi
    done

    # Process the selected font size
    case $PRINTT in
        18) printbig 18 ;;
        16) printbig 16 ;;
        14) printbig 14 ;;
        12) printbig 12 ;;
        10) printbig 10 ;;
        8)  printbig 8 ;;
        *)  echo "Error: Invalid font size selected"
            exit 1 ;;
    esac
}

# Execute main function
main "$@"



