// Quantum Robot Web Interface JavaScript

class QuantumRobotInterface {
    constructor() {
        this.socket = io();
        this.telemetryData = {
            battery: [],
            entropy: [],
            timestamps: []
        };
        
        this.setupSocketHandlers();
        this.initializeCharts();
        this.setupEventListeners();
    }

    setupSocketHandlers() {
        this.socket.on('connect', () => {
            this.updateConnectionStatus(true);
            this.log('Connected to robot server');
        });

        this.socket.on('disconnect', () => {
            this.updateConnectionStatus(false);
            this.log('Disconnected from robot server');
        });

        this.socket.on('telemetry_update', (data) => {
            this.updateTelemetry(data);
        });

        this.socket.on('command_result', (data) => {
            if (data.success) {
                this.log(`Command executed: ${data.command}`);
            } else {
                this.log(`Command failed: ${data.command}`, 'error');
            }
        });

        this.socket.on('quantum_decision', (data) => {
            this.updateQuantumState(data);
            this.addDecisionToHistory(data);
        });
    }

    initializeCharts() {
        // Battery Chart
        const batteryCtx = document.getElementById('batteryChart').getContext('2d');
        this.batteryChart = new Chart(batteryCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Battery Voltage',
                    data: [],
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: false,
                        min: 3.0,
                        max: 4.5
                    }
                }
            }
        });

        // Entropy Chart
        const entropyCtx = document.getElementById('entropyChart').getContext('2d');
        this.entropyChart = new Chart(entropyCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Quantum Entropy',
                    data: [],
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.1)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1.0
                    }
                }
            }
        });
    }

    setupEventListeners() {
        // Parameter sliders
        document.getElementById('speed').addEventListener('input', (e) => {
            document.getElementById('speed-value').textContent = e.target.value;
        });

        document.getElementById('coherence').addEventListener('input', (e) => {
            document.getElementById('coherence-value').textContent = e.target.value + 's';
        });

        // Keyboard controls
        document.addEventListener('keydown', (e) => {
            switch(e.key.toLowerCase()) {
                case 'w':
                case 'arrowup':
                    this.sendCommand('FORWARD');
                    break;
                case 's':
                case 'arrowdown':
                    this.sendCommand('BACKWARD');
                    break;
                case 'a':
                case 'arrowleft':
                    this.sendCommand('LEFT');
                    break;
                case 'd':
                case 'arrowright':
                    this.sendCommand('RIGHT');
                    break;
                case ' ':
                    e.preventDefault();
                    this.sendCommand('STOP');
                    break;
            }
        });
    }

    updateConnectionStatus(connected) {
        const indicator = document.getElementById('status-indicator');
        const text = document.getElementById('status-text');
        
        if (connected) {
            indicator.className = 'indicator online';
            text.textContent = 'Connected';
        } else {
            indicator.className = 'indicator offline';
            text.textContent = 'Disconnected';
        }
    }

    sendCommand(command) {
        this.socket.emit('robot_command', { command: command });
        this.log(`Sending command: ${command}`);
    }

    updateParameters() {
        const speed = document.getElementById('speed').value;
        const coherence = document.getElementById('coherence').value;
        
        this.sendCommand(`SPEED:${speed}`);
        this.sendCommand(`COHERENCE_TIME:${coherence}`);
        
        this.log(`Updated parameters: Speed=${speed}, Coherence=${coherence}s`);
    }

    updateTelemetry(data) {
        // Update telemetry cards
        if (data.battery_voltage !== undefined) {
            document.getElementById('battery').textContent = data.battery_voltage.toFixed(2);
        }
        
        if (data.rssi !== undefined) {
            document.getElementById('rssi').textContent = data.rssi;
        }
        
        if (data.temperature !== undefined) {
            document.getElementById('temperature').textContent = data.temperature.toFixed(1);
        }
        
        if (data.quantum_entropy !== undefined) {
            document.getElementById('entropy').textContent = data.quantum_entropy.toFixed(3);
        }

        // Update charts
        this.updateCharts(data);
    }

    updateCharts(data) {
        const timestamp = new Date().toLocaleTimeString();
        
        // Battery chart
        if (data.battery_voltage !== undefined) {
            this.batteryChart.data.labels.push(timestamp);
            this.batteryChart.data.datasets[0].data.push(data.battery_voltage);
            
            // Keep only last 50 points
            if (this.batteryChart.data.labels.length > 50) {
                this.batteryChart.data.labels.shift();
                this.batteryChart.data.datasets[0].data.shift();
            }
            
            this.batteryChart.update('none');
        }

        // Entropy chart
        if (data.quantum_entropy !== undefined) {
            this.entropyChart.data.labels.push(timestamp);
            this.entropyChart.data.datasets[0].data.push(data.quantum_entropy);
            
            // Keep only last 50 points
            if (this.entropyChart.data.labels.length > 50) {
                this.entropyChart.data.labels.shift();
                this.entropyChart.data.datasets[0].data.shift();
            }
            
            this.entropyChart.update('none');
        }
    }

    updateQuantumState(data) {
        if (data.left_amplitude !== undefined) {
            const leftBar = document.getElementById('left-amplitude');
            const leftValue = document.getElementById('left-value');
            
            const leftPercent = (data.left_amplitude * 100);
            leftBar.style.width = leftPercent + '%';
            leftValue.textContent = data.left_amplitude.toFixed(3);
        }

        if (data.right_amplitude !== undefined) {
            const rightBar = document.getElementById('right-amplitude');
            const rightValue = document.getElementById('right-value');
            
            const rightPercent = (data.right_amplitude * 100);
            rightBar.style.width = rightPercent + '%';
            rightValue.textContent = data.right_amplitude.toFixed(3);
        }
    }

    addDecisionToHistory(decision) {
        const decisionsList = document.getElementById('decisions-list');
        const timestamp = new Date().toLocaleTimeString();
        
        const decisionElement = document.createElement('div');
        decisionElement.className = `decision ${decision.direction.toLowerCase()}`;
        decisionElement.innerHTML = `
            <span class="time">${timestamp}</span>
            <span class="direction">${decision.direction}</span>
            <span class="probability">${(decision.probability * 100).toFixed(1)}%</span>
        `;
        
        decisionsList.insertBefore(decisionElement, decisionsList.firstChild);
        
        // Keep only last 10 decisions
        while (decisionsList.children.length > 10) {
            decisionsList.removeChild(decisionsList.lastChild);
        }
    }

    log(message, level = 'info') {
        const logContainer = document.getElementById('log-container');
        const timestamp = new Date().toLocaleTimeString();
        
        const logElement = document.createElement('div');
        logElement.className = `log-entry ${level}`;
        logElement.innerHTML = `<span class="timestamp">[${timestamp}]</span> ${message}`;
        
        logContainer.appendChild(logElement);
        logContainer.scrollTop = logContainer.scrollHeight;
        
        // Keep only last 100 log entries
        while (logContainer.children.length > 100) {
            logContainer.removeChild(logContainer.firstChild);
        }
    }

    clearLog() {
        document.getElementById('log-container').innerHTML = '';
    }
}

// Global functions for button onclick handlers
function sendCommand(command) {
    window.robotInterface.sendCommand(command);
}

function updateParameters() {
    window.robotInterface.updateParameters();
}

function clearLog() {
    window.robotInterface.clearLog();
}

// Initialize interface when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.robotInterface = new QuantumRobotInterface();
});
