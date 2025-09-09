#!/bin/bash

# Manim Docker Render Script
# Usage: ./render_manim.sh <path_to_python_file> [scene_name] [quality]
# Example: ./render_manim.sh "Riyaziyyat/Orta Məktəb/video-1/manim_video.py" MobileVideo -qh

set -e

# Check if file path is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <path_to_python_file> [scene_name] [quality]"
    echo "Example: $0 'Riyaziyyat/Orta Məktəb/video-1/manim_video.py' MobileVideo -qh"
    echo ""
    echo "Quality options:"
    echo "  -ql  Low quality (480p)"
    echo "  -qm  Medium quality (720p)"  
    echo "  -qh  High quality (1080p)"
    echo "  -qp  Production quality (1440p)"
    echo "  -qk  4K quality (2160p)"
    exit 1
fi

PYTHON_FILE="$1"
SCENE_NAME="${2:-}"
QUALITY="${3:--qh}"

# Check if file exists
if [ ! -f "$PYTHON_FILE" ]; then
    echo "Error: File '$PYTHON_FILE' not found"
    exit 1
fi

# Get the directory containing the Python file
DIR_PATH=$(dirname "$PYTHON_FILE")
FILE_NAME=$(basename "$PYTHON_FILE")

# Create output directory if it doesn't exist
mkdir -p "$DIR_PATH/media"

echo "Rendering manim animation..."
echo "File: $PYTHON_FILE"
echo "Scene: $SCENE_NAME"
echo "Quality: $QUALITY"
echo "Output directory: $DIR_PATH/media"

# Run manim with Docker
# Mount the current directory to /manim in the container
docker run --rm -it \
    -v "$(pwd):/manim" \
    -w "/manim" \
    manimcommunity/manim:latest \
    manim "$PYTHON_FILE" $SCENE_NAME $QUALITY

echo "Rendering complete!"
echo "Output files are in: $DIR_PATH/media/"

# List the generated files
if [ -d "$DIR_PATH/media" ]; then
    echo ""
    echo "Generated files:"
    find "$DIR_PATH/media" -name "*.mp4" -o -name "*.png" | sort
fi