"""
Quantum Data Logger
Handles data persistence, export, and mission logging for quantum robot experiments.

Author: Quantum Robotics Team
License: MIT
"""

import sqlite3
import json
import csv
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Union
import logging

class QuantumDataLogger:
    """
    Comprehensive data logging system for quantum robot experiments.
    
    Features:
    - SQLite database storage
    - JSON/CSV export capabilities
    - Mission-based data organization
    - Real-time telemetry logging
    - Quantum state tracking
    - Statistical analysis
    """
    
    def __init__(self, db_path: str = "data/quantum_robot.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        
        # Setup logging
        self.logger = logging.getLogger("QuantumDataLogger")
        
        # Initialize database
        self.init_database()
        
        # Current mission
        self.current_mission_id = None
        
    def init_database(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Missions table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS missions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            start_time TIMESTAMP NOT NULL,
            end_time TIMESTAMP,
            parameters JSON,
            status TEXT DEFAULT 'active'
        )
        """)
        
        # Telemetry table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mission_id INTEGER,
            timestamp TIMESTAMP NOT NULL,
            battery_voltage REAL,
            motor_current REAL,
            temperature REAL,
            rssi INTEGER,
            cpu_temp REAL,
            free_heap INTEGER,
            distance REAL,
            FOREIGN KEY (mission_id) REFERENCES missions (id)
        )
        """)
        
        # Quantum events table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS quantum_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mission_id INTEGER,
            timestamp TIMESTAMP NOT NULL,
            event_type TEXT NOT NULL,
            direction TEXT,
            left_amplitude REAL,
            right_amplitude REAL,
            left_probability REAL,
            right_probability REAL,
            quantum_entropy REAL,
            coherence REAL,
            measurement_result TEXT,
            FOREIGN KEY (mission_id) REFERENCES missions (id)
        )
        """)
        
        # Robot positions table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mission_id INTEGER,
            timestamp TIMESTAMP NOT NULL,
            x_position REAL NOT NULL,
            y_position REAL NOT NULL,
            heading REAL,
            movement_command TEXT,
            FOREIGN KEY (mission_id) REFERENCES missions (id)
        )
        """)
        
        # Commands table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mission_id INTEGER,
            timestamp TIMESTAMP NOT NULL,
            command_type TEXT NOT NULL,
            command_data TEXT,
            source TEXT,
            response TEXT,
            execution_time REAL,
            FOREIGN KEY (mission_id) REFERENCES missions (id)
        )
        """)
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_telemetry_mission_time ON telemetry (mission_id, timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_quantum_mission_time ON quantum_events (mission_id, timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_positions_mission_time ON positions (mission_id, timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_commands_mission_time ON commands (mission_id, timestamp)")
        
        conn.commit()
        conn.close()
        
        self.logger.info(f"Database initialized: {self.db_path}")
        
    def start_mission(self, name: str, description: str = "", parameters: Dict = None) -> int:
        """
        Start a new mission logging session.
        
        Args:
            name: Mission name
            description: Mission description
            parameters: Mission parameters dict
            
        Returns:
            Mission ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO missions (name, description, start_time, parameters, status)
        VALUES (?, ?, ?, ?, 'active')
        """, (name, description, datetime.now().isoformat(), json.dumps(parameters or {})))
        
        mission_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        self.current_mission_id = mission_id
        self.logger.info(f"Started mission '{name}' with ID {mission_id}")
        
        return mission_id
        
    def end_mission(self, mission_id: Optional[int] = None):
        """End the current or specified mission"""
        if mission_id is None:
            mission_id = self.current_mission_id
            
        if mission_id is None:
            self.logger.warning("No active mission to end")
            return
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        UPDATE missions 
        SET end_time = ?, status = 'completed'
        WHERE id = ?
        """, (datetime.now().isoformat(), mission_id))
        
        conn.commit()
        conn.close()
        
        if mission_id == self.current_mission_id:
            self.current_mission_id = None
            
        self.logger.info(f"Ended mission {mission_id}")
        
    def log_telemetry(self, telemetry_data: Dict):
        """Log telemetry data point"""
        if self.current_mission_id is None:
            self.logger.warning("No active mission - telemetry not logged")
            return
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO telemetry (
            mission_id, timestamp, battery_voltage, motor_current, 
            temperature, rssi, cpu_temp, free_heap, distance
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.current_mission_id,
            datetime.now().isoformat(),
            telemetry_data.get('battery_voltage'),
            telemetry_data.get('motor_current'), 
            telemetry_data.get('temperature'),
            telemetry_data.get('rssi'),
            telemetry_data.get('cpu_temp'),
            telemetry_data.get('free_heap'),
            telemetry_data.get('distance')
        ))
        
        conn.commit()
        conn.close()
        
    def log_quantum_event(self, quantum_decision: Dict):
        """Log quantum decision/measurement event"""
        if self.current_mission_id is None:
            return
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO quantum_events (
            mission_id, timestamp, event_type, direction,
            left_amplitude, right_amplitude, left_probability, right_probability,
            quantum_entropy, coherence, measurement_result
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.current_mission_id,
            datetime.now().isoformat(),
            quantum_decision.get('event_type', 'measurement'),
            quantum_decision.get('direction'),
            quantum_decision.get('left_amplitude'),
            quantum_decision.get('right_amplitude'),
            quantum_decision.get('left_probability'),
            quantum_decision.get('right_probability'),
            quantum_decision.get('entropy'),
            quantum_decision.get('coherence'),
            quantum_decision.get('measurement_result')
        ))
        
        conn.commit()
        conn.close()
        
    def log_position(self, x: float, y: float, heading: float = 0, command: str = ""):
        """Log robot position"""
        if self.current_mission_id is None:
            return
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO positions (mission_id, timestamp, x_position, y_position, heading, movement_command)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            self.current_mission_id,
            datetime.now().isoformat(),
            x, y, heading, command
        ))
        
        conn.commit()
        conn.close()
        
    def log_command(self, command_type: str, command_data: str = "", 
                   source: str = "gui", response: str = "", execution_time: float = 0):
        """Log command execution"""
        if self.current_mission_id is None:
            return
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO commands (
            mission_id, timestamp, command_type, command_data, 
            source, response, execution_time
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            self.current_mission_id,
            datetime.now().isoformat(),
            command_type, command_data, source, response, execution_time
        ))
        
        conn.commit()
        conn.close()
        
    def get_mission_data(self, mission_id: int) -> Dict:
        """Get all data for a specific mission"""
        conn = sqlite3.connect(self.db_path)
        
        # Get mission info
        mission_df = pd.read_sql_query(
            "SELECT * FROM missions WHERE id = ?", 
            conn, params=[mission_id]
        )
        
        if mission_df.empty:
            conn.close()
            raise ValueError(f"Mission {mission_id} not found")
            
        # Get all related data
        telemetry_df = pd.read_sql_query(
            "SELECT * FROM telemetry WHERE mission_id = ? ORDER BY timestamp", 
            conn, params=[mission_id]
        )
        
        quantum_df = pd.read_sql_query(
            "SELECT * FROM quantum_events WHERE mission_id = ? ORDER BY timestamp", 
            conn, params=[mission_id]
        )
        
        positions_df = pd.read_sql_query(
            "SELECT * FROM positions WHERE mission_id = ? ORDER BY timestamp", 
            conn, params=[mission_id]
        )
        
        commands_df = pd.read_sql_query(
            "SELECT * FROM commands WHERE mission_id = ? ORDER BY timestamp", 
            conn, params=[mission_id]
        )
        
        conn.close()
        
        return {
            'mission': mission_df.iloc[0].to_dict() if not mission_df.empty else {},
            'telemetry': telemetry_df,
            'quantum_events': quantum_df,
            'positions': positions_df,
            'commands': commands_df
        }
        
    def export_mission_data(self, mission_id: int, export_format: str = 'csv', 
                          output_dir: str = 'exports') -> List[str]:
        """
        Export mission data in specified format.
        
        Args:
            mission_id: Mission to export
            export_format: 'csv', 'json', or 'excel'
            output_dir: Output directory
            
        Returns:
            List of created file paths
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        data = self.get_mission_data(mission_id)
        mission_name = data['mission'].get('name', f'mission_{mission_id}')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        exported_files = []
        
        if export_format.lower() == 'csv':
            # Export each table as separate CSV
            for table_name, df in data.items():
                if table_name != 'mission' and not df.empty:
                    filename = f"{mission_name}_{table_name}_{timestamp}.csv"
                    filepath = output_path / filename
                    df.to_csv(filepath, index=False)
                    exported_files.append(str(filepath))
                    
        elif export_format.lower() == 'json':
            # Export as single JSON file
            export_data = {}
            for table_name, df in data.items():
                if table_name == 'mission':
                    export_data[table_name] = df
                elif not df.empty:
                    export_data[table_name] = df.to_dict('records')
                    
            filename = f"{mission_name}_complete_{timestamp}.json"
            filepath = output_path / filename
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            exported_files.append(str(filepath))
            
        elif export_format.lower() == 'excel':
            # Export as Excel with multiple sheets
            filename = f"{mission_name}_complete_{timestamp}.xlsx"
            filepath = output_path / filename
            
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                for table_name, df in data.items():
                    if table_name != 'mission' and not df.empty:
                        df.to_excel(writer, sheet_name=table_name, index=False)
                        
            exported_files.append(str(filepath))
            
        self.logger.info(f"Exported mission {mission_id} data: {exported_files}")
        return exported_files
        
    def get_mission_statistics(self, mission_id: int) -> Dict:
        """Generate comprehensive mission statistics"""
        data = self.get_mission_data(mission_id)
        
        stats = {
            'mission_info': data['mission'],
            'duration': None,
            'telemetry_stats': {},
            'quantum_stats': {},
            'movement_stats': {},
            'command_stats': {}
        }
        
        # Calculate mission duration
        mission = data['mission']
        if mission.get('start_time') and mission.get('end_time'):
            start = datetime.fromisoformat(mission['start_time'])
            end = datetime.fromisoformat(mission['end_time'])
            duration = end - start
            stats['duration'] = {
                'total_seconds': duration.total_seconds(),
                'hours': duration.total_seconds() / 3600,
                'formatted': str(duration)
            }
            
        # Telemetry statistics
        if not data['telemetry'].empty:
            telemetry_df = data['telemetry']
            stats['telemetry_stats'] = {
                'data_points': len(telemetry_df),
                'battery_voltage': {
                    'min': telemetry_df['battery_voltage'].min(),
                    'max': telemetry_df['battery_voltage'].max(),
                    'mean': telemetry_df['battery_voltage'].mean(),
                    'std': telemetry_df['battery_voltage'].std()
                } if 'battery_voltage' in telemetry_df.columns else {},
                'temperature': {
                    'min': telemetry_df['temperature'].min(),
                    'max': telemetry_df['temperature'].max(),
                    'mean': telemetry_df['temperature'].mean()
                } if 'temperature' in telemetry_df.columns else {},
                'rssi': {
                    'min': telemetry_df['rssi'].min(),
                    'max': telemetry_df['rssi'].max(),
                    'mean': telemetry_df['rssi'].mean()
                } if 'rssi' in telemetry_df.columns else {}
            }
            
        # Quantum event statistics
        if not data['quantum_events'].empty:
            quantum_df = data['quantum_events']
            total_decisions = len(quantum_df)
            left_decisions = len(quantum_df[quantum_df['direction'] == 'LEFT'])
            right_decisions = len(quantum_df[quantum_df['direction'] == 'RIGHT'])
            
            stats['quantum_stats'] = {
                'total_decisions': total_decisions,
                'left_decisions': left_decisions,
                'right_decisions': right_decisions,
                'left_probability': left_decisions / total_decisions if total_decisions > 0 else 0,
                'right_probability': right_decisions / total_decisions if total_decisions > 0 else 0,
                'average_entropy': quantum_df['quantum_entropy'].mean() if 'quantum_entropy' in quantum_df.columns else 0,
                'average_coherence': quantum_df['coherence'].mean() if 'coherence' in quantum_df.columns else 0
            }
            
        # Movement statistics
        if not data['positions'].empty:
            positions_df = data['positions']
            
            # Calculate total distance traveled
            total_distance = 0
            if len(positions_df) > 1:
                for i in range(1, len(positions_df)):
                    dx = positions_df.iloc[i]['x_position'] - positions_df.iloc[i-1]['x_position']
                    dy = positions_df.iloc[i]['y_position'] - positions_df.iloc[i-1]['y_position']
                    total_distance += (dx**2 + dy**2)**0.5
                    
            stats['movement_stats'] = {
                'total_distance': total_distance,
                'positions_recorded': len(positions_df),
                'x_range': {
                    'min': positions_df['x_position'].min(),
                    'max': positions_df['x_position'].max(),
                    'span': positions_df['x_position'].max() - positions_df['x_position'].min()
                },
                'y_range': {
                    'min': positions_df['y_position'].min(),
                    'max': positions_df['y_position'].max(),
                    'span': positions_df['y_position'].max() - positions_df['y_position'].min()
                }
            }
            
        # Command statistics
        if not data['commands'].empty:
            commands_df = data['commands']
            command_counts = commands_df['command_type'].value_counts()
            
            stats['command_stats'] = {
                'total_commands': len(commands_df),
                'command_types': command_counts.to_dict(),
                'average_execution_time': commands_df['execution_time'].mean() if 'execution_time' in commands_df.columns else 0
            }
            
        return stats
        
    def list_missions(self) -> pd.DataFrame:
        """Get list of all missions"""
        conn = sqlite3.connect(self.db_path)
        missions_df = pd.read_sql_query(
            "SELECT id, name, description, start_time, end_time, status FROM missions ORDER BY start_time DESC", 
            conn
        )
        conn.close()
        return missions_df
        
    def delete_mission(self, mission_id: int):
        """Delete mission and all associated data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete in reverse dependency order
        tables = ['commands', 'positions', 'quantum_events', 'telemetry', 'missions']
        
        for table in tables:
            if table == 'missions':
                cursor.execute(f"DELETE FROM {table} WHERE id = ?", (mission_id,))
            else:
                cursor.execute(f"DELETE FROM {table} WHERE mission_id = ?", (mission_id,))
                
        conn.commit()
        conn.close()
        
        self.logger.info(f"Deleted mission {mission_id} and all associated data")
        
    def cleanup_old_missions(self, days_old: int = 30):
        """Delete missions older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Find old missions
        cursor.execute(
            "SELECT id, name FROM missions WHERE start_time < ?", 
            (cutoff_date.isoformat(),)
        )
        old_missions = cursor.fetchall()
        
        # Delete each old mission
        for mission_id, mission_name in old_missions:
            self.delete_mission(mission_id)
            self.logger.info(f"Cleaned up old mission: {mission_name} (ID: {mission_id})")
            
        conn.close()
        return len(old_missions)
