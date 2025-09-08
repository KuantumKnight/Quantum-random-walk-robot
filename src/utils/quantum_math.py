"""
Quantum Mathematics and Simulation Module
Implements quantum mechanics concepts for robot control algorithms.

Author: Quantum Robotics Team
License: MIT
"""

import numpy as np
import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import math
import cmath

class QuantumState(Enum):
    """Quantum state enumeration"""
    SUPERPOSITION = "superposition"
    LEFT_COLLAPSED = "left_collapsed"
    RIGHT_COLLAPSED = "right_collapsed"
    ENTANGLED = "entangled"

@dataclass
class QuantumDecision:
    """Data structure for quantum decision results"""
    direction: str
    probability: float
    amplitude_left: complex
    amplitude_right: complex
    entropy: float
    coherence: float
    timestamp: float

class QuantumWavefunction:
    """
    Represents a quantum wavefunction for robot decision making.
    
    The wavefunction is represented as |ψ⟩ = α|L⟩ + β|R⟩ where:
    - α is the amplitude for left turn
    - β is the amplitude for right turn
    - |α|² + |β|² = 1 (normalization condition)
    """
    
    def __init__(self, alpha: complex = 0.707+0j, beta: complex = 0.707+0j):
        """
        Initialize quantum wavefunction.
        
        Args:
            alpha: Complex amplitude for left state
            beta: Complex amplitude for right state
        """
        self.alpha = alpha
        self.beta = beta
        self.normalize()
        
    def normalize(self):
        """Ensure wavefunction normalization |α|² + |β|² = 1"""
        norm = math.sqrt(abs(self.alpha)**2 + abs(self.beta)**2)
        if norm > 0:
            self.alpha /= norm
            self.beta /= norm
            
    def get_probabilities(self) -> Tuple[float, float]:
        """
        Calculate measurement probabilities.
        
        Returns:
            Tuple of (left_probability, right_probability)
        """
        left_prob = abs(self.alpha)**2
        right_prob = abs(self.beta)**2
        return left_prob, right_prob
        
    def collapse(self) -> str:
        """
        Simulate wavefunction collapse (measurement).
        
        Returns:
            'LEFT' or 'RIGHT' based on quantum probabilities
        """
        left_prob, right_prob = self.get_probabilities()
        
        # Generate quantum-inspired random number
        random_val = self._quantum_random()
        
        if random_val < left_prob:
            # Collapse to left state
            self.alpha = 1.0 + 0j
            self.beta = 0.0 + 0j
            return "LEFT"
        else:
            # Collapse to right state
            self.alpha = 0.0 + 0j
            self.beta = 1.0 + 0j
            return "RIGHT"
            
    def _quantum_random(self) -> float:
        """
        Generate quantum-inspired random number using environmental noise.
        
        In a real quantum system, this would use true quantum randomness.
        Here we simulate it with multiple entropy sources.
        
        Returns:
            Random float between 0 and 1
        """
        import time
        
        # Combine multiple sources of entropy
        entropy_sources = [
            time.time() * 1000000,  # Microsecond timing
            hash(str(time.time())) % 1000000,  # Hash-based entropy
            random.getrandbits(32),  # System random
        ]
        
        # XOR combine entropy sources
        combined = 0
        for source in entropy_sources:
            combined ^= int(source) % 1000000
            
        # Convert to normalized float
        return (combined % 1000000) / 1000000.0
        
    def apply_decoherence(self, decoherence_rate: float, dt: float):
        """
        Apply quantum decoherence over time.
        
        Args:
            decoherence_rate: Rate of decoherence (1/time)
            dt: Time step
        """
        # Decoherence reduces off-diagonal matrix elements
        decay_factor = math.exp(-decoherence_rate * dt)
        
        # Add random phase noise
        phase_noise = 2 * math.pi * random.random() * decoherence_rate * dt
        self.alpha *= cmath.exp(1j * phase_noise) * decay_factor
        self.beta *= cmath.exp(1j * phase_noise) * decay_factor
        
        self.normalize()
        
    def entangle_with(self, other_wavefunction: 'QuantumWavefunction') -> 'EntangledState':
        """
        Create entangled state with another wavefunction.
        
        Args:
            other_wavefunction: Another QuantumWavefunction to entangle with
            
        Returns:
            EntangledState object representing the entangled system
        """
        return EntangledState(self, other_wavefunction)

