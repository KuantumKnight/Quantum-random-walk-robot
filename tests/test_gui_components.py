"""
Unit tests for GUI components
"""

import unittest
import tkinter as tk
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gui.config_manager import ConfigManager, NetworkConfig, QuantumConfig
from gui.telemetry_visualizer import TelemetryVisualizer
from utils.data_logger import QuantumDataLogger

class TestConfigManager(unittest.TestCase):
    """Test configuration management"""
    
    def setUp(self):
        """Setup test fixtures"""
        self.config_manager = ConfigManager("test_config")
        
    def test_default_configuration(self):
        """Test default configuration values"""
        self.assertEqual(self.config_manager.network.robot_ip, "192.168.4.1")
        self.assertEqual(self.config_manager.network.robot_port, 80)
        self.assertEqual(self.config_manager.quantum.default_left_amplitude, 0.707)
        self.assertEqual(self.config_manager.quantum.default_right_amplitude, 0.707)
        
    def test_configuration_validation(self):
        """Test configuration validation"""
        # Valid configuration should pass
        issues = self.config_manager.validate_configuration()
        self.assertEqual(len(issues), 0)
        
        # Invalid port should fail
        self.config_manager.network.robot_port = 70000
        issues = self.config_manager.validate_configuration()
        self.assertGreater(len(issues), 0)
        
    def test_profile_management(self):
        """Test profile creation and loading"""
        # Create test profile
        success = self.config_manager.create_profile("test_profile", "Test profile")
        self.assertTrue(success)
        
        # List profiles should include new profile
        profiles = self.config_manager.list_profiles()
        profile_names = [p['name'] for p in profiles]
        self.assertIn("test_profile", profile_names)
        
        # Load profile
        success = self.config_manager.load_profile("test_profile")
        self.assertTrue(success)
        self.assertEqual(self.config_manager.current_profile, "test_profile")

class TestTelemetryVisualizer(unittest.TestCase):
    """Test telemetry visualization"""
    
    def setUp(self):
        """Setup test fixtures"""
        self.root = tk.Tk()
        self.visualizer = TelemetryVisualizer()
        
    def tearDown(self):
        """Cleanup"""
        self.root.destroy()
        
    def test_telemetry_update(self):
        """Test telemetry data update"""
        test_data = {
            'battery_voltage': 3.7,
            'motor_current': 0.5,
            'temperature': 25.0,
            'rssi': -45
        }
        
        # Update telemetry
        self.visualizer.update_telemetry(test_data)
        
        # Check data storage
        self.assertEqual(len(self.visualizer.telemetry_data['battery_voltage']), 1)
        self.assertEqual(self.visualizer.telemetry_data['battery_voltage'][0], 3.7)
        
    def test_warning_detection(self):
        """Test warning threshold detection"""
        # Mock callback
        warning_callback = Mock()
        self.visualizer.add_warning_callback(warning_callback)
        
        # Send low battery data
        low_battery_data = {
            'battery_voltage': 3.0,  # Below threshold
            'motor_current': 0.5,
            'temperature': 25.0,
            'rssi': -45
        }
        
        self.visualizer.update_telemetry(low_battery_data)
        
        # Should trigger warning callback
        warning_callback.assert_called()

class TestDataLogger(unittest.TestCase):
    """Test data logging functionality"""
    
    def setUp(self):
        """Setup test fixtures"""
        self.logger = QuantumDataLogger("test_data/test_robot.db")
        
    def test_mission_management(self):
        """Test mission creation and management"""
        # Start mission
        mission_id = self.logger.start_mission(
            "Test Mission",
            "Test mission description",
            {"test_param": "test_value"}
        )
        
        self.assertIsInstance(mission_id, int)
        self.assertEqual(self.logger.current_mission_id, mission_id)
        
        # End mission
        self.logger.end_mission(mission_id)
        self.assertIsNone(self.logger.current_mission_id)
        
    def test_data_logging(self):
        """Test data logging functionality"""
        # Start mission
        mission_id = self.logger.start_mission("Test Mission")
        
        # Log telemetry
        telemetry_data = {
            'battery_voltage': 3.7,
            'motor_current': 0.5,
            'temperature': 25.0,
            'rssi': -45
        }
        self.logger.log_telemetry(telemetry_data)
        
        # Log quantum event
        quantum_data = {
            'direction': 'LEFT',
            'left_probability': 0.6,
            'right_probability': 0.4,
            'entropy': 0.97
        }
        self.logger.log_quantum_event(quantum_data)
        
        # Log position
        self.logger.log_position(1.0, 2.0, 45.0, "LEFT")
        
        # Get mission data
        mission_data = self.logger.get_mission_data(mission_id)
        
        # Verify data was logged
        self.assertGreater(len(mission_data['telemetry']), 0)
        self.assertGreater(len(mission_data['quantum_events']), 0)
        self.assertGreater(len(mission_data['positions']), 0)

if __name__ == '__main__':
    unittest.main()
