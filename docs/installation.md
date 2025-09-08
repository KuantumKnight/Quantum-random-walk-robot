# Installation Guide

This guide covers the complete installation process for the Quantum Random Walk Robot system.

## Prerequisites

### Software Requirements
- **Python 3.8+** (recommended: Python 3.10 or 3.11)
- **Git** for version control
- **Arduino CLI** or **Arduino IDE** for firmware flashing
- **Serial drivers** for Arduino and NodeMCU

### Hardware Requirements
- Arduino Uno (or compatible)
- NodeMCU ESP8266 development board
- L298N motor driver module
- 2x DC geared motors
- Robot chassis and wheels
- Power supplies (9V for Arduino, 12V for motors)
- Connecting wires and breadboard

## Installation Steps

### 1. Clone the Repository

git clone https://github.com/yourusername/quantum-random-walk-robot.git
cd quantum-random-walk-robot

text

### 2. Automated Installation (Recommended)

**Linux/macOS:**
chmod +x scripts/install_dependencies.sh
./scripts/install_dependencies.sh

text

**Windows:**
scripts\install_dependencies.bat

text

### 3. Manual Installation

If automated installation fails, follow these manual steps:

**Create Virtual Environment:**
python3 -m venv venv
source venv/bin/activate # Linux/macOS

or
venv\Scripts\activate # Windows

text

**Install Dependencies:**
pip install --upgrade pip
pip install -r requirements.txt

text

**Install Development Tools (Optional):**
pip install -e ".[dev]"
pre-commit install

text

### 4. Hardware Setup

Follow the [Hardware Setup Guide](hardware-setup.md) to assemble your robot.

### 5. Flash Firmware

**Automated Flashing:**
python scripts/flash_firmware.py --install-deps

text

**Manual Flashing:**
1. Open Arduino IDE
2. Install ESP8266 board package
3. Flash `src/firmware/arduino/quantum_robot_controller.ino` to Arduino
4. Flash `src/firmware/nodemcu/wifi_quantum_bridge.ino` to NodeMCU

### 6. Test Installation

**Run Tests:**
python scripts/run_tests.py --unit --lint

text

**Test GUI:**
python -m src.gui.quantum_robot_gui

text

## Configuration

### Network Configuration
Edit `config/default_config.json` to match your setup:

{
"network": {
"robot_ip": "192.168.4.1",
"robot_port": 80,
"auth_key": "your_secure_key"
}
}

text

### Robot Calibration
1. Run the GUI application
2. Connect to your robot
3. Use the calibration tools in Settings menu
4. Save calibration parameters

## Troubleshooting

### Common Issues

**Python Import Errors:**
Ensure you're in the virtual environment
source venv/bin/activate

Reinstall packages
pip install -r requirements.txt

text

**Arduino/NodeMCU Not Detected:**
- Check USB cable connections
- Install CH340 or FTDI drivers
- Try different USB ports
- Check device manager (Windows) or `lsusb` (Linux)

**WiFi Connection Issues:**
- Verify NodeMCU is creating AP (QuantumRobot)
- Check IP address is 192.168.4.1
- Restart NodeMCU if needed
- Check firewall settings

**GUI Won't Start:**
- Install tkinter: `sudo apt install python3-tk` (Linux)
- Try alternative GUI: `pip install PyQt6`
- Check display settings in remote sessions

### Getting Help

