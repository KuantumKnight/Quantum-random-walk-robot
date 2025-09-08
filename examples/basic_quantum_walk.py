#!/usr/bin/env python3
"""
Basic Quantum Walk Example
Demonstrates simple quantum random walk robot control.

Author: Quantum Robotics Team
License: MIT
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gui.quantum_robot_gui import QuantumRobotGUI
from utils.quantum_math import QuantumWalkSimulator
from utils.data_logger import QuantumDataLogger

def main():
    """Basic quantum walk demonstration"""
    
    print("=== Basic Quantum Walk Example ===")
    print("This example demonstrates a simple quantum random walk.")
    print("The robot will make quantum-inspired movement decisions.")
    print()
    
    # Initialize components
    print("Initializing quantum simulator...")
    quantum_sim = QuantumWalkSimulator()
    
    print("Setting up data logger...")
    data_logger = QuantumDataLogger()
    
    # Start mission
    mission_id = data_logger.start_mission(
        name="Basic Quantum Walk Demo",
        description="Simple demonstration of quantum random walk behavior",
        parameters={
            "left_amplitude": 0.707,
            "right_amplitude": 0.707,
            "coherence_time": 1.0,
            "noise_level": 0.1
        }
    )
    
    print(f"Started mission: {mission_id}")
    
    # Initialize quantum system
    quantum_sim.initialize(
        left_amplitude=0.707,
        right_amplitude=0.707,
        coherence_time=1.0,
        noise_level=0.1
    )
    
    print("\nStarting quantum walk simulation...")
    print("Making 10 quantum decisions...")
    print()
    
    # Simulate quantum walk
    for i in range(10):
        # Make quantum decision
        decision = quantum_sim.make_quantum_decision()
        
        # Log the decision
        data_logger.log_quantum_event({
            'event_type': 'measurement',
            'direction': decision.direction,
            'left_amplitude': abs(decision.amplitude_left),
            'right_amplitude': abs(decision.amplitude_right),
            'left_probability': decision.amplitude_left * decision.amplitude_left.conjugate() if hasattr(decision.amplitude_left, 'conjugate') else decision.amplitude_left ** 2,
            'right_probability': decision.amplitude_right * decision.amplitude_right.conjugate() if hasattr(decision.amplitude_right, 'conjugate') else decision.amplitude_right ** 2,
            'entropy': decision.entropy,
            'coherence': decision.coherence,
            'measurement_result': decision.direction
        })
        
        # Simulate robot position (for demonstration)
        x_pos = i if decision.direction == "RIGHT" else -i
        y_pos = 0
        data_logger.log_position(x_pos, y_pos, 0, decision.direction)
        
        print(f"Step {i+1}: {decision.direction} "
              f"(P_L={decision.probability:.3f}, "
              f"Entropy={decision.entropy:.3f})")
        
        # Wait between decisions
        time.sleep(0.5)
    
    # End mission
    data_logger.end_mission(mission_id)
    
    # Generate statistics
    print("\n=== Mission Statistics ===")
    stats = data_logger.get_mission_statistics(mission_id)
    
    quantum_stats = stats.get('quantum_stats', {})
    print(f"Total decisions: {quantum_stats.get('total_decisions', 0)}")
    print(f"Left decisions: {quantum_stats.get('left_decisions', 0)}")
    print(f"Right decisions: {quantum_stats.get('right_decisions', 0)}")
    print(f"Left probability: {quantum_stats.get('left_probability', 0):.3f}")
    print(f"Right probability: {quantum_stats.get('right_probability', 0):.3f}")
    print(f"Average entropy: {quantum_stats.get('average_entropy', 0):.3f}")
    print(f"Average coherence: {quantum_stats.get('average_coherence', 0):.3f}")
    
    # Export data
    print("\nExporting mission data...")
    export_files = data_logger.export_mission_data(mission_id, 'csv', 'exports')
    print(f"Data exported to: {export_files}")
    
    print("\n=== Demo Complete ===")
    print("Check the 'exports' directory for saved data files.")

if __name__ == "__main__":
    main()
