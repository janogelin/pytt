# QR Code Generator for 3D Printing (qrgen_for3dprint.py)

This script generates a QR code for any URL and exports it as either:
- A minimal SVG file (for 2D vector/CAD use, e.g., Fusion 360 sketches)
- A 3D STEP file (for direct 3D printing or CAD import, e.g., Fusion 360 bodies)

## Features
- **SVG Output:** Each QR code module is a closed polyline, ready for extrusion in CAD.
- **STEP Output:** Each QR code module is a 3D box (extruded to a specified height, default 1mm).
- **Cylinder Base:** Optionally add a circular base under the QR code, with an outer railing (frame) for easy 3D printing.
- **Automatic Scaling:** If you specify a cylinder diameter, the QR code is automatically scaled to fit inside the cylinder.
- **Customizable:** Control border, box size, QR code height, cylinder height, margin, and diameter.
- **Robust:** Handles missing dependencies, invalid input, and file write errors gracefully.

## Dependencies
- Python 3.x
- [qrcode](https://pypi.org/project/qrcode/) (`pip install qrcode[pil]`)
- [cadquery](https://github.com/CadQuery/cadquery) (`pip install cadquery`) (only needed for STEP output)

## Usage

### Generate SVG (2D)
```sh
python3 qrgen_for3dprint.py --url https://www.example.com --output example.svg
```
- Import the SVG into Fusion 360 (Insert > Insert SVG), select all QR boxes, and extrude to your desired height.

### Generate STEP (3D, extruded QR code)
```sh
python3 qrgen_for3dprint.py --step --url https://www.example.com --output example.step
```
- Import the STEP file into Fusion 360 (Insert > Insert CAD). Each QR code box is already extruded.

### Generate STEP with Cylinder Base and Railing
```sh
python3 qrgen_for3dprint.py --step --cylinder --output qr_on_cylinder.step
```
- Adds a circular base and a 1mm-high, 1mm-thick outer railing (frame) around the QR code.
- Use `--cylinder-diameter` to set the base diameter and auto-scale the QR code to fit.
- Use `--qr-height` to set the QR code box height (default: 1mm).
- Use `--cylinder-height` and `--cylinder-margin` to further customize the base.

#### Example with all options:
```sh
python3 qrgen_for3dprint.py --step --cylinder --cylinder-diameter 60 --qr-height 1.5 --cylinder-height 3 --output qr_on_cylinder.step
```

## Command-Line Options
- `--url` : The URL to encode (default: Instagram Walnut Event)
- `--output` : Output filename (.svg or .step)
- `--border` : Border size for the QR code
- `--box-size` : Size of one QR code square (SVG units or mm)
- `--qr-height` : Height of extruded QR code boxes (mm, STEP only)
- `--step` : Generate a STEP file (default is SVG)
- `--cylinder` : Add a cylinder base (STEP only)
- `--cylinder-height` : Height of the cylinder base (mm)
- `--cylinder-margin` : Margin around the QR code on the cylinder (mm)
- `--cylinder-diameter` : Set the cylinder diameter (mm) and auto-scale QR code to fit
- `--test` : Run built-in tests

## Example Output
- SVG: Minimal, clean, and ready for CAD import and extrusion.
- STEP: 3D model with QR code as extruded boxes, optionally on a round base with a frame.

---

**Author:** (your name) 