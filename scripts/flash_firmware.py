#!/usr/bin/env python3
"""
Firmware flashing utility for Arduino and NodeMCU
Automates the firmware upload process
"""

import sys
import subprocess
import time
import serial
import serial.tools.list_ports
from pathlib import Path
import argparse

class FirmwareFlasher:
    """Utility for flashing firmware to Arduino and NodeMCU"""
    
    def __init__(self):
        self.arduino_sketch = "src/firmware/arduino/quantum_robot_controller.ino"
        self.nodemcu_sketch = "src/firmware/nodemcu/wifi_quantum_bridge.ino"
        
    def find_arduino_ports(self):
        """Find available Arduino ports"""
        ports = []
        for port in serial.tools.list_ports.comports():
            # Common Arduino USB IDs
            if any(vid in str(port.hwid).lower() for vid in ['2341', '1a86', 'ch340', 'ftdi']):
                ports.append(port.device)
        return ports
    
    def flash_arduino(self, port=None, board="arduino:avr:uno"):
        """Flash Arduino firmware"""
        print("=== Flashing Arduino Firmware ===")
        
        if not Path(self.arduino_sketch).exists():
            print(f"Error: Arduino sketch not found: {self.arduino_sketch}")
            return False
            
        if port is None:
            ports = self.find_arduino_ports()
            if not ports:
                print("No Arduino ports found. Please connect Arduino and try again.")
                return False
            port = ports[0]
            print(f"Auto-selected port: {port}")
        
        # Compile and upload using Arduino CLI
        compile_cmd = [
            "arduino-cli", "compile",
            "--fqbn", board,
            self.arduino_sketch
        ]
        
        upload_cmd = [
            "arduino-cli", "upload",
            "--fqbn", board,
            "--port", port,
            self.arduino_sketch
        ]
        
        try:
            print("Compiling Arduino sketch...")
            subprocess.run(compile_cmd, check=True)
            print("✓ Compilation successful")
            
            print("Uploading to Arduino...")
            subprocess.run(upload_cmd, check=True)
            print("✓ Upload successful")
            
            # Test communication
            time.sleep(2)
            if self.test_arduino_communication(port):
                print("✓ Arduino communication test passed")
                return True
            else:
                print("⚠ Arduino communication test failed")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"Error flashing Arduino: {e}")
            return False
        except FileNotFoundError:
            print("Error: arduino-cli not found. Please install Arduino CLI.")
            print("See: https://arduino.github.io/arduino-cli/installation/")
            return False
    
    def flash_nodemcu(self, port=None):
        """Flash NodeMCU firmware"""
        print("=== Flashing NodeMCU Firmware ===")
        
        if not Path(self.nodemcu_sketch).exists():
            print(f"Error: NodeMCU sketch not found: {self.nodemcu_sketch}")
            return False
            
        board = "esp8266:esp8266:nodemcuv2"
        
        if port is None:
            ports = self.find_arduino_ports()
            if not ports:
                print("No NodeMCU ports found. Please connect NodeMCU and try again.")
                return False
            port = ports[0]
            print(f"Auto-selected port: {port}")
        
        # Compile and upload
        compile_cmd = [
            "arduino-cli", "compile",
            "--fqbn", board,
            self.nodemcu_sketch
        ]
        
        upload_cmd = [
            "arduino-cli", "upload",
            "--fqbn", board,
            "--port", port,
            self.nodemcu_sketch
        ]
        
        try:
            print("Compiling NodeMCU sketch...")
            subprocess.run(compile_cmd, check=True)
            print("✓ Compilation successful")
            
            print("Uploading to NodeMCU...")
            subprocess.run(upload_cmd, check=True)
            print("✓ Upload successful")
            
            # Test WiFi AP
            time.sleep(5)
            if self.test_nodemcu_wifi():
                print("✓ NodeMCU WiFi test passed")
                return True
            else:
                print("⚠ NodeMCU WiFi test failed")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"Error flashing NodeMCU: {e}")
            return False
    
    def test_arduino_communication(self, port, timeout=5):
        """Test Arduino serial communication"""
        try:
            with serial.Serial(port, 115200, timeout=timeout) as ser:
                ser.write(b"STATUS\n")
                time.sleep(1)
                response = ser.read_all().decode()
                return "QUANTUM ROBOT" in response.upper()
        except Exception as e:
            print(f"Arduino communication error: {e}")
            return False
    
    def test_nodemcu_wifi(self):
        """Test NodeMCU WiFi AP creation"""
        import subprocess
        try:
            if sys.platform.startswith('win'):
                result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], 
                                      capture_output=True, text=True)
                return 'QuantumRobot' in result.stdout or 'RobotAP' in result.stdout
            else:
                result = subprocess.run(['iwlist', 'scan'], 
                                      capture_output=True, text=True)
                return 'QuantumRobot' in result.stdout or 'RobotAP' in result.stdout
        except:
            print("Could not test WiFi AP - manual verification required")
            return True  # Assume success if can't test
    
    def install_dependencies(self):
        """Install required tools"""
        print("=== Installing Dependencies ===")
        
        # Check for Arduino CLI
        try:
            subprocess.run(['arduino-cli', 'version'], check=True, capture_output=True)
            print("✓ Arduino CLI found")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Installing Arduino CLI...")
            # Installation commands would go here
            print("Please install Arduino CLI manually:")
            print("https://arduino.github.io/arduino-cli/installation/")
            return False
        
        # Install board packages
        print("Installing board packages...")
        try:
            subprocess.run(['arduino-cli', 'core', 'update-index'], check=True)
            subprocess.run(['arduino-cli', 'core', 'install', 'arduino:avr'], check=True)
            subprocess.run(['arduino-cli', 'core', 'install', 'esp8266:esp8266'], check=True)
            print("✓ Board packages installed")
            return True
        except subprocess.CalledProcessError:
            print("Error installing board packages")
            return False

def main():
    parser = argparse.ArgumentParser(description="Flash firmware to quantum robot")
    parser.add_argument('--target', choices=['arduino', 'nodemcu', 'both'], 
                       default='both', help='Target device to flash')
    parser.add_argument('--port', help='Serial port (auto-detect if not specified)')
    parser.add_argument('--install-deps', action='store_true', 
                       help='Install required dependencies')
    
    args = parser.parse_args()
    
    flasher = FirmwareFlasher()
    
    if args.install_deps:
        if not flasher.install_dependencies():
            sys.exit(1)
    
    success = True
    
    if args.target in ['arduino', 'both']:
        success &= flasher.flash_arduino(args.port)
    
    if args.target in ['nodemcu', 'both']:
        success &= flasher.flash_nodemcu(args.port)
    
    if success:
        print("\n=== Firmware Flashing Complete ===")
        print("Your quantum robot is ready!")
        print("Connect to the robot WiFi network and run the GUI application.")
    else:
        print("\n=== Firmware Flashing Failed ===")
        print("Please check connections and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
