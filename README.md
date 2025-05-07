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

# Additional Scripts and Programs in this Repository

## Python Scripts

### add_numbers.py
**Purpose:** Add two numbers or two numbers represented as linked lists (LeetCode style).
- Command-line or interactive mode.
- Handles both integer/float addition and linked-list digit addition.
- Input validation, overflow protection, and test cases included.
**Usage:**
```sh
python3 add_numbers.py 3 5
# or just run for interactive tests
python3 add_numbers.py
```

### image_resizer.py
**Purpose:** Resize images to 640x480 (or proportional) using different interpolation methods.
- Supports nearest, bilinear, and bicubic interpolation.
- Command-line interface for batch processing.
- Uses Pillow (PIL) for image operations.
**Usage:**
```sh
python3 image_resizer.py input.jpg --methods nearest bilinear bicubic
```

### ollama_music.py
**Purpose:** Query an Ollama LLM server for a music-related prompt and print the response.
- Sends a prompt to a local Ollama server (default: gemma3:4b model).
- Prints the LLM's response.
**Usage:**
```sh
python3 ollama_music.py
```

### sumkeyvalue.py
**Purpose:** Sum values by key from input data (stdin or file).
- Reads key-value pairs, sums values for each key, and prints sorted results.
- Handles malformed lines gracefully.
**Usage:**
```sh
cat input.txt | ./sumkeyvalue.py
```

### test_add_numbers.py
**Purpose:** Unit tests for `add_numbers.py` (including edge cases, overflow, and input validation).
**Usage:**
```sh
python3 -m unittest test_add_numbers.py
```

### url_list.py
**Purpose:** Read URLs from a file, validate them, and store them in a linked list.
- Validates URLs using regex.
- Prints valid and invalid URLs separately.
**Usage:**
```sh
python3 url_list.py urls.txt
```

---

## Shell Scripts

### a2cprint.sh
**Purpose:** Print files with color and selectable font size using `a2ps`.
- Menu for font size selection.
- Validates input and dependencies.
**Usage:**
```sh
./a2cprint.sh output.ps input.txt
```

### iptables_block_port80.sh
**Purpose:** Block all incoming TCP traffic on a specified port (default: 80) using iptables.
**Usage:**
```sh
sudo ./iptables_block_port80.sh [port]
```

### launch_cursor.sh
**Purpose:** Launch the Cursor editor AppImage, ensure it is executable, and create a symlink in `~/bin`.
**Usage:**
```sh
./launch_cursor.sh ~/Applications/cursor.AppImage
```

### prime_numbers.sh
**Purpose:** Print all prime numbers up to a given limit.
**Usage:**
```sh
./prime_numbers.sh 100
```

### zombie_checker.sh
**Purpose:** Identify zombie processes on a Linux system and provide information about their parent processes.
**Usage:**
```sh
./zombie_checker.sh
```

---

## C Programs

### url_list.c
**Purpose:** Read URLs from a file and store them in a linked list, then print the list.
**Usage:**
```sh
gcc url_list.c -o url_list
./url_list
```

### zombie.c
**Purpose:** Demonstrate zombie process creation in Linux.
- Parent process creates a child, which exits immediately.
- Parent sleeps, leaving a zombie process.
- Useful for learning about process management.
**Usage:**
```sh
gcc zombie.c -o zombie
./zombie
```

---

**Author:** Jan Gelin  
**Contact:** jan@gelin.us 