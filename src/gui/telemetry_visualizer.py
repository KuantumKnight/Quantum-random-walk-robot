"""
Telemetry Visualization Module
Advanced real-time telemetry plotting and analysis tools.

Author: Quantum Robotics Team
License: MIT
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np
from collections import deque
import time
from typing import Dict, List, Optional, Callable

class TelemetryVisualizer:
    """
    Advanced telemetry visualization system with multiple plot types,
    real-time updates, and customizable displays.
    """
    
    def __init__(self):
        self.telemetry_data = {
            'timestamps': deque(maxlen=500),
            'battery_voltage': deque(maxlen=500),
            'motor_current': deque(maxlen=500),
            'temperature': deque(maxlen=500),
            'rssi': deque(maxlen=500),
            'cpu_temp': deque(maxlen=500),
            'free_heap': deque(maxlen=500),
            'distance': deque(maxlen=500),
            'quantum_entropy': deque(maxlen=500),
            'quantum_coherence': deque(maxlen=500)
        }
        
        self.warning_thresholds = {
            'battery_voltage': {'low': 3.3, 'critical': 3.0},
            'temperature': {'high': 60.0, 'critical': 70.0},
            'motor_current': {'high': 1.5, 'critical': 2.0},
            'rssi': {'weak': -80, 'critical': -90}
        }
        
        self.plot_colors = {
            'battery_voltage': '#00ff00',
            'motor_current': '#ff4444',
            'temperature': '#ffaa00',
            'rssi': '#0088ff',
            'cpu_temp': '#ff8800',
            'free_heap': '#aa44ff',
            'distance': '#44ffaa',
            'quantum_entropy': '#ff44ff',
            'quantum_coherence': '#44ffff'
        }
        
        self.callbacks = []
        
    def setup_panel(self, parent_frame):
        """Setup telemetry visualization panel"""
        # Create notebook for different telemetry views
        self.telemetry_notebook = ttk.Notebook(parent_frame)
        self.telemetry_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Setup different telemetry tabs
        self._setup_live_plots_tab()
        self._setup_statistics_tab()
        self._setup_warnings_tab()
        self._setup_raw_data_tab()
        
    def _setup_live_plots_tab(self):
        """Setup live plotting tab"""
        live_frame = ttk.Frame(self.telemetry_notebook)
        self.telemetry_notebook.add(live_frame, text="📊 Live Plots")
        
        # Create matplotlib figure with subplots
        self.fig, self.axes = plt.subplots(2, 2, figsize=(12, 8))
        self.fig.patch.set_facecolor('#1a1a1a')
        self.fig.suptitle('Real-Time Telemetry', color='white', fontsize=14)
        
        # Configure subplots
        plot_configs = [
            ('Battery & Power', ['battery_voltage', 'motor_current']),
            ('Temperature', ['temperature', 'cpu_temp']),
            ('Communication', ['rssi', 'free_heap']),
            ('Quantum Properties', ['quantum_entropy', 'quantum_coherence'])
        ]
        
        self.plot_lines = {}
        
        for i, (title, metrics) in enumerate(plot_configs):
            ax = self.axes.flat[i]
            ax.set_facecolor('#0a0a0a')
            ax.set_title(title, color='white', fontsize=12)
            ax.tick_params(colors='white')
            ax.grid(True, alpha=0.3)
            
            for metric in metrics:
                line, = ax.plot([], [], color=self.plot_colors[metric], 
                              label=metric.replace('_', ' ').title(), 
                              linewidth=2, alpha=0.8)
                self.plot_lines[metric] = line
                
            ax.legend(facecolor='#2a2a2a', edgecolor='white', 
                     labelcolor='white', fontsize=8)
            
        # Embed in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, live_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Controls frame
        controls_frame = ttk.Frame(live_frame)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(controls_frame, text="Update Rate:").pack(side=tk.LEFT)
        self.update_rate_var = tk.StringVar(value="Fast")
        update_combo = ttk.Combobox(controls_frame, textvariable=self.update_rate_var,
                                   values=["Slow", "Medium", "Fast"], width=10)
        update_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(controls_frame, text="Clear Data", 
                  command=self.clear_telemetry_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Export Plot", 
                  command=self.export_plot).pack(side=tk.LEFT, padx=5)
        
    def _setup_statistics_tab(self):
        """Setup statistics display tab"""
        stats_frame = ttk.Frame(self.telemetry_notebook)
        self.telemetry_notebook.add(stats_frame, text="📈 Statistics")
        
        # Create treeview for statistics
        columns = ('Metric', 'Current', 'Min', 'Max', 'Average', 'Std Dev')
        self.stats_tree = ttk.Treeview(stats_frame, columns=columns, show='headings')
        
        for col in columns:
            self.stats_tree.heading(col, text=col)
            self.stats_tree.column(col, width=100)
            
        # Scrollbar
        stats_scrollbar = ttk.Scrollbar(stats_frame, orient=tk.VERTICAL, 
                                       command=self.stats_tree.yview)
        self.stats_tree.configure(yscrollcommand=stats_scrollbar.set)
        
        self.stats_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        stats_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def _setup_warnings_tab(self):
        """Setup warnings and alerts tab"""
        warnings_frame = ttk.Frame(self.telemetry_notebook)
        self.telemetry_notebook.add(warnings_frame, text="⚠️ Warnings")
        
        # Warning display area
        self.warnings_text = tk.Text(warnings_frame, height=15, bg='#1a1a1a', 
                                    fg='yellow', font=('Consolas', 10))
        warnings_scrollbar = ttk.Scrollbar(warnings_frame, orient=tk.VERTICAL,
                                          command=self.warnings_text.yview)
        self.warnings_text.configure(yscrollcommand=warnings_scrollbar.set)
        
        self.warnings_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        warnings_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Warning controls
        controls_frame = ttk.Frame(warnings_frame)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(controls_frame, text="Clear Warnings", 
                  command=self.clear_warnings).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Export Warnings", 
                  command=self.export_warnings).pack(side=tk.LEFT, padx=5)
        
    def _setup_raw_data_tab(self):
        """Setup raw data display tab"""
        raw_frame = ttk.Frame(self.telemetry_notebook)
        self.telemetry_notebook.add(raw_frame, text="📋 Raw Data")
        
        # Raw data display
        self.raw_data_text = tk.Text(raw_frame, height=20, bg='#1a1a1a', 
                                    fg='white', font=('Consolas', 9))
        raw_scrollbar = ttk.Scrollbar(raw_frame, orient=tk.VERTICAL,
                                     command=self.raw_data_text.yview)
        self.raw_data_text.configure(yscrollcommand=raw_scrollbar.set)
        
        self.raw_data_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        raw_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def update_telemetry(self, telemetry_data: Dict):
        """Update telemetry with new data point"""
        timestamp = time.time()
        
        # Store data
        self.telemetry_data['timestamps'].append(timestamp)
        
        for key, value in telemetry_data.items():
            if key in self.telemetry_data and value is not None:
                self.telemetry_data[key].append(float(value))
                
        # Update visualizations
        self._update_live_plots()
        self._update_statistics()
        self._check_warnings(telemetry_data)
        self._update_raw_data(telemetry_data)
        
    def _update_live_plots(self):
        """Update live plotting displays"""
        if len(self.telemetry_data['timestamps']) < 2:
            return
            
        # Convert timestamps to relative time
        times = list(self.telemetry_data['timestamps'])
        relative_times = [(t - times[0]) for t in times]
        
        # Update each plot line
        for metric, line in self.plot_lines.items():
            if len(self.telemetry_data[metric]) > 0:
                data = list(self.telemetry_data[metric])
                line.set_data(relative_times[-len(data):], data)
                
        # Update axes limits
        for ax in self.axes.flat:
            ax.relim()
            ax.autoscale_view()
            
        # Redraw
        self.canvas.draw_idle()
        
    def _update_statistics(self):
        """Update statistics display"""
        # Clear existing items
        for item in self.stats_tree.get_children():
            self.stats_tree.delete(item)
            
        # Calculate and display statistics
        for metric, data in self.telemetry_data.items():
            if metric != 'timestamps' and len(data) > 0:
                data_array = np.array(list(data))
                
                current = data_array[-1] if len(data_array) > 0 else 0
                min_val = np.min(data_array)
                max_val = np.max(data_array)
                avg_val = np.mean(data_array)
                std_val = np.std(data_array)
                
                self.stats_tree.insert('', 'end', values=(
                    metric.replace('_', ' ').title(),
                    f"{current:.2f}",
                    f"{min_val:.2f}",
                    f"{max_val:.2f}",
                    f"{avg_val:.2f}",
                    f"{std_val:.2f}"
                ))
                
    def _check_warnings(self, telemetry_data: Dict):
        """Check for warning conditions"""
        warnings = []
        timestamp = time.strftime("%H:%M:%S")
        
        for metric, value in telemetry_data.items():
            if metric in self.warning_thresholds and value is not None:
                thresholds = self.warning_thresholds[metric]
                
                if 'critical' in thresholds and value <= thresholds['critical']:
                    warnings.append(f"[{timestamp}] CRITICAL: {metric} = {value}")
                elif 'high' in thresholds and value >= thresholds['high']:
                    warnings.append(f"[{timestamp}] WARNING: {metric} high = {value}")
                elif 'low' in thresholds and value <= thresholds['low']:
                    warnings.append(f"[{timestamp}] WARNING: {metric} low = {value}")
                elif 'weak' in thresholds and value <= thresholds['weak']:
                    warnings.append(f"[{timestamp}] WARNING: {metric} weak = {value}")
                    
        # Display warnings
        for warning in warnings:
            self.warnings_text.insert(tk.END, warning + "\n")
            self.warnings_text.see(tk.END)
            
            # Trigger callbacks
            for callback in self.callbacks:
                callback(warning)
                
    def _update_raw_data(self, telemetry_data: Dict):
        """Update raw data display"""
        timestamp = time.strftime("%H:%M:%S.%f")[:-3]
        
        raw_line = f"[{timestamp}] "
        for key, value in telemetry_data.items():
            raw_line += f"{key}={value} "
            
        self.raw_data_text.insert(tk.END, raw_line + "\n")
        self.raw_data_text.see(tk.END)
        
        # Limit text length
        lines = self.raw_data_text.get(1.0, tk.END).split('\n')
        if len(lines) > 1000:
            self.raw_data_text.delete(1.0, f"{len(lines)-1000}.0")
            
    def add_warning_callback(self, callback: Callable):
        """Add callback for warning events"""
        self.callbacks.append(callback)
        
    def clear_telemetry_data(self):
        """Clear all telemetry data"""
        for data_list in self.telemetry_data.values():
            data_list.clear()
            
    def clear_warnings(self):
        """Clear warnings display"""
        self.warnings_text.delete(1.0, tk.END)
        
    def export_plot(self):
        """Export current plot as image"""
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf")]
        )
        if filename:
            self.fig.savefig(filename, facecolor='#1a1a1a', dpi=300)
            
    def export_warnings(self):
        """Export warnings to file"""
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        if filename:
            with open(filename, 'w') as f:
                f.write(self.warnings_text.get(1.0, tk.END))
