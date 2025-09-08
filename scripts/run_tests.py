#!/usr/bin/env python3
"""
Test runner with comprehensive coverage and reporting
"""

import subprocess
import sys
import argparse
from pathlib import Path

def run_unit_tests(verbose=False, coverage=True):
    """Run unit tests"""
    print("=== Running Unit Tests ===")
    
    cmd = ["python", "-m", "pytest", "tests/"]
    
    if verbose:
        cmd.append("-v")
    
    if coverage:
        cmd.extend(["--cov=src", "--cov-report=html", "--cov-report=term-missing"])
    
    result = subprocess.run(cmd)
    return result.returncode == 0

def run_integration_tests():
    """Run integration tests"""
    print("=== Running Integration Tests ===")
    
    cmd = ["python", "-m", "pytest", "tests/integration/", "-v"]
    result = subprocess.run(cmd)
    return result.returncode == 0

def run_hardware_tests():
    """Run hardware tests (requires connected hardware)"""
    print("=== Running Hardware Tests ===")
    
    # Check if hardware is connected
    print("Checking for connected hardware...")
    
    cmd = ["python", "tests/hardware/test_connection.py"]
    result = subprocess.run(cmd)
    return result.returncode == 0

def run_linting():
    """Run code linting"""
    print("=== Running Code Linting ===")
    
    success = True
    
    # Black formatting check
    print("Checking code formatting...")
    result = subprocess.run(["black", "--check", "src/", "tests/", "examples/"])
    success &= result.returncode == 0
    
    # Flake8 linting
    print("Running flake8 linting...")
    result = subprocess.run(["flake8", "src/", "tests/", "examples/"])
    success &= result.returncode == 0
    
    # MyPy type checking
    print("Running type checking...")
    result = subprocess.run(["mypy", "src/"])
    success &= result.returncode == 0
    
    return success

def generate_test_report():
    """Generate comprehensive test report"""
    print("=== Generating Test Report ===")
    
    timestamp = Path("test_report.html").stat().st_mtime if Path("test_report.html").exists() else 0
    
    # Generate HTML report
    subprocess.run([
        "python", "-m", "pytest", 
        "--html=test_report.html", 
        "--self-contained-html",
        "tests/"
    ])
    
    print("Test report generated: test_report.html")
    return True

def main():
    parser = argparse.ArgumentParser(description="Run quantum robot tests")
    parser.add_argument('--unit', action='store_true', help='Run unit tests only')
    parser.add_argument('--integration', action='store_true', help='Run integration tests')
    parser.add_argument('--hardware', action='store_true', help='Run hardware tests')
    parser.add_argument('--lint', action='store_true', help='Run linting only')
    parser.add_argument('--no-coverage', action='store_true', help='Skip coverage reporting')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--report', action='store_true', help='Generate HTML test report')
    
    args = parser.parse_args()
    
    # If no specific tests requested, run all
    if not any([args.unit, args.integration, args.hardware, args.lint]):
        args.unit = True
        args.lint = True
    
    success = True
    
    if args.lint:
        success &= run_linting()
    
    if args.unit:
        success &= run_unit_tests(args.verbose, not args.no_coverage)
    
    if args.integration:
        success &= run_integration_tests()
    
    if args.hardware:
        print("Hardware tests require connected Arduino and NodeMCU")
        confirm = input("Continue with hardware tests? (y/N): ")
        if confirm.lower() == 'y':
            success &= run_hardware_tests()
    
    if args.report:
        generate_test_report()
    
    if success:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
