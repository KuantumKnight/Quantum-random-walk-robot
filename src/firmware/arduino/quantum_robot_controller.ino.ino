/*
Quantum Robot Controller - Enhanced Arduino Firmware
Implements quantum-inspired decision making with comprehensive telemetry

Author: Quantum Robotics Team  
License: MIT
Version: 2.0.0
*/

#include <Arduino.h>
#include <SoftwareSerial.h>
#include <EEPROM.h>

// ============================================================================
// HARDWARE CONFIGURATION
// ============================================================================

// Motor Driver Pins (L298N)
const int MOTOR_LEFT_PWM = 3;    // ENA - PWM speed control (left motor)
const int MOTOR_RIGHT_PWM = 11;  // ENB - PWM speed control (right motor)
const int MOTOR_LEFT_DIR1 = 4;   // IN1 - Left motor direction 1
const int MOTOR_LEFT_DIR2 = 5;   // IN2 - Left motor direction 2  
const int MOTOR_RIGHT_DIR1 = 6;  // IN3 - Right motor direction 1
const int MOTOR_RIGHT_DIR2 = 7;  // IN4 - Right motor direction 2

// Sensor Pins
const int BATTERY_SENSOR_PIN = A1;     // Battery voltage divider
const int CURRENT_SENSOR_PIN = A2;     // Motor current sensor (ACS712)
const int TEMPERATURE_SENSOR_PIN = A3;  // Temperature sensor (LM35/TMP36)
const int ULTRASONIC_TRIG_PIN = 8;     // Ultrasonic trigger
const int ULTRASONIC_ECHO_PIN = 9;     // Ultrasonic echo
const int QUANTUM_ENTROPY_PIN = A0;    // Analog noise for quantum entropy

// LED Indicators
const int STATUS_LED_PIN = 13;         // Built-in LED for status
const int QUANTUM_LED_PIN = 12;        // LED indicates quantum state

// ============================================================================
// QUANTUM PARAMETERS & STATE
// ============================================================================

// Quantum Wavefunction Amplitudes (normalized)
float quantumAmplitudeLeft = 0.707;   // |ψ_L|
float quantumAmplitudeRight = 0.707;  // |ψ_R|
float quantumPhaseLeft = 0.0;         // Phase of left amplitude
float quantumPhaseRight = 0.0;        // Phase of right amplitude

// Quantum System Parameters
float coherenceTime = 1000.0;         // Quantum coherence time (ms)
float decoherenceRate = 0.001;        // Decoherence rate (1/ms)
float quantumNoise = 0.1;             // Environmental noise level
unsigned long lastQuantumUpdate = 0;  // Last quantum state update time

// Quantum State Variables
enum QuantumState {
  SUPERPOSITION,
  LEFT_COLLAPSED,
  RIGHT_COLLAPSED,
  DECOHERENT
};

QuantumState currentQuantumState = SUPERPOSITION;
unsigned long quantumStateStartTime = 0;
int totalQuantumDecisions = 0;
int leftDecisions = 0;
int rightDecisions = 0;

// ============================================================================
// ROBOT CONTROL PARAMETERS
// ============================================================================

// Motor Control
int motorSpeed = 200;                 // PWM speed value (0-255)
int motorSpeedLeft = 200;             // Individual motor speeds for calibration
int motorSpeedRight = 200;
bool motorsEnabled = true;
bool emergencyStop = false;

// Movement Parameters  
unsigned long movementInterval = 1000; // Time between quantum decisions (ms)
unsigned long lastMovementTime = 0;
String currentMovement = "STOP";
String lastMovement = "STOP";

// Manual Override System
String manualCommand = "";
unsigned long manualExpireTime = 0;
const unsigned long MANUAL_TIMEOUT = 2000; // Manual command timeout (ms)

// Safety & Monitoring
const unsigned long WATCHDOG_TIMEOUT = 5000;  // Communication watchdog (ms)
const float LOW_BATTERY_THRESHOLD = 3.2;      // Low battery cutoff (V)
const float HIGH_CURRENT_THRESHOLD = 2.0;     // High current alarm (A)
const float HIGH_TEMP_THRESHOLD = 60.0;       // High temperature alarm (°C)

unsigned long lastCommandTime = 0;
unsigned long startupTime = 0;
bool systemRunning = false;
bool quantumWalkActive = false;

// ============================================================================
// TELEMETRY & LOGGING
// ============================================================================

struct TelemetryData {
  float batteryVoltage;
  float motorCurrent;
  float temperature;
  float ultrasonicDistance;
  int freeMemory;
  unsigned long uptime;
  float quantumEntropy;
  float quantumCoherence;
  String currentState;
  String lastDecision;
};

TelemetryData telemetry;
unsigned long lastTelemetryTime = 0;
const unsigned long TELEMETRY_INTERVAL = 2000; // Send telemetry every 2s

// Statistics
unsigned long totalCommands = 0;
unsigned long totalMovements = 0;
float totalDistance = 0.0;
unsigned long missionStartTime = 0;

// ============================================================================
// SETUP FUNCTION
// ============================================================================

void setup() {
  // Initialize serial communication (high baud rate for better performance)
  Serial.begin(115200);
  
  // Initialize hardware pins
  initializeHardware();
  
  // Initialize quantum system
  initializeQuantumSystem();
  
  // Load saved parameters from EEPROM
  loadParameters();
  
  // Initialize telemetry
  initializeTelemetry();
  
  // System startup
  startupTime = millis();
  systemRunning = true;
  
  // Startup sequence
  performStartupSequence();
  
  Serial.println("=== QUANTUM ROBOT CONTROLLER v2.0 ===");
  Serial.println("Enhanced Arduino firmware ready");
  Serial.println("Quantum random walk system initialized");
  Serial.println("Waiting for commands...");
  
  sendSystemStatus();
}

