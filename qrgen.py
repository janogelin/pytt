"""
qrgen.py

Generate a QR code for a given URL and export it as a DXF file using qrcode and ezdxf libraries.

Features:
- Generates a QR code matrix for any URL.
- Exports the QR code as a vector DXF file (each black module is a closed polyline).
- Includes error handling for missing dependencies, invalid input, and file write errors.
- Contains a test block demonstrating usage and output.

Author: (your name)
"""

import sys

# Error handling for missing dependencies
try:
    import qrcode
except ImportError:
    print("Error: The 'qrcode' library is not installed. Install it with 'pip install qrcode[pil]'.")
    sys.exit(1)

try:
    import ezdxf
except ImportError:
    print("Error: The 'ezdxf' library is not installed. Install it with 'pip install ezdxf'.")
    sys.exit(1)


def generate_qr_dxf(url, output_filename, module_size=10, border=1):
    """
    Generate a QR code for the given URL and export it as a DXF file.

    Args:
        url (str): The URL or string to encode in the QR code.
        output_filename (str): The filename for the output DXF file.
        module_size (int): Size of one QR code square in drawing units (default: 10).
        border (int): Border size for the QR code (default: 1).

    Raises:
        ValueError: If the URL is empty or not a string.
        Exception: For file write errors or DXF generation issues.
    """
    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL must be a non-empty string.")
    if not output_filename.lower().endswith('.dxf'):
        raise ValueError("Output filename must end with .dxf")

    # Generate QR code matrix
    qr = qrcode.QRCode(border=border)
    qr.add_data(url)
    qr.make(fit=True)
    matrix = qr.get_matrix()
    size = len(matrix)

    # Create a new DXF document
    doc = ezdxf.new()
    msp = doc.modelspace()

    # Draw each black square as a closed polyline
    for y in range(size):
        for x in range(size):
            if matrix[y][x]:
                x0 = x * module_size
                y0 = y * module_size
                x1 = x0 + module_size
                y1 = y0 + module_size
                msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True)

    # Attempt to save the DXF file
    try:
        doc.saveas(output_filename)
    except Exception as e:
        raise Exception(f"Failed to save DXF file '{output_filename}': {e}")

    return output_filename


def test_generate_qr_dxf():
    """
    Test the generate_qr_dxf function with a sample URL and output file.
    Prints the result and checks for file creation.
    """
    import os
    test_url = "https://www.instagram.com/walnutevent/"
    test_filename = "test_qr_walnutevent_instagram.dxf"
    print(f"Generating QR code DXF for: {test_url}")
    try:
        output = generate_qr_dxf(test_url, test_filename)
        print(f"DXF file generated: {output}")
        if os.path.exists(output):
            print("Test passed: DXF file exists.")
            os.remove(output)  # Clean up after test
        else:
            print("Test failed: DXF file was not created.")
    except Exception as e:
        print(f"Test failed with exception: {e}")


if __name__ == "__main__":
    # Example usage and test block
    print("\n--- QR Code DXF Generator ---\n")
    # Run test
    test_generate_qr_dxf()
    # You can also generate a real file by uncommenting below:
    try:
        filename = generate_qr_dxf("https://www.instagram.com/walnutevent/", "walnutevent_qr.dxf")
        print(f"Saved as {filename}")
    except Exception as err:
        print(f"Error: {err}")