class EntangledState:
    """
    Represents an entangled quantum state between two robots.
    
    The entangled state can be written as:
    |ψ⟩ = (1/√2)(|L₁R₂⟩ + |R₁L₂⟩)
    
    This creates anti-correlated behavior where if robot 1 goes left,
    robot 2 goes right, and vice versa.
    """
    
    def __init__(self, wavefunction1: QuantumWavefunction, wavefunction2: QuantumWavefunction):
        self.wf1 = wavefunction1
        self.wf2 = wavefunction2
        self.entanglement_strength = 1.0
        
    def measure_both(self) -> Tuple[str, str]:
        """
        Measure both entangled systems simultaneously.
        
        Returns:
            Tuple of (robot1_direction, robot2_direction)
        """
        # Generate entangled measurement
        random_val = self.wf1._quantum_random()
        
        if random_val < 0.5:
            # Anti-correlated: Robot 1 left, Robot 2 right
            return "LEFT", "RIGHT"
        else:
            # Anti-correlated: Robot 1 right, Robot 2 left
            return "RIGHT", "LEFT"
            
    def break_entanglement(self):
        """Break the entanglement between systems"""
        self.entanglement_strength = 0.0

class QuantumWalkSimulator:
    """
    Main quantum walk simulator for robot control.
    
    This class manages the quantum state evolution, decision making,
    and analysis of the quantum random walk process.
    """
    
    def __init__(self):
        self.wavefunction = QuantumWavefunction()
        self.current_state = QuantumState.SUPERPOSITION
        self.decision_history = []
        self.entropy_history = []
        self.coherence_history = []
        
        # Simulation parameters
        self.decoherence_rate = 0.1  # 1/second
        self.coherence_time = 1.0     # seconds
        self.noise_level = 0.1
        
        # Timing
        self.last_decision_time = 0
        self.total_decisions = 0
        
    def initialize(self, left_amplitude: float = 0.707, right_amplitude: float = 0.707,
                  coherence_time: float = 1.0, noise_level: float = 0.1):
        """
        Initialize quantum simulator with parameters.
        
        Args:
            left_amplitude: Amplitude for left turn state
            right_amplitude: Amplitude for right turn state
            coherence_time: Quantum coherence time in seconds
            noise_level: Environmental noise level (0-1)
        """
        # Set wavefunction amplitudes
        self.wavefunction.alpha = complex(left_amplitude, 0)
        self.wavefunction.beta = complex(right_amplitude, 0)
        self.wavefunction.normalize()
        
        # Set simulation parameters
        self.coherence_time = coherence_time
        self.noise_level = noise_level
        self.decoherence_rate = 1.0 / coherence_time if coherence_time > 0 else 0
        
        # Reset state
        self.current_state = QuantumState.SUPERPOSITION
        self.decision_history.clear()
        self.entropy_history.clear()
        self.coherence_history.clear()
        
    def step(self):
        """Execute one simulation step"""
        import time
        current_time = time.time()
        
        if self.last_decision_time > 0:
            dt = current_time - self.last_decision_time
            
            # Apply quantum evolution
            self.evolve_quantum_state(dt)
            
            # Update histories
            self.update_histories()
            
        self.last_decision_time = current_time
        
    def evolve_quantum_state(self, dt: float):
        """
        Evolve quantum state over time step dt.
        
        Args:
            dt: Time step in seconds
        """
        # Apply decoherence
        self.wavefunction.apply_decoherence(self.decoherence_rate, dt)
        
        # Add environmental noise
        if self.noise_level > 0:
            noise_alpha = complex(
                random.gauss(0, self.noise_level * dt),
                random.gauss(0, self.noise_level * dt)
            )
            noise_beta = complex(
                random.gauss(0, self.noise_level * dt), 
                random.gauss(0, self.noise_level * dt)
            )
            
            self.wavefunction.alpha += noise_alpha
            self.wavefunction.beta += noise_beta
            self.wavefunction.normalize()
            
    def make_quantum_decision(self) -> QuantumDecision:
        """
        Make a quantum-inspired decision.
        
        Returns:
            QuantumDecision object with decision results
        """
        import time
        
        # Get current probabilities
        left_prob, right_prob = self.wavefunction.get_probabilities()
        
        # Calculate quantum properties
        entropy = self.calculate_entropy()
        coherence = self.calculate_coherence()
        
        # Collapse wavefunction
        direction = self.wavefunction.collapse()
        
        # Create decision object
        decision = QuantumDecision(
            direction=direction,
            probability=left_prob if direction == "LEFT" else right_prob,
            amplitude_left=self.wavefunction.alpha,
            amplitude_right=self.wavefunction.beta,
            entropy=entropy,
            coherence=coherence,
            timestamp=time.time()
        )
        
        # Update state
        self.current_state = (QuantumState.LEFT_COLLAPSED if direction == "LEFT" 
                            else QuantumState.RIGHT_COLLAPSED)
        
        # Store in history
        self.decision_history.append(decision)
        self.total_decisions += 1
        
        # Reset to superposition for next decision
        self.reset_to_superposition()
        
        return decision
        
    def calculate_entropy(self) -> float:
        """
        Calculate von Neumann entropy of quantum state.
        
        Returns:
            Quantum entropy value
        """
        left_prob, right_prob = self.wavefunction.get_probabilities()
        
        entropy = 0.0
        if left_prob > 0:
            entropy -= left_prob * math.log2(left_prob)
        if right_prob > 0:
            entropy -= right_prob * math.log2(right_prob)
            
        return entropy
        
    def calculate_coherence(self) -> float:
        """
        Calculate quantum coherence measure.
        
        Returns:
            Coherence value between 0 and 1
        """
        # Coherence related to off-diagonal density matrix elements
        alpha = self.wavefunction.alpha
        beta = self.wavefunction.beta
        
        # Calculate coherence as |⟨L|R⟩|
        coherence = abs(alpha.conjugate() * beta)
        return coherence
        
    def reset_to_superposition(self):
        """Reset wavefunction to superposition state"""
        # Reset to equal superposition (can be customized)
        self.wavefunction.alpha = complex(0.707, 0)
        self.wavefunction.beta = complex(0.707, 0)
        self.current_state = QuantumState.SUPERPOSITION
        
    def update_histories(self):
        """Update historical data for analysis"""
        entropy = self.calculate_entropy()
        coherence = self.calculate_coherence()
        
        self.entropy_history.append(entropy)
        self.coherence_history.append(coherence)
        
        # Keep history size manageable
        max_history = 1000
        if len(self.entropy_history) > max_history:
            self.entropy_history.pop(0)
        if len(self.coherence_history) > max_history:
            self.coherence_history.pop(0)
            
    def get_current_state(self) -> Dict:
        """
        Get current quantum state information.
        
        Returns:
            Dictionary with current state data
        """
        left_prob, right_prob = self.wavefunction.get_probabilities()
        
        return {
            'state': self.current_state.value,
            'left_prob': left_prob,
            'right_prob': right_prob,
            'entropy': self.calculate_entropy(),
            'coherence': self.calculate_coherence(),
            'total_decisions': self.total_decisions,
            'alpha': self.wavefunction.alpha,
            'beta': self.wavefunction.beta
        }
        
    def get_statistics(self) -> Dict:
        """
        Calculate statistical properties of the quantum walk.
        
        Returns:
            Dictionary with statistical data
        """
        if not self.decision_history:
            return {}
            
        left_count = sum(1 for d in self.decision_history if d.direction == "LEFT")
        right_count = len(self.decision_history) - left_count
        
        return {
            'total_decisions': len(self.decision_history),
            'left_decisions': left_count,
            'right_decisions': right_count,
            'left_fraction': left_count / len(self.decision_history),
            'right_fraction': right_count / len(self.decision_history),
            'mean_entropy': np.mean(self.entropy_history) if self.entropy_history else 0,
            'mean_coherence': np.mean(self.coherence_history) if self.coherence_history else 0,
            'entropy_std': np.std(self.entropy_history) if self.entropy_history else 0,
            'coherence_std': np.std(self.coherence_history) if self.coherence_history else 0
        }

