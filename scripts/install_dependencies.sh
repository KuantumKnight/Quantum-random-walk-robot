#!/bin/bash
# Installation script for Quantum Random Walk Robot

set -e

echo "=== Quantum Random Walk Robot Setup ==="
echo "Installing dependencies and setting up environment..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )[0-9]+\.[0-9]+' || echo "0.0")
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.8+ required. Found: $python_version"
    exit 1
fi

echo "✓ Python version check passed: $python_version"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "✓ Virtual environment activated"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing Python packages..."
pip install -r requirements.txt

echo "✓ Python packages installed"

# Install development dependencies (optional)
if [[ "${1:-}" == "--dev" ]]; then
    echo "Installing development dependencies..."
    pip install -e ".[dev]"
    pre-commit install
    echo "✓ Development environment ready"
fi

# Create necessary directories
echo "Creating project directories..."
mkdir -p data exports logs temp config/profiles

echo "✓ Directory structure created"

# Set permissions (Unix-like systems)
if [[ "$OSTYPE" != "msys" && "$OSTYPE" != "win32" ]]; then
    chmod +x scripts/*.sh
    chmod +x scripts/*.py
    echo "✓ Permissions set"
fi

echo ""
echo "=== Installation Complete ==="
echo "To activate the environment:"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "  venv\\Scripts\\activate"
else
    echo "  source venv/bin/activate"
fi
echo ""
echo "To run the application:"
echo "  python -m src.gui.quantum_robot_gui"
echo ""
echo "For hardware setup, see: docs/hardware-setup.md"
