"""
Web interface for Quantum Random Walk Robot
Provides browser-based control and monitoring
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import threading
import time
import json
from pathlib import Path

class WebInterface:
    """Web-based interface for robot control"""
    
    def __init__(self, robot_controller=None, port=8080):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'quantum_robot_secret_key_2025'
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        
        self.robot_controller = robot_controller
        self.port = port
        
        self.setup_routes()
        self.setup_socketio_events()
        
    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            return render_template('index.html')
            
        @self.app.route('/api/status')
        def get_status():
            if self.robot_controller:
                return jsonify({
                    'connected': self.robot_controller.is_connected(),
                    'quantum_walk_active': getattr(self.robot_controller, 'quantum_walk_active', False),
                    'timestamp': time.time()
                })
            else:
                return jsonify({'connected': False, 'timestamp': time.time()})
                
        @self.app.route('/api/command', methods=['POST'])
        def send_command():
            command = request.json.get('command')
            if self.robot_controller and command:
                success = self.robot_controller.send_command(command)
                return jsonify({'success': success})
            return jsonify({'success': False, 'error': 'No robot controller'})
            
        @self.app.route('/api/telemetry')
        def get_telemetry():
            if self.robot_controller:
                return jsonify(self.robot_controller.get_latest_telemetry())
            return jsonify({})
            
        @self.app.route('/static/<path:filename>')
        def serve_static(filename):
            return send_from_directory('web/static', filename)
            
    def setup_socketio_events(self):
        """Setup SocketIO events for real-time communication"""
        
        @self.socketio.on('connect')
        def handle_connect():
            print('Web client connected')
            emit('status', {'connected': True})
            
        @self.socketio.on('disconnect')
        def handle_disconnect():
            print('Web client disconnected')
            
        @self.socketio.on('robot_command')
        def handle_robot_command(data):
            command = data.get('command')
            if self.robot_controller and command:
                success = self.robot_controller.send_command(command)
                emit('command_result', {'command': command, 'success': success})
                
        @self.socketio.on('request_telemetry')
        def handle_telemetry_request():
            if self.robot_controller:
                telemetry = self.robot_controller.get_latest_telemetry()
                emit('telemetry_data', telemetry)
                
    def start_telemetry_broadcast(self):
        """Start broadcasting telemetry to connected clients"""
        def broadcast_loop():
            while True:
                if self.robot_controller:
                    telemetry = self.robot_controller.get_latest_telemetry()
                    self.socketio.emit('telemetry_update', telemetry)
                time.sleep(1)  # Broadcast every second
                
        thread = threading.Thread(target=broadcast_loop, daemon=True)
        thread.start()
        
    def run(self, debug=False):
        """Run the web interface"""
        self.start_telemetry_broadcast()
        self.socketio.run(self.app, host='0.0.0.0', port=self.port, debug=debug)
