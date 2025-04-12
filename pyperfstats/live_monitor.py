"""
Live terminal-based monitoring for performance metrics.
"""
import os
import sys
import time
import psutil
import threading
import curses
from datetime import datetime


class LiveMonitor:
    """
    Terminal-based live performance monitor using curses.
    """
    
    def __init__(self, process=None, refresh_rate=1.0):
        """
        Initialize the live monitor.
        
        Args:
            process (psutil.Process, optional): Process to monitor. If None, will be set later.
            refresh_rate (float): UI refresh rate in seconds.
        """
        self.process = process
        self.refresh_rate = refresh_rate
        self.running = False
        self.history = {
            'cpu': [],
            'memory': [],
            'threads': []
        }
        self.max_history = 60  # Keep up to 60 data points (for scrolling graphs)
        self.start_time = None
    
    def _collect_metrics(self):
        """Collect performance metrics from the process."""
        if not self.process or not self.process.is_running():
            return None
            
        try:
            # Get basic metrics
            cpu = self.process.cpu_percent()
            mem = self.process.memory_info().rss / (1024 ** 2)  # MB
            num_threads = self.process.num_threads()
            
            # Get additional metrics if possible
            try:
                io_counters = self.process.io_counters()
                disk_read = io_counters.read_bytes / (1024 ** 2)
                disk_write = io_counters.write_bytes / (1024 ** 2)
            except (psutil.AccessDenied, psutil.ZombieProcess, AttributeError):
                disk_read = 0
                disk_write = 0
                
            try:
                open_files = len(self.process.open_files())
            except (psutil.AccessDenied, psutil.ZombieProcess):
                open_files = 0
                
            try:
                connections = len(self.process.connections())
            except (psutil.AccessDenied, psutil.ZombieProcess):
                connections = 0
                
            # Update history
            self.history['cpu'].append(cpu)
            if len(self.history['cpu']) > self.max_history:
                self.history['cpu'].pop(0)
                
            self.history['memory'].append(mem)
            if len(self.history['memory']) > self.max_history:
                self.history['memory'].pop(0)
                
            self.history['threads'].append(num_threads)
            if len(self.history['threads']) > self.max_history:
                self.history['threads'].pop(0)
                
            return {
                'cpu': cpu,
                'memory': mem,
                'threads': num_threads,
                'disk_read': disk_read,
                'disk_write': disk_write,
                'open_files': open_files,
                'connections': connections
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            return None
    
    def _draw_header(self, stdscr, term_width):
        """Draw the header with title and basic info."""
        title = "PyPerfStats Live Monitor"
        process_info = f"Process: {self.process.pid} ({self.process.name()})" if self.process else "No process"
        
        # Draw title
        stdscr.addstr(0, (term_width - len(title)) // 2, title, curses.A_BOLD)
        
        # Draw process info
        stdscr.addstr(1, 2, process_info)
        
        # Draw runtime
        if self.start_time:
            runtime = time.time() - self.start_time
            hours, remainder = divmod(runtime, 3600)
            minutes, seconds = divmod(remainder, 60)
            runtime_str = f"Runtime: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
            stdscr.addstr(1, term_width - len(runtime_str) - 2, runtime_str)
            
        # Draw separator
        stdscr.addstr(2, 0, "=" * term_width)
    
    def _draw_metrics(self, stdscr, metrics, row, term_width):
        """Draw the basic metrics as text."""
        if not metrics:
            stdscr.addstr(row, 2, "Process not available")
            return row + 1
            
        # Draw CPU, Memory, and Thread metrics
        cpu_str = f"CPU: {metrics['cpu']:.1f}%"
        mem_str = f"Memory: {metrics['memory']:.1f} MB"
        thread_str = f"Threads: {metrics['threads']}"
        
        stdscr.addstr(row, 2, cpu_str)
        stdscr.addstr(row, 25, mem_str)
        stdscr.addstr(row, 50, thread_str)
        
        # Draw IO metrics
        row += 1
        disk_read_str = f"Disk Read: {metrics['disk_read']:.2f} MB"
        disk_write_str = f"Disk Write: {metrics['disk_write']:.2f} MB"
        
        stdscr.addstr(row, 2, disk_read_str)
        stdscr.addstr(row, 30, disk_write_str)
        
        # Draw file and network metrics
        row += 1
        files_str = f"Open Files: {metrics['open_files']}"
        conn_str = f"Connections: {metrics['connections']}"
        
        stdscr.addstr(row, 2, files_str)
        stdscr.addstr(row, 30, conn_str)
        
        # Draw separator
        row += 1
        stdscr.addstr(row, 0, "-" * term_width)
        
        return row + 1
    
    def _draw_sparkline(self, stdscr, row, col, width, data, max_value=None, label="", color_pair=0):
        """Draw a simple sparkline (ASCII graph)."""
        if not data:
            return
            
        # Calculate the scale
        if max_value is None:
            max_value = max(data) if data else 1
        max_value = max(max_value, 1)  # Avoid division by zero
        
        # Draw the label
        stdscr.addstr(row, col, label)
        
        # Draw the sparkline
        bar_chars = "▁▂▃▄▅▆▇█"
        for i, value in enumerate(data):
            if i >= width - len(label) - 1:
                break
                
            # Calculate the bar height
            normalized = value / max_value
            bar_idx = min(int(normalized * (len(bar_chars) - 1)), len(bar_chars) - 1)
            
            # Draw the bar
            try:
                stdscr.addstr(row, col + len(label) + i, bar_chars[bar_idx], curses.color_pair(color_pair))
            except curses.error:
                # This can happen if we try to write to the bottom-right corner
                pass
    
    def _draw_graphs(self, stdscr, row, term_width):
        """Draw history graphs for CPU, Memory, and Threads."""
        # Calculate available space
        graph_width = term_width - 15
        
        # Draw CPU graph
        self._draw_sparkline(stdscr, row, 2, graph_width, self.history['cpu'], 100, "CPU: ", 1)
        row += 1
        
        # Draw Memory graph
        max_memory = max(self.history['memory']) if self.history['memory'] else 100
        self._draw_sparkline(stdscr, row, 2, graph_width, self.history['memory'], max_memory * 1.1, "MEM: ", 2)
        row += 1
        
        # Draw Threads graph
        max_threads = max(self.history['threads']) if self.history['threads'] else 10
        self._draw_sparkline(stdscr, row, 2, graph_width, self.history['threads'], max_threads * 1.2, "THR: ", 3)
        row += 1
        
        return row
    
    def _draw_footer(self, stdscr, row, term_width):
        """Draw the footer with instructions."""
        stdscr.addstr(row, 0, "=" * term_width)
        row += 1
        
        help_text = "Press 'q' to quit, 'p' to pause/resume"
        stdscr.addstr(row, (term_width - len(help_text)) // 2, help_text)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stdscr.addstr(row, term_width - len(timestamp) - 2, timestamp)
    
    def _curses_main(self, stdscr):
        """Main function for the curses UI."""
        # Set up colors
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_RED, -1)  # CPU
        curses.init_pair(2, curses.COLOR_GREEN, -1)  # Memory
        curses.init_pair(3, curses.COLOR_BLUE, -1)  # Threads
        
        # Hide cursor
        curses.curs_set(0)
        
        # Set timeout for getch() to enable non-blocking input
        stdscr.timeout(int(self.refresh_rate * 1000))
        
        # Record start time
        self.start_time = time.time()
        paused = False
        
        # Main loop
        while self.running:
            # Get terminal dimensions
            term_height, term_width = stdscr.getmaxyx()
            
            # Clear the screen
            stdscr.clear()
            
            # Draw the header
            self._draw_header(stdscr, term_width)
            
            # Draw the metrics
            row = 3
            if not paused:
                metrics = self._collect_metrics()
                row = self._draw_metrics(stdscr, metrics, row, term_width)
            else:
                stdscr.addstr(row, 2, "MONITORING PAUSED", curses.A_BOLD)
                row += 2
            
            # Draw the graphs
            row = self._draw_graphs(stdscr, row + 1, term_width)
            
            # Draw the footer
            self._draw_footer(stdscr, term_height - 2, term_width)
            
            # Refresh the screen
            stdscr.refresh()
            
            # Process input
            try:
                key = stdscr.getch()
                if key == ord('q'):
                    self.running = False
                elif key == ord('p'):
                    paused = not paused
            except KeyboardInterrupt:
                self.running = False
    
    def start(self, pid=None):
        """
        Start the live monitor.
        
        Args:
            pid (int, optional): Process ID to monitor. If None, uses the current process.
        """
        if pid is not None:
            try:
                self.process = psutil.Process(pid)
            except psutil.NoSuchProcess:
                print(f"No process found with PID {pid}")
                return
        elif self.process is None:
            # Monitor the current process if none specified
            self.process = psutil.Process()
        
        self.running = True
        
        try:
            # Start the curses UI
            curses.wrapper(self._curses_main)
        except KeyboardInterrupt:
            self.running = False
        finally:
            # Cleanup
            print("Live monitoring stopped.")


def monitor_process(pid=None, refresh_rate=1.0):
    """
    Start monitoring a process with a live terminal UI.
    
    Args:
        pid (int, optional): Process ID to monitor. If None, uses the current process.
        refresh_rate (float): UI refresh rate in seconds.
    """
    monitor = LiveMonitor(refresh_rate=refresh_rate)
    monitor.start(pid)


def monitor_script(script_path, script_args=None, refresh_rate=1.0):
    """
    Run and monitor a Python script with a live terminal UI.
    
    Args:
        script_path (str): Path to the Python script.
        script_args (list, optional): Arguments to pass to the script.
        refresh_rate (float): UI refresh rate in seconds.
    """
    import subprocess
    import threading
    
    # Prepare the command
    cmd = [sys.executable, script_path]
    if script_args:
        cmd.extend(script_args)
    
    # Start the process
    process = subprocess.Popen(cmd)
    
    # Give it a moment to initialize
    time.sleep(0.5)
    
    # Create and start the monitor
    monitor = LiveMonitor(refresh_rate=refresh_rate)
    monitor_thread = threading.Thread(target=monitor.start, args=(process.pid,))
    monitor_thread.daemon = True
    monitor_thread.start()
    
    try:
        # Wait for the process to complete
        process.wait()
    except KeyboardInterrupt:
        # Try to terminate the process gracefully
        process.terminate()
    finally:
        # Wait for monitor to clean up
        monitor.running = False
        monitor_thread.join(timeout=2)