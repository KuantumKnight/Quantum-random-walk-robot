/*
WiFi Quantum Bridge - Enhanced NodeMCU ESP8266 Firmware
Advanced WiFi bridge with quantum telemetry and multi-client support

Author: Quantum Robotics Team
License: MIT
Version: 2.0.0
*/

#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <ArduinoJson.h>
#include <EEPROM.h>

// ============================================================================
// NETWORK CONFIGURATION
// ============================================================================

// WiFi Access Point settings
const char* AP_SSID = "QuantumRobot";
const char* AP_PASSWORD = "quantum2025";
const String AUTH_KEY = "pass123";

// Network configuration
IPAddress local_IP(192, 168, 4, 1);
IPAddress gateway(192, 168, 4, 1);
IPAddress subnet(255, 255, 255, 0);

// Server instances
WiFiServer tcpServer(80);           // Main control server
ESP8266WebServer httpServer(8080);  // Web interface server

// ============================================================================
// SYSTEM VARIABLES
// ============================================================================

// Connection management
WiFiClient currentClient;
bool clientConnected = false;
unsigned long lastClientActivity = 0;
const unsigned long CLIENT_TIMEOUT = 30000; // 30 seconds

// Communication buffers
String serialBuffer = "";
String tcpBuffer = "";

// System monitoring
unsigned long startTime = 0;
unsigned long lastTelemetryTime = 0;
unsigned long lastHeartbeat = 0;
const unsigned long TELEMETRY_INTERVAL = 2000;  // 2 seconds
const unsigned long HEARTBEAT_INTERVAL = 1000;  // 1 second

// Performance metrics
unsigned long totalCommands = 0;
unsigned long totalResponses = 0;
unsigned long connectionAttempts = 0;
unsigned long dataBytesSent = 0;
unsigned long dataBytesReceived = 0;

// System health
float cpuTemperature = 0.0;
int freeHeapMemory = 0;
int wifiSignalStrength = 0;
float batteryVoltage = 0.0;

// Configuration storage
struct NetworkConfig {
  char ssid[32];
  char password[32];
  char auth_key[16];
  uint32_t checksum;
};

NetworkConfig config;

// ============================================================================
// SETUP FUNCTION
// ============================================================================

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  startTime = millis();
  
  // Initialize EEPROM
  EEPROM.begin(512);
  
  // Load configuration
  loadConfiguration();
  
  // Initialize WiFi
  initializeWiFi();
  
  // Initialize servers
  initializeServers();
  
  // Initialize web interface
  setupWebInterface();
  
  // Initialize mDNS
  if (MDNS.begin("quantumrobot")) {
    Serial.println("mDNS responder started");
    MDNS.addService("http", "tcp", 8080);
    MDNS.addService("quantum", "tcp", 80);
  }
  
  printSystemInfo();
  
  Serial.println("=== QUANTUM WIFI BRIDGE v2.0 READY ===");
  Serial.println("Listening for connections...");
}

void initializeWiFi() {
  // Configure WiFi access point
  WiFi.mode(WIFI_AP);
  WiFi.softAPConfig(local_IP, gateway, subnet);
  
  bool apStarted = WiFi.softAP(config.ssid, config.password);
  
  if (apStarted) {
    Serial.print("Access Point started: ");
    Serial.println(config.ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.softAPIP());
    Serial.print("MAC address: ");
    Serial.println(WiFi.softAPmacAddress());
  } else {
    Serial.println("Failed to start Access Point!");
  }
  
  // Configure for maximum performance
  WiFi.setOutputPower(20.5); // Maximum power
  WiFi.setPhyMode(WIFI_PHY_MODE_11N); // 802.11n mode
}

void initializeServers() {
  // Start TCP server for robot control
  tcpServer.begin();
  tcpServer.setNoDelay(true);
  
  Serial.println("TCP server started on port 80");
}

void setupWebInterface() {
  // Web interface routes
  httpServer.on("/", handleRoot);
  httpServer.on("/status", handleStatus);
  httpServer.on("/config", handleConfig);
  httpServer.on("/quantum", handleQuantumData);
  httpServer.on("/control", HTTP_POST, handleWebControl);
  httpServer.on("/telemetry", handleTelemetry);
  httpServer.onNotFound(handleNotFound);
  
  // Enable CORS
  httpServer.enableCORS(true);
  
  httpServer.begin();
  Serial.println("Web server started on port 8080");
}

