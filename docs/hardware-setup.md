# Hardware Setup Guide

This guide provides step-by-step instructions for assembling the Quantum Random Walk Robot hardware.

## Required Components

### Core Electronics
- **Arduino Uno** (or compatible) - Robot brain
- **NodeMCU ESP8266** - WiFi communication bridge  
- **L298N Motor Driver** - Motor control interface
- **2x DC Geared Motors** (6-12V) - Robot movement
- **Robot Chassis** - Physical platform
- **12V Battery Pack** - Power supply for motors
- **9V Battery or Power Bank** - Power for Arduino
- **Breadboard and Jumper Wires** - Connections

### Optional Sensors
- **HC-SR04 Ultrasonic Sensor** - Obstacle detection
- **MPU6050 IMU** - Orientation tracking
- **LM35 Temperature Sensor** - System monitoring
- **ACS712 Current Sensor** - Motor current monitoring
- **Voltage Divider Components** - Battery monitoring

## Assembly Instructions

### Step 1: Prepare the Chassis
1. Attach DC motors to the robot chassis
2. Mount wheels on motor shafts
3. Secure battery packs to chassis
4. Create mounting points for electronics

### Step 2: Arduino Connections
Arduino Pin → L298N Motor Driver
3 (PWM) → ENA (Left motor speed)
4 → IN1 (Left motor direction 1)
5 → IN2 (Left motor direction 2)
6 → IN3 (Right motor direction 1)
7 → IN4 (Right motor direction 2)
11 (PWM) → ENB (Right motor speed)
GND → GND
5V → VCC (Logic power)

**Motor Connections:**
L298N → Motors
OUT1 → Left Motor +
OUT2 → Left Motor -
OUT3 → Right Motor +
OUT4 → Right Motor -

**Power Connections:**
12V Battery → L298N VCC (Motor power)
Arduino → L298N GND (Common ground)

### Step 3: NodeMCU ESP8266 Connections

NodeMCU Pin → Arduino Pin
GND → GND
VU (5V) → 5V or VIN
RX (GPIO3) → TX (Pin 1)
TX (GPIO1) → RX (Pin 0)

**Battery Monitoring:**
NodeMCU A0 → Voltage Divider → 12V Battery
(10kΩ + 10kΩ resistors)

### Step 4: Optional Sensor Connections

**Ultrasonic Sensor (HC-SR04):**
Arduino Pin → HC-SR04
8 → Trig
9 → Echo
5V → VCC
GND → GND

**Temperature Sensor (LM35):**
Arduino Pin → LM35
A3 → OUT
5V → VCC
GND → GND
**Current Sensor (ACS712):**
Arduino Pin → ACS712
A2 → OUT
5V → VCC
GND → GND
Motor + → IP+ (In series with motor)
Motor - → IP-

## Wiring Diagram
                ┌─────────────┐
                │   Arduino   │
                │     Uno     │
                └─────┬───────┘
                      │ Serial
                ┌─────┴───────┐
                │   NodeMCU   │
                │   ESP8266   │
                └─────┬───────┘
                      │ WiFi
                ┌─────┴───────┐
                │   Python    │
                │     GUI     │
                └─────────────┘

Arduino ──── L298N ──── DC Motors
   │                       │
   └── Sensors         12V Battery
   │
9V Battery


## Power System

### Power Requirements
- **Arduino**: 7-12V DC (9V battery recommended)
- **NodeMCU**: 3.3V (powered via Arduino 5V → VU pin)
- **Motors**: 6-12V DC (12V battery pack)
- **L298N Logic**: 5V (from Arduino)

### Battery Life Optimization
- Use efficient motors (low current draw)
- Implement sleep modes when idle
- Monitor battery voltage and implement low-power warnings
- Consider using LiPo batteries for longer runtime

## Testing Procedures

### 1. Power System Test
Connect only power supplies

Check Arduino receives power (LED on)

Check NodeMCU receives power (LED on)

Measure voltages with multimeter
### 2. Motor Test
Upload basic motor test code

Test each motor individually

Check direction and speed control

Verify motor driver heating is normal

### 3. WiFi Communication Test
Upload NodeMCU firmware

Check WiFi AP creation (192.168.4.1)

Test TCP connection from computer

Verify command forwarding to Arduino

text

### 4. Sensor Test
Test each sensor individually

Verify analog readings make sense

Check for noise or interference

Calibrate sensors if needed

text

## Troubleshooting

### Common Issues

**Robot not moving:**
- Check battery levels
- Verify motor connections
- Test L298N enable pins
- Check PWM signals with oscilloscope

**WiFi not connecting:**
- Verify NodeMCU power (3.3V)
- Check serial connections
- Monitor serial output for errors
- Reset NodeMCU and try again

**Erratic behavior:**
- Check for loose connections
- Verify common ground between all components
- Add decoupling capacitors near ICs
- Check for electromagnetic interference

**Motor noise affecting sensors:**
- Add ferrite cores to motor wires
- Use shielded cables
- Separate power and signal grounds
- Add filtering capacitors

### Safety Considerations

⚠️ **Important Safety Notes:**
- Always disconnect power when making connections
- Check polarity before connecting batteries
- Use appropriate fuses for motor circuits
- Ensure adequate ventilation for components
- Keep conductive materials away from circuits
- Use proper gauge wire for motor currents

## Next Steps

After completing hardware assembly:
1. Upload firmware to both Arduino and NodeMCU
2. Test basic connectivity with Python GUI
3. Calibrate sensors and motors
4. Run example quantum walk programs
5. Begin experimenting with quantum parameters

For software setup, see [Software Installation Guide](installation.md).


