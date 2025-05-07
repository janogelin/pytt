"""
qrgen_for3dprint.py

Generate a QR code for a given URL and export it as an SVG (2D) or STEP (3D) file compatible with Autodesk Fusion 360.

Features:
- Generates a QR code matrix for any URL (default: Instagram Walnut Event).
- Exports the QR code as a minimal SVG file (each module as a closed <polyline> with stroke only, no fill) for Fusion 360 import.
- Optionally exports a STEP file with each module as a 3D box extruded to 1mm height (requires cadquery).
- Includes error handling for missing dependencies, invalid input, and file write errors.
- Contains a test block demonstrating usage and output.
- Supports command-line arguments for production use.

Author: (your name)
"""

import sys
import argparse
import os
import math

def check_dependencies(step_mode=False):
    """
    Check for required dependencies and exit with an error message if missing.
    """
    try:
        import qrcode
    except ImportError:
        print("Error: The 'qrcode' library is not installed. Install it with 'pip install qrcode[pil]'.")
        sys.exit(1)
    if step_mode:
        try:
            import cadquery as cq
        except ImportError:
            print("Error: The 'cadquery' library is not installed. Install it with 'pip install cadquery'.")
            sys.exit(1)


def generate_fusion360_svg(url, output_filename, border=1, box_size=10):
    """
    Generate a QR code for the given URL and export it as a Fusion 360–compatible SVG file, using <polyline> elements for each module.

    Args:
        url (str): The URL or string to encode in the QR code.
        output_filename (str): The filename for the output SVG file.
        border (int): Border size for the QR code (default: 1).
        box_size (int): Size of one QR code square in SVG user units (default: 10).

    Raises:
        ValueError: If the URL is empty or not a string, or if the filename is not .svg.
        Exception: For file write errors or SVG generation issues.
    """
    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL must be a non-empty string.")
    if not output_filename.lower().endswith('.svg'):
        raise ValueError("Output filename must end with .svg")

    import qrcode  # Import locally to avoid NameError if only STEP is used
    # Generate QR code matrix
    qr = qrcode.QRCode(border=border)
    qr.add_data(url)
    qr.make(fit=True)
    matrix = qr.get_matrix()
    size = len(matrix)

    # SVG dimensions
    svg_size = size * box_size
    viewbox = f"0 0 {svg_size} {svg_size}"

    # Start SVG content
    svg_lines = [
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
        '<!-- Import this SVG into Fusion 360 and extrude each closed polyline (QR box) to 5mm height -->',
        f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{svg_size}" height="{svg_size}" viewBox="{viewbox}">',
        # No background, only black stroked polylines for Fusion 360
    ]

    # Draw each black square as a closed polyline (no fill)
    for y in range(size):
        for x in range(size):
            if matrix[y][x]:
                x0 = x * box_size
                y0 = y * box_size
                x1 = x0 + box_size
                y1 = y0 + box_size
                # Polyline for a square: four corners, closed
                points = f"{x0},{y0} {x1},{y0} {x1},{y1} {x0},{y1} {x0},{y0}"
                svg_lines.append(
                    f'<polyline points="{points}" stroke="black" fill="none" stroke-width="1" />'
                )

    svg_lines.append('</svg>')
    svg_content = '\n'.join(svg_lines)

    # Attempt to save the SVG file
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(svg_content)
    except Exception as e:
        raise Exception(f"Failed to save SVG file '{output_filename}': {e}")

    return output_filename