// ============================================================================
// MAIN LOOP
// ============================================================================

void loop() {
  unsigned long currentTime = millis();
  
  // Handle TCP client connections
  handleTCPClients();
  
  // Process serial data from Arduino
  processSerialData();
  
  // Handle web server requests
  httpServer.handleClient();
  
  // Update system monitoring
  updateSystemMonitoring(currentTime);
  
  // Send heartbeat
  sendHeartbeat(currentTime);
  
  // Handle mDNS
  MDNS.update();
  
  // Small delay for stability
  delay(10);
}

// ============================================================================
// TCP CLIENT HANDLING
// ============================================================================

void handleTCPClients() {
  // Check for new clients
  WiFiClient newClient = tcpServer.available();
  
  if (newClient) {
    if (!clientConnected) {
      currentClient = newClient;
      clientConnected = true;
      lastClientActivity = millis();
      connectionAttempts++;
      
      Serial.println("New TCP client connected");
      Serial.print("Client IP: ");
      Serial.println(currentClient.remoteIP());
      
      sendWelcomeMessage();
    } else {
      // Already have a client, reject new connection
      newClient.println("BUSY: Another client is connected");
      newClient.stop();
    }
  }
  
  // Handle existing client
  if (clientConnected && currentClient.connected()) {
    if (currentClient.available()) {
      processTCPData();
      lastClientActivity = millis();
    }
    
    // Check for client timeout
    if (millis() - lastClientActivity > CLIENT_TIMEOUT) {
      Serial.println("Client timeout - disconnecting");
      disconnectClient();
    }
  } else if (clientConnected) {
    // Client disconnected
    Serial.println("TCP client disconnected");
    disconnectClient();
  }
}

void processTCPData() {
  while (currentClient.available()) {
    char c = currentClient.read();
    dataBytesReceived++;
    
    if (c == '\n') {
      tcpBuffer.trim();
      if (tcpBuffer.length() > 0) {
        processClientCommand(tcpBuffer);
        totalCommands++;
      }
      tcpBuffer = "";
    } else if (c != '\r') {
      tcpBuffer += c;
    }
  }
}

void processClientCommand(String command) {
  Serial.print("TCP CMD: ");
  Serial.println(command);
  
  // Validate authentication
  if (!command.startsWith(AUTH_KEY)) {
    sendToClient("ERROR: Authentication failed");
    Serial.println("Authentication failed");
    return;
  }
  
  // Extract actual command
  String cmd = command.substring(AUTH_KEY.length());
  cmd.trim();
  
  if (cmd.length() == 0) {
    sendToClient("ERROR: Empty command");
    return;
  }
  
  // Process command types
  if (cmd == "PING") {
    handlePingCommand();
  } else if (cmd == "STATUS") {
    handleStatusRequest();
  } else if (cmd == "TELEMETRY") {
    handleTelemetryRequest();
  } else if (cmd == "QUANTUM_STATE") {
    handleQuantumStateRequest();
  } else if (cmd.startsWith("CONFIG:")) {
    handleConfigCommand(cmd);
  } else if (cmd == "RESET") {
    handleResetCommand();
  } else {
    // Forward to Arduino
    forwardToArduino(cmd);
  }
}

void handlePingCommand() {
  unsigned long responseTime = millis();
  sendToClient("PONG");
  sendSystemTelemetry();
  
  Serial.print("Ping response time: ");
  Serial.print(millis() - responseTime);
  Serial.println(" ms");
}

void handleStatusRequest() {
  StaticJsonDocument<512> status;
  
  status["system"] = "Quantum WiFi Bridge";
  status["version"] = "2.0.0";
  status["uptime"] = (millis() - startTime) / 1000;
  status["heap_free"] = ESP.getFreeHeap();
  status["heap_fragmentation"] = ESP.getHeapFragmentation();
  status["cpu_freq"] = ESP.getCpuFreqMHz();
  status["flash_size"] = ESP.getFlashChipSize();
  status["wifi_clients"] = WiFi.softAPgetStationNum();
  status["total_commands"] = totalCommands;
  status["total_responses"] = totalResponses;
  status["bytes_sent"] = dataBytesSent;
  status["bytes_received"] = dataBytesReceived;
  
  String statusJson;
  serializeJson(status, statusJson);
  sendToClient("STATUS:" + statusJson);
}