void initializeHardware() {
  // Motor control pins
  pinMode(MOTOR_LEFT_PWM, OUTPUT);
  pinMode(MOTOR_RIGHT_PWM, OUTPUT);
  pinMode(MOTOR_LEFT_DIR1, OUTPUT);
  pinMode(MOTOR_LEFT_DIR2, OUTPUT);
  pinMode(MOTOR_RIGHT_DIR1, OUTPUT);
  pinMode(MOTOR_RIGHT_DIR2, OUTPUT);
  
  // Sensor pins
  pinMode(BATTERY_SENSOR_PIN, INPUT);
  pinMode(CURRENT_SENSOR_PIN, INPUT);
  pinMode(TEMPERATURE_SENSOR_PIN, INPUT);
  pinMode(QUANTUM_ENTROPY_PIN, INPUT);
  pinMode(ULTRASONIC_TRIG_PIN, OUTPUT);
  pinMode(ULTRASONIC_ECHO_PIN, INPUT);
  
  // LED indicators
  pinMode(STATUS_LED_PIN, OUTPUT);
  pinMode(QUANTUM_LED_PIN, OUTPUT);
  
  // Initialize motors to stop
  stopAllMotors();
  
  Serial.println("Hardware initialized");
}

void initializeQuantumSystem() {
  // Initialize quantum amplitudes to equal superposition
  quantumAmplitudeLeft = 0.707;   // 1/√2
  quantumAmplitudeRight = 0.707;  // 1/√2
  quantumPhaseLeft = 0.0;
  quantumPhaseRight = 0.0;
  
  // Reset quantum state
  currentQuantumState = SUPERPOSITION;
  quantumStateStartTime = millis();
  
  // Seed quantum random number generator with true entropy
  seedQuantumRandom();
  
  Serial.println("Quantum system initialized");
}

void seedQuantumRandom() {
  // Use multiple entropy sources for quantum-quality randomness
  unsigned long entropy = 0;
  
  // Sample analog noise
  for (int i = 0; i < 16; i++) {
    entropy ^= analogRead(QUANTUM_ENTROPY_PIN) << i;
    delayMicroseconds(100);
  }
  
  // Add timing entropy
  entropy ^= micros();
  entropy ^= millis();
  
  // Seed random number generator
  randomSeed(entropy & 0xFFFFFFFF);
  
  Serial.print("Quantum entropy seed: 0x");
  Serial.println(entropy, HEX);
}

void performStartupSequence() {
  Serial.println("Performing startup sequence...");
  
  // LED startup pattern
  for (int i = 0; i < 3; i++) {
    digitalWrite(STATUS_LED_PIN, HIGH);
    digitalWrite(QUANTUM_LED_PIN, HIGH);
    delay(200);
    digitalWrite(STATUS_LED_PIN, LOW);
    digitalWrite(QUANTUM_LED_PIN, LOW);
    delay(200);
  }
  
  // Motor test (brief movement)
  Serial.println("Motor test...");
  setMotorSpeeds(100, 100);
  moveForward();
  delay(200);
  stopAllMotors();
  
  Serial.println("Startup sequence complete");
}

// ============================================================================
// MAIN LOOP
// ============================================================================

void loop() {
  unsigned long currentTime = millis();
  
  // Process serial commands from NodeMCU
  processSerialCommands();
  
  // Safety systems
  checkWatchdog(currentTime);
  checkSystemSafety();
  
  // Quantum system evolution
  updateQuantumSystem(currentTime);
  
  // Robot movement control
  handleMovement(currentTime);
  
  // Telemetry and monitoring
  updateTelemetry(currentTime);
  
  // Status indicators
  updateStatusLEDs();
  
  // Small delay for stability
  delay(10);
}

// ============================================================================
// COMMAND PROCESSING
// ============================================================================

void processSerialCommands() {
  static String commandBuffer = "";
  
  while (Serial.available()) {
    char c = Serial.read();
    
    if (c == '\n') {
      commandBuffer.trim();
      if (commandBuffer.length() > 0) {
        processCommand(commandBuffer);
        totalCommands++;
        lastCommandTime = millis();
      }
      commandBuffer = "";
    } else if (c != '\r') {
      commandBuffer += c;
    }
  }
}

