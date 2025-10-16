#!/usr/bin/env python3
"""
Image Optimizer
Converts images to WebP format, compresses, and resizes to user-specified width (default: 300px)
Maintains high quality while minimizing file size
"""

import os
import sys
from pathlib import Path
from PIL import Image

def optimize_image(input_path, output_dir=None, max_width=300, quality=85):
    """
    Optimize an image: convert to WebP, resize, and compress

    Args:
        input_path: Path to input image
        output_dir: Output directory (default: same as input)
        max_width: Maximum width in pixels (default: 300)
        quality: WebP quality 0-100 (default: 85 - high quality, good compression)
    """
    input_path = Path(input_path)

    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        return False

    # Set output directory
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = input_path.parent

    # Generate output filename
    output_path = output_dir / f"{input_path.stem}.webp"

    try:
        # Open image
        print(f"Processing: {input_path.name}")
        img = Image.open(input_path)

        # Convert RGBA to RGB if necessary (WebP doesn't handle transparency the same way)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # Get original dimensions
        original_width, original_height = img.size
        original_size = input_path.stat().st_size / 1024  # KB

        # Resize if wider than max_width
        if original_width > max_width:
            ratio = max_width / original_width
            new_height = int(original_height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            print(f"   Resized: {original_width}x{original_height} → {max_width}x{new_height}")
        else:
            print(f"   Size: {original_width}x{original_height} (no resize needed)")

        # Save as WebP with high quality compression
        img.save(
            output_path,
            'WebP',
            quality=quality,
            method=6,  # Slowest but best compression
            lossless=False
        )

        # Show results
        output_size = output_path.stat().st_size / 1024  # KB
        savings = ((original_size - output_size) / original_size) * 100

        print(f"   Size: {original_size:.1f}KB → {output_size:.1f}KB ({savings:.1f}% reduction)")
        print(f"   Saved: {output_path}")
        print()

        return True

    except Exception as e:
        print(f"   Error processing {input_path.name}: {e}")
        print()
        return False


def optimize_directory(input_dir, output_dir=None, max_width=300, quality=85):
    """
    Optimize all images in a directory

    Args:
        input_dir: Directory containing images
        output_dir: Output directory (default: same as input)
        max_width: Maximum width in pixels
        quality: WebP quality 0-100
    """
    input_dir = Path(input_dir)

    if not input_dir.exists():
        print(f"Error: Directory not found: {input_dir}")
        return

    # Supported image formats
    supported_formats = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'}

    # Find all images
    images = [
        f for f in input_dir.iterdir()
        if f.is_file() and f.suffix.lower() in supported_formats
    ]

    if not images:
        print(f"No images found in {input_dir}")
        return

    print(f"Found {len(images)} images to optimize")
    print(f"Input: {input_dir}")
    print(f"Output: {output_dir or input_dir}")
    print(f"Max width: {max_width}px")
    print(f"Quality: {quality}/100")
    print()

    # Process each image
    success_count = 0
    for img_path in images:
        if optimize_image(img_path, output_dir, max_width, quality):
            success_count += 1

    print(f"Complete! Successfully optimized {success_count}/{len(images)} images")


def main():
    """Main function - parse arguments and run optimization"""

    print("=" * 60)
    print("The Lunar Almanac - Image Optimizer")
    print("=" * 60)
    print()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  Single file:  python optimize-images.py <image.png>")
        print("  Directory:    python optimize-images.py <directory>")
        print()
        print("Options:")
        print("  --output <dir>     Output directory (default: same as input)")
        print("  --width <pixels>   Max width (default: 300, will prompt interactively if not provided)")
        print("  --quality <0-100>  Quality (default: 85)")
        print()
        print("Examples:")
        print("  python optimize-images.py myth-cu-chulainn.png")
        print("  python optimize-images.py ./mythology-images/")
        print("  python optimize-images.py ./images/ --output ./optimized/ --width 400")
        sys.exit(1)

    # Parse arguments
    input_path = Path(sys.argv[1])
    output_dir = None
    max_width = None  # Use None to indicate not provided yet
    quality = 85

    # Parse optional arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--output' and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--width' and i + 1 < len(sys.argv):
            try:
                max_width = int(sys.argv[i + 1])
                if max_width <= 0:
                    raise ValueError
            except ValueError:
                print(f"Error: Invalid width value: {sys.argv[i + 1]}. Must be a positive integer.")
                sys.exit(1)
            i += 2
        elif sys.argv[i] == '--quality' and i + 1 < len(sys.argv):
            try:
                quality = int(sys.argv[i + 1])
                if not (0 <= quality <= 100):
                    raise ValueError
            except ValueError:
                print(f"Error: Invalid quality value: {sys.argv[i + 1]}. Must be 0-100.")
                sys.exit(1)
            i += 2
        else:
            print(f"Warning: Unknown argument: {sys.argv[i]}")
            i += 1

    # Interactive prompt for max_width if not provided and in terminal
    if max_width is None:
        if sys.stdin.isatty():
            try:
                user_input = input(f"Enter max width in pixels (default: 300): ").strip()
                max_width = int(user_input) if user_input else 300
                if max_width <= 0:
                    raise ValueError
            except ValueError:
                print("Error: Invalid input. Using default width of 300.")
                max_width = 300
        else:
            print("No --width provided and not in interactive mode. Using default: 300px")
            max_width = 300

    # Process file or directory
    if input_path.is_file():
        optimize_image(input_path, output_dir, max_width, quality)
    elif input_path.is_dir():
        optimize_directory(input_path, output_dir, max_width, quality)
    else:
        print(f"Error: Not a file or directory: {input_path}")
        sys.exit(1)


if __name__ == '__main__':
    main()