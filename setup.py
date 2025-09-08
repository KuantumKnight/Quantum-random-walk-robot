#!/usr/bin/env python3
"""
Setup script for Quantum Random Walk Robot
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    with open(requirements_path) as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="quantum-random-walk-robot",
    version="2.0.0",
    author="Quantum Robotics Team",
    author_email="quantum.robot.project@gmail.com",
    description="A quantum-inspired robotics control system with real-time visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/quantum-random-walk-robot",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/quantum-random-walk-robot/issues",
        "Source": "https://github.com/yourusername/quantum-random-walk-robot",
        "Documentation": "https://quantum-random-walk-robot.readthedocs.io",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Education",
        "Topic :: System :: Hardware :: Hardware Drivers",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
        "ml": [
            "tensorflow>=2.13.0",
            "torch>=2.0.0",
            "scikit-learn>=1.3.0",
        ],
        "vision": [
            "opencv-python>=4.8.0",
            "pillow>=10.0.0",
        ],
        "advanced": [
            "pyqt6>=6.5.0",
            "pygame>=2.5.0",
            "pyserial>=3.5",
        ],
    },
    entry_points={
        "console_scripts": [
            "quantum-robot=gui.quantum_robot_gui:main",
            "quantum-demo=examples.basic_quantum_walk:main",
            "quantum-entanglement=examples.multi_robot_entanglement:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.md", "*.txt", "*.yaml", "*.yml"],
        "assets": ["icons/*", "themes/*", "schematics/*"],
        "config": ["*.json"],
        "docs": ["*.md", "*.rst"],
    },
    zip_safe=False,
    keywords=[
        "quantum", "robotics", "random-walk", "physics", "education",
        "arduino", "esp8266", "gui", "visualization", "quantum-mechanics"
    ],
    platforms=["any"],
)