def generate_fusion360_step(url, output_filename, border=1, box_size=10, height=1.0, cylinder=False, cylinder_height=3.0, cylinder_margin=5.0, cylinder_diameter=None):
    """
    Generate a QR code for the given URL and export it as a Fusion 360–compatible STEP file.
    If cylinder=True, create a cylinder base and place the QR code boxes on top, centered.
    If cylinder_diameter is specified, scale the QR code to fit inside the cylinder.
    Adds an outer railing (frame) 1mm high and 1mm thick on the edge of the cylinder if cylinder=True.

    Args:
        url (str): The URL or string to encode in the QR code.
        output_filename (str): The filename for the output STEP file.
        border (int): Border size for the QR code (default: 1).
        box_size (int): Size of one QR code square in mm (default: 10).
        height (float): Extrusion height in mm (default: 1.0).
        cylinder (bool): If True, add a cylinder base under the QR code.
        cylinder_height (float): Height of the cylinder base in mm.
        cylinder_margin (float): Margin (padding) around the QR code on the cylinder in mm.
        cylinder_diameter (float or None): If set, use this as the cylinder diameter (mm) and scale QR code to fit.

    Raises:
        ValueError: If the URL is empty or not a string, or if the filename is not .step/.stp.
        Exception: For file write errors or STEP generation issues.
    """
    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL must be a non-empty string.")
    if not (output_filename.lower().endswith('.step') or output_filename.lower().endswith('.stp')):
        raise ValueError("Output filename must end with .step or .stp")

    import qrcode  # Local import
    import cadquery as cq
    # Generate QR code matrix
    qr = qrcode.QRCode(border=border)
    qr.add_data(url)
    qr.make(fit=True)
    matrix = qr.get_matrix()
    size = len(matrix)

    qr_width = size * box_size
    qr_height = size * box_size

    # If cylinder, create base and center QR code on top
    if cylinder:
        # Cylinder diameter: QR code width + 2 * margin, unless overridden
        if cylinder_diameter is not None:
            cyl_diameter = cylinder_diameter
            # If QR code is too large, scale it down so its diagonal fits inside the cylinder (with a small margin)
            margin = 1.0  # 0.5mm on each side
            max_qr_width = (cyl_diameter - margin) / math.sqrt(2)
            if qr_width > max_qr_width:
                scale = max_qr_width / qr_width
                box_size = box_size * scale
                qr_width = size * box_size
                qr_height = size * box_size
                print(f"[INFO] Scaling QR code to fit inside cylinder diameter {cyl_diameter}mm. New box_size: {box_size:.3f}mm (fits diagonal)")
        else:
            cyl_diameter = qr_width + 2 * cylinder_margin
        cyl_height = cylinder_height
        # Create cylinder base (centered at origin, Z=0)
        base = cq.Workplane("XY").circle(cyl_diameter / 2).extrude(cyl_height)
        # Place QR code boxes on top of cylinder (Z = cyl_height)
        qr_boxes = cq.Workplane("XY")
        x_offset = -qr_width / 2
        y_offset = -qr_height / 2
        for y in range(size):
            for x in range(size):
                if matrix[y][x]:
                    x0 = x * box_size + x_offset
                    y0 = (size - 1 - y) * box_size + y_offset  # Flip Y for CAD
                    qr_boxes = qr_boxes.union(
                        cq.Workplane("XY").box(box_size, box_size, height).translate((x0 + box_size/2, y0 + box_size/2, cyl_height + height/2))
                    )
        # Add outer railing (frame) 1mm high and 1mm thick on the edge of the cylinder
        railing_height = 1.0
        railing_thickness = 1.0
        outer_radius = cyl_diameter / 2
        inner_radius = outer_radius - railing_thickness
        railing = (
            cq.Workplane("XY")
            .circle(outer_radius)
            .circle(inner_radius)
            .extrude(railing_height)
            .translate((0, 0, cyl_height))
        )
        result = base.union(qr_boxes).union(railing)
    else:
        # No cylinder, just QR code boxes (as before)
        result = cq.Workplane("XY")
        for y in range(size):
            for x in range(size):
                if matrix[y][x]:
                    x0 = x * box_size
                    y0 = (size - 1 - y) * box_size  # Flip Y for CAD coordinate system
                    result = result.union(
                        cq.Workplane("XY").box(box_size, box_size, height).translate((x0 + box_size/2, y0 + box_size/2, height/2))
                    )

    # Attempt to save the STEP file
    try:
        result.val().exportStep(output_filename)
    except Exception as e:
        raise Exception(f"Failed to save STEP file '{output_filename}': {e}")

    return output_filename


def test_generate_fusion360_svg():
    """
    Test the generate_fusion360_svg function with a sample URL and output file.
    Prints the result and checks for file creation.
    """
    test_url = "https://www.instagram.com/walnutevent/"
    test_filename = "test_qr_walnutevent_instagram.svg"
    print(f"Generating Fusion 360–compatible QR code SVG for: {test_url}")
    try:
        output = generate_fusion360_svg(test_url, test_filename)
        print(f"SVG file generated: {output}")
        if os.path.exists(output):
            print("Test passed: SVG file exists.")
            os.remove(output)  # Clean up after test
        else:
            print("Test failed: SVG file was not created.")
    except Exception as e:
        print(f"Test failed with exception: {e}")


def test_generate_fusion360_step():
    """
    Test the generate_fusion360_step function with a sample URL and output file.
    Prints the result and checks for file creation.
    """
    test_url = "https://www.instagram.com/walnutevent/"
    test_filename = "test_qr_walnutevent_instagram.step"
    print(f"Generating Fusion 360–compatible QR code STEP for: {test_url}")
    try:
        output = generate_fusion360_step(test_url, test_filename)
        print(f"STEP file generated: {output}")
        if os.path.exists(output):
            print("Test passed: STEP file exists.")
            os.remove(output)  # Clean up after test
        else:
            print("Test failed: STEP file was not created.")
    except Exception as e:
        print(f"Test failed with exception: {e}")
    # Test with cylinder base
    test_filename_cyl = "test_qr_walnutevent_instagram_cyl.step"
    print(f"Generating Fusion 360–compatible QR code STEP with cylinder base for: {test_url}")
    try:
        output = generate_fusion360_step(test_url, test_filename_cyl, cylinder=True, cylinder_height=3.0, cylinder_margin=5.0)
        print(f"STEP file with cylinder base generated: {output}")
        if os.path.exists(output):
            print("Test passed: STEP file with cylinder exists.")
            os.remove(output)  # Clean up after test
        else:
            print("Test failed: STEP file with cylinder was not created.")
    except Exception as e:
        print(f"Test failed with exception: {e}")