void handleTelemetryRequest() {
  sendSystemTelemetry();
}

void handleQuantumStateRequest() {
  // Request quantum state from Arduino
  Serial.println("QUANTUM_STATE");
  // Response will be forwarded by processSerialData()
}

void handleConfigCommand(String cmd) {
  // Handle configuration commands
  String configData = cmd.substring(7); // Remove "CONFIG:"
  
  StaticJsonDocument<256> configDoc;
  DeserializationError error = deserializeJson(configDoc, configData);
  
  if (error) {
    sendToClient("ERROR: Invalid JSON");
    return;
  }
  
  // Update configuration
  if (configDoc.containsKey("ssid")) {
    strncpy(config.ssid, configDoc["ssid"], sizeof(config.ssid) - 1);
  }
  if (configDoc.containsKey("password")) {
    strncpy(config.password, configDoc["password"], sizeof(config.password) - 1);
  }
  if (configDoc.containsKey("auth_key")) {
    strncpy(config.auth_key, configDoc["auth_key"], sizeof(config.auth_key) - 1);
  }
  
  saveConfiguration();
  sendToClient("CONFIG_UPDATED");
}

void handleResetCommand() {
  sendToClient("RESETTING");
  delay(1000);
  ESP.restart();
}

void forwardToArduino(String command) {
  Serial.println(command);
  sendToClient("COMMAND_FORWARDED");
}

void sendToClient(String message) {
  if (clientConnected && currentClient.connected()) {
    currentClient.println(message);
    dataBytesSent += message.length() + 1;
    totalResponses++;
  }
}

void sendWelcomeMessage() {
  sendToClient("WELCOME: Quantum WiFi Bridge v2.0");
  sendToClient("READY: System operational");
  sendSystemTelemetry();
}

void disconnectClient() {
  if (currentClient) {
    currentClient.stop();
  }
  clientConnected = false;
  Serial.println("Client disconnected");
}

// ============================================================================
// SERIAL COMMUNICATION WITH ARDUINO
// ============================================================================

void processSerialData() {
  while (Serial.available()) {
    char c = Serial.read();
    
    if (c == '\n') {
      serialBuffer.trim();
      if (serialBuffer.length() > 0) {
        processArduinoMessage(serialBuffer);
      }
      serialBuffer = "";
    } else if (c != '\r') {
      serialBuffer += c;
    }
  }
}

void processArduinoMessage(String message) {
  // Forward Arduino responses to connected client
  if (clientConnected) {
    sendToClient(message);
  }
  
  // Log important messages
  if (message.startsWith("TELEMETRY:") || 
      message.startsWith("QUANTUM_INFO:") ||
      message.startsWith("ERROR:") ||
      message.startsWith("WARNING:")) {
    Serial.print("Arduino: ");
    Serial.println(message);
  }
}

// ============================================================================
// WEB INTERFACE HANDLERS
// ============================================================================

void handleRoot() {
  String html = generateWebInterface();
  httpServer.send(200, "text/html", html);
}

void handleStatus() {
  StaticJsonDocument<1024> status;
  
  // System information
  status["system"]["name"] = "Quantum WiFi Bridge";
  status["system"]["version"] = "2.0.0";
  status["system"]["uptime"] = (millis() - startTime) / 1000;
  
  // Memory information
  status["memory"]["free"] = ESP.getFreeHeap();
  status["memory"]["fragmentation"] = ESP.getHeapFragmentation();
  status["memory"]["max_block"] = ESP.getMaxFreeBlockSize();
  
  // WiFi information
  status["wifi"]["ssid"] = config.ssid;
  status["wifi"]["ip"] = WiFi.softAPIP().toString();
  status["wifi"]["mac"] = WiFi.softAPmacAddress();
  status["wifi"]["clients"] = WiFi.softAPgetStationNum();
  
  // Performance statistics
  status["performance"]["commands"] = totalCommands;
  status["performance"]["responses"] = totalResponses;
  status["performance"]["bytes_sent"] = dataBytesSent;
  status["performance"]["bytes_received"] = dataBytesReceived;
  status["performance"]["connections"] = connectionAttempts;
  
  String statusJson;
  serializeJson(status, statusJson);
  httpServer.send(200, "application/json", statusJson);
}

