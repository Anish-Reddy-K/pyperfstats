# PyPerfStats

A lightweight Python performance profiler that collects CPU, memory, and other system metrics while your script runs.

## Installation

```bash
pip install pyperfstats
```

## Features

- Simple and intuitive command-line interface
- Collects key system metrics:
  - CPU usage
  - Memory usage
  - Thread count
  - Open files and connections
  - Disk I/O activity
  - Network usage
  - Context switches
- Real-time monitoring with interactive terminal UI
  - Live graphs and statistics
  - Monitor any running process by PID
  - Launch and monitor scripts in real-time
- Exports performance data to CSV for custom analysis
- Built-in visualization tools:
  - Time-series charts for CPU usage
  - Time-series charts for memory usage
  - Combined charts for quick analysis
  - Advanced multi-metric dashboards
- Generates comprehensive HTML reports
- Profile running processes by PID or launch and profile new scripts
- Statistical analysis with min, max, mean, median, and percentiles

## Usage

### Profile a Python Script

```bash
# Basic profiling
pyperfstats profile your_script.py

# Customize output and sampling rate
pyperfstats profile your_script.py --output stats.csv --interval 0.5

# Pass arguments to your script
pyperfstats profile your_script.py --args "arg1,arg2"

# Generate visualization after profiling
pyperfstats profile your_script.py --visualize

# Generate comprehensive HTML report
pyperfstats profile your_script.py --report

# Live monitoring with terminal UI
pyperfstats profile your_script.py --live
```

### Profile an Existing Process

```bash
# Attach to an existing process by PID and save data to CSV
pyperfstats attach 1234

# Live monitoring of an existing process
pyperfstats attach 1234 --live
```

### Direct Live Monitoring

```bash
# Monitor a specific process with live terminal UI
pyperfstats live 1234

# Monitor the current Python process
pyperfstats live
```

### Visualize Performance Data

```bash
# Generate combined visualization
pyperfstats visualize stats.csv

# Generate specific visualization
pyperfstats visualize stats.csv --type cpu

# Save visualization to file
pyperfstats visualize stats.csv --output performance.png
```

### Generate HTML Report

```bash
# Generate comprehensive HTML report
pyperfstats report stats.csv
```

### View Statistics Summary

```bash
# View statistical summary of performance data
pyperfstats stats stats.csv
```

## Python API

You can also use PyPerfStats programmatically in your own Python code:

```python
from pyperfstats import PerfProfiler, plot_combined_metrics, monitor_process, generate_html_report

# Profile a script and save to CSV
profiler = PerfProfiler(output_file="stats.csv")
csv_file = profiler.profile_script("your_script.py")

# Visualize results
plot_combined_metrics(csv_file)

# Generate an HTML report
report_path = generate_html_report(csv_file)
print(f"Report generated at: {report_path}")

# Monitor a process in real-time
# This will open an interactive terminal UI
monitor_process(pid=1234)
```

## License

MIT