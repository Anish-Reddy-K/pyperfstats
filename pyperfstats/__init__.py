"""
PyPerfStats: A lightweight Python performance profiler
"""
from .profiler import PerfProfiler
from .visualize import (
    plot_cpu_usage,
    plot_memory_usage,
    plot_combined_metrics,
    plot_advanced_metrics,
    generate_html_report
)
from .live_monitor import monitor_process, monitor_script, LiveMonitor

__version__ = '0.1.0'