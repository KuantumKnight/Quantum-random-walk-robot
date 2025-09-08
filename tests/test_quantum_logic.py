"""
Unit tests for quantum mathematics and logic
"""

import unittest
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.quantum_math import (
    QuantumWavefunction, QuantumWalkSimulator, 
    QuantumStateAnalyzer, EntangledState
)

class TestQuantumWavefunction(unittest.TestCase):
    """Test quantum wavefunction operations"""
    
    def setUp(self):
        """Setup test fixtures"""
        self.wf = QuantumWavefunction()
        
    def test_normalization(self):
        """Test wavefunction normalization"""
        # Test default normalization
        prob_sum = abs(self.wf.alpha)**2 + abs(self.wf.beta)**2
        self.assertAlmostEqual(prob_sum, 1.0, places=6)
        
        # Test custom amplitudes
        wf2 = QuantumWavefunction(alpha=0.6, beta=0.8)
        prob_sum = abs(wf2.alpha)**2 + abs(wf2.beta)**2
        self.assertAlmostEqual(prob_sum, 1.0, places=6)
        
    def test_probabilities(self):
        """Test probability calculations"""
        left_prob, right_prob = self.wf.get_probabilities()
        
        # Probabilities should sum to 1
        self.assertAlmostEqual(left_prob + right_prob, 1.0, places=6)
        
        # Probabilities should be non-negative
        self.assertGreaterEqual(left_prob, 0)
        self.assertGreaterEqual(right_prob, 0)
        
    def test_collapse(self):
        """Test wavefunction collapse"""
        # Test multiple collapses
        results = []
        for _ in range(100):
            wf = QuantumWavefunction()
            result = wf.collapse()
            results.append(result)
            
            # After collapse, one amplitude should be 1, other should be 0
            if result == "LEFT":
                self.assertAlmostEqual(abs(wf.alpha), 1.0, places=6)
                self.assertAlmostEqual(abs(wf.beta), 0.0, places=6)
            else:
                self.assertAlmostEqual(abs(wf.alpha), 0.0, places=6)
                self.assertAlmostEqual(abs(wf.beta), 1.0, places=6)
                
        # Should have both LEFT and RIGHT results (probabilistic)
        self.assertIn("LEFT", results)
        self.assertIn("RIGHT", results)

class TestQuantumWalkSimulator(unittest.TestCase):
    """Test quantum walk simulator"""
    
    def setUp(self):
        """Setup test fixtures"""
        self.simulator = QuantumWalkSimulator()
        
    def test_initialization(self):
        """Test simulator initialization"""
        self.simulator.initialize(
            left_amplitude=0.6,
            right_amplitude=0.8,
            coherence_time=2.0,
            noise_level=0.05
        )
        
        self.assertAlmostEqual(abs(self.simulator.wavefunction.alpha), 0.6, places=2)
        self.assertAlmostEqual(abs(self.simulator.wavefunction.beta), 0.8, places=2)
        self.assertEqual(self.simulator.coherence_time, 2.0)
        self.assertEqual(self.simulator.noise_level, 0.05)
        
    def test_quantum_decision(self):
        """Test quantum decision making"""
        # Make several decisions
        decisions = []
        for _ in range(50):
            decision = self.simulator.make_quantum_decision()
            decisions.append(decision.direction)
            
            # Validate decision structure
            self.assertIn(decision.direction, ["LEFT", "RIGHT"])
            self.assertIsInstance(decision.probability, float)
            self.assertIsInstance(decision.entropy, float)
            self.assertIsInstance(decision.coherence, float)
            
        # Should have both directions (probabilistic)
        self.assertIn("LEFT", decisions)
        self.assertIn("RIGHT", decisions)
        
    def test_entropy_calculation(self):
        """Test quantum entropy calculation"""
        entropy = self.simulator.calculate_entropy()
        
        # Entropy should be between 0 and 1 for 2-state system
        self.assertGreaterEqual(entropy, 0)
        self.assertLessEqual(entropy, 1)
        
        # Maximum entropy for equal superposition
        self.simulator.wavefunction.alpha = complex(0.707, 0)
        self.simulator.wavefunction.beta = complex(0.707, 0)
        max_entropy = self.simulator.calculate_entropy()
        self.assertAlmostEqual(max_entropy, 1.0, places=3)
        
    def test_coherence_calculation(self):
        """Test quantum coherence calculation"""
        coherence = self.simulator.calculate_coherence()
        
        # Coherence should be non-negative
        self.assertGreaterEqual(coherence, 0)
        
class TestQuantumStateAnalyzer(unittest.TestCase):
    """Test quantum state analysis tools"""
    
    def setUp(self):
        """Setup test fixtures"""
        self.analyzer = QuantumStateAnalyzer()
        
    def test_randomness_analysis(self):
        """Test randomness quality analysis"""
        # Create test sequence
        simulator = QuantumWalkSimulator()
        decisions = []
        
        for _ in range(100):
            decision = simulator.make_quantum_decision()
            decisions.append(decision)
            
        # Analyze randomness
        results = self.analyzer.analyze_randomness_quality(decisions)
        
        # Should contain analysis results
        self.assertIn('sequence_length', results)
        self.assertIn('runs_test', results)
        self.assertIn('frequency_test', results)
        self.assertEqual(results['sequence_length'], 100)

class TestEntangledState(unittest.TestCase):
    """Test quantum entanglement"""
    
    def setUp(self):
        """Setup test fixtures"""
        self.wf1 = QuantumWavefunction()
        self.wf2 = QuantumWavefunction()
        self.entangled = EntangledState(self.wf1, self.wf2)
        
    def test_entangled_measurement(self):
        """Test entangled measurements"""
        # Perform multiple measurements
        measurements = []
        for _ in range(100):
            result1, result2 = self.entangled.measure_both()
            measurements.append((result1, result2))
            
        # Check for anti-correlation
        anti_correlated = sum(1 for r1, r2 in measurements if r1 != r2)
        correlation_ratio = anti_correlated / len(measurements)
        
        # Should be perfectly anti-correlated
        self.assertGreater(correlation_ratio, 0.8)  # Allow some statistical variation

if __name__ == '__main__':
    unittest.main()