void processCommand(String cmd) {
  Serial.print("CMD: "); Serial.println(cmd);
  
  // ========== QUANTUM PARAMETERS ==========
  
  if (cmd.startsWith("QUANTUM_LEFT:")) {
    float amplitude = cmd.substring(13).toFloat();
    quantumAmplitudeLeft = constrain(amplitude, 0.0, 1.0);
    normalizeQuantumAmplitudes();
    Serial.print("Quantum left amplitude: "); Serial.println(quantumAmplitudeLeft, 4);
    return;
  }
  
  if (cmd.startsWith("QUANTUM_RIGHT:")) {
    float amplitude = cmd.substring(14).toFloat();
    quantumAmplitudeRight = constrain(amplitude, 0.0, 1.0);
    normalizeQuantumAmplitudes();
    Serial.print("Quantum right amplitude: "); Serial.println(quantumAmplitudeRight, 4);
    return;
  }
  
  if (cmd.startsWith("COHERENCE_TIME:")) {
    coherenceTime = constrain(cmd.substring(15).toFloat() * 1000, 100, 10000);
    decoherenceRate = 1.0 / coherenceTime;
    Serial.print("Coherence time: "); Serial.print(coherenceTime); Serial.println(" ms");
    return;
  }
  
  if (cmd.startsWith("QUANTUM_NOISE:")) {
    quantumNoise = constrain(cmd.substring(14).toFloat(), 0.0, 1.0);
    Serial.print("Quantum noise: "); Serial.println(quantumNoise, 3);
    return;
  }
  
  // ========== ROBOT PARAMETERS ==========
  
  if (cmd.startsWith("SPEED:")) {
    int speed = cmd.substring(6).toInt();
    motorSpeed = map(constrain(speed, 1, 10), 1, 10, 50, 255);
    motorSpeedLeft = motorSpeed;
    motorSpeedRight = motorSpeed;
    Serial.print("Motor speed: "); Serial.println(motorSpeed);
    return;
  }
  
  if (cmd.startsWith("INTERVAL:")) {
    float seconds = cmd.substring(9).toFloat();
    movementInterval = constrain(seconds * 1000, 100, 10000);
    Serial.print("Movement interval: "); Serial.print(movementInterval); Serial.println(" ms");
    return;
  }
  
  if (cmd.startsWith("CALIBRATE:")) {
    // Motor calibration: "CALIBRATE:LEFT:adjustment" or "CALIBRATE:RIGHT:adjustment"
    int firstColon = cmd.indexOf(':', 10);
    if (firstColon > 0) {
      String motor = cmd.substring(10, firstColon);
      int adjustment = cmd.substring(firstColon + 1).toInt();
      
      if (motor == "LEFT") {
        motorSpeedLeft = constrain(motorSpeed + adjustment, 0, 255);
        Serial.print("Left motor calibrated: "); Serial.println(motorSpeedLeft);
      } else if (motor == "RIGHT") {
        motorSpeedRight = constrain(motorSpeed + adjustment, 0, 255);
        Serial.print("Right motor calibrated: "); Serial.println(motorSpeedRight);
      }
    }
    return;
  }
  
  // ========== SYSTEM COMMANDS ==========
  
  if (cmd == "START_QUANTUM_WALK") {
    startQuantumWalk();
    return;
  }
  
  if (cmd == "STOP_QUANTUM_WALK") {
    stopQuantumWalk();
    return;
  }
  
  if (cmd == "EMERGENCY_STOP") {
    activateEmergencyStop();
    return;
  }
  
  if (cmd == "RESET_EMERGENCY") {
    resetEmergencyStop();
    return;
  }
  
  if (cmd == "SYSTEM_RESET") {
    performSystemReset();
    return;
  }
  
  // ========== MANUAL MOVEMENT COMMANDS ==========
  
  if (cmd == "FORWARD" || cmd == "BACKWARD" || cmd == "LEFT" || cmd == "RIGHT") {
    if (!emergencyStop && motorsEnabled) {
      manualCommand = cmd;
      manualExpireTime = millis() + MANUAL_TIMEOUT;
      executeMovement(cmd);
      Serial.print("Manual override: "); Serial.println(cmd);
    } else {
      Serial.println("Movement blocked - emergency stop or motors disabled");
    }
    return;
  }
  
  if (cmd == "STOP") {
    stopAllMotors();
    manualCommand = "";
    Serial.println("Manual stop");
    return;
  }
  
  // ========== INFORMATION COMMANDS ==========
  
  if (cmd == "STATUS") {
    sendDetailedStatus();
    return;
  }
  
  if (cmd == "QUANTUM_STATE") {
    sendQuantumStateInfo();
    return;
  }
  
  if (cmd == "TELEMETRY") {
    sendTelemetryData();
    return;
  }
  
  if (cmd == "STATISTICS") {
    sendStatistics();
    return;
  }
  
  if (cmd == "SAVE_PARAMS") {
    saveParameters();
    Serial.println("Parameters saved to EEPROM");
    return;
  }
  
  if (cmd == "LOAD_PARAMS") {
    loadParameters();
    Serial.println("Parameters loaded from EEPROM");
    return;
  }
  
  // Unknown command
  Serial.print("Unknown command: "); Serial.println(cmd);
}

// ============================================================================
// QUANTUM SYSTEM FUNCTIONS
// ============================================================================

void updateQuantumSystem(unsigned long currentTime) {
  if (currentTime - lastQuantumUpdate >= 50) { // Update at 20 Hz
    lastQuantumUpdate = currentTime;
    
    // Calculate time step
    float dt = 50.0; // milliseconds
    
    // Apply quantum evolution
    evolveQuantumState(dt);
    
    // Check for decoherence
    if (currentTime - quantumStateStartTime > coherenceTime) {
      if (currentQuantumState == SUPERPOSITION) {
        // Decoherence timeout - collapse randomly
        makeQuantumDecision();
      }
    }
    
    // Update quantum LED indicator
    updateQuantumLED();
  }
}

void evolveQuantumState(float dt) {
  // Apply decoherence (amplitude damping)
  float decayFactor = exp(-decoherenceRate * dt);
  
  // Add quantum noise (environmental interaction)
  if (quantumNoise > 0) {
    float noiseAmplitude = quantumNoise * sqrt(dt / 1000.0); // Scale with sqrt(time)
    
    // Generate quantum noise from analog entropy
    float noise1 = generateQuantumNoise() * noiseAmplitude;
    float noise2 = generateQuantumNoise() * noiseAmplitude;
    
    // Apply noise to amplitudes
    quantumAmplitudeLeft += noise1;
    quantumAmplitudeRight += noise2;
    
    // Apply decoherence
    quantumAmplitudeLeft *= decayFactor;
    quantumAmplitudeRight *= decayFactor;
    
    // Renormalize to maintain quantum constraint
    normalizeQuantumAmplitudes();
  }
}

float generateQuantumNoise() {
  // Generate quantum-inspired noise using analog sensor readings
  int entropy1 = analogRead(QUANTUM_ENTROPY_PIN);
  delayMicroseconds(10);
  int entropy2 = analogRead(QUANTUM_ENTROPY_PIN);
  
  // Combine entropy sources
  unsigned long combined = entropy1 ^ (entropy2 << 10) ^ micros();
  
  // Convert to normalized float (-1 to 1)
  return (float)((int)(combined % 2001) - 1000) / 1000.0;
}

