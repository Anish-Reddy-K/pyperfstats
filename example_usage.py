"""
Example of how to use PyPerfStats programmatically
"""
from pyperfstats import PerfProfiler, plot_combined_metrics, generate_html_report

def profile_script_example():
    """Example of profiling a script"""
    # Initialize the profiler
    profiler = PerfProfiler(output_file="my_script_stats.csv")
    
    # Profile a script (replace with your script path)
    csv_file = profiler.profile_script("your_script.py")
    
    # Visualize the results
    plot_combined_metrics(csv_file)
    
    # Generate an HTML report
    report_path = generate_html_report(csv_file)
    print(f"Report generated at: {report_path}")

def profile_process_example():
    """Example of profiling an existing process"""
    # Get a process ID (this is just an example, replace with a real PID)
    pid = 1234  # Replace with an actual process ID
    
    # Initialize the profiler
    profiler = PerfProfiler(output_file="process_stats.csv")
    
    # Profile the process
    try:
        csv_file = profiler.profile_process(pid)
        # Generate a report
        report_path = generate_html_report(csv_file)
        print(f"Report generated at: {report_path}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Running script profiling example...")
    # Uncomment to run the example:
    # profile_script_example()
    
    print("\nProcess profiling example would go here...")
    # Uncomment to run the example (with a valid PID):
    # profile_process_example()