- Check [Troubleshooting Guide](troubleshooting.md)
- Search existing [GitHub Issues](https://github.com/yourusername/quantum-random-walk-robot/issues)
- Join our [Discord Community](#)
- Email: support@quantumrobot.org

## Next Steps

After successful installation:

1. **Complete Hardware Setup** - Follow hardware assembly guide
2. **Run Example Scripts** - Try `examples/basic_quantum_walk.py`
3. **Explore Features** - Use the GUI to experiment with quantum parameters
4. **Read Documentation** - Check out the theory background
5. **Contribute** - See [Contributing Guide](../CONTRIBUTING.md)

## Advanced Installation

### Docker Installation

Build Docker image
docker build -t quantum-robot .

Run with GUI support (Linux)
docker run -it --rm
-e DISPLAY=$DISPLAY
-v /tmp/.X11-unix:/tmp/.X11-unix
-v $(pwd)/data:/app/data
quantum-robot

text

### Development Installation

Clone with submodules
git clone --recursive https://github.com/yourusername/quantum-random-walk-robot.git

Install in development mode
pip install -e ".[dev,docs,ml,vision]"

Setup pre-commit hooks
pre-commit install

Run full test suite
python scripts/run_tests.py --integration --hardware

text

### Custom Board Support

To use different Arduino-compatible boards:

1. Install board packages in Arduino CLI
2. Modify `scripts/flash_firmware.py` with new board FQBN
3. Update pin mappings in firmware if needed
4. Test hardware compatibility

For questions about specific boards, please open an issue with your hardware details.
docs/api-documentation.md

text
# API Documentation

This document provides comprehensive API documentation for the Quantum Random Walk Robot system.

## Core Modules

### QuantumWalkSimulator

The main quantum simulation engine.

from utils.quantum_math import QuantumWalkSimulator

simulator = QuantumWalkSimulator()

text

#### Methods

##### `initialize(left_amplitude, right_amplitude, coherence_time, noise_level)`
Initialize the quantum system with parameters.

**Parameters:**
- `left_amplitude` (float): Amplitude for left turn state (0.0-1.0)
- `right_amplitude` (float): Amplitude for right turn state (0.0-1.0)
- `coherence_time` (float): Quantum coherence time in seconds
- `noise_level` (float): Environmental noise level (0.0-1.0)

**Example:**
simulator.initialize(
left_amplitude=0.707,
right_amplitude=0.707,
coherence_time=1.0,
noise_level=0.1
)

text

##### `make_quantum_decision()`
Make a quantum-inspired decision.

**Returns:**
- `QuantumDecision`: Object containing decision results

**Example:**
decision = simulator.make_quantum_decision()
print(f"Direction: {decision.direction}")
print(f"Probability: {decision.probability}")
print(f"Entropy: {decision.entropy}")

text

##### `calculate_entropy()`
Calculate von Neumann entropy of the quantum state.

**Returns:**
- `float`: Entropy value between 0 and 1

##### `calculate_coherence()`
Calculate quantum coherence measure.

**Returns:**
- `float`: Coherence value between 0 and 1

### QuantumDataLogger

Database and logging system for missions and telemetry.

from utils.data_logger import QuantumDataLogger

logger = QuantumDataLogger("data/robot.db")

text

#### Methods

##### `start_mission(name, description="", parameters=None)`
Start a new mission logging session.

**Parameters:**
- `name` (str): Mission name
- `description` (str, optional): Mission description
- `parameters` (dict, optional): Mission parameters

**Returns:**
- `int`: Mission ID

**Example:**
mission_id = logger.start_mission(
"Test Mission",
"Testing quantum walk behavior",
{"speed": 5, "coherence_time": 1.0}
)

text

##### `log_telemetry(telemetry_data)`
Log telemetry data point.

**Parameters:**
- `telemetry_data` (dict): Telemetry data dictionary

**Example:**
logger.log_telemetry({
'battery_voltage': 3.7,
'motor_current': 0.5,
'temperature': 25.0,
'rssi': -45
})

text

##### `export_mission_data(mission_id, format='csv', output_dir='exports')`
Export mission data in specified format.

**Parameters:**
- `mission_id` (int): Mission to export
- `format` (str): Export format ('csv', 'json', 'excel')
- `output_dir` (str): Output directory path

**Returns:**
- `list`: List of created file paths

### ConfigManager

Configuration management system.

from gui.config_manager import ConfigManager

config = ConfigManager()

text

#### Properties

- `config.network`: Network configuration (NetworkConfig)
- `config.quantum`: Quantum parameters (QuantumConfig)
- `config.robot`: Robot settings (RobotConfig)
- `config.gui`: GUI preferences (GUIConfig)

#### Methods

##### `create_profile(profile_name, description="")`
Create a new configuration profile.

**Parameters:**
- `profile_name` (str): Name for the new profile
- `description` (str, optional): Profile description

**Returns:**
- `bool`: Success status

##### `load_profile(profile_name)`
Load a configuration profile.

**Parameters:**
- `profile_name` (str): Profile name to load

**Returns:**
- `bool`: Success status

##### `validate_configuration()`
Validate current configuration.

**Returns:**
- `list`: List of validation issues (empty if valid)

### TelemetryVisualizer

Real-time telemetry visualization system.

from gui.telemetry_visualizer import TelemetryVisualizer

visualizer = TelemetryVisualizer()

text

#### Methods

##### `setup_panel(parent_frame)`
Setup telemetry visualization panel in parent frame.

**Parameters:**
- `parent_frame`: Tkinter parent widget

##### `update_telemetry(telemetry_data)`
Update telemetry with new data point.

**Parameters:**
- `telemetry_data` (dict): Telemetry data dictionary

##### `add_warning_callback(callback)`
Add callback function for warning events.

**Parameters:**
- `callback` (callable): Function to call on warnings

**Example:**
def handle_warning(warning_message):
print(f"Warning: {warning_message}")

visualizer.add_warning_callback(handle_warning)

text

## Data Structures

### QuantumDecision

Result of a quantum measurement/decision.

**Attributes:**
- `direction` (str): Decision result ('LEFT' or 'RIGHT')
- `probability` (float): Probability of chosen direction
- `amplitude_left` (complex): Left state amplitude
- `amplitude_right` (complex): Right state amplitude
- `entropy` (float): Quantum entropy at decision time
- `coherence` (float): Quantum coherence measure
- `timestamp` (float): Decision timestamp

### NetworkConfig

Network connection configuration.

**Attributes:**
- `robot_ip` (str): Robot IP address
- `robot_port` (int): Robot TCP port
- `auth_key` (str): Authentication key
- `connection_timeout` (int): Connection timeout seconds
- `max_retries` (int): Maximum connection retry attempts
- `keepalive_interval` (int): Keepalive interval seconds

### QuantumConfig

Quantum system parameters.

**Attributes:**
- `default_left_amplitude` (float): Default left turn amplitude
- `default_right_amplitude` (float): Default right turn amplitude
- `default_coherence_time` (float): Default coherence time
- `default_quantum_noise` (float): Default noise level
- `entropy_update_rate` (float): Entropy update rate
- `decoherence_model` (str): Decoherence model type

## Hardware Communication

### Arduino Communication Protocol

Commands sent to Arduino via NodeMCU serial bridge:

#### Movement Commands
- `FORWARD` - Move robot forward
- `BACKWARD` - Move robot backward
- `LEFT` - Turn robot left
- `RIGHT` - Turn robot right
- `STOP` - Stop all motors

#### Parameter Commands
- `SPEED:N` - Set motor speed (N = 1-10)
- `QUANTUM_LEFT:F` - Set left amplitude (F = 0.0-1.0)
- `QUANTUM_RIGHT:F` - Set right amplitude (F = 0.0-1.0)
- `COHERENCE_TIME:F` - Set coherence time (F seconds)
- `QUANTUM_NOISE:F` - Set noise level (F = 0.0-1.0)

#### System Commands
- `START_QUANTUM_WALK` - Begin quantum walk
- `STOP_QUANTUM_WALK` - End quantum walk
- `EMERGENCY_STOP` - Emergency stop
- `STATUS` - Request system status
- `QUANTUM_STATE` - Request quantum state info

### NodeMCU Communication Protocol

TCP communication with NodeMCU WiFi bridge:

#### Authentication
All commands must be prefixed with auth key:
pass123COMMAND_NAME

text

#### Telemetry Response Format
RSSI:-45,BAT:3.7,HEAP_FREE:25000,CPU_TEMP:28.5,UPTIME:3600

text

## Error Handling

### Exception Types

class QuantumRobotError(Exception):
"""Base exception for quantum robot errors"""
pass

class ConnectionError(QuantumRobotError):
"""Network connection errors"""
pass

class HardwareError(QuantumRobotError):
"""Hardware communication errors"""
pass

class ConfigurationError(QuantumRobotError):
"""Configuration validation errors"""
pass

text

### Error Response Handling

try:
decision = simulator.make_quantum_decision()
except QuantumRobotError as e:
print(f"Error: {e}")
# Handle error appropriately

text

## Examples

### Basic Usage

from utils.quantum_math import QuantumWalkSimulator
from utils.data_logger import QuantumDataLogger

Initialize systems
simulator = QuantumWalkSimulator()
logger = QuantumDataLogger()

Start mission
mission_id = logger.start_mission("API Example")

Configure quantum system
simulator.initialize(0.6, 0.8, 1.5, 0.05)

Make decisions and log them
for i in range(10):
decision = simulator.make_quantum_decision()

text
logger.log_quantum_event({
    'direction': decision.direction,
    'probability': decision.probability,
    'entropy': decision.entropy
})
End mission and export data
logger.end_mission(mission_id)
files = logger.export_mission_data(mission_id, 'json')
print(f"Data exported to: {files}")

text

### Advanced Configuration

from gui.config_manager import ConfigManager

config = ConfigManager()

Customize quantum parameters
config.quantum.default_coherence_time = 2.0
config.quantum.default_quantum_noise = 0.2

Create custom profile
config.create_profile(
"high_coherence",
"High coherence time configuration"
)

Validate and save
issues = config.validate_configuration()
if not issues:
config.save_configuration()
else:
print(f"Configuration issues: {issues}")

text

## Testing

### Unit Testing

import unittest
from utils.quantum_math import QuantumWalkSimulator

class TestQuantumLogic(unittest.TestCase):
def test_decision_making(self):
simulator = QuantumWalkSimulator()
decision = simulator.make_quantum_decision()

text
    self.assertIn(decision.direction, ['LEFT', 'RIGHT'])
    self.assertGreaterEqual(decision.probability, 0)
    self.assertLessEqual(decision.probability, 1)
text

### Integration Testing

def test_full_workflow():
# Test complete workflow from initialization to data export
simulator = QuantumWalkSimulator()
logger = QuantumDataLogger(":memory:") # In-memory DB for testing

text
mission_id = logger.start_mission("Integration Test")
simulator.initialize(0.707, 0.707, 1.0, 0.1)

# Make decisions
for _ in range(5):
    decision = simulator.make_quantum_decision()
    logger.log_quantum_event({
        'direction': decision.direction,
        'entropy': decision.entropy
    })

# Verify data
data = logger.get_mission_data(mission_id)
assert len(data['quantum_events']) == 5

logger.end_mission(mission_id)
text

For more examples, see the `examples/` directory in the repository.
docs/troubleshooting.md

text
# Troubleshooting Guide

This guide helps resolve common issues with the Quantum Random Walk Robot system.

## Installation Issues

### Python Environment Problems

**Error: `ModuleNotFoundError: No module named 'tkinter'`**

*Linux:*
sudo apt-get install python3-tk

or
sudo yum install tkinter

text

*macOS:*
brew install python-tk

text

*Windows:*
- Reinstall Python with "tcl/tk and IDLE" option checked

**Error: `No module named 'matplotlib'`**

Ensure virtual environment is activated
source venv/bin/activate # Linux/macOS
venv\Scripts\activate # Windows

Reinstall requirements
pip install -r requirements.txt

text

### Arduino IDE Issues

**Error: Board not found or compilation fails**

1. Install board packages:
   - Go to File → Preferences
   - Add ESP8266 board URL: `http://arduino.esp8266.com/stable/package_esp8266com_index.json`
   - Go to Tools → Board → Board Manager
   - Install "esp8266" by ESP8266 Community

2. Select correct board:
   - Arduino: "Arduino Uno"
   - NodeMCU: "NodeMCU 1.0 (ESP-12E Module)"

3. Select correct port:
   - Check Device Manager (Windows) or `/dev/ttyUSB*` (Linux)

**Error: Upload fails with "avrdude" errors**

- Check USB cable (try different cable/port)
- Install CH340 or FTDI drivers
- Close Arduino IDE serial monitor during upload
- Press reset button during upload (if needed)

## Hardware Issues

### Power System Problems

**Robot not responding or motors not moving**

1. **Check power supplies:**
   - Arduino: 7-12V (9V battery recommended)
   - Motors: 6-12V (separate 12V battery pack)
   - Ensure common ground connection

2. **Verify connections:**
Arduino Pin → L298N Pin
3 (PWM) → ENA
4 → IN1
5 → IN2
6 → IN3
7 → IN4
11 (PWM) → ENB

text

3. **Test motors individually:**
// Add to Arduino setup() for testing
digitalWrite(IN1, HIGH);
digitalWrite(IN2, LOW);
analogWrite(ENA, 200);

text

**Battery drains quickly**

- Use efficient motors (lower current draw)
- Check for short circuits
- Implement sleep modes
- Consider higher capacity batteries

### Communication Issues

**NodeMCU WiFi AP not visible**

1. **Check NodeMCU power:**
- Should have 3.3V power LED on
- Try powering from separate 5V supply

2. **Verify firmware upload:**
- Check serial output for startup messages
- Should see "AP IP: 192.168.4.1"

3. **Reset network settings:**
// Add to NodeMCU setup() temporarily
WiFi.disconnect();
WiFi.softAPdisconnect(true);
delay(1000);

text

**Arduino not receiving commands**

1. **Check serial connections:**
NodeMCU TX (GPIO1) → Arduino RX (Pin 0)
NodeMCU RX (GPIO3) → Arduino TX (Pin 1)
NodeMCU GND → Arduino GND

text

2. **Verify baud rates match:**
- Arduino: `Serial.begin(115200);`
- NodeMCU: `Serial.begin(115200);`

3. **Test serial communication:**
// Arduino loop() - add for testing
if (Serial.available()) {
String cmd = Serial.readString();
Serial.println("Received: " + cmd);
}

text

### Motor Control Issues

**Motors running at wrong speed or direction**

1. **Check motor connections:**
L298N OUT1 → Left Motor +
L298N OUT2 → Left Motor -
L298N OUT3 → Right Motor +
L298N OUT4 → Right Motor -

text

2. **Calibrate motor speeds:**
// Adjust in Arduino code
int motorSpeedLeft = 200; // Adjust for left motor
int motorSpeedRight = 205; // Adjust for right motor

text

3. **Test L298N enable pins:**
// Should be HIGH for motor operation
digitalWrite(ENA, HIGH);
digitalWrite(ENB, HIGH);

text

**One motor not working**

- Swap motor connections to isolate problem
- Check L298N channel (try different OUT pins)
- Measure voltage at motor terminals
- Test motor with external power supply

## Software Issues

### GUI Application Problems

**GUI won't start or appears blank**

1. **Virtual environment issues:**
Deactivate and reactivate
deactivate
source venv/bin/activate
pip install -r requirements.txt

text

2. **Display issues (Linux remote/SSH):**
export DISPLAY=:0

or for SSH
ssh -X username@hostname

text

3. **Theme issues:**
- Try different theme in config
- Check system display scaling
- Update graphics drivers

**Connection timeouts or failures**

1. **Network configuration:**
Check config/default_config.json
{
"network": {
"robot_ip": "192.168.4.1",
"robot_port": 80,
"connection_timeout": 10
}
}

text

2. **Firewall issues:**
- Allow Python through firewall
- Check port 80 access
- Try disabling firewall temporarily

3. **WiFi connection:**
Check if connected to robot AP
iwconfig # Linux
netsh wlan show profiles # Windows

text

### Data Logging Issues

**Database errors or corruption**

1. **Check file permissions:**
ls -la data/
chmod 664 data/*.db

text

2. **Database recovery:**
Python script to check database
import sqlite3
conn = sqlite3.connect('data/quantum_robot.db')
result = conn.execute("PRAGMA integrity_check;")
print(result.fetchall())

text

3. **Backup and recreate:**
mv data/quantum_robot.db data/quantum_robot_backup.db

Restart application to create new database
text

### Performance Issues

**Slow GUI updates or lag**

1. **Reduce update rates:**
{
"gui": {
"telemetry_update_rate": 200,
"max_log_entries": 500
}
}

text

2. **Close unused tabs/windows**

3. **Check system resources:**
top # Linux/macOS
taskmgr # Windows

text

**Memory usage growing over time**

1. **Limit data history:**
In telemetry_visualizer.py
self.telemetry_data = {
'timestamps': deque(maxlen=100), # Reduce from 500
# ... other data
}

text

2. **Restart application periodically**

3. **Check for memory leaks in custom code**

## Quantum Physics Concepts

### Understanding Quantum Behavior

**Why doesn't the robot always turn left/right equally?**

This is correct quantum behavior! In quantum mechanics:
- Probabilities don't guarantee equal outcomes in small samples
- True randomness shows "clustering" and patterns
- Large numbers of measurements approach theoretical probabilities

**Entropy values seem wrong**

Entropy calculation: S = -Σ p_i × log₂(p_i)
- Maximum entropy for 2-state system: 1.0 bit
- Equal probabilities (0.5, 0.5): entropy = 1.0
- Unequal probabilities: entropy < 1.0
- Collapsed state (1.0, 0.0): entropy = 0.0

**Coherence time doesn't seem to work**

- Coherence time affects how long superposition lasts
- In simulation, it controls decoherence rate
- Real quantum systems have very short coherence times
- Robot coherence time is artificially long for demonstration

## Advanced Diagnostics

### Network Debugging

**Monitor TCP traffic:**
Linux/macOS
sudo tcpdump -i any port 80

or use Wireshark GUI
text

**Test connectivity:**
Check if robot responds
ping 192.168.4.1
telnet 192.168.4.1 80

text

**NodeMCU serial debugging:**
// Add to NodeMCU code for debugging
Serial.println("Debug: Received command: " + command);
Serial.println("Debug: Free heap: " + String(ESP.getFreeHeap()));

text

### Hardware Debugging

**Oscilloscope measurements:**
- PWM signals on pins 3, 11 (should be 0-5V square waves)
- Motor voltage (should match battery voltage)
- Serial communication (should be 3.3V logic levels)

**Multimeter checks:**
- Arduino 5V rail: 4.8-5.2V
- NodeMCU 3.3V rail: 3.1-3.5V
- Motor supply: Battery voltage
- Ground continuity between all components

### Performance Profiling

**Python profiling:**
import cProfile
import pstats

Profile the GUI application
cProfile.run('main()', 'profile_stats')
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative').print_stats(10)

text

**Memory profiling:**
pip install memory-profiler
python -m memory_profiler src/gui/quantum_robot_gui.py

text

## Getting Further Help

### Before Asking for Help

1. **Check this troubleshooting guide**
2. **Search existing GitHub issues**
3. **Try with minimal configuration**
4. **Test individual components**
5. **Gather system information:**
python --version
pip list
uname -a # Linux/macOS

text

### How to Report Issues

When reporting problems, include:

1. **System information:**
- Operating system and version
- Python version
- Hardware setup (Arduino model, etc.)

2. **Complete error messages:**
Traceback (most recent call last):
File "...", line ..., in ...
Error: ...

text

3. **Steps to reproduce:**
- What you were trying to do
- What happened instead
- Minimal example if possible

4. **Configuration files:**
- Contents of `config/default_config.json`
- Any custom settings

5. **Log files:**
- GUI application logs
- Arduino serial output
- NodeMCU serial output

### Community Support

- **GitHub Issues:** [Repository Issues](https://github.com/yourusername/quantum-random-walk-robot/issues)
- **Discord:** [Community Server](https://discord.gg/quantumrobot)
- **Email:** support@quantumrobot.org
- **Documentation:** [Project Wiki](https://github.com/yourusername/quantum-random-walk-robot/wiki)

### Professional Support

For commercial applications or advanced customization:
- Consulting services available
- Custom hardware design
- Educational institution partnerships
- Enterprise support contracts

Contact: enterprise@quantumrobot.org

