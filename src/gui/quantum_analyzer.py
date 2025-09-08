"""
Quantum Analysis Module
Advanced quantum state analysis and educational visualization tools.

Author: Quantum Robotics Team
License: MIT
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from typing import Dict, List, Optional
import cmath
from collections import deque

class QuantumAnalyzer:
    """
    Advanced quantum state analysis and visualization system.
    
    Features:
    - Real-time quantum state monitoring
    - Wavefunction visualization
    - Probability distribution analysis
    - Quantum entropy tracking
    - Educational demonstrations
    """
    
    def __init__(self):
        self.quantum_history = {
            'timestamps': deque(maxlen=1000),
            'left_amplitudes': deque(maxlen=1000),
            'right_amplitudes': deque(maxlen=1000),
            'left_probabilities': deque(maxlen=1000),
            'right_probabilities': deque(maxlen=1000),
            'entropies': deque(maxlen=1000),
            'coherences': deque(maxlen=1000),
            'decisions': deque(maxlen=1000)
        }
        
        self.current_state = None
        
    def setup_panel(self, parent_frame):
        """Setup quantum analysis panel"""
        # Create notebook for different analysis views
        self.analysis_notebook = ttk.Notebook(parent_frame)
        self.analysis_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Setup analysis tabs
        self._setup_wavefunction_tab()
        self._setup_probability_tab()
        self._setup_entropy_tab()
        self._setup_educational_tab()
        
    def _setup_wavefunction_tab(self):
        """Setup wavefunction visualization tab"""
        wave_frame = ttk.Frame(self.analysis_notebook)
        self.analysis_notebook.add(wave_frame, text="🌊 Wavefunction")
        
        # Create figure for wavefunction plots
        self.wave_fig, (self.wave_ax, self.phase_ax) = plt.subplots(2, 1, figsize=(8, 6))
        self.wave_fig.patch.set_facecolor('#1a1a1a')
        
        # Amplitude plot
        self.wave_ax.set_facecolor('#0a0a0a')
        self.wave_ax.set_title('Quantum Amplitude', color='white')
        self.wave_ax.set_ylabel('Amplitude', color='white')
        self.wave_ax.tick_params(colors='white')
        self.wave_ax.grid(True, alpha=0.3)
        
        # Phase plot
        self.phase_ax.set_facecolor('#0a0a0a')
        self.phase_ax.set_title('Quantum Phase', color='white')
        self.phase_ax.set_xlabel('State', color='white')
        self.phase_ax.set_ylabel('Phase (radians)', color='white')
        self.phase_ax.tick_params(colors='white')
        self.phase_ax.grid(True, alpha=0.3)
        
        self.wave_canvas = FigureCanvasTkAgg(self.wave_fig, wave_frame)
        self.wave_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Current state display
        state_frame = ttk.LabelFrame(wave_frame, text="Current Quantum State")
        state_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.state_labels = {}
        state_info = [
            ('Left Amplitude', 'left_amp'),
            ('Right Amplitude', 'right_amp'),
            ('Left Probability', 'left_prob'),
            ('Right Probability', 'right_prob'),
            ('Quantum Entropy', 'entropy'),
            ('Coherence', 'coherence')
        ]
        
        for i, (label, key) in enumerate(state_info):
            row = i // 2
            col = i % 2
            
            ttk.Label(state_frame, text=f"{label}:").grid(row=row, column=col*2, sticky=tk.W, padx=5)
            value_label = ttk.Label(state_frame, text="0.000")
            value_label.grid(row=row, column=col*2+1, sticky=tk.W, padx=5)
            self.state_labels[key] = value_label
            
    def _setup_probability_tab(self):
        """Setup probability analysis tab"""
        prob_frame = ttk.Frame(self.analysis_notebook)
        self.analysis_notebook.add(prob_frame, text="📊 Probabilities")
        
        # Create probability plots
        self.prob_fig, ((self.dist_ax, self.hist_ax), 
                       (self.time_ax, self.decision_ax)) = plt.subplots(2, 2, figsize=(10, 8))
        self.prob_fig.patch.set_facecolor('#1a1a1a')
        
        # Probability distribution
        self.dist_ax.set_facecolor('#0a0a0a')
        self.dist_ax.set_title('Current Probability Distribution', color='white')
        self.dist_ax.tick_params(colors='white')
        
        # Probability histogram
        self.hist_ax.set_facecolor('#0a0a0a')
        self.hist_ax.set_title('Probability History', color='white')
        self.hist_ax.tick_params(colors='white')
        
        # Probability over time
        self.time_ax.set_facecolor('#0a0a0a')
        self.time_ax.set_title('Probabilities vs Time', color='white')
        self.time_ax.tick_params(colors='white')
        
        # Decision outcomes
        self.decision_ax.set_facecolor('#0a0a0a')
        self.decision_ax.set_title('Decision Outcomes', color='white')
        self.decision_ax.tick_params(colors='white')
        
        self.prob_canvas = FigureCanvasTkAgg(self.prob_fig, prob_frame)
        self.prob_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def _setup_entropy_tab(self):
        """Setup entropy analysis tab"""
        entropy_frame = ttk.Frame(self.analysis_notebook)
        self.analysis_notebook.add(entropy_frame, text="📈 Entropy")
        
        # Create entropy plots
        self.entropy_fig, (self.entropy_time_ax, self.entropy_dist_ax) = plt.subplots(2, 1, figsize=(8, 6))
        self.entropy_fig.patch.set_facecolor('#1a1a1a')
        
        # Entropy over time
        self.entropy_time_ax.set_facecolor('#0a0a0a')
        self.entropy_time_ax.set_title('Quantum Entropy Over Time', color='white')
        self.entropy_time_ax.set_ylabel('Entropy (bits)', color='white')
        self.entropy_time_ax.tick_params(colors='white')
        self.entropy_time_ax.grid(True, alpha=0.3)
        
        # Entropy distribution
        self.entropy_dist_ax.set_facecolor('#0a0a0a')
        self.entropy_dist_ax.set_title('Entropy Distribution', color='white')
        self.entropy_dist_ax.set_xlabel('Entropy (bits)', color='white')
        self.entropy_dist_ax.set_ylabel('Frequency', color='white')
        self.entropy_dist_ax.tick_params(colors='white')
        self.entropy_dist_ax.grid(True, alpha=0.3)
        
        self.entropy_canvas = FigureCanvasTkAgg(self.entropy_fig, entropy_frame)
        self.entropy_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Entropy statistics
        stats_frame = ttk.LabelFrame(entropy_frame, text="Entropy Statistics")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.entropy_stats = {}
        stat_labels = ['Mean', 'Std Dev', 'Min', 'Max', 'Current']
        
        for i, label in enumerate(stat_labels):
            ttk.Label(stats_frame, text=f"{label}:").grid(row=0, column=i*2, sticky=tk.W, padx=5)
            value_label = ttk.Label(stats_frame, text="0.000")
            value_label.grid(row=0, column=i*2+1, sticky=tk.W, padx=5)
            self.entropy_stats[label.lower().replace(' ', '_')] = value_label
            
    def _setup_educational_tab(self):
        """Setup educational demonstrations tab"""
        edu_frame = ttk.Frame(self.analysis_notebook)
        self.analysis_notebook.add(edu_frame, text="🎓 Education")
        
        # Educational content
        content_frame = ttk.Frame(edu_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Concept explanations
        ttk.Label(content_frame, text="Quantum Concepts Demonstrated:", 
                 font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        concepts = [
            ("Superposition", "Robot exists in multiple states simultaneously until measurement"),
            ("Wavefunction Collapse", "Measurement forces robot to choose definite direction"),
            ("Quantum Entropy", "Measure of uncertainty in quantum state"),
            ("Coherence", "Degree of quantum interference between states"),
            ("Probability Amplitudes", "Complex numbers determining measurement outcomes")
        ]
        
        for concept, explanation in concepts:
            concept_frame = ttk.Frame(content_frame)
            concept_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(concept_frame, text=f"• {concept}:", 
                     font=('Arial', 10, 'bold')).pack(anchor=tk.W)
            ttk.Label(concept_frame, text=f"  {explanation}", 
                     wraplength=500).pack(anchor=tk.W, padx=20)
                     
        # Interactive demonstrations
        demo_frame = ttk.LabelFrame(content_frame, text="Interactive Demonstrations")
        demo_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(demo_frame, text="Demonstrate Superposition", 
                  command=self._demo_superposition).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(demo_frame, text="Show Wavefunction Collapse", 
                  command=self._demo_collapse).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(demo_frame, text="Quantum Interference", 
                  command=self._demo_interference).pack(side=tk.LEFT, padx=5, pady=5)
                  
    def process_quantum_state(self, quantum_state: Dict):
        """Process new quantum state data"""
        import time
        
        self.current_state = quantum_state
        
        # Store in history
        self.quantum_history['timestamps'].append(time.time())
        
        if 'alpha' in quantum_state and 'beta' in quantum_state:
            alpha = quantum_state['alpha']
            beta = quantum_state['beta']
            
            # Handle complex numbers
            if isinstance(alpha, complex):
                self.quantum_history['left_amplitudes'].append(abs(alpha))
            else:
                self.quantum_history['left_amplitudes'].append(float(alpha))
                
            if isinstance(beta, complex):
                self.quantum_history['right_amplitudes'].append(abs(beta))
            else:
                self.quantum_history['right_amplitudes'].append(float(beta))
        
        # Store probabilities
        for key in ['left_prob', 'right_prob', 'entropy', 'coherence']:
            if key in quantum_state:
                history_key = key.replace('prob', 'probabilities').replace('entropy', 'entropies').replace('coherence', 'coherences')
                self.quantum_history[history_key].append(float(quantum_state[key]))
                
        # Update visualizations
        self._update_wavefunction_display()
        self._update_probability_display()
        self._update_entropy_display()
        
    def _update_wavefunction_display(self):
        """Update wavefunction visualization"""
        if not self.current_state:
            return
            
        # Update current state labels
        state_mapping = {
            'left_amp': self.current_state.get('alpha', 0),
            'right_amp': self.current_state.get('beta', 0),
            'left_prob': self.current_state.get('left_prob', 0),
            'right_prob': self.current_state.get('right_prob', 0),
            'entropy': self.current_state.get('entropy', 0),
            'coherence': self.current_state.get('coherence', 0)
        }
        
        for key, value in state_mapping.items():
            if key in self.state_labels:
                if isinstance(value, complex):
                    self.state_labels[key].config(text=f"{abs(value):.4f}")
                else:
                    self.state_labels[key].config(text=f"{float(value):.4f}")
                    
        # Update wavefunction plots
        self.wave_ax.clear()
        self.phase_ax.clear()
        
        # Configure plots
        self.wave_ax.set_facecolor('#0a0a0a')
        self.wave_ax.set_title('Quantum Amplitude', color='white')
        self.wave_ax.tick_params(colors='white')
        
        self.phase_ax.set_facecolor('#0a0a0a')
        self.phase_ax.set_title('Quantum Phase', color='white')
        self.phase_ax.tick_params(colors='white')
        
        # Plot amplitudes
        states = ['Left', 'Right']
        amplitudes = [abs(self.current_state.get('alpha', 0)), 
                     abs(self.current_state.get('beta', 0))]
        
        self.wave_ax.bar(states, amplitudes, color=['blue', 'red'], alpha=0.7)
        self.wave_ax.set_ylabel('Amplitude', color='white')
        
        # Plot phases (if complex)
        alpha = self.current_state.get('alpha', 0)
        beta = self.current_state.get('beta', 0)
        
        if isinstance(alpha, complex) and isinstance(beta, complex):
            phases = [cmath.phase(alpha), cmath.phase(beta)]
            self.phase_ax.bar(states, phases, color=['blue', 'red'], alpha=0.7)
        else:
            phases = [0, 0]  # Real amplitudes have zero phase
            self.phase_ax.bar(states, phases, color=['blue', 'red'], alpha=0.7)
            
        self.phase_ax.set_ylabel('Phase (radians)', color='white')
        self.phase_ax.set_ylim(-np.pi, np.pi)
        
        self.wave_canvas.draw_idle()
        
    def _update_probability_display(self):
        """Update probability visualization"""
        if len(self.quantum_history['left_probabilities']) < 2:
            return
            
        # Clear all subplots
        for ax in [self.dist_ax, self.hist_ax, self.time_ax, self.decision_ax]:
            ax.clear()
            ax.set_facecolor('#0a0a0a')
            ax.tick_params(colors='white')
            
        # Current probability distribution
        if self.current_state:
            left_prob = self.current_state.get('left_prob', 0)
            right_prob = self.current_state.get('right_prob', 0)
            
            self.dist_ax.pie([left_prob, right_prob], 
                           labels=['Left', 'Right'],
                           colors=['blue', 'red'],
                           autopct='%1.1f%%',
                           textprops={'color': 'white'})
            self.dist_ax.set_title('Current Probability Distribution', color='white')
            
        # Probability histogram
        left_probs = list(self.quantum_history['left_probabilities'])
        if left_probs:
            self.hist_ax.hist(left_probs, bins=20, alpha=0.7, color='blue', 
                            label='Left Probability')
            self.hist_ax.set_title('Probability History', color='white')
            self.hist_ax.set_xlabel('Probability', color='white')
            self.hist_ax.set_ylabel('Frequency', color='white')
            self.hist_ax.legend()
            
        # Probabilities over time
        if len(self.quantum_history['timestamps']) > 1:
            times = list(self.quantum_history['timestamps'])
            rel_times = [(t - times[0]) for t in times[-100:]]
            
            left_probs = list(self.quantum_history['left_probabilities'])[-100:]
            right_probs = list(self.quantum_history['right_probabilities'])[-100:]
            
            self.time_ax.plot(rel_times, left_probs, 'b-', label='Left', alpha=0.8)
            self.time_ax.plot(rel_times, right_probs, 'r-', label='Right', alpha=0.8)
            self.time_ax.set_title('Probabilities vs Time', color='white')
            self.time_ax.set_xlabel('Time (s)', color='white')
            self.time_ax.set_ylabel('Probability', color='white')
            self.time_ax.legend()
            self.time_ax.grid(True, alpha=0.3)
            
        # Decision outcomes
        decisions = list(self.quantum_history['decisions'])
        if decisions:
            left_count = decisions.count('LEFT')
            right_count = decisions.count('RIGHT')
            
            if left_count + right_count > 0:
                self.decision_ax.bar(['Left Decisions', 'Right Decisions'], 
                                   [left_count, right_count],
                                   color=['blue', 'red'], alpha=0.7)
                self.decision_ax.set_title('Decision Outcomes', color='white')
                self.decision_ax.set_ylabel('Count', color='white')
                
        self.prob_canvas.draw_idle()
        
    def _update_entropy_display(self):
        """Update entropy visualization"""
        entropies = list(self.quantum_history['entropies'])
        if len(entropies) < 2:
            return
            
        # Clear plots
        self.entropy_time_ax.clear()
        self.entropy_dist_ax.clear()
        
        # Configure plots
        self.entropy_time_ax.set_facecolor('#0a0a0a')
        self.entropy_time_ax.set_title('Quantum Entropy Over Time', color='white')
        self.entropy_time_ax.tick_params(colors='white')
        self.entropy_time_ax.grid(True, alpha=0.3)
        
        self.entropy_dist_ax.set_facecolor('#0a0a0a')
        self.entropy_dist_ax.set_title('Entropy Distribution', color='white')
        self.entropy_dist_ax.tick_params(colors='white')
        self.entropy_dist_ax.grid(True, alpha=0.3)
        
        # Entropy over time
        times = list(self.quantum_history['timestamps'])
        if len(times) >= len(entropies):
            rel_times = [(t - times[0]) for t in times[-len(entropies):]]
            self.entropy_time_ax.plot(rel_times, entropies, 'purple', linewidth=2)
            self.entropy_time_ax.set_xlabel('Time (s)', color='white')
            self.entropy_time_ax.set_ylabel('Entropy (bits)', color='white')
            
        # Entropy distribution
        self.entropy_dist_ax.hist(entropies, bins=20, alpha=0.7, color='purple')
        self.entropy_dist_ax.set_xlabel('Entropy (bits)', color='white')
        self.entropy_dist_ax.set_ylabel('Frequency', color='white')
        
        # Update statistics
        entropy_array = np.array(entropies)
        stats = {
            'mean': np.mean(entropy_array),
            'std_dev': np.std(entropy_array),
            'min': np.min(entropy_array),
            'max': np.max(entropy_array),
            'current': entropy_array[-1] if len(entropy_array) > 0 else 0
        }
        
        for key, value in stats.items():
            if key in self.entropy_stats:
                self.entropy_stats[key].config(text=f"{value:.4f}")
                
        self.entropy_canvas.draw_idle()
        
    # Educational demonstration methods
    def _demo_superposition(self):
        """Demonstrate quantum superposition"""
        # This would show an educational animation of superposition
        pass
        
    def _demo_collapse(self):
        """Demonstrate wavefunction collapse"""
        # This would show an animation of wavefunction collapse
        pass
        
    def _demo_interference(self):
        """Demonstrate quantum interference"""
        # This would show quantum interference effects
        pass