void handleConfig() {
  if (httpServer.method() == HTTP_POST) {
    // Update configuration
    String body = httpServer.arg("plain");
    StaticJsonDocument<256> configDoc;
    
    DeserializationError error = deserializeJson(configDoc, body);
    if (!error) {
      if (configDoc.containsKey("ssid")) {
        strncpy(config.ssid, configDoc["ssid"], sizeof(config.ssid) - 1);
      }
      if (configDoc.containsKey("password")) {
        strncpy(config.password, configDoc["password"], sizeof(config.password) - 1);
      }
      if (configDoc.containsKey("auth_key")) {
        strncpy(config.auth_key, configDoc["auth_key"], sizeof(config.auth_key) - 1);
      }
      
      saveConfiguration();
      httpServer.send(200, "application/json", "{\"status\":\"updated\"}");
    } else {
      httpServer.send(400, "application/json", "{\"error\":\"invalid_json\"}");
    }
  } else {
    // Return current configuration
    StaticJsonDocument<256> configDoc;
    configDoc["ssid"] = config.ssid;
    configDoc["auth_key"] = config.auth_key;
    // Don't send password for security
    
    String configJson;
    serializeJson(configDoc, configJson);
    httpServer.send(200, "application/json", configJson);
  }
}

void handleQuantumData() {
  // Return quantum-related telemetry
  StaticJsonDocument<512> quantum;
  
  quantum["timestamp"] = millis();
  quantum["system_entropy"] = calculateSystemEntropy();
  quantum["wifi_noise"] = getWiFiNoise();
  quantum["random_seed"] = generateTrueRandom();
  
  String quantumJson;
  serializeJson(quantum, quantumJson);
  httpServer.send(200, "application/json", quantumJson);
}

void handleWebControl() {
  String command = httpServer.arg("command");
  
  if (command.length() > 0) {
    Serial.println(command);
    httpServer.send(200, "application/json", "{\"status\":\"sent\"}");
  } else {
    httpServer.send(400, "application/json", "{\"error\":\"no_command\"}");
  }
}

void handleTelemetry() {
  String telemetry = generateTelemetryJSON();
  httpServer.send(200, "application/json", telemetry);
}

void handleNotFound() {
  httpServer.send(404, "text/plain", "404: Not Found");
}