void normalizeQuantumAmplitudes() {
  // Ensure |ψ_L|² + |ψ_R|² = 1 (quantum normalization condition)
  float normSquared = quantumAmplitudeLeft * quantumAmplitudeLeft + 
                     quantumAmplitudeRight * quantumAmplitudeRight;
  
  if (normSquared > 0) {
    float norm = sqrt(normSquared);
    quantumAmplitudeLeft /= norm;
    quantumAmplitudeRight /= norm;
  } else {
    // Degenerate case - reset to equal superposition
    quantumAmplitudeLeft = 0.707;
    quantumAmplitudeRight = 0.707;
  }
}

String makeQuantumDecision() {
  // Calculate measurement probabilities
  float leftProb = quantumAmplitudeLeft * quantumAmplitudeLeft;   // |ψ_L|²
  float rightProb = quantumAmplitudeRight * quantumAmplitudeRight; // |ψ_R|²
  
  // Generate quantum measurement (wavefunction collapse)
  float measurement = generateQuantumRandom();
  
  String decision;
  if (measurement < leftProb) {
    // Collapse to LEFT state
    decision = "LEFT";
    quantumAmplitudeLeft = 1.0;
    quantumAmplitudeRight = 0.0;
    currentQuantumState = LEFT_COLLAPSED;
    leftDecisions++;
  } else {
    // Collapse to RIGHT state  
    decision = "RIGHT";
    quantumAmplitudeLeft = 0.0;
    quantumAmplitudeRight = 1.0;
    currentQuantumState = RIGHT_COLLAPSED;
    rightDecisions++;
  }
  
  totalQuantumDecisions++;
  
  Serial.print("QUANTUM_DECISION: ");
  Serial.print(decision);
  Serial.print(" (P_L="); Serial.print(leftProb, 4);
  Serial.print(", P_R="); Serial.print(rightProb, 4);
  Serial.print(", measurement="); Serial.print(measurement, 4);
  Serial.println(")");
  
  // Reset to superposition for next decision cycle
  resetQuantumSuperposition();
  
  return decision;
}

float generateQuantumRandom() {
  // High-quality quantum-inspired random number generation
  unsigned long entropy = 0;
  
  // Sample multiple entropy sources
  for (int i = 0; i < 4; i++) {
    entropy ^= analogRead(QUANTUM_ENTROPY_PIN) << (i * 8);
    entropy ^= micros();
    delayMicroseconds(50);
  }
  
  // Additional mixing
  entropy ^= millis();
  entropy ^= random(0, 65535) << 16;
  
  // Convert to normalized float [0, 1)
  return (float)(entropy % 1000000) / 1000000.0;
}

void resetQuantumSuperposition() {
  // Reset to equal superposition state
  quantumAmplitudeLeft = 0.707;   // 1/√2
  quantumAmplitudeRight = 0.707;  // 1/√2
  quantumPhaseLeft = 0.0;
  quantumPhaseRight = 0.0;
  currentQuantumState = SUPERPOSITION;
  quantumStateStartTime = millis();
}

float calculateQuantumEntropy() {
  // Calculate von Neumann entropy: S = -Tr(ρ log ρ)
  float leftProb = quantumAmplitudeLeft * quantumAmplitudeLeft;
  float rightProb = quantumAmplitudeRight * quantumAmplitudeRight;
  
  float entropy = 0.0;
  if (leftProb > 0) {
    entropy -= leftProb * log(leftProb) / log(2.0); // log2
  }
  if (rightProb > 0) {
    entropy -= rightProb * log(rightProb) / log(2.0);
  }
  
  return entropy;
}

float calculateQuantumCoherence() {
  // Quantum coherence measure (off-diagonal density matrix elements)
  // For pure state: coherence = 2 * |Re(ψ_L* ψ_R)|
  float coherence = 2.0 * abs(quantumAmplitudeLeft * quantumAmplitudeRight);
  return coherence;
}

// ============================================================================
// MOVEMENT CONTROL FUNCTIONS
// ============================================================================

void handleMovement(unsigned long currentTime) {
  // Clear expired manual commands
  if (manualCommand != "" && currentTime > manualExpireTime) {
    manualCommand = "";
    Serial.println("Manual override expired");
  }
  
  // Execute quantum decisions at regular intervals
  if (quantumWalkActive && currentTime - lastMovementTime >= movementInterval) {
    lastMovementTime = currentTime;
    
    if (manualCommand != "") {
      // Manual override active
      executeMovement(manualCommand);
      Serial.print("Manual: "); Serial.println(manualCommand);
    } else {
      // Make quantum decision
      String quantumDecision = makeQuantumDecision();
      executeMovement(quantumDecision);
      totalMovements++;
    }
  }
}

void executeMovement(String direction) {
  if (emergencyStop || !motorsEnabled) {
    stopAllMotors();
    return;
  }
  
  // Check safety conditions
  if (!checkSafetyConditions()) {
    Serial.println("Movement blocked by safety system");
    stopAllMotors();
    return;
  }
  
  currentMovement = direction;
  lastMovement = direction;
  
  if (direction == "FORWARD") {
    moveForward();
  } else if (direction == "BACKWARD") {
    moveBackward();
  } else if (direction == "LEFT") {
    turnLeft();
  } else if (direction == "RIGHT") {
    turnRight();
  } else if (direction == "STOP") {
    stopAllMotors();
  }
  
  Serial.print("MOVE: "); Serial.println(direction);
}

void moveForward() {
  // Both motors forward
  digitalWrite(MOTOR_LEFT_DIR1, HIGH);
  digitalWrite(MOTOR_LEFT_DIR2, LOW);
  digitalWrite(MOTOR_RIGHT_DIR1, HIGH);
  digitalWrite(MOTOR_RIGHT_DIR2, LOW);
  
  analogWrite(MOTOR_LEFT_PWM, motorSpeedLeft);
  analogWrite(MOTOR_RIGHT_PWM, motorSpeedRight);
  
  currentMovement = "FORWARD";
}

