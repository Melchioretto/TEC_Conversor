#!/bin/bash

# Install Python packages
pip install pyperclip
pip install PyGObject

# Install system dependencies for GTK
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v apt-get >/dev/null; then
        sudo apt-get install python3-gi gir1.2-gtk-3.0 -y
    elif command -v dnf >/dev/null; then
        sudo dnf install python3-gobject gtk3 -y
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Please install GTK dependencies manually on macOS."
elif [[ "$OSTYPE" == "cygwin" ]]; then
    echo "Cygwin is not officially supported. Please use a different environment."
elif [[ "$OSTYPE" == "msys" ]]; then
    echo "MSYS/MinGW is not officially supported. Please use a different environment."
else
    echo "Unknown operating system. Please install dependencies manually."
fi

echo "All dependencies installed."
