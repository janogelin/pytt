#!/bin/bash

# Check if argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <path_to_cursor.AppImage>"
    echo "Example: $0 ~/Applications/cursor.AppImage"
    exit 1
fi

# Define paths using $HOME environment variable
CURSOR_APP="$1"
SYMLINK_PATH="$HOME/bin/cursor"

# Check if Cursor.AppImage exists
if [ ! -f "$CURSOR_APP" ]; then
    echo "Error: Cursor.AppImage not found at $CURSOR_APP"
    echo "Please ensure the application is installed in the correct location."
    exit 1
fi

# Check if Cursor.AppImage is executable
if [ ! -x "$CURSOR_APP" ]; then
    echo "Error: Cursor.AppImage is not executable"
    echo "Attempting to make it executable..."
    if ! chmod +x "$CURSOR_APP"; then
        echo "Failed to make Cursor.AppImage executable. Please check permissions."
        exit 2
    fi
    echo "Successfully made Cursor.AppImage executable"
fi

# Launch Cursor with --no-sandbox flag in background
"$CURSOR_APP" --no-sandbox &
if [ $? -ne 0 ]; then
    echo "Error: Failed to launch Cursor.AppImage"
    exit 3
fi

# Create bin directory if it doesn't exist
if [ ! -d "$HOME/bin" ]; then
    if ! mkdir -p "$HOME/bin"; then
        echo "Error: Failed to create $HOME/bin directory"
        exit 4
    fi
fi

# Remove existing symlink if it exists
if [ -L "$SYMLINK_PATH" ]; then
    if ! rm "$SYMLINK_PATH"; then
        echo "Error: Failed to remove existing symlink"
        exit 5
    fi
fi

# Create new symlink
if ! ln -s "$CURSOR_APP" "$SYMLINK_PATH"; then
    echo "Error: Failed to create symlink"
    exit 6
fi

echo "Cursor.AppImage launched successfully"
echo "Symlink created at $SYMLINK_PATH"

# Final verification
if [ -f "$CURSOR_APP" ] && [ -x "$CURSOR_APP" ] && [ -L "$SYMLINK_PATH" ]; then
    echo "All checks passed:"
    echo "✓ Cursor.AppImage exists"
    echo "✓ Cursor.AppImage is executable"
    echo "✓ Symlink is properly set up"
    exit 0
else
    echo "Warning: Final verification failed. Please check the installation manually."
    exit 7
fi 