void moveBackward() {
  // Both motors backward
  digitalWrite(MOTOR_LEFT_DIR1, LOW);
  digitalWrite(MOTOR_LEFT_DIR2, HIGH);
  digitalWrite(MOTOR_RIGHT_DIR1, LOW);
  digitalWrite(MOTOR_RIGHT_DIR2, HIGH);
  
  analogWrite(MOTOR_LEFT_PWM, motorSpeedLeft);
  analogWrite(MOTOR_RIGHT_PWM, motorSpeedRight);
  
  currentMovement = "BACKWARD";
}

void turnLeft() {
  // Left motor backward, right motor forward (rotate left)
  digitalWrite(MOTOR_LEFT_DIR1, LOW);
  digitalWrite(MOTOR_LEFT_DIR2, HIGH);
  digitalWrite(MOTOR_RIGHT_DIR1, HIGH);
  digitalWrite(MOTOR_RIGHT_DIR2, LOW);
  
  analogWrite(MOTOR_LEFT_PWM, motorSpeedLeft);
  analogWrite(MOTOR_RIGHT_PWM, motorSpeedRight);
  
  currentMovement = "LEFT";
}

void turnRight() {
  // Left motor forward, right motor backward (rotate right)
  digitalWrite(MOTOR_LEFT_DIR1, HIGH);
  digitalWrite(MOTOR_LEFT_DIR2, LOW);
  digitalWrite(MOTOR_RIGHT_DIR1, LOW);
  digitalWrite(MOTOR_RIGHT_DIR2, HIGH);
  
  analogWrite(MOTOR_LEFT_PWM, motorSpeedLeft);
  analogWrite(MOTOR_RIGHT_PWM, motorSpeedRight);
  
  currentMovement = "RIGHT";
}

void stopAllMotors() {
  // Stop both motors
  digitalWrite(MOTOR_LEFT_DIR1, LOW);
  digitalWrite(MOTOR_LEFT_DIR2, LOW);
  digitalWrite(MOTOR_RIGHT_DIR1, LOW);
  digitalWrite(MOTOR_RIGHT_DIR2, LOW);
  
  analogWrite(MOTOR_LEFT_PWM, 0);
  analogWrite(MOTOR_RIGHT_PWM, 0);
  
  currentMovement = "STOP";
}

void setMotorSpeeds(int leftSpeed, int rightSpeed) {
  motorSpeedLeft = constrain(leftSpeed, 0, 255);
  motorSpeedRight = constrain(rightSpeed, 0, 255);
}

// ============================================================================
// SAFETY SYSTEMS
// ============================================================================

void checkWatchdog(unsigned long currentTime) {
  if (lastCommandTime > 0 && currentTime - lastCommandTime > WATCHDOG_TIMEOUT) {
    if (currentMovement != "STOP") {
      Serial.println("WATCHDOG: Communication timeout - stopping");
      stopAllMotors();
      quantumWalkActive = false;
    }
  }
}

bool checkSafetyConditions() {
  // Battery voltage check
  updateSensorReadings();
  
  if (telemetry.batteryVoltage > 1.0 && telemetry.batteryVoltage < LOW_BATTERY_THRESHOLD) {
    Serial.print("SAFETY: Battery low - "); 
    Serial.print(telemetry.batteryVoltage); Serial.println("V");
    return false;
  }
  
  // Motor current check
  if (telemetry.motorCurrent > HIGH_CURRENT_THRESHOLD) {
    Serial.print("SAFETY: Current high - ");
    Serial.print(telemetry.motorCurrent); Serial.println("A");
    return false;
  }
  
  // Temperature check
  if (telemetry.temperature > HIGH_TEMP_THRESHOLD) {
    Serial.print("SAFETY: Temperature high - ");
    Serial.print(telemetry.temperature); Serial.println("°C");
    return false;
  }
  
  // Obstacle detection (if ultrasonic sensor connected)
  if (telemetry.ultrasonicDistance > 0 && telemetry.ultrasonicDistance < 10.0) {
    Serial.print("SAFETY: Obstacle detected - ");
    Serial.print(telemetry.ultrasonicDistance); Serial.println("cm");
    return false;
  }
  
  return true;
}

void checkSystemSafety() {
  static unsigned long lastSafetyCheck = 0;
  
  if (millis() - lastSafetyCheck >= 1000) { // Check every second
    lastSafetyCheck = millis();
    
    updateSensorReadings();
    
    // Critical battery level
    if (telemetry.batteryVoltage > 1.0 && telemetry.batteryVoltage < 3.0) {
      Serial.println("CRITICAL: Battery critically low - emergency stop");
      activateEmergencyStop();
    }
    
    // Memory check
    int freeMemory = getFreeMemory();
    if (freeMemory < 100) {
      Serial.print("WARNING: Low memory - "); Serial.print(freeMemory); Serial.println(" bytes");
    }
    
    // System health warnings
    if (telemetry.motorCurrent > HIGH_CURRENT_THRESHOLD * 0.8) {
      Serial.println("WARNING: Motor current approaching limit");
    }
    
    if (telemetry.temperature > HIGH_TEMP_THRESHOLD * 0.8) {
      Serial.println("WARNING: Temperature approaching limit");
    }
  }
}

void activateEmergencyStop() {
  emergencyStop = true;
  quantumWalkActive = false;
  stopAllMotors();
  
  Serial.println("=== EMERGENCY STOP ACTIVATED ===");
  
  // Emergency LED pattern
  for (int i = 0; i < 5; i++) {
    digitalWrite(STATUS_LED_PIN, HIGH);
    delay(100);
    digitalWrite(STATUS_LED_PIN, LOW);
    delay(100);
  }
}