class QuantumStateAnalyzer:
    """
    Advanced analysis tools for quantum walk data.
    
    Provides statistical analysis, pattern detection, and 
    educational insights into quantum behavior.
    """
    
    def __init__(self):
        self.analysis_results = {}
        
    def analyze_randomness_quality(self, decisions: List[QuantumDecision]) -> Dict:
        """
        Analyze the quality of randomness in decision sequence.
        
        Args:
            decisions: List of quantum decisions
            
        Returns:
            Dictionary with randomness quality metrics
        """
        if len(decisions) < 2:
            return {}
            
        # Convert decisions to binary sequence
        binary_sequence = [1 if d.direction == "LEFT" else 0 for d in decisions]
        
        # Statistical tests
        results = {
            'sequence_length': len(binary_sequence),
            'runs_test': self._runs_test(binary_sequence),
            'frequency_test': self._frequency_test(binary_sequence),
            'autocorrelation': self._autocorrelation_test(binary_sequence),
            'entropy_rate': self._entropy_rate(binary_sequence)
        }
        
        return results
        
    def _runs_test(self, sequence: List[int]) -> Dict:
        """Statistical runs test for randomness"""
        n = len(sequence)
        if n < 2:
            return {'test': 'runs', 'result': 'insufficient_data'}
            
        # Count runs
        runs = 1
        for i in range(1, n):
            if sequence[i] != sequence[i-1]:
                runs += 1
                
        # Count ones and zeros
        ones = sum(sequence)
        zeros = n - ones
        
        if ones == 0 or zeros == 0:
            return {'test': 'runs', 'result': 'degenerate'}
            
        # Expected runs and variance
        expected_runs = (2 * ones * zeros) / n + 1
        variance = (2 * ones * zeros * (2 * ones * zeros - n)) / (n * n * (n - 1))
        
        # Z-statistic
        if variance > 0:
            z_stat = (runs - expected_runs) / math.sqrt(variance)
            p_value = 2 * (1 - self._standard_normal_cdf(abs(z_stat)))
        else:
            z_stat = 0
            p_value = 1
            
        return {
            'test': 'runs',
            'runs_observed': runs,
            'runs_expected': expected_runs,
            'z_statistic': z_stat,
            'p_value': p_value,
            'result': 'random' if p_value > 0.05 else 'non_random'
        }
        
    def _frequency_test(self, sequence: List[int]) -> Dict:
        """Frequency test for equal probability of 0s and 1s"""
        n = len(sequence)
        if n == 0:
            return {'test': 'frequency', 'result': 'insufficient_data'}
            
        ones = sum(sequence)
        proportion = ones / n
        
        # Z-statistic for proportion test
        expected_proportion = 0.5
        z_stat = (proportion - expected_proportion) / math.sqrt(expected_proportion * (1 - expected_proportion) / n)
        p_value = 2 * (1 - self._standard_normal_cdf(abs(z_stat)))
        
        return {
            'test': 'frequency',
            'proportion_ones': proportion,
            'expected_proportion': expected_proportion,
            'z_statistic': z_stat,
            'p_value': p_value,
            'result': 'random' if p_value > 0.05 else 'biased'
        }
        
    def _autocorrelation_test(self, sequence: List[int], max_lag: int = 10) -> Dict:
        """Test for autocorrelation in the sequence"""
        n = len(sequence)
        if n < max_lag * 2:
            return {'test': 'autocorrelation', 'result': 'insufficient_data'}
            
        # Convert to mean-centered sequence
        mean_val = sum(sequence) / n
        centered = [x - mean_val for x in sequence]
        
        # Calculate autocorrelations
        autocorrs = []
        for lag in range(1, min(max_lag + 1, n // 2)):
            numerator = sum(centered[i] * centered[i + lag] for i in range(n - lag))
            denominator = sum(x * x for x in centered)
            
            if denominator > 0:
                autocorr = numerator / denominator
            else:
                autocorr = 0
                
            autocorrs.append(autocorr)
            
        # Find maximum autocorrelation
        max_autocorr = max(abs(ac) for ac in autocorrs) if autocorrs else 0
        
        return {
            'test': 'autocorrelation',
            'autocorrelations': autocorrs,
            'max_autocorrelation': max_autocorr,
            'result': 'random' if max_autocorr < 0.2 else 'correlated'
        }
        
    def _entropy_rate(self, sequence: List[int]) -> float:
        """Calculate entropy rate of the sequence"""
        if len(sequence) < 2:
            return 0
            
        # Count bigrams
        bigram_counts = {}
        for i in range(len(sequence) - 1):
            bigram = (sequence[i], sequence[i + 1])
            bigram_counts[bigram] = bigram_counts.get(bigram, 0) + 1
            
        # Calculate entropy rate
        total_bigrams = len(sequence) - 1
        entropy_rate = 0
        
        for count in bigram_counts.values():
            if count > 0:
                prob = count / total_bigrams
                entropy_rate -= prob * math.log2(prob)
                
        return entropy_rate
        
    def _standard_normal_cdf(self, x: float) -> float:
        """Approximation of standard normal CDF"""
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))