String generateWebInterface() {
  String html = R"(
<!DOCTYPE html>
<html>
<head>
    <title>Quantum Robot Control</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: #1a1a1a; 
            color: #ffffff; 
            margin: 0; 
            padding: 20px; 
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
        }
        .header { 
            text-align: center; 
            margin-bottom: 30px; 
        }
        .control-panel {
            background: #2d2d2d;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .btn {
            background: #4CAF50;
            border: none;
            color: white;
            padding: 10px 20px;
            margin: 5px;
            border-radius: 5px;
            cursor: pointer;
        }
        .btn:hover { background: #45a049; }
        .btn-danger { background: #f44336; }
        .btn-danger:hover { background: #da190b; }
        .status {
            background: #333;
            border-radius: 5px;
            padding: 10px;
            margin: 10px 0;
            font-family: monospace;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖⚛️ Quantum Robot Control</h1>
            <p>Web interface for quantum random walk robot</p>
        </div>
        
        <div class="control-panel">
            <h3>Manual Control</h3>
            <div class="grid">
                <button class="btn" onclick="sendCommand('FORWARD')">↑ Forward</button>
                <button class="btn" onclick="sendCommand('LEFT')">← Left</button>
                <button class="btn" onclick="sendCommand('STOP')">⏹ Stop</button>
                <button class="btn" onclick="sendCommand('RIGHT')">Right →</button>
                <button class="btn" onclick="sendCommand('BACKWARD')">↓ Backward</button>
            </div>
        </div>
        
        <div class="control-panel">
            <h3>Quantum Control</h3>
            <button class="btn" onclick="sendCommand('START_QUANTUM_WALK')">🚀 Start Quantum Walk</button>
            <button class="btn" onclick="sendCommand('STOP_QUANTUM_WALK')">⏹ Stop Quantum Walk</button>
            <button class="btn btn-danger" onclick="sendCommand('EMERGENCY_STOP')">🛑 Emergency Stop</button>
        </div>
        
        <div class="control-panel">
            <h3>System Status</h3>
            <div id="status" class="status">
                Loading status...
            </div>
            <button class="btn" onclick="updateStatus()">🔄 Refresh</button>
        </div>
    </div>
    
    <script>
        function sendCommand(cmd) {
            fetch('/control', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: 'command=' + cmd
            })
            .then(response => response.json())
            .then(data => {
                console.log('Command sent:', cmd, data);
                updateStatus();
            })
            .catch(error => console.error('Error:', error));
        }
        
        function updateStatus() {
            fetch('/status')
            .then(response => response.json())
            .then(data => {
                document.getElementById('status').innerHTML = 
                    '<strong>System:</strong> ' + data.system.name + ' v' + data.system.version + '<br>' +
                    '<strong>Uptime:</strong> ' + data.system.uptime + ' seconds<br>' +
                    '<strong>Free Memory:</strong> ' + data.memory.free + ' bytes<br>' +
                    '<strong>WiFi Clients:</strong> ' + data.wifi.clients + '<br>' +
                    '<strong>Commands Processed:</strong> ' + data.performance.commands;
            })
            .catch(error => {
                document.getElementById('status').innerHTML = 'Error loading status';
                console.error('Error:', error);
            });
        }
        
        // Auto-refresh status every 5 seconds
        setInterval(updateStatus, 5000);
        
        // Initial status load
        updateStatus();
    </script>
</body>
</html>
  )";
  
  return html;
}

// ============================================================================
// SYSTEM MONITORING
// ============================================================================

void updateSystemMonitoring(unsigned long currentTime) {
  if (currentTime - lastTelemetryTime >= TELEMETRY_INTERVAL) {
    lastTelemetryTime = currentTime;
    
    // Update system metrics
    freeHeapMemory = ESP.getFreeHeap();
    cpuTemperature = readCPUTemperature();
    wifiSignalStrength = WiFi.RSSI();
    batteryVoltage = readBatteryVoltage();
    
    // Check system health
    checkSystemHealth();
  }
}

void sendHeartbeat(unsigned long currentTime) {
  if (currentTime - lastHeartbeat >= HEARTBEAT_INTERVAL) {
    lastHeartbeat = currentTime;
    
    if (clientConnected) {
      sendSystemTelemetry();
    }
  }
}

void sendSystemTelemetry() {
  String telemetry = "BRIDGE_TELEMETRY:";
  telemetry += "HEAP=" + String(ESP.getFreeHeap());
  telemetry += ",UPTIME=" + String((millis() - startTime) / 1000);
  telemetry += ",CLIENTS=" + String(WiFi.softAPgetStationNum());
  telemetry += ",RSSI=" + String(WiFi.RSSI());
  telemetry += ",CPU_FREQ=" + String(ESP.getCpuFreqMHz());
  telemetry += ",FLASH_SIZE=" + String(ESP.getFlashChipSize());
  telemetry += ",COMMANDS=" + String(totalCommands);
  
  sendToClient(telemetry);
}

String generateTelemetryJSON() {
  StaticJsonDocument<512> telemetry;
  
  telemetry["timestamp"] = millis();
  telemetry["uptime"] = (millis() - startTime) / 1000;
  telemetry["heap"]["free"] = ESP.getFreeHeap();
  telemetry["heap"]["fragmentation"] = ESP.getHeapFragmentation();
  telemetry["wifi"]["clients"] = WiFi.softAPgetStationNum();
  telemetry["wifi"]["rssi"] = WiFi.RSSI();
  telemetry["performance"]["commands"] = totalCommands;
  telemetry["performance"]["responses"] = totalResponses;
  telemetry["performance"]["bytes_sent"] = dataBytesSent;
  telemetry["performance"]["bytes_received"] = dataBytesReceived;
  
  String telemetryJson;
  serializeJson(telemetry, telemetryJson);
  return telemetryJson;
}

float readCPUTemperature() {
  // ESP8266 doesn't have built-in temperature sensor
  // Estimate based on system load and heap usage
  float load = (float)(ESP.getMaxFreeBlockSize()) / ESP.getFreeHeap();
  return 25.0 + (load * 30.0); // Rough approximation
}

float readBatteryVoltage() {
  // Read battery voltage from analog pin A0
  int rawValue = analogRead(A0);
  float voltage = (rawValue / 1023.0) * 3.3 * 2.0; // Voltage divider
  return voltage;
}

float calculateSystemEntropy() {
  // Calculate system entropy based on various noise sources
  float entropy = 0.0;
  
  // WiFi noise entropy
  entropy += abs(WiFi.RSSI()) / 100.0;
  
  // Memory fragmentation entropy
  entropy += ESP.getHeapFragmentation() / 100.0;
  
  // Timing entropy
  entropy += (micros() % 1000) / 1000.0;
  
  return entropy;
}

float getWiFiNoise() {
  // Return WiFi signal strength as noise source
  return abs(WiFi.RSSI()) / 100.0;
}

uint32_t generateTrueRandom() {
  // Generate true random number using system entropy
  uint32_t random = 0;
  
  // Combine multiple entropy sources
  random ^= micros();
  random ^= ESP.getCycleCount();
  random ^= ESP.getFreeHeap();
  random ^= analogRead(A0) << 16;
  
  return random;
}

void checkSystemHealth() {
  // Check for system health issues
  if (ESP.getFreeHeap() < 5000) {
    Serial.println("WARNING: Low memory");
  }
  
  if (ESP.getHeapFragmentation() > 80) {
    Serial.println("WARNING: High memory fragmentation");
  }
  
  // Reset if memory critically low
  if (ESP.getFreeHeap() < 1000) {
    Serial.println("CRITICAL: Memory exhausted - restarting");
    delay(1000);
    ESP.restart();
  }
}

// ============================================================================
// CONFIGURATION MANAGEMENT
// ============================================================================

void loadConfiguration() {
  EEPROM.get(0, config);
  
  // Verify checksum
  uint32_t calculatedChecksum = calculateConfigChecksum();
  
  if (config.checksum != calculatedChecksum) {
    Serial.println("Invalid configuration - using defaults");
    setDefaultConfiguration();
    saveConfiguration();
  } else {
    Serial.println("Configuration loaded from EEPROM");
  }
}

void saveConfiguration() {
  config.checksum = calculateConfigChecksum();
  EEPROM.put(0, config);
  EEPROM.commit();
  
  Serial.println("Configuration saved to EEPROM");
}

void setDefaultConfiguration() {
  strcpy(config.ssid, AP_SSID);
  strcpy(config.password, AP_PASSWORD);
  strcpy(config.auth_key, AUTH_KEY.c_str());
}

uint32_t calculateConfigChecksum() {
  uint32_t checksum = 0;
  uint8_t* data = (uint8_t*)&config;
  
  for (size_t i = 0; i < sizeof(config) - sizeof(config.checksum); i++) {
    checksum += data[i];
  }
  
  return checksum;
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

void printSystemInfo() {
  Serial.println("\n=== SYSTEM INFORMATION ===");
  Serial.print("Chip ID: "); Serial.println(ESP.getChipId(), HEX);
  Serial.print("Flash ID: "); Serial.println(ESP.getFlashChipId(), HEX);
  Serial.print("Flash Size: "); Serial.print(ESP.getFlashChipSize()); Serial.println(" bytes");
  Serial.print("Free Heap: "); Serial.print(ESP.getFreeHeap()); Serial.println(" bytes");
  Serial.print("CPU Frequency: "); Serial.print(ESP.getCpuFreqMHz()); Serial.println(" MHz");
  Serial.print("SDK Version: "); Serial.println(ESP.getSdkVersion());
  Serial.print("Boot Version: "); Serial.println(ESP.getBootVersion());
  Serial.print("Boot Mode: "); Serial.println(ESP.getBootMode());
  Serial.println("===========================\n");
}