void resetEmergencyStop() {
  emergencyStop = false;
  Serial.println("Emergency stop reset - system ready");
}

// ============================================================================
// SENSOR READING FUNCTIONS
// ============================================================================

void updateSensorReadings() {
  // Battery voltage (through voltage divider)
  int batteryRaw = analogRead(BATTERY_SENSOR_PIN);
  telemetry.batteryVoltage = (batteryRaw / 1023.0) * 5.0 * 2.0; // Assuming 2:1 divider
  
  // Motor current (ACS712 sensor)
  int currentRaw = analogRead(CURRENT_SENSOR_PIN);
  float currentVoltage = (currentRaw / 1023.0) * 5.0;
  telemetry.motorCurrent = abs(currentVoltage - 2.5) / 0.185; // ACS712-5A: 185mV/A
  
  // Temperature (LM35 sensor: 10mV/°C)
  int tempRaw = analogRead(TEMPERATURE_SENSOR_PIN);
  float tempVoltage = (tempRaw / 1023.0) * 5.0;
  telemetry.temperature = tempVoltage * 100.0; // LM35: 10mV/°C
  
  // Ultrasonic distance
  telemetry.ultrasonicDistance = readUltrasonicDistance();
  
  // System info
  telemetry.freeMemory = getFreeMemory();
  telemetry.uptime = (millis() - startupTime) / 1000;
  
  // Quantum properties
  telemetry.quantumEntropy = calculateQuantumEntropy();
  telemetry.quantumCoherence = calculateQuantumCoherence();
  telemetry.currentState = getQuantumStateName();
  telemetry.lastDecision = lastMovement;
}

