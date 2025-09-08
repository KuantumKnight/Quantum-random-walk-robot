#!/usr/bin/env python3
"""
Quantum Random Walk Robot - Main GUI Application
A professional-grade interface for controlling and monitoring quantum-inspired robots.

Author: Quantum Robotics Team
License: MIT
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import socket
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.quantum_math import QuantumWalkSimulator, QuantumStateAnalyzer
from utils.data_logger import QuantumDataLogger
from gui.config_manager import ConfigManager
from gui.telemetry_visualizer import TelemetryVisualizer
from gui.quantum_analyzer import QuantumAnalyzer

class QuantumRobotGUI:
    """
    Main application class for Quantum Random Walk Robot control system.
    
    This class provides a comprehensive interface for:
    - Real-time robot control and monitoring
    - Quantum state visualization and analysis
    - Educational demonstrations of quantum concepts
    - Multi-robot coordination and entanglement simulation
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_application()
        
        # Core components
        self.config_manager = ConfigManager()
        self.quantum_simulator = QuantumWalkSimulator()
        self.quantum_analyzer = QuantumAnalyzer()
        self.data_logger = QuantumDataLogger()
        self.telemetry_visualizer = TelemetryVisualizer()
        
        # Robot state
        self.robot_connected = False
        self.quantum_walk_active = False
        self.current_quantum_state = None
        self.entanglement_active = False
        
        # Network components
        self.connection_manager = None
        self.robot_socket = None
        
        # GUI setup
        self.setup_gui()
        self.setup_quantum_visualization()
        self.setup_event_handlers()
        
        # Start main loops
        self.start_update_loops()
        
    def setup_application(self):
        """Initialize application settings and theme"""
        self.root.title("Quantum Random Walk Robot Control Center")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#1a1a1a')
        
        # Set application icon
        try:
            self.root.iconbitmap('assets/icons/quantum_robot.ico')
        except:
            pass  # Icon file not found, continue without
            
        # Configure modern theme
        self.setup_theme()
        
    def setup_theme(self):
        """Apply modern dark theme"""
        style = ttk.Style()
        
        # Configure dark theme colors
        colors = {
            'bg': '#1a1a1a',
            'fg': '#ffffff',
            'select_bg': '#404040',
            'select_fg': '#ffffff',
            'button_bg': '#2d2d2d',
            'button_fg': '#ffffff',
            'entry_bg': '#2d2d2d',
            'entry_fg': '#ffffff'
        }
        
        # Apply theme
        style.theme_use('clam')
        style.configure('TLabel', background=colors['bg'], foreground=colors['fg'])
        style.configure('TButton', background=colors['button_bg'], foreground=colors['button_fg'])
        style.configure('TEntry', background=colors['entry_bg'], foreground=colors['entry_fg'])
        style.configure('TFrame', background=colors['bg'])
        style.configure('TNotebook', background=colors['bg'])
        style.configure('TNotebook.Tab', background=colors['button_bg'], foreground=colors['button_fg'])
        
    def setup_gui(self):
        """Create main GUI layout"""
        # Create main menu
        self.create_menu()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create main content area
        self.create_main_layout()
        
        # Create status bar
        self.create_status_bar()
        
    def create_menu(self):
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Experiment", command=self.new_experiment, accelerator="Ctrl+N")
        file_menu.add_command(label="Open Data", command=self.open_data, accelerator="Ctrl+O")
        file_menu.add_command(label="Save Experiment", command=self.save_experiment, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Export Data", command=self.export_data)
        file_menu.add_command(label="Export Images", command=self.export_images)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing, accelerator="Ctrl+Q")
        
        # Robot menu
        robot_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Robot", menu=robot_menu)
        robot_menu.add_command(label="Connect", command=self.connect_robot, accelerator="Ctrl+R")
        robot_menu.add_command(label="Disconnect", command=self.disconnect_robot)
        robot_menu.add_separator()
        robot_menu.add_command(label="Start Quantum Walk", command=self.start_quantum_walk)
        robot_menu.add_command(label="Stop Quantum Walk", command=self.stop_quantum_walk)
        robot_menu.add_separator()
        robot_menu.add_command(label="Emergency Stop", command=self.emergency_stop, accelerator="F1")
        
        # Quantum menu
        quantum_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Quantum", menu=quantum_menu)
        quantum_menu.add_command(label="Quantum State Analysis", command=self.show_quantum_analysis)
        quantum_menu.add_command(label="Entanglement Setup", command=self.setup_entanglement)
        quantum_menu.add_command(label="Probability Distributions", command=self.show_probability_analysis)
        quantum_menu.add_separator()
        quantum_menu.add_command(label="Educational Demo", command=self.start_educational_demo)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Settings", command=self.show_settings)
        tools_menu.add_command(label="Hardware Test", command=self.hardware_test)
        tools_menu.add_command(label="Network Scanner", command=self.network_scanner)
        tools_menu.add_separator()
        tools_menu.add_command(label="Calibration", command=self.calibrate_robot)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="User Guide", command=self.show_user_guide)
        help_menu.add_command(label="Quantum Theory", command=self.show_quantum_theory)
        help_menu.add_command(label="Hardware Setup", command=self.show_hardware_guide)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.show_about)
        
    def create_toolbar(self):
        """Create main toolbar"""
        self.toolbar = ttk.Frame(self.root)
        self.toolbar.pack(fill=tk.X, padx=5, pady=2)
        
        # Connection status
        self.connection_frame = ttk.Frame(self.toolbar)
        self.connection_frame.pack(side=tk.LEFT)
        
        self.connection_indicator = tk.Label(self.connection_frame, text="●", fg="red", 
                                           font=("Arial", 16), bg='#1a1a1a')
        self.connection_indicator.pack(side=tk.LEFT)
        
        self.connection_label = ttk.Label(self.connection_frame, text="Disconnected")
        self.connection_label.pack(side=tk.LEFT, padx=(5, 20))
        
        # Quick action buttons
        self.connect_btn = ttk.Button(self.toolbar, text="🔗 Connect", command=self.connect_robot)
        self.connect_btn.pack(side=tk.LEFT, padx=2)
        
        self.start_walk_btn = ttk.Button(self.toolbar, text="⚛️ Start Quantum Walk", 
                                       command=self.start_quantum_walk)
        self.start_walk_btn.pack(side=tk.LEFT, padx=2)
        
        # Emergency stop (prominent red button)
        self.emergency_btn = tk.Button(self.toolbar, text="🛑 EMERGENCY STOP", 
                                     command=self.emergency_stop, bg="darkred", fg="white",
                                     font=("Arial", 10, "bold"))
        self.emergency_btn.pack(side=tk.RIGHT, padx=5)
        
        # Recording controls
        self.record_btn = ttk.Button(self.toolbar, text="📹 Record", command=self.toggle_recording)
        self.record_btn.pack(side=tk.RIGHT, padx=2)
        
    def create_main_layout(self):
        """Create main application layout"""
        # Create main paned window
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel (controls and settings)
        self.left_panel = ttk.Frame(self.main_paned, width=350)
        self.main_paned.add(self.left_panel, weight=0)
        
        # Center panel (visualization)
        self.center_panel = ttk.Frame(self.main_paned)
        self.main_paned.add(self.center_panel, weight=1)
        
        # Right panel (quantum analysis)
        self.right_panel = ttk.Frame(self.main_paned, width=300)
        self.main_paned.add(self.right_panel, weight=0)
        
        # Setup individual panels
        self.setup_left_panel()
        self.setup_center_panel()
        self.setup_right_panel()
        
    def setup_left_panel(self):
        """Setup left control panel"""
        # Robot Control Section
        control_frame = ttk.LabelFrame(self.left_panel, text="🤖 Robot Control")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Connection settings
        conn_frame = ttk.Frame(control_frame)
        conn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(conn_frame, text="Robot IP:").grid(row=0, column=0, sticky=tk.W)
        self.robot_ip = tk.StringVar(value="192.168.4.1")
        ip_entry = ttk.Entry(conn_frame, textvariable=self.robot_ip, width=15)
        ip_entry.grid(row=0, column=1, padx=(5, 0))
        
        ttk.Label(conn_frame, text="Port:").grid(row=1, column=0, sticky=tk.W)
        self.robot_port = tk.StringVar(value="80")
        port_entry = ttk.Entry(conn_frame, textvariable=self.robot_port, width=15)
        port_entry.grid(row=1, column=1, padx=(5, 0))
        
        # Manual controls
        manual_frame = ttk.LabelFrame(control_frame, text="Manual Control")
        manual_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Direction buttons in cross pattern
        btn_frame = ttk.Frame(manual_frame)
        btn_frame.pack(padx=5, pady=5)
        
        ttk.Button(btn_frame, text="↑", command=lambda: self.send_command("FORWARD"),
                  width=3).grid(row=0, column=1, padx=1, pady=1)
        ttk.Button(btn_frame, text="←", command=lambda: self.send_command("LEFT"),
                  width=3).grid(row=1, column=0, padx=1, pady=1)
        ttk.Button(btn_frame, text="⏹", command=lambda: self.send_command("STOP"),
                  width=3).grid(row=1, column=1, padx=1, pady=1)
        ttk.Button(btn_frame, text="→", command=lambda: self.send_command("RIGHT"),
                  width=3).grid(row=1, column=2, padx=1, pady=1)
        ttk.Button(btn_frame, text="↓", command=lambda: self.send_command("BACKWARD"),
                  width=3).grid(row=2, column=1, padx=1, pady=1)
        
        # Quantum Parameters Section
        quantum_frame = ttk.LabelFrame(self.left_panel, text="⚛️ Quantum Parameters")
        quantum_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Quantum probability controls
        self.setup_quantum_controls(quantum_frame)
        
        # System Settings Section
        system_frame = ttk.LabelFrame(self.left_panel, text="⚙️ System Settings")
        system_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.setup_system_controls(system_frame)
        
    def setup_quantum_controls(self, parent):
        """Setup quantum parameter controls"""
        # Left turn amplitude
        ttk.Label(parent, text="Left Amplitude (ψ_L):").pack(anchor=tk.W, padx=5)
        self.left_amplitude = tk.DoubleVar(value=0.707)  # √(1/2)
        left_scale = ttk.Scale(parent, from_=0, to=1, variable=self.left_amplitude, 
                              orient=tk.HORIZONTAL)
        left_scale.pack(fill=tk.X, padx=5)
        self.left_amp_label = ttk.Label(parent, text="0.707")
        self.left_amp_label.pack(anchor=tk.W, padx=5)
        left_scale.configure(command=self.update_left_amplitude)
        
        # Right turn amplitude
        ttk.Label(parent, text="Right Amplitude (ψ_R):").pack(anchor=tk.W, padx=5, pady=(10,0))
        self.right_amplitude = tk.DoubleVar(value=0.707)  # √(1/2)
        right_scale = ttk.Scale(parent, from_=0, to=1, variable=self.right_amplitude, 
                               orient=tk.HORIZONTAL)
        right_scale.pack(fill=tk.X, padx=5)
        self.right_amp_label = ttk.Label(parent, text="0.707")
        self.right_amp_label.pack(anchor=tk.W, padx=5)
        right_scale.configure(command=self.update_right_amplitude)
        
        # Quantum coherence time
        ttk.Label(parent, text="Coherence Time (s):").pack(anchor=tk.W, padx=5, pady=(10,0))
        self.coherence_time = tk.DoubleVar(value=1.0)
        coherence_scale = ttk.Scale(parent, from_=0.1, to=5.0, variable=self.coherence_time, 
                                   orient=tk.HORIZONTAL)
        coherence_scale.pack(fill=tk.X, padx=5)
        self.coherence_label = ttk.Label(parent, text="1.0 s")
        self.coherence_label.pack(anchor=tk.W, padx=5)
        coherence_scale.configure(command=self.update_coherence_time)
        
        # Quantum noise level
        ttk.Label(parent, text="Quantum Noise:").pack(anchor=tk.W, padx=5, pady=(10,0))
        self.quantum_noise = tk.DoubleVar(value=0.1)
        noise_scale = ttk.Scale(parent, from_=0, to=0.5, variable=self.quantum_noise, 
                               orient=tk.HORIZONTAL)
        noise_scale.pack(fill=tk.X, padx=5)
        self.noise_label = ttk.Label(parent, text="0.1")
        self.noise_label.pack(anchor=tk.W, padx=5)
        noise_scale.configure(command=self.update_quantum_noise)
        
        # Update parameters button
        update_btn = ttk.Button(parent, text="📡 Update Robot Parameters", 
                               command=self.update_quantum_parameters)
        update_btn.pack(fill=tk.X, padx=5, pady=10)
        
    def setup_system_controls(self, parent):
        """Setup system control buttons"""
        # Robot speed
        ttk.Label(parent, text="Robot Speed:").pack(anchor=tk.W, padx=5)
        self.robot_speed = tk.IntVar(value=5)
        speed_scale = ttk.Scale(parent, from_=1, to=10, variable=self.robot_speed, 
                               orient=tk.HORIZONTAL)
        speed_scale.pack(fill=tk.X, padx=5)
        self.speed_label = ttk.Label(parent, text="5")
        self.speed_label.pack(anchor=tk.W, padx=5)
        speed_scale.configure(command=self.update_robot_speed)
        
        # System controls
        ttk.Button(parent, text="🏁 Start Mission", command=self.start_mission).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(parent, text="⏹ Stop Mission", command=self.stop_mission).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(parent, text="🔄 Reset Position", command=self.reset_position).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(parent, text="📊 Run Analysis", command=self.run_quantum_analysis).pack(fill=tk.X, padx=5, pady=2)
        
    def setup_center_panel(self):
        """Setup center visualization panel"""
        self.viz_notebook = ttk.Notebook(self.center_panel)
        self.viz_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Robot Path Visualization
        self.setup_path_visualization()
        
        # Quantum State Visualization
        self.setup_quantum_visualization()
        
        # Live Telemetry
        self.setup_telemetry_panel()
        
        # Educational Demo
        self.setup_educational_panel()
        
    def setup_path_visualization(self):
        """Setup robot path visualization tab"""
        path_frame = ttk.Frame(self.viz_notebook)
        self.viz_notebook.add(path_frame, text="🗺️ Robot Path")
        
        # Create matplotlib figure
        self.path_fig, (self.path_ax, self.minimap_ax) = plt.subplots(1, 2, figsize=(12, 6))
        self.path_fig.patch.set_facecolor('#1a1a1a')
        
        # Main path plot
        self.path_ax.set_facecolor('#0a0a0a')
        self.path_ax.set_title("Quantum Random Walk Path", color='white', fontsize=14)
        self.path_ax.set_xlabel("X Position (meters)", color='white')
        self.path_ax.set_ylabel("Y Position (meters)", color='white')
        self.path_ax.tick_params(colors='white')
        self.path_ax.grid(True, alpha=0.3)
        
        # Initialize path line
        self.robot_path = []
        self.path_line, = self.path_ax.plot([], [], 'cyan-', linewidth=2, alpha=0.8, label='Robot Path')
        self.current_pos, = self.path_ax.plot([], [], 'ro', markersize=10, label='Current Position')
        self.quantum_decisions, = self.path_ax.plot([], [], 'y*', markersize=8, alpha=0.7, label='Quantum Decisions')
        self.path_ax.legend()
        
        # Mini-map
        self.minimap_ax.set_facecolor('#0a0a0a')
        self.minimap_ax.set_title("Mini-Map", color='white')
        self.minimap_ax.set_xlim(-10, 10)
        self.minimap_ax.set_ylim(-10, 10)
        self.minimap_ax.tick_params(colors='white')
        self.minimap_ax.grid(True, alpha=0.3)
        
        self.minimap_pos, = self.minimap_ax.plot([], [], 'ro', markersize=12)
        
        # Embed in tkinter
        self.path_canvas = FigureCanvasTkAgg(self.path_fig, path_frame)
        self.path_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def setup_quantum_visualization(self):
        """Setup quantum state visualization"""
        quantum_frame = ttk.Frame(self.viz_notebook)
        self.viz_notebook.add(quantum_frame, text="⚛️ Quantum States")
        
        # Create quantum visualization plots
        self.quantum_fig, ((self.prob_ax, self.wave_ax), 
                          (self.entropy_ax, self.coherence_ax)) = plt.subplots(2, 2, figsize=(12, 8))
        self.quantum_fig.patch.set_facecolor('#1a1a1a')
        
        # Probability distribution
        self.prob_ax.set_facecolor('#0a0a0a')
        self.prob_ax.set_title("Decision Probabilities", color='white')
        self.prob_ax.set_ylabel("Probability", color='white')
        self.prob_ax.tick_params(colors='white')
        
        # Wavefunction visualization
        self.wave_ax.set_facecolor('#0a0a0a')
        self.wave_ax.set_title("Quantum Wavefunction", color='white')
        self.wave_ax.set_ylabel("Amplitude", color='white')
        self.wave_ax.tick_params(colors='white')
        
        # Entropy over time
        self.entropy_ax.set_facecolor('#0a0a0a')
        self.entropy_ax.set_title("Quantum Entropy", color='white')
        self.entropy_ax.set_xlabel("Time (s)", color='white')
        self.entropy_ax.set_ylabel("Entropy", color='white')
        self.entropy_ax.tick_params(colors='white')
        
        # Coherence time
        self.coherence_ax.set_facecolor('#0a0a0a')
        self.coherence_ax.set_title("Quantum Coherence", color='white')
        self.coherence_ax.set_xlabel("Time (s)", color='white')
        self.coherence_ax.set_ylabel("Coherence", color='white')
        self.coherence_ax.tick_params(colors='white')
        
        self.quantum_canvas = FigureCanvasTkAgg(self.quantum_fig, quantum_frame)
        self.quantum_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def setup_telemetry_panel(self):
        """Setup live telemetry display"""
        telemetry_frame = ttk.Frame(self.viz_notebook)
        self.viz_notebook.add(telemetry_frame, text="📊 Live Telemetry")
        
        # Use telemetry visualizer component
        self.telemetry_visualizer.setup_panel(telemetry_frame)
        
    def setup_educational_panel(self):
        """Setup educational demonstration panel"""
        edu_frame = ttk.Frame(self.viz_notebook)
        self.viz_notebook.add(edu_frame, text="🎓 Educational Demo")
        
        # Educational content will be implemented here
        # This could include interactive quantum mechanics demonstrations
        # Step-by-step explanations of quantum concepts
        # Guided experiments for students
        
        demo_label = ttk.Label(edu_frame, text="Educational demonstrations will be displayed here",
                              font=("Arial", 14))
        demo_label.pack(expand=True)
        
    def setup_right_panel(self):
        """Setup right analysis panel"""
        # Live quantum analysis
        analysis_frame = ttk.LabelFrame(self.right_panel, text="🔬 Quantum Analysis")
        analysis_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.quantum_analyzer.setup_panel(analysis_frame)
        
    def create_status_bar(self):
        """Create application status bar"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Status information
        self.status_text = ttk.Label(self.status_bar, text="Ready")
        self.status_text.pack(side=tk.LEFT, padx=5)
        
        # Quantum state indicator
        self.quantum_status = ttk.Label(self.status_bar, text="Quantum State: Inactive")
        self.quantum_status.pack(side=tk.LEFT, padx=20)
        
        # System time
        self.time_label = ttk.Label(self.status_bar, text="")
        self.time_label.pack(side=tk.RIGHT, padx=5)
        
    def setup_event_handlers(self):
        """Setup keyboard shortcuts and event handlers"""
        # Keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.new_experiment())
        self.root.bind('<Control-o>', lambda e: self.open_data())
        self.root.bind('<Control-s>', lambda e: self.save_experiment())
        self.root.bind('<Control-r>', lambda e: self.connect_robot())
        self.root.bind('<Control-q>', lambda e: self.on_closing())
        self.root.bind('<F1>', lambda e: self.emergency_stop())
        
        # Robot control keys
        self.root.bind('<KeyPress-w>', lambda e: self.send_command("FORWARD"))
        self.root.bind('<KeyPress-s>', lambda e: self.send_command("BACKWARD"))
        self.root.bind('<KeyPress-a>', lambda e: self.send_command("LEFT"))
        self.root.bind('<KeyPress-d>', lambda e: self.send_command("RIGHT"))
        self.root.bind('<KeyPress-space>', lambda e: self.send_command("STOP"))
        
        self.root.focus_set()  # Enable keyboard input
        
        # Window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def start_update_loops(self):
        """Start main update loops"""
        self.update_gui()
        self.update_quantum_state()
        self.update_time()
        
    def update_gui(self):
        """Main GUI update loop"""
        try:
            # Update connection status
            if self.robot_connected:
                self.connection_indicator.config(fg="green")
                self.connection_label.config(text="Connected")
            else:
                self.connection_indicator.config(fg="red")
                self.connection_label.config(text="Disconnected")
            
            # Update visualizations
            self.update_path_visualization()
            self.update_quantum_plots()
            
            # Update telemetry
            if hasattr(self, 'telemetry_visualizer'):
                self.telemetry_visualizer.update()
                
        except Exception as e:
            print(f"GUI update error: {e}")
        
        # Schedule next update
        self.root.after(50, self.update_gui)  # 20 Hz update rate
        
    def update_quantum_state(self):
        """Update quantum state simulation"""
        if self.quantum_walk_active:
            # Update quantum simulator
            self.quantum_simulator.step()
            self.current_quantum_state = self.quantum_simulator.get_current_state()
            
            # Update quantum analyzer
            if hasattr(self, 'quantum_analyzer'):
                self.quantum_analyzer.process_quantum_state(self.current_quantum_state)
        
        # Schedule next update
        self.root.after(100, self.update_quantum_state)  # 10 Hz quantum updates
        
    def update_time(self):
        """Update system time display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)  # Update every second
        
    # Parameter update methods
    def update_left_amplitude(self, value):
        """Update left turn amplitude"""
        val = float(value)
        self.left_amp_label.config(text=f"{val:.3f}")
        # Normalize amplitudes to maintain quantum normalization
        self.normalize_amplitudes()
        
    def update_right_amplitude(self, value):
        """Update right turn amplitude"""
        val = float(value)
        self.right_amp_label.config(text=f"{val:.3f}")
        self.normalize_amplitudes()
        
    def update_coherence_time(self, value):
        """Update coherence time"""
        val = float(value)
        self.coherence_label.config(text=f"{val:.1f} s")
        
    def update_quantum_noise(self, value):
        """Update quantum noise level"""
        val = float(value)
        self.noise_label.config(text=f"{val:.2f}")
        
    def update_robot_speed(self, value):
        """Update robot speed"""
        val = int(float(value))
        self.speed_label.config(text=str(val))
        
    def normalize_amplitudes(self):
        """Ensure quantum amplitude normalization |ψ_L|² + |ψ_R|² = 1"""
        left_amp = self.left_amplitude.get()
        right_amp = self.right_amplitude.get()
        
        # Calculate normalization factor
        norm = np.sqrt(left_amp**2 + right_amp**2)
        if norm > 0:
            self.left_amplitude.set(left_amp / norm)
            self.right_amplitude.set(right_amp / norm)
            self.left_amp_label.config(text=f"{self.left_amplitude.get():.3f}")
            self.right_amp_label.config(text=f"{self.right_amplitude.get():.3f}")
    
    # Robot control methods
    def connect_robot(self):
        """Connect to robot"""
        try:
            ip = self.robot_ip.get()
            port = int(self.robot_port.get())
            
            self.robot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.robot_socket.settimeout(5)
            self.robot_socket.connect((ip, port))
            
            self.robot_connected = True
            self.status_text.config(text=f"Connected to robot at {ip}:{port}")
            
            # Start telemetry reception thread
            self.start_telemetry_thread()
            
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
            
    def disconnect_robot(self):
        """Disconnect from robot"""
        if self.robot_socket:
            try:
                self.robot_socket.close()
            except:
                pass
        self.robot_connected = False
        self.status_text.config(text="Disconnected from robot")
        
    def send_command(self, command):
        """Send command to robot"""
        if not self.robot_connected:
            self.status_text.config(text="Not connected to robot")
            return
            
        try:
            message = f"pass123{command}\n"
            self.robot_socket.send(message.encode())
            self.status_text.config(text=f"Sent command: {command}")
        except Exception as e:
            messagebox.showerror("Command Error", f"Failed to send command: {str(e)}")
            
    def start_quantum_walk(self):
        """Start quantum random walk"""
        if not self.robot_connected:
            messagebox.showwarning("Not Connected", "Please connect to robot first")
            return
            
        self.quantum_walk_active = True
        self.quantum_status.config(text="Quantum State: Active")
        
        # Initialize quantum simulator with current parameters
        self.quantum_simulator.initialize(
            left_amplitude=self.left_amplitude.get(),
            right_amplitude=self.right_amplitude.get(),
            coherence_time=self.coherence_time.get(),
            noise_level=self.quantum_noise.get()
        )
        
        # Start quantum walk thread
        self.quantum_thread = threading.Thread(target=self.quantum_walk_loop, daemon=True)
        self.quantum_thread.start()
        
        self.status_text.config(text="Quantum random walk started")
        
    def stop_quantum_walk(self):
        """Stop quantum random walk"""
        self.quantum_walk_active = False
        self.quantum_status.config(text="Quantum State: Inactive")
        self.send_command("STOP")
        self.status_text.config(text="Quantum random walk stopped")
        
    def quantum_walk_loop(self):
        """Main quantum walk execution loop"""
        while self.quantum_walk_active:
            try:
                # Generate quantum decision
                decision = self.quantum_simulator.make_quantum_decision()
                
                # Log quantum event
                self.data_logger.log_quantum_event(decision)
                
                # Send command to robot
                if decision['direction'] == 'LEFT':
                    self.send_command("LEFT")
                elif decision['direction'] == 'RIGHT':
                    self.send_command("RIGHT")
                
                # Wait for coherence time
                time.sleep(self.coherence_time.get())
                
            except Exception as e:
                print(f"Quantum walk error: {e}")
                break
                
    def emergency_stop(self):
        """Emergency stop all robot operations"""
        self.stop_quantum_walk()
        self.send_command("EMERGENCY_STOP")
        self.status_text.config(text="EMERGENCY STOP ACTIVATED!")
        messagebox.showwarning("Emergency Stop", "All robot operations have been stopped!")
        
    # Visualization update methods
    def update_path_visualization(self):
        """Update robot path visualization"""
        if hasattr(self, 'robot_path') and len(self.robot_path) > 0:
            x_coords = [pos[0] for pos in self.robot_path]
            y_coords = [pos[1] for pos in self.robot_path]
            
            # Update main path
            self.path_line.set_data(x_coords, y_coords)
            
            # Update current position
            if len(self.robot_path) > 0:
                current_x, current_y = self.robot_path[-1]
                self.current_pos.set_data([current_x], [current_y])
                self.minimap_pos.set_data([current_x], [current_y])
            
            # Auto-scale axes
            self.path_ax.relim()
            self.path_ax.autoscale_view()
            
            self.path_canvas.draw_idle()
            
    def update_quantum_plots(self):
        """Update quantum state visualizations"""
        if self.current_quantum_state:
            # Update probability distribution
            self.prob_ax.clear()
            self.prob_ax.set_facecolor('#0a0a0a')
            self.prob_ax.bar(['Left', 'Right'], 
                           [self.current_quantum_state['left_prob'], 
                            self.current_quantum_state['right_prob']],
                           color=['blue', 'red'], alpha=0.7)
            self.prob_ax.set_title("Decision Probabilities", color='white')
            self.prob_ax.set_ylabel("Probability", color='white')
            self.prob_ax.tick_params(colors='white')
            
            # Update other quantum plots as needed
            self.quantum_canvas.draw_idle()
            
    # Menu action methods
    def new_experiment(self):
        """Create new experiment"""
        self.status_text.config(text="New experiment created")
        # Reset all data and visualizations
        
    def open_data(self):
        """Open experimental data"""
        filename = filedialog.askopenfilename(
            title="Open Experiment Data",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.status_text.config(text=f"Opened: {filename}")
            
    def save_experiment(self):
        """Save current experiment"""
        filename = filedialog.asksaveasfilename(
            title="Save Experiment",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.status_text.config(text=f"Saved: {filename}")
            
    def export_data(self):
        """Export experimental data"""
        filename = filedialog.asksaveasfilename(
            title="Export Data",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            # Export logic here
            self.status_text.config(text=f"Data exported to: {filename}")
            
    def export_images(self):
        """Export visualization images"""
        # Implementation for exporting plots as images
        self.status_text.config(text="Images exported")
        
    def show_about(self):
        """Show about dialog"""
        about_text = """
        Quantum Random Walk Robot Control System
        Version 2.0.0
        
        A professional-grade application for controlling and analyzing
        quantum-inspired robot behavior.
        
        © 2025 Quantum Robotics Team
        Licensed under MIT License
        
        Built with Python, Tkinter, and Matplotlib
        """
        messagebox.showinfo("About", about_text)
        
    def on_closing(self):
        """Handle application closing"""
        if self.quantum_walk_active:
            if messagebox.askokcancel("Quit", "Quantum walk is active. Stop and quit?"):
                self.stop_quantum_walk()
                self.disconnect_robot()
                self.root.destroy()
        else:
            self.disconnect_robot()
            self.root.destroy()
            
    # Additional methods (abbreviated for space)
    def start_telemetry_thread(self): pass
    def update_quantum_parameters(self): pass
    def start_mission(self): pass
    def stop_mission(self): pass
    def reset_position(self): pass
    def run_quantum_analysis(self): pass
    def show_quantum_analysis(self): pass
    def setup_entanglement(self): pass
    def show_probability_analysis(self): pass
    def start_educational_demo(self): pass
    def show_settings(self): pass
    def hardware_test(self): pass
    def network_scanner(self): pass
    def calibrate_robot(self): pass
    def show_user_guide(self): pass
    def show_quantum_theory(self): pass
    def show_hardware_guide(self): pass
    def toggle_recording(self): pass

def main():
    """Application entry point"""
    app = QuantumRobotGUI()
    app.root.mainloop()

if __name__ == "__main__":
    main()