# Educational utility functions
def demonstrate_quantum_superposition():
    """
    Educational demonstration of quantum superposition principle.
    
    Returns:
        Dictionary with demonstration results
    """
    wf = QuantumWavefunction(alpha=0.6+0j, beta=0.8+0j)
    left_prob, right_prob = wf.get_probabilities()
    
    return {
        'concept': 'Quantum Superposition',
        'explanation': 'Robot exists in superposition of LEFT and RIGHT states',
        'wavefunction': f'|ψ⟩ = {wf.alpha:.3f}|L⟩ + {wf.beta:.3f}|R⟩',
        'probabilities': {
            'left': left_prob,
            'right': right_prob,
            'total': left_prob + right_prob  # Should be 1
        },
        'key_insight': 'Measurement collapses superposition to definite state'
    }

def demonstrate_wavefunction_collapse():
    """
    Educational demonstration of wavefunction collapse.
    
    Returns:
        List of collapse events for visualization
    """
    wf = QuantumWavefunction()
    collapse_events = []
    
    for i in range(10):
        # Record pre-collapse state
        left_prob, right_prob = wf.get_probabilities()
        
        # Perform measurement (collapse)
        result = wf.collapse()
        
        collapse_events.append({
            'measurement': i + 1,
            'pre_collapse_left_prob': left_prob,
            'pre_collapse_right_prob': right_prob,
            'collapse_result': result,
            'explanation': f'Wavefunction collapsed to {result} state'
        })
        
        # Reset for next measurement
        wf = QuantumWavefunction()
        
    return {
        'concept': 'Wavefunction Collapse',
        'events': collapse_events,
        'key_insight': 'Each measurement forces definite outcome from probabilities'
    }

def demonstrate_quantum_entanglement():
    """
    Educational demonstration of quantum entanglement.
    
    Returns:
        Dictionary with entanglement demonstration results
    """
    # Create two wavefunctions
    wf1 = QuantumWavefunction()
    wf2 = QuantumWavefunction()
    
    # Create entangled state
    entangled = wf1.entangle_with(wf2)
    
    # Perform correlated measurements
    measurements = []
    for i in range(10):
        result1, result2 = entangled.measure_both()
        measurements.append({
            'measurement': i + 1,
            'robot1': result1,
            'robot2': result2,
            'correlated': result1 != result2  # Should always be True for anti-correlation
        })
        
    return {
        'concept': 'Quantum Entanglement',
        'explanation': 'Two robots in anti-correlated entangled state',
        'measurements': measurements,
        'correlation_coefficient': -1.0,  # Perfect anti-correlation
        'key_insight': 'Measuring one robot instantly determines the other'
    }