float readUltrasonicDistance() {
  // Trigger ultrasonic pulse
  digitalWrite(ULTRASONIC_TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(ULTRASONIC_TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(ULTRASONIC_TRIG_PIN, LOW);
  
  // Read echo pulse duration
  unsigned long duration = pulseIn(ULTRASONIC_ECHO_PIN, HIGH, 30000); // 30ms timeout
  
  if (duration == 0) {
    return -1; // No echo received
  }
  
  // Calculate distance in cm
  float distance = duration * 0.034 / 2;
  return distance;
}

int getFreeMemory() {
  // Estimate free memory on Arduino
  extern int __heap_start, *__brkval;
  int v;
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval);
}

String getQuantumStateName() {
  switch (currentQuantumState) {
    case SUPERPOSITION: return "SUPERPOSITION";
    case LEFT_COLLAPSED: return "LEFT_COLLAPSED";
    case RIGHT_COLLAPSED: return "RIGHT_COLLAPSED";
    case DECOHERENT: return "DECOHERENT";
    default: return "UNKNOWN";
  }
}

// ============================================================================
// TELEMETRY AND REPORTING (Continued from previous)
// ============================================================================

void updateTelemetry(unsigned long currentTime) {
  if (currentTime - lastTelemetryTime >= TELEMETRY_INTERVAL) {
    lastTelemetryTime = currentTime;
    
    updateSensorReadings();
    sendTelemetryData();
  }
}

void sendTelemetryData() {
  Serial.print("TELEMETRY:");
  Serial.print("BAT="); Serial.print(telemetry.batteryVoltage, 2);
  Serial.print(",CURRENT="); Serial.print(telemetry.motorCurrent, 2);
  Serial.print(",TEMP="); Serial.print(telemetry.temperature, 1);
  Serial.print(",DIST="); Serial.print(telemetry.ultrasonicDistance, 1);
  Serial.print(",MEM="); Serial.print(telemetry.freeMemory);
  Serial.print(",UPTIME="); Serial.print(telemetry.uptime);
  Serial.print(",ENTROPY="); Serial.print(telemetry.quantumEntropy, 4);
  Serial.print(",COHERENCE="); Serial.print(telemetry.quantumCoherence, 4);
  Serial.print(",STATE="); Serial.print(telemetry.currentState);
  Serial.print(",LAST="); Serial.print(telemetry.lastDecision);
  Serial.print(",QSTATE="); Serial.print(getQuantumStateName());
  Serial.print(",SPEED="); Serial.print(motorSpeed);
  Serial.print(",EMERGENCY="); Serial.print(emergencyStop ? "1" : "0");
  Serial.println();
}

void sendDetailedStatus() {
  Serial.println("==== QUANTUM ROBOT STATUS ====");
  Serial.print("System Running: "); Serial.println(systemRunning ? "YES" : "NO");
  Serial.print("Quantum Walk Active: "); Serial.println(quantumWalkActive ? "YES" : "NO");
  Serial.print("Emergency Stop: "); Serial.println(emergencyStop ? "ACTIVE" : "INACTIVE");
  Serial.print("Current Movement: "); Serial.println(currentMovement);
  Serial.print("Motor Speed: "); Serial.println(motorSpeed);
  Serial.print("Battery Voltage: "); Serial.print(telemetry.batteryVoltage, 2); Serial.println("V");
  Serial.print("Motor Current: "); Serial.print(telemetry.motorCurrent, 2); Serial.println("A");
  Serial.print("Temperature: "); Serial.print(telemetry.temperature, 1); Serial.println("°C");
  Serial.print("Free Memory: "); Serial.print(telemetry.freeMemory); Serial.println(" bytes");
  Serial.print("Uptime: "); Serial.print(telemetry.uptime); Serial.println(" seconds");
  
  Serial.println("---- Quantum State ----");
  Serial.print("Current State: "); Serial.println(getQuantumStateName());
  Serial.print("Left Amplitude: "); Serial.println(quantumAmplitudeLeft, 6);
  Serial.print("Right Amplitude: "); Serial.println(quantumAmplitudeRight, 6);
  Serial.print("Quantum Entropy: "); Serial.println(telemetry.quantumEntropy, 6);
  Serial.print("Quantum Coherence: "); Serial.println(telemetry.quantumCoherence, 6);
  Serial.print("Coherence Time: "); Serial.print(coherenceTime); Serial.println(" ms");
  Serial.print("Quantum Noise: "); Serial.println(quantumNoise, 3);
  
  Serial.println("---- Decision Statistics ----");
  Serial.print("Total Decisions: "); Serial.println(totalQuantumDecisions);
  Serial.print("Left Decisions: "); Serial.println(leftDecisions);
  Serial.print("Right Decisions: "); Serial.println(rightDecisions);
  if (totalQuantumDecisions > 0) {
    Serial.print("Left Probability: "); Serial.println((float)leftDecisions / totalQuantumDecisions, 4);
    Serial.print("Right Probability: "); Serial.println((float)rightDecisions / totalQuantumDecisions, 4);
  }
  
  Serial.println("===============================");
}

void sendQuantumStateInfo() {
  Serial.print("QUANTUM_INFO:");
  Serial.print("STATE="); Serial.print(getQuantumStateName());
  Serial.print(",AMP_L="); Serial.print(quantumAmplitudeLeft, 6);
  Serial.print(",AMP_R="); Serial.print(quantumAmplitudeRight, 6);
  Serial.print(",PROB_L="); Serial.print(quantumAmplitudeLeft * quantumAmplitudeLeft, 6);
  Serial.print(",PROB_R="); Serial.print(quantumAmplitudeRight * quantumAmplitudeRight, 6);
  Serial.print(",ENTROPY="); Serial.print(calculateQuantumEntropy(), 6);
  Serial.print(",COHERENCE="); Serial.print(calculateQuantumCoherence(), 6);
  Serial.print(",DECISIONS="); Serial.print(totalQuantumDecisions);
  Serial.println();
}

void sendStatistics() {
  Serial.println("==== SYSTEM STATISTICS ====");
  Serial.print("Total Commands: "); Serial.println(totalCommands);
  Serial.print("Total Movements: "); Serial.println(totalMovements);
  Serial.print("Mission Runtime: "); 
  if (missionStartTime > 0) {
    Serial.print((millis() - missionStartTime) / 1000); Serial.println(" seconds");
  } else {
    Serial.println("No mission active");
  }
  Serial.print("System Uptime: "); Serial.print((millis() - startupTime) / 1000); Serial.println(" seconds");
  Serial.print("Average Decision Rate: ");
  if (telemetry.uptime > 0) {
    Serial.print((float)totalQuantumDecisions / telemetry.uptime, 2); Serial.println(" decisions/second");
  } else {
    Serial.println("N/A");
  }
  Serial.println("============================");
}

void sendSystemStatus() {
  Serial.print("SYSTEM_STATUS:");
  Serial.print("RUNNING="); Serial.print(systemRunning ? "1" : "0");
  Serial.print(",QUANTUM="); Serial.print(quantumWalkActive ? "1" : "0");
  Serial.print(",EMERGENCY="); Serial.print(emergencyStop ? "1" : "0");
  Serial.print(",MOTORS="); Serial.print(motorsEnabled ? "1" : "0");
  Serial.print(",VERSION=2.0.0");
  Serial.print(",UPTIME="); Serial.print((millis() - startupTime) / 1000);
  Serial.println();
}

// ============================================================================
// QUANTUM CONTROL FUNCTIONS
// ============================================================================

void startQuantumWalk() {
  if (emergencyStop) {
    Serial.println("Cannot start quantum walk - emergency stop active");
    return;
  }
  
  quantumWalkActive = true;
  missionStartTime = millis();
  resetQuantumSuperposition();
  
  Serial.println("Quantum random walk started");
  Serial.print("Initial quantum state: |ψ⟩ = ");
  Serial.print(quantumAmplitudeLeft, 4); Serial.print("|L⟩ + ");
  Serial.print(quantumAmplitudeRight, 4); Serial.println("|R⟩");
  
  sendSystemStatus();
}

void stopQuantumWalk() {
  quantumWalkActive = false;
  stopAllMotors();
  
  Serial.println("Quantum random walk stopped");
  
  // Print final statistics
  if (totalQuantumDecisions > 0) {
    Serial.println("Final quantum walk statistics:");
    Serial.print("Total decisions: "); Serial.println(totalQuantumDecisions);
    Serial.print("Left turns: "); Serial.print(leftDecisions);
    Serial.print(" ("); Serial.print(100.0 * leftDecisions / totalQuantumDecisions, 1); Serial.println("%)");
    Serial.print("Right turns: "); Serial.print(rightDecisions);
    Serial.print(" ("); Serial.print(100.0 * rightDecisions / totalQuantumDecisions, 1); Serial.println("%)");
  }
  
  sendSystemStatus();
}

// ============================================================================
// PARAMETER STORAGE (EEPROM)
// ============================================================================

struct StoredParameters {
  float quantumAmplitudeLeft;
  float quantumAmplitudeRight;
  float coherenceTime;
  float quantumNoise;
  int motorSpeed;
  int motorSpeedLeft;
  int motorSpeedRight;
  unsigned long movementInterval;
  uint16_t checksum;
};

void saveParameters() {
  StoredParameters params;
  params.quantumAmplitudeLeft = quantumAmplitudeLeft;
  params.quantumAmplitudeRight = quantumAmplitudeRight;
  params.coherenceTime = coherenceTime;
  params.quantumNoise = quantumNoise;
  params.motorSpeed = motorSpeed;
  params.motorSpeedLeft = motorSpeedLeft;
  params.motorSpeedRight = motorSpeedRight;
  params.movementInterval = movementInterval;
  
  // Calculate checksum
  params.checksum = calculateChecksum((uint8_t*)&params, sizeof(params) - sizeof(params.checksum));
  
  // Write to EEPROM
  EEPROM.put(0, params);
  
  Serial.println("Parameters saved to EEPROM");
}

void loadParameters() {
  StoredParameters params;
  EEPROM.get(0, params);
  
  // Verify checksum
  uint16_t calculatedChecksum = calculateChecksum((uint8_t*)&params, sizeof(params) - sizeof(params.checksum));
  
  if (calculatedChecksum == params.checksum) {
    // Valid parameters - load them
    quantumAmplitudeLeft = params.quantumAmplitudeLeft;
    quantumAmplitudeRight = params.quantumAmplitudeRight;
    coherenceTime = params.coherenceTime;
    quantumNoise = params.quantumNoise;
    motorSpeed = params.motorSpeed;
    motorSpeedLeft = params.motorSpeedLeft;
    motorSpeedRight = params.motorSpeedRight;
    movementInterval = params.movementInterval;
    
    // Recalculate derived parameters
    decoherenceRate = 1.0 / coherenceTime;
    normalizeQuantumAmplitudes();
    
    Serial.println("Parameters loaded from EEPROM");
  } else {
    Serial.println("EEPROM parameters invalid - using defaults");
  }
}

uint16_t calculateChecksum(uint8_t* data, size_t length) {
  uint16_t checksum = 0;
  for (size_t i = 0; i < length; i++) {
    checksum += data[i];
  }
  return checksum;
}

void initializeTelemetry() {
  // Initialize telemetry structure with default values
  telemetry.batteryVoltage = 0.0;
  telemetry.motorCurrent = 0.0;
  telemetry.temperature = 0.0;
  telemetry.ultrasonicDistance = 0.0;
  telemetry.freeMemory = 0;
  telemetry.uptime = 0;
  telemetry.quantumEntropy = 0.0;
  telemetry.quantumCoherence = 0.0;
  telemetry.currentState = "SUPERPOSITION";
  telemetry.lastDecision = "NONE";
}

void performSystemReset() {
  Serial.println("Performing system reset...");
  
  // Reset quantum system
  totalQuantumDecisions = 0;
  leftDecisions = 0;
  rightDecisions = 0;
  resetQuantumSuperposition();
  
  // Reset movement
  stopAllMotors();
  quantumWalkActive = false;
  currentMovement = "STOP";
  lastMovement = "STOP";
  
  // Reset statistics
  totalCommands = 0;
  totalMovements = 0;
  totalDistance = 0.0;
  missionStartTime = 0;
  
  // Reset safety
  emergencyStop = false;
  motorsEnabled = true;
  
  Serial.println("System reset complete");
  sendSystemStatus();
}

// ============================================================================
// LED STATUS INDICATORS
// ============================================================================

void updateStatusLEDs() {
  static unsigned long lastLEDUpdate = 0;
  static bool ledState = false;
  
  if (millis() - lastLEDUpdate >= 500) { // Update every 500ms
    lastLEDUpdate = millis();
    ledState = !ledState;
    
    // Status LED patterns
    if (emergencyStop) {
      // Rapid blinking for emergency
      digitalWrite(STATUS_LED_PIN, (millis() / 100) % 2);
    } else if (quantumWalkActive) {
      // Slow blinking for active quantum walk
      digitalWrite(STATUS_LED_PIN, ledState);
    } else {
      // Solid on when connected but not walking
      digitalWrite(STATUS_LED_PIN, HIGH);
    }
    
    updateQuantumLED();
  }
}

void updateQuantumLED() {
  // Quantum LED indicates quantum state
  switch (currentQuantumState) {
    case SUPERPOSITION:
      // Breathing pattern - fade in and out
      {
        float phase = (millis() % 2000) / 1000.0 * PI;
        int brightness = (int)(127 * (1 + sin(phase)));
        analogWrite(QUANTUM_LED_PIN, brightness);
      }
      break;
      
    case LEFT_COLLAPSED:
      // Brief flash for left collapse
      digitalWrite(QUANTUM_LED_PIN, HIGH);
      delay(50);
      digitalWrite(QUANTUM_LED_PIN, LOW);
      break;
      
    case RIGHT_COLLAPSED:
      // Double flash for right collapse
      digitalWrite(QUANTUM_LED_PIN, HIGH);
      delay(50);
      digitalWrite(QUANTUM_LED_PIN, LOW);
      delay(50);
      digitalWrite(QUANTUM_LED_PIN, HIGH);
      delay(50);
      digitalWrite(QUANTUM_LED_PIN, LOW);
      break;
      
    case DECOHERENT:
      // Random flickering
      digitalWrite(QUANTUM_LED_PIN, random(0, 2));
      break;
  }
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

void printWelcomeMessage() {
  Serial.println();
  Serial.println("========================================");
  Serial.println("    QUANTUM RANDOM WALK ROBOT v2.0");
  Serial.println("    Enhanced Arduino Controller");
  Serial.println("========================================");
  Serial.println();
  Serial.println("Quantum mechanics meets robotics!");
  Serial.println("This system demonstrates quantum-inspired");
  Serial.println("decision making in autonomous robots.");
  Serial.println();
  Serial.println("Commands available:");
  Serial.println("- START_QUANTUM_WALK  : Begin quantum walk");
  Serial.println("- STOP_QUANTUM_WALK   : End quantum walk");
  Serial.println("- FORWARD/BACKWARD/LEFT/RIGHT : Manual control");
  Serial.println("- EMERGENCY_STOP      : Emergency stop");
  Serial.println("- STATUS              : System status");
  Serial.println("- QUANTUM_STATE       : Quantum state info");
  Serial.println("- TELEMETRY           : Sensor readings");
  Serial.println("- SAVE_PARAMS/LOAD_PARAMS : Parameter storage");
  Serial.println();
  Serial.println("Ready for quantum exploration!");
  Serial.println("========================================");
  Serial.println();
}
