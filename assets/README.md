# Assets Directory

This directory contains visual assets for the Quantum Random Walk Robot project.

## Directory Structure

assets/
├── icons/ # Application icons and UI elements
├── images/ # Documentation images and screenshots
├── schematics/ # Circuit diagrams and hardware schematics
└── themes/ # GUI theme files

text

## File Formats

### Icons
- **Format:** PNG with transparency
- **Sizes:** 16x16, 32x32, 64x64, 128x128 pixels
- **Style:** Consistent with quantum/robotics theme

### Images
- **Screenshots:** PNG format, high resolution
- **Diagrams:** SVG preferred, PNG acceptable
- **Photos:** JPEG for photos, PNG for technical images

### Schematics
- **Fritzing:** .fzz files for circuit diagrams
- **KiCad:** .kicad_sch and .kicad_pcb files
- **Eagle:** .sch and .brd files
- **Exports:** PDF and PNG versions for documentation

## Usage Guidelines

### Icons
- Use quantum-themed icons (atoms, waves, particles)
- Maintain consistent color scheme (blues, purples, cyans)
- Include both light and dark theme variants

### Documentation Images
- High contrast for visibility
- Annotated with clear labels
- Consistent styling across all images

### Hardware Schematics
- Follow standard schematic symbols
- Include component values and part numbers
- Provide both simplified and detailed versions

## Attribution

Some icons and images may be sourced from:
- Quantum computing icon libraries
- Creative Commons resources
- Custom designs by project contributors

See individual file metadata for specific attributions.
Dockerfile (Optional but useful)

text
# Quantum Random Walk Robot - Docker Container
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-tk \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config/ ./config/
COPY examples/ ./examples/
COPY docs/ ./docs/

# Create data directory
RUN mkdir -p data exports logs

# Set environment variables
ENV PYTHONPATH=/app/src
ENV DISPLAY=:0

# Expose port for web interface (if added)
EXPOSE 8080

# Default command
CMD ["python", "-m", "src.gui.quantum_robot_gui"]
Makefile (Optional build automation)

makefile
# Quantum Random Walk Robot - Build Automation

.PHONY: help install test lint format clean build docker

help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies"
	@echo "  test        - Run test suite"
	@echo "  lint        - Run code linting"
	@echo "  format      - Format code with black"
	@echo "  clean       - Clean build artifacts"
	@echo "  build       - Build distribution packages"
	@echo "  docker      - Build Docker image"

install:
	python -m venv venv
	./venv/bin/pip install -r requirements.txt
	./venv/bin/pip install -e .

test:
	./venv/bin/python scripts/run_tests.py

lint:
	./venv/bin/flake8 src/ tests/ examples/
	./venv/bin/mypy src/

format:
	./venv/bin/black src/ tests/ examples/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: clean
	./venv/bin/python -m build

docker:
	docker build -t quantum-robot .

flash-arduino:
	python scripts/flash_firmware.py --target arduino

flash-nodemcu:
	python scripts/flash_firmware.py --target nodemcu

flash-all: flash-arduino flash-nodemcu

run:
	./venv/bin/python -m src.gui.quantum_robot_gui

demo:
	./venv/bin/python examples/basic_quantum_walk.py