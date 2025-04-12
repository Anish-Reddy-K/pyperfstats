"""
Core profiling functionality for collecting system metrics from Python processes.
"""
import os
import csv
import time
import psutil
import subprocess
import threading
from datetime import datetime


class PerfProfiler:
    """Performance profiler for Python applications."""
    
    def __init__(self, output_file=None):
        """
        Initialize the performance profiler.
        
        Args:
            output_file (str, optional): Path to output CSV file.
                                        If None, generates a default filename.
        """
        self.output_file = output_file or f"perfstats_{time.strftime('%Y%m%d_%H%M%S')}.csv"
        self.process = None
        self.monitoring = False
        self.monitor_thread = None
        
    def _initialize_log_file(self):
        """Initialize the CSV log file with headers."""
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(self.output_file)), exist_ok=True)
        
        with open(self.output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp", 
                "cpu_percent", 
                "memory_mb", 
                "num_threads", 
                "open_files", 
                "connections",
                "disk_read_mb",
                "disk_write_mb",
                "network_sent_mb",
                "network_recv_mb",
                "ctx_switches"
            ])
    
    def _get_process_metrics(self):
        """Get current process metrics."""
        metrics = {}
        
        try:
            # Get basic performance metrics
            metrics["cpu"] = self.process.cpu_percent()
            metrics["mem"] = self.process.memory_info().rss / (1024 ** 2)  # RAM usage in MB
            metrics["num_threads"] = self.process.num_threads()
            
            # Get open files count (handle permission errors)
            try:
                metrics["open_files"] = len(self.process.open_files())
            except (psutil.AccessDenied, psutil.ZombieProcess):
                metrics["open_files"] = 0
                
            # Get network connection count (handle permission errors)
            try:
                metrics["connections"] = len(self.process.connections())
            except (psutil.AccessDenied, psutil.ZombieProcess):
                metrics["connections"] = 0
            
            # Get disk I/O metrics
            try:
                io_counters = self.process.io_counters()
                metrics["disk_read_mb"] = io_counters.read_bytes / (1024 ** 2)
                metrics["disk_write_mb"] = io_counters.write_bytes / (1024 ** 2)
            except (psutil.AccessDenied, psutil.ZombieProcess, AttributeError):
                metrics["disk_read_mb"] = 0
                metrics["disk_write_mb"] = 0
            
            # Get network metrics
            metrics["network_sent_mb"] = 0
            metrics["network_recv_mb"] = 0
            
            # Get context switch info
            try:
                ctx_info = self.process.num_ctx_switches()
                metrics["ctx_switches"] = ctx_info.voluntary + ctx_info.involuntary
            except (psutil.AccessDenied, psutil.ZombieProcess, AttributeError):
                metrics["ctx_switches"] = 0
                
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            print(f"Error getting process metrics: {e}")
            return None
            
        return metrics
            
    def _monitor_process(self, interval=1.0):
        """
        Monitor the process and record metrics.
        
        Args:
            interval (float): Monitoring interval in seconds.
        """
        self._initialize_log_file()
        
        try:
            while self.monitoring and self.process and self.process.is_running():
                # Get current timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                metrics = self._get_process_metrics()
                if not metrics:
                    break
                
                # Log to file
                with open(self.output_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        timestamp,
                        f"{metrics['cpu']:.2f}",
                        f"{metrics['mem']:.2f}",
                        metrics['num_threads'],
                        metrics['open_files'],
                        metrics['connections'],
                        f"{metrics['disk_read_mb']:.2f}",
                        f"{metrics['disk_write_mb']:.2f}",
                        f"{metrics['network_sent_mb']:.2f}",
                        f"{metrics['network_recv_mb']:.2f}",
                        metrics['ctx_switches']
                    ])
                
                # Print to console (simplified output)
                print(f"[PERF] {timestamp} | CPU: {metrics['cpu']:.2f}% | RAM: {metrics['mem']:.2f} MB | Threads: {metrics['num_threads']}")
                
                time.sleep(interval)
        
        finally:
            self.monitoring = False
    
    def profile_script(self, script_path, script_args=None, interval=1.0):
        """
        Profile the execution of a Python script.
        
        Args:
            script_path (str): Path to the Python script to profile.
            script_args (list, optional): Arguments to pass to the script.
            interval (float): Monitoring interval in seconds.
        
        Returns:
            str: Path to the output CSV file.
        """
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Script file not found: {script_path}")
        
        # Prepare the command to run the script
        cmd = ['python', script_path]
        if script_args:
            cmd.extend(script_args)
        
        # Start the process
        process = subprocess.Popen(cmd)
        self.process = psutil.Process(process.pid)
        self.monitoring = True
        
        # Monitor in a separate thread
        self.monitor_thread = threading.Thread(target=self._monitor_process, args=(interval,))
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        # Wait for the process to complete
        process.wait()
        
        # Wait for monitoring to complete
        if self.monitor_thread.is_alive():
            self.monitoring = False
            self.monitor_thread.join(timeout=5)
        
        return self.output_file
    
    def profile_process(self, pid, interval=1.0):
        """
        Profile an existing process by its PID.
        
        Args:
            pid (int): Process ID to profile.
            interval (float): Monitoring interval in seconds.
            
        Returns:
            str: Path to the output CSV file.
        """
        try:
            self.process = psutil.Process(pid)
            self.monitoring = True
            
            # Monitor in the current thread (blocking)
            self._monitor_process(interval)
            
        except psutil.NoSuchProcess:
            raise ValueError(f"No process found with PID {pid}")
            
        return self.output_file
    
    def generate_stats_summary(self):
        """
        Generate a statistical summary of the collected performance data.
        
        Returns:
            dict: Summary statistics for each metric.
        """
        import pandas as pd
        
        if not os.path.exists(self.output_file):
            raise FileNotFoundError(f"No data file found at {self.output_file}")
            
        df = pd.read_csv(self.output_file)
        
        # Calculate statistics for numeric columns
        summary = {}
        for col in df.columns:
            if col == 'timestamp':
                continue
                
            try:
                numeric_data = pd.to_numeric(df[col])
                summary[col] = {
                    'min': numeric_data.min(),
                    'max': numeric_data.max(),
                    'mean': numeric_data.mean(),
                    'median': numeric_data.median(),
                    'p95': numeric_data.quantile(0.95),
                    'p99': numeric_data.quantile(0.99)
                }
            except:
                pass
                
        return summary