"""
Configuration Manager
Handles application settings, user preferences, and robot profiles.

Author: Quantum Robotics Team
License: MIT
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging
from dataclasses import dataclass, asdict
from copy import deepcopy

@dataclass
class NetworkConfig:
    """Network connection configuration"""
    robot_ip: str = "192.168.4.1"
    robot_port: int = 80
    auth_key: str = "pass123"
    connection_timeout: int = 5
    max_retries: int = 3
    keepalive_interval: int = 10

@dataclass 
class QuantumConfig:
    """Quantum system parameters"""
    default_left_amplitude: float = 0.707
    default_right_amplitude: float = 0.707
    default_coherence_time: float = 1.0
    default_quantum_noise: float = 0.1
    entropy_update_rate: float = 0.1
    decoherence_model: str = "exponential"

@dataclass
class RobotConfig:
    """Robot-specific parameters"""
    default_speed: int = 5
    max_speed: int = 10
    min_speed: int = 1
    default_movement_interval: float = 1.0
    calibration_left: int = 0
    calibration_right: int = 0
    safety_distance: float = 10.0
    battery_low_threshold: float = 3.3
    current_high_threshold: float = 2.0

@dataclass
class GUIConfig:
    """GUI appearance and behavior settings"""
    theme: str = "dark"
    window_width: int = 1400
    window_height: int = 900
    auto_save_logs: bool = True
    telemetry_update_rate: int = 100
    max_log_entries: int = 1000
    enable_animations: bool = True
    language: str = "en"

@dataclass
class LoggingConfig:
    """Logging system configuration"""
    log_level: str = "INFO"
    log_to_file: bool = True
    max_log_files: int = 10
    log_file_size: int = 10485760  # 10MB
    log_format: str = "[%(asctime)s] %(levelname)s: %(message)s"
    enable_debug: bool = False

class ConfigManager:
    """
    Comprehensive configuration management system.
    
    Features:
    - Multiple configuration profiles
    - Automatic backup and restore
    - Validation and error checking
    - Environment variable override
    - Configuration migration
    """
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        # Configuration files
        self.main_config_file = self.config_dir / "config.json"
        self.profiles_dir = self.config_dir / "profiles"
        self.profiles_dir.mkdir(exist_ok=True)
        
        # Logger
        self.logger = logging.getLogger("ConfigManager")
        
        # Configuration objects
        self.network = NetworkConfig()
        self.quantum = QuantumConfig()
        self.robot = RobotConfig()
        self.gui = GUIConfig()
        self.logging_config = LoggingConfig()
        
        # Current profile
        self.current_profile = "default"
        
        # Load configuration
        self.load_configuration()
        
        # Apply environment overrides
        self.apply_environment_overrides()
        
    def load_configuration(self):
        """Load configuration from files"""
        try:
            if self.main_config_file.exists():
                with open(self.main_config_file, 'r') as f:
                    config_data = json.load(f)
                
                # Load each configuration section
                if 'network' in config_data:
                    self.network = NetworkConfig(**config_data['network'])
                    
                if 'quantum' in config_data:
                    self.quantum = QuantumConfig(**config_data['quantum'])
                    
                if 'robot' in config_data:
                    self.robot = RobotConfig(**config_data['robot'])
                    
                if 'gui' in config_data:
                    self.gui = GUIConfig(**config_data['gui'])
                    
                if 'logging' in config_data:
                    self.logging_config = LoggingConfig(**config_data['logging'])
                    
                if 'current_profile' in config_data:
                    self.current_profile = config_data['current_profile']
                
                self.logger.info(f"Configuration loaded from {self.main_config_file}")
                
            else:
                self.logger.info("No configuration file found, using defaults")
                self.save_configuration()
                
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            self.logger.info("Using default configuration")
            
    def save_configuration(self):
        """Save current configuration to file"""
        try:
            config_data = {
                'version': '2.0.0',
                'last_updated': str(Path().cwd()),
                'current_profile': self.current_profile,
                'network': asdict(self.network),
                'quantum': asdict(self.quantum),
                'robot': asdict(self.robot),
                'gui': asdict(self.gui),
                'logging': asdict(self.logging_config)
            }
            
            # Create backup if file exists
            if self.main_config_file.exists():
                backup_file = self.config_dir / f"config_backup_{int(Path().stat().st_mtime)}.json"
                import shutil
                shutil.copy2(self.main_config_file, backup_file)
                
            # Write new configuration
            with open(self.main_config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
                
            self.logger.info(f"Configuration saved to {self.main_config_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
            
    def apply_environment_overrides(self):
        """Apply environment variable overrides"""
        env_overrides = {
            'QUANTUM_ROBOT_IP': ('network', 'robot_ip'),
            'QUANTUM_ROBOT_PORT': ('network', 'robot_port'),
            'QUANTUM_AUTH_KEY': ('network', 'auth_key'),
            'QUANTUM_LOG_LEVEL': ('logging_config', 'log_level'),
            'QUANTUM_THEME': ('gui', 'theme'),
        }
        
        for env_var, (config_section, config_key) in env_overrides.items():
            env_value = os.getenv(env_var)
            if env_value:
                config_obj = getattr(self, config_section)
                if hasattr(config_obj, config_key):
                    # Type conversion
                    original_value = getattr(config_obj, config_key)
                    if isinstance(original_value, int):
                        env_value = int(env_value)
                    elif isinstance(original_value, float):
                        env_value = float(env_value)
                    elif isinstance(original_value, bool):
                        env_value = env_value.lower() in ('true', '1', 'yes', 'on')
                        
                    setattr(config_obj, config_key, env_value)
                    self.logger.info(f"Applied environment override: {env_var}={env_value}")
                    
    def create_profile(self, profile_name: str, description: str = "") -> bool:
        """Create a new configuration profile"""
        try:
            profile_file = self.profiles_dir / f"{profile_name}.json"
            
            if profile_file.exists():
                self.logger.warning(f"Profile {profile_name} already exists")
                return False
                
            profile_data = {
                'name': profile_name,
                'description': description,
                'created_at': str(Path().cwd()),
                'network': asdict(self.network),
                'quantum': asdict(self.quantum),
                'robot': asdict(self.robot),
                'gui': asdict(self.gui),
                'logging': asdict(self.logging_config)
            }
            
            with open(profile_file, 'w') as f:
                json.dump(profile_data, f, indent=2)
                
            self.logger.info(f"Created profile: {profile_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create profile {profile_name}: {e}")
            return False
            
    def load_profile(self, profile_name: str) -> bool:
        """Load a configuration profile"""
        try:
            profile_file = self.profiles_dir / f"{profile_name}.json"
            
            if not profile_file.exists():
                self.logger.error(f"Profile {profile_name} not found")
                return False
                
            with open(profile_file, 'r') as f:
                profile_data = json.load(f)
                
            # Load configuration from profile
            if 'network' in profile_data:
                self.network = NetworkConfig(**profile_data['network'])
                
            if 'quantum' in profile_data:
                self.quantum = QuantumConfig(**profile_data['quantum'])
                
            if 'robot' in profile_data:
                self.robot = RobotConfig(**profile_data['robot'])
                
            if 'gui' in profile_data:
                self.gui = GUIConfig(**profile_data['gui'])
                
            if 'logging' in profile_data:
                self.logging_config = LoggingConfig(**profile_data['logging'])
                
            self.current_profile = profile_name
            self.save_configuration()
            
            self.logger.info(f"Loaded profile: {profile_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load profile {profile_name}: {e}")
            return False
            
    def list_profiles(self) -> List[Dict[str, str]]:
        """List all available profiles"""
        profiles = []
        
        for profile_file in self.profiles_dir.glob("*.json"):
            try:
                with open(profile_file, 'r') as f:
                    profile_data = json.load(f)
                    
                profiles.append({
                    'name': profile_data.get('name', profile_file.stem),
                    'description': profile_data.get('description', ''),
                    'created_at': profile_data.get('created_at', 'Unknown')
                })
                
            except Exception as e:
                self.logger.warning(f"Failed to read profile {profile_file}: {e}")
                
        return profiles
        
    def delete_profile(self, profile_name: str) -> bool:
        """Delete a configuration profile"""
        try:
            profile_file = self.profiles_dir / f"{profile_name}.json"
            
            if not profile_file.exists():
                self.logger.error(f"Profile {profile_name} not found")
                return False
                
            profile_file.unlink()
            
            # Reset to default if current profile was deleted
            if self.current_profile == profile_name:
                self.current_profile = "default"
                self.save_configuration()
                
            self.logger.info(f"Deleted profile: {profile_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete profile {profile_name}: {e}")
            return False
            
    def reset_to_defaults(self):
        """Reset all configuration to default values"""
        self.network = NetworkConfig()
        self.quantum = QuantumConfig()
        self.robot = RobotConfig()
        self.gui = GUIConfig()
        self.logging_config = LoggingConfig()
        self.current_profile = "default"
        
        self.save_configuration()
        self.logger.info("Configuration reset to defaults")
        
    def validate_configuration(self) -> List[str]:
        """Validate current configuration and return list of issues"""
        issues = []
        
        # Validate network configuration
        if not (1 <= self.network.robot_port <= 65535):
            issues.append(f"Invalid robot port: {self.network.robot_port}")
            
        if self.network.connection_timeout < 1:
            issues.append("Connection timeout must be at least 1 second")
            
        if self.network.max_retries < 0:
            issues.append("Max retries cannot be negative")
            
        # Validate quantum configuration
        if not (0 <= self.quantum.default_left_amplitude <= 1):
            issues.append("Left amplitude must be between 0 and 1")
            
        if not (0 <= self.quantum.default_right_amplitude <= 1):
            issues.append("Right amplitude must be between 0 and 1")
            
        if self.quantum.default_coherence_time <= 0:
            issues.append("Coherence time must be positive")
            
        if not (0 <= self.quantum.default_quantum_noise <= 1):
            issues.append("Quantum noise must be between 0 and 1")
            
        # Validate robot configuration
        if not (self.robot.min_speed <= self.robot.default_speed <= self.robot.max_speed):
            issues.append("Default speed must be between min and max speed")
            
        if self.robot.default_movement_interval <= 0:
            issues.append("Movement interval must be positive")
            
        if self.robot.battery_low_threshold <= 0:
            issues.append("Battery low threshold must be positive")
            
        # Validate GUI configuration
        if self.gui.theme not in ['dark', 'light']:
            issues.append("Theme must be 'dark' or 'light'")
            
        if self.gui.telemetry_update_rate <= 0:
            issues.append("Telemetry update rate must be positive")
            
        # Validate logging configuration
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.logging_config.log_level not in valid_log_levels:
            issues.append(f"Log level must be one of: {valid_log_levels}")
            
        return issues
        
    def get_config_dict(self) -> Dict[str, Any]:
        """Get complete configuration as dictionary"""
        return {
            'network': asdict(self.network),
            'quantum': asdict(self.quantum),
            'robot': asdict(self.robot),
            'gui': asdict(self.gui),
            'logging': asdict(self.logging_config),
            'current_profile': self.current_profile
        }
        
    def update_config(self, section: str, updates: Dict[str, Any]) -> bool:
        """Update specific configuration section"""
        try:
            config_obj = getattr(self, section)
            
            for key, value in updates.items():
                if hasattr(config_obj, key):
                    setattr(config_obj, key, value)
                else:
                    self.logger.warning(f"Unknown configuration key: {section}.{key}")
                    
            self.save_configuration()
            self.logger.info(f"Updated configuration section: {section}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update configuration: {e}")
            return False
            
    def export_configuration(self, export_path: str) -> bool:
        """Export configuration to external file"""
        try:
            export_file = Path(export_path)
            config_data = self.get_config_dict()
            
            with open(export_file, 'w') as f:
                json.dump(config_data, f, indent=2)
                
            self.logger.info(f"Configuration exported to {export_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export configuration: {e}")
            return False
            
    def import_configuration(self, import_path: str) -> bool:
        """Import configuration from external file"""
        try:
            import_file = Path(import_path)
            
            if not import_file.exists():
                self.logger.error(f"Import file not found: {import_file}")
                return False
                
            with open(import_file, 'r') as f:
                config_data = json.load(f)
                
            # Validate before importing
            backup_config = deepcopy(self.get_config_dict())
            
            try:
                # Load new configuration
                if 'network' in config_data:
                    self.network = NetworkConfig(**config_data['network'])
                if 'quantum' in config_data:
                    self.quantum = QuantumConfig(**config_data['quantum'])
                if 'robot' in config_data:
                    self.robot = RobotConfig(**config_data['robot'])
                if 'gui' in config_data:
                    self.gui = GUIConfig(**config_data['gui'])
                if 'logging' in config_data:
                    self.logging_config = LoggingConfig(**config_data['logging'])
                    
                # Validate imported configuration
                issues = self.validate_configuration()
                if issues:
                    raise ValueError(f"Invalid configuration: {issues}")
                    
                self.save_configuration()
                self.logger.info(f"Configuration imported from {import_file}")
                return True
                
            except Exception as e:
                # Restore backup on error
                if 'network' in backup_config:
                    self.network = NetworkConfig(**backup_config['network'])
                if 'quantum' in backup_config:
                    self.quantum = QuantumConfig(**backup_config['quantum'])
                if 'robot' in backup_config:
                    self.robot = RobotConfig(**backup_config['robot'])
                if 'gui' in backup_config:
                    self.gui = GUIConfig(**backup_config['gui'])
                if 'logging' in backup_config:
                    self.logging_config = LoggingConfig(**backup_config['logging'])
                    
                raise e
                
        except Exception as e:
            self.logger.error(f"Failed to import configuration: {e}")
            return False
