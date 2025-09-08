#!/usr/bin/env python3
"""
Multi-Robot Quantum Entanglement Example
Demonstrates quantum entanglement between two robots.

Author: Quantum Robotics Team
License: MIT
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.quantum_math import QuantumWalkSimulator, EntangledState, QuantumWavefunction

class EntangledRobotPair:
    """Manages a pair of entangled quantum robots"""
    
    def __init__(self, robot1_name: str, robot2_name: str):
        self.robot1_name = robot1_name
        self.robot2_name = robot2_name
        
        # Create individual quantum systems
        self.wf1 = QuantumWavefunction()
        self.wf2 = QuantumWavefunction()
        
        # Create entangled state
        self.entangled_state = self.wf1.entangle_with(self.wf2)
        
        # Statistics
        self.measurements = []
        self.correlation_count = 0
        self.total_measurements = 0
        
    def measure_both_robots(self):
        """Perform entangled measurement on both robots"""
        result1, result2 = self.entangled_state.measure_both()
        
        self.measurements.append((result1, result2))
        self.total_measurements += 1
        
        # Check for anti-correlation (entangled robots should be anti-correlated)
        if result1 != result2:
            self.correlation_count += 1
            
        return result1, result2
        
    def get_correlation_coefficient(self):
        """Calculate correlation coefficient"""
        if self.total_measurements == 0:
            return 0
        return -1.0 if self.correlation_count == self.total_measurements else 0.0
        
    def get_statistics(self):
        """Get measurement statistics"""
        return {
            'total_measurements': self.total_measurements,
            'correlation_count': self.correlation_count,
            'correlation_coefficient': self.get_correlation_coefficient(),
            'measurements': self.measurements.copy()
        }

def main():
    """Multi-robot entanglement demonstration"""
    
    print("=== Multi-Robot Quantum Entanglement Demo ===")
    print("This example demonstrates quantum entanglement between two robots.")
    print("Entangled robots will show anti-correlated behavior.")
    print()
    
    # Create entangled robot pair
    print("Creating entangled robot pair...")
    robots = EntangledRobotPair("QuantumBot_A", "QuantumBot_B")
    
    print(f"Robot 1: {robots.robot1_name}")
    print(f"Robot 2: {robots.robot2_name}")
    print("Robots are now quantum entangled!")
    print()
    
    # Demonstrate entangled measurements
    print("Performing entangled measurements...")
    print("(Entangled robots should show anti-correlated results)")
    print()
    print(f"{'Measurement':<12} {'Robot A':<10} {'Robot B':<10} {'Correlated?'}")
    print("-" * 45)
    
    for i in range(15):
        result1, result2 = robots.measure_both_robots()
        correlated = "Yes" if result1 != result2 else "No"
        
        print(f"{i+1:<12} {result1:<10} {result2:<10} {correlated}")
        
        time.sleep(0.3)  # Small delay for visualization
    
    # Display statistics
    print()
    print("=== Entanglement Statistics ===")
    stats = robots.get_statistics()
    
    print(f"Total measurements: {stats['total_measurements']}")
    print(f"Anti-correlated results: {stats['correlation_count']}")
    print(f"Correlation percentage: {(stats['correlation_count']/stats['total_measurements']*100):.1f}%")
    print(f"Correlation coefficient: {stats['correlation_coefficient']:.3f}")
    
    # Perfect anti-correlation should give coefficient of -1.0
    if abs(stats['correlation_coefficient'] + 1.0) < 0.1:
        print("✓ Perfect quantum entanglement achieved!")
    else:
        print("⚠ Partial entanglement detected")
    
    print()
    print("=== Quantum Physics Explanation ===")
    print("In quantum entanglement, measuring one robot instantly determines")
    print("the state of the other robot, regardless of distance. This demo")
    print("shows anti-correlated entanglement where:")
    print("- If Robot A goes LEFT, Robot B goes RIGHT")
    print("- If Robot A goes RIGHT, Robot B goes LEFT")
    print("This demonstrates 'spooky action at a distance' in robotics!")
    
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    main()
