#!/bin/bash

# Update package list and install system dependencies
sudo apt update
sudo apt upgrade
sudo apt install -y python3-gi gir1.2-gtk-3.0

# Install Python packages
pip install pyperclip
pip install PyGObject

echo "Instalação completa. Agora você pode rodar o Conversor !."
