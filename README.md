# The Lunar Almanac Image Optimizer

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

A simple Python script to optimize images for web use. It converts images of any supported format (PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP) to WebP format, resizes them to a specified maximum width (default: 300px), and compresses them to 85% quality by default. This helps minimize file sizes while maintaining high visual quality—perfect for websites, blogs, or projects like The Lunar Almanac.

## Features
- **Batch Processing**: Optimize a single image or an entire directory.
- **Resizable**: Scales images down to a user-specified width while preserving aspect ratio (using LANCZOS resampling for high quality).
- **Compression**: Converts to WebP with configurable quality (0-100).
- **Transparency Handling**: Converts RGBA images to RGB on a white background (WebP support for alpha is limited in some contexts).
- **Interactive Prompt**: If not specified via CLI, prompts for max width in interactive terminals.
- **CLI Options**: Customize output directory, width, and quality.
- **Feedback**: Prints detailed progress, including size reductions and savings percentages.

## Requirements
- Python 3.8 or higher
- Pillow (Python Imaging Library): `pip install pillow`

The script uses the Pillow library for image processing. No other external dependencies.

## Installation
1. Clone or download this repository.
2. Install the dependency: pip install pillow
3. (Optional) Create a virtual environment for isolation:
 - python3 -m venv env
 - source env/bin/activate  # On Windows: env\Scripts\activate
 - pip install pillow
4. Make the script executable (optional, for direct running):
 - chmod +x optimize-images.py

## Usage
Run the script from the command line. It supports single files or directories.

  ### Basic Commands
  - **Single file**:
    python3 optimize-images.py test-image.png
    (If `--width` is omitted in a terminal, you'll be prompted interactively.)

- **Entire directory**:
  python3 optimize-images.py ./mythology-images/

- **Custom settings** (e.g., output dir, width, quality):
  python3 optimize-images.py ./images/ --output ./optimized/ --width 400 --quality 90

  ### Options
  - `--output <dir>`: Output directory (default: same as input). Creates if it doesn't exist.
  - `--width <pixels>`: Max width in pixels (default: 300; prompts interactively if omitted in terminal).
  - `--quality <0-100>`: WebP quality level (default: 85; higher = better quality, larger files).

  ### Examples
  - Optimize a single image with defaults (will prompt for width if needed):
    python3 optimize-images.py test-image.png

  - Optimize a directory and save to a new folder with custom size/quality:
    python3 optimize-images.py ./mythology-images/ --output ./optimized-myths/ --width 600 --quality 80

  - Output files are saved as `.webp` in the specified directory, overwriting if exists (be cautious!).

## How It Works
1. Opens the image with Pillow.
2. Converts modes as needed (e.g., RGBA to RGB).
3. Resizes if wider than max_width, maintaining aspect ratio.
4. Saves as WebP with method=6 for optimal compression.
5. Reports original vs. new size and savings.

For directories, it recursively scans for supported images but only processes files directly in the folder (not subfolders). Extend the script if needed for recursion.

## Limitations
- Does not handle alpha transparency in output (converts to white background).
- No recursive directory processing (top-level only).
- GIF animations are converted to static WebP (loses animation).
- Requires a terminal for interactive prompts; defaults to 300px in non-interactive runs.

## Contributing
Feel free to fork and submit pull requests! Ideas for improvements:
- Add recursive directory support.
- Option for lossless WebP.
- Preserve transparency with WebP alpha.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details (add one if not present).

---

Optimized for The Lunar Almanac project. Questions? Open an issue!