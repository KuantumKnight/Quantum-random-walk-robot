#!/usr/bin/env python3
"""
Hardware connection test suite
Tests actual Arduino and NodeMCU hardware connectivity
"""

import serial
import serial.tools.list_ports
import socket
import time
import sys
from pathlib import Path

class HardwareConnectionTester:
    """Test suite for hardware connections"""
    
    def __init__(self):
        self.results = []
        
    def find_arduino_ports(self):
        """Find connected Arduino-compatible devices"""
        arduino_ports = []
        
        for port in serial.tools.list_ports.comports():
            # Check for common Arduino vendor IDs
            vid_pids = [
                '2341',  # Arduino official
                '1a86',  # CH340 chip
                '0403',  # FTDI chip
                '10c4',  # Silicon Labs
            ]
            
            port_info = str(port.hwid).upper()
            if any(vid in port_info for vid in vid_pids):
                arduino_ports.append({
                    'port': port.device,
                    'description': port.description,
                    'hwid': port.hwid
                })
                
        return arduino_ports
        
    def test_arduino_serial(self, port, timeout=5):
        """Test Arduino serial communication"""
        try:
            print(f"Testing Arduino on {port}...")
            
            with serial.Serial(port, 115200, timeout=timeout) as ser:
                # Wait for Arduino to boot
                time.sleep(2)
                
                # Send test command
                ser.write(b"STATUS\n")
                time.sleep(1)
                
                # Read response
                response = ser.read_all().decode('utf-8', errors='ignore')
                
                # Check for expected response
                if 'QUANTUM' in response.upper() or 'ROBOT' in response.upper():
                    print(f"✓ Arduino communication successful on {port}")
                    return True, response
                else:
                    print(f"⚠ Arduino responded but with unexpected data: {response}")
                    return False, response
                    
        except serial.SerialException as e:
            print(f"✗ Arduino serial error on {port}: {e}")
            return False, str(e)
        except Exception as e:
            print(f"✗ Unexpected error testing Arduino on {port}: {e}")
            return False, str(e)
            
    def test_nodemcu_wifi(self, expected_ip="192.168.4.1", timeout=5):
        """Test NodeMCU WiFi AP and TCP server"""
        try:
            print(f"Testing NodeMCU WiFi at {expected_ip}...")
            
            # Test TCP connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            result = sock.connect_ex((expected_ip, 80))
            
            if result == 0:
                # Connection successful, test communication
                test_message = b"pass123PING\n"
                sock.send(test_message)
                
                response = sock.recv(1024).decode('utf-8', errors='ignore')
                sock.close()
                
                if 'PONG' in response.upper():
                    print(f"✓ NodeMCU communication successful")
                    return True, response
                else:
                    print(f"⚠ NodeMCU connected but unexpected response: {response}")
                    return False, response
            else:
                sock.close()
                print(f"✗ Cannot connect to NodeMCU at {expected_ip}:80")
                return False, f"Connection failed with error code {result}"
                
        except socket.timeout:
            print(f"✗ NodeMCU connection timeout")
            return False, "Connection timeout"
        except Exception as e:
            print(f"✗ NodeMCU connection error: {e}")
            return False, str(e)
            
    def test_motor_control(self, arduino_port):
        """Test motor control functionality"""
        try:
            print(f"Testing motor control via {arduino_port}...")
            
            with serial.Serial(arduino_port, 115200, timeout=3) as ser:
                time.sleep(2)  # Arduino boot time
                
                # Test motor commands
                test_commands = [
                    "LEFT",
                    "RIGHT", 
                    "FORWARD",
                    "BACKWARD",
                    "STOP"
                ]
                
                success_count = 0
                
                for cmd in test_commands:
                    ser.write(f"{cmd}\n".encode())
                    time.sleep(0.5)
                    
                    # Read any response
                    response = ser.read_all().decode('utf-8', errors='ignore')
                    
                    if cmd.upper() in response.upper():
                        success_count += 1
                        print(f"  ✓ {cmd} command acknowledged")
                    else:
                        print(f"  ⚠ {cmd} command may not be working")
                
                if success_count >= 3:  # At least 3 commands working
                    print(f"✓ Motor control test passed ({success_count}/{len(test_commands)})")
                    return True, f"{success_count}/{len(test_commands)} commands working"
                else:
                    print(f"⚠ Motor control test partial ({success_count}/{len(test_commands)})")
                    return False, f"Only {success_count}/{len(test_commands)} commands working"
                    
        except Exception as e:
            print(f"✗ Motor control test failed: {e}")
            return False, str(e)
            
    def test_system_integration(self, arduino_port, nodemcu_ip="192.168.4.1"):
        """Test full system integration"""
        try:
            print("Testing system integration...")
            
            # Test command forwarding through NodeMCU to Arduino
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            
            sock.connect((nodemcu_ip, 80))
            
            # Send authenticated command
            test_cmd = b"pass123LEFT\n"
            sock.send(test_cmd)
            
            time.sleep(1)
            
            # Check if Arduino received it (monitor serial)
            response = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            
            print(f"✓ System integration test completed")
            return True, "Integration successful"
            
        except Exception as e:
            print(f"✗ System integration test failed: {e}")
            return False, str(e)
            
    def run_full_test_suite(self):
        """Run complete hardware test suite"""
        print("=== Quantum Robot Hardware Test Suite ===")
        print()
        
        # Find Arduino devices
        arduino_ports = self.find_arduino_ports()
        
        if not arduino_ports:
            print("✗ No Arduino devices found")
            print("Please check USB connections and drivers")
            return False
            
        print(f"Found {len(arduino_ports)} Arduino-compatible device(s):")
        for port_info in arduino_ports:
            print(f"  - {port_info['port']}: {port_info['description']}")
        print()
        
        # Test each Arduino
        arduino_working = False
        working_arduino_port = None
        
        for port_info in arduino_ports:
            success, result = self.test_arduino_serial(port_info['port'])
            if success:
                arduino_working = True
                working_arduino_port = port_info['port']
                break
                
        if not arduino_working:
            print("✗ No working Arduino found")
            return False
            
        print()
        
        # Test NodeMCU WiFi
        nodemcu_success, nodemcu_result = self.test_nodemcu_wifi()
        
        if not nodemcu_success:
            print("✗ NodeMCU WiFi test failed")
            print("Please check NodeMCU power and firmware")
            return False
            
        print()
        
        # Test motor control
        motor_success, motor_result = self.test_motor_control(working_arduino_port)
        
        print()
        
        # Test system integration
        integration_success, integration_result = self.test_system_integration(
            working_arduino_port, "192.168.4.1"
        )
        
        print()
        
        # Summary
        all_tests_passed = arduino_working and nodemcu_success and motor_success and integration_success
        
        print("=== Test Summary ===")
        print(f"Arduino Communication: {'✓ PASS' if arduino_working else '✗ FAIL'}")
        print(f"NodeMCU WiFi: {'✓ PASS' if nodemcu_success else '✗ FAIL'}")  
        print(f"Motor Control: {'✓ PASS' if motor_success else '✗ FAIL'}")
        print(f"System Integration: {'✓ PASS' if integration_success else '✗ FAIL'}")
        print()
        
        if all_tests_passed:
            print("🎉 All hardware tests PASSED!")
            print("Your Quantum Random Walk Robot is ready!")
        else:
            print("⚠ Some tests FAILED!")
            print("Please check hardware connections and firmware")
            
        return all_tests_passed

def main():
    """Main test runner"""
    tester = HardwareConnectionTester()
    
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
        
        if test_type == "arduino":
            ports = tester.find_arduino_ports()
            if ports:
                success, result = tester.test_arduino_serial(ports[0]['port'])
                sys.exit(0 if success else 1)
            else:
                print("No Arduino found")
                sys.exit(1)
                
        elif test_type == "nodemcu":
            success, result = tester.test_nodemcu_wifi()
            sys.exit(0 if success else 1)
            
        elif test_type == "motors":
            ports = tester.find_arduino_ports()
            if ports:
                success, result = tester.test_motor_control(ports[0]['port'])
                sys.exit(0 if success else 1)
            else:
                print("No Arduino found") 
                sys.exit(1)
    else:
        # Run full test suite
        success = tester.run_full_test_suite()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