def main():
    """
    Main function to parse command-line arguments and generate the QR code SVG or STEP.
    """
    parser = argparse.ArgumentParser(
        description="Generate a Fusion 360–compatible QR code as an SVG (2D) or STEP (3D) file for a given URL.",
        epilog="Example: python qrgen_for3dprint.py --url https://www.example.com --output example.svg --step"
    )
    parser.add_argument('--url', type=str, default="https://www.instagram.com/walnutevent/",
                        help="The URL or string to encode in the QR code (default: Instagram Walnut Event)")
    parser.add_argument('--output', type=str, default="qr_walnutevent_instagram.svg",
                        help="Output SVG or STEP filename (default: qr_walnutevent_instagram.svg)")
    parser.add_argument('--border', type=int, default=1,
                        help="Border size for the QR code (default: 1)")
    parser.add_argument('--box-size', type=int, default=10,
                        help="Size of one QR code square in SVG user units or mm (default: 10)")
    parser.add_argument('--qr-height', type=float, default=1.0,
                        help="Height of the extruded QR code boxes in mm (default: 1.0, only with --step)")
    parser.add_argument('--step', action='store_true',
                        help="Generate a STEP file with 3D extruded boxes (requires cadquery, output filename must end with .step or .stp)")
    parser.add_argument('--cylinder', action='store_true',
                        help="Add a cylinder base under the QR code in the STEP file (only with --step)")
    parser.add_argument('--cylinder-height', type=float, default=2.0,
                        help="Height of the cylinder base in mm (default: 3.0, only with --cylinder)")
    parser.add_argument('--cylinder-margin', type=float, default=5.0,
                        help="Margin around the QR code on the cylinder in mm (default: 5.0, only with --cylinder)")
    parser.add_argument('--cylinder-diameter', type=float, default=None,
                        help="Override the cylinder diameter in mm (default: QR code width + 2 * margin)")
    parser.add_argument('--test', action='store_true',
                        help="Run the built-in test block instead of generating a QR code.")

    args = parser.parse_args()

    check_dependencies(step_mode=args.step)

    if args.test:
        print("\n--- Running Test Block ---\n")
        test_generate_fusion360_svg()
        test_generate_fusion360_step()
        return

    if args.step:
        print(f"\n--- Fusion 360 QR Code STEP Generator ---\n")
        print(f"URL: {args.url}")
        print(f"Output file: {args.output}")
        print(f"Border: {args.border}, Box size: {args.box_size}, Height: {args.qr_height}mm")
        if args.cylinder:
            print(f"Cylinder base enabled: height={args.cylinder_height}mm, margin={args.cylinder_margin}mm, diameter={args.cylinder_diameter if args.cylinder_diameter is not None else 'auto'}mm")
        try:
            filename = generate_fusion360_step(
                args.url, args.output, border=args.border, box_size=args.box_size, height=args.qr_height,
                cylinder=args.cylinder, cylinder_height=args.cylinder_height, cylinder_margin=args.cylinder_margin, cylinder_diameter=args.cylinder_diameter
            )
            print(f"Fusion 360–compatible STEP QR code saved as: {filename}")
            print("\nInstructions:")
            print("1. Import the STEP directly into your slicer (e.g. PrusaSlicer).")
            if args.cylinder:
                print("2. The QR code is extruded on top of a cylinder base.")
            else:
                print("2. Each QR code box is already extruded to 1mm height.")
        except Exception as err:
            print(f"Error: {err}")
            sys.exit(1)
    else:
        print(f"\n--- Fusion 360 QR Code SVG Generator ---\n")
        print(f"URL: {args.url}")
        print(f"Output file: {args.output}")
        print(f"Border: {args.border}, Box size: {args.box_size}")
        try:
            filename = generate_fusion360_svg(args.url, args.output, border=args.border, box_size=args.box_size)
            print(f"Fusion 360–compatible SVG QR code saved as: {filename}")
            print("\nInstructions:")
            print("1. Import the SVG into Fusion 360 (Insert > Insert SVG).")
            print("2. Select all closed polylines (QR boxes) in the sketch.")
            print("3. Use the 'Extrude' tool to extrude them to 1mm height.")
        except Exception as err:
            print(f"Error: {err}")
            sys.exit(1)


if __name__ == "__main__":
    main() 