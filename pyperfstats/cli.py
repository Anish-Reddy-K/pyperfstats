"""
Command-line interface for the pyperfstats package.
"""
import os
import sys
import click
import webbrowser
from .profiler import PerfProfiler
from .visualize import (
    plot_cpu_usage,
    plot_memory_usage,
    plot_combined_metrics,
    plot_advanced_metrics,
    generate_html_report
)
from .live_monitor import monitor_process, monitor_script


@click.group()
def cli():
    """PyPerfStats: A lightweight Python performance profiler."""
    pass


@cli.command()
@click.argument('script_path', type=click.Path(exists=True))
@click.option('--output', '-o', help='Output CSV file path')
@click.option('--interval', '-i', type=float, default=1.0, help='Sampling interval in seconds')
@click.option('--args', help='Arguments to pass to the script (comma separated)')
@click.option('--visualize/--no-visualize', default=False, help='Open visualization after profiling')
@click.option('--report/--no-report', default=False, help='Generate HTML report after profiling')
@click.option('--live', is_flag=True, help='Show live monitoring UI instead of saving to CSV')
def profile(script_path, output, interval, args, visualize, report, live):
    """Profile a Python script and collect performance metrics."""
    script_args = args.split(',') if args else None
    
    if live:
        # Use the live monitor
        try:
            click.echo(f"Starting live monitoring for script: {script_path}")
            monitor_script(script_path, script_args, refresh_rate=interval)
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)
    else:
        # Use the CSV file profiler
        profiler = PerfProfiler(output_file=output)
        try:
            csv_file = profiler.profile_script(script_path, script_args, interval)
            click.echo(f"Performance data saved to: {csv_file}")
            
            if report:
                report_path = generate_html_report(csv_file)
                click.echo(f"HTML report generated: {report_path}")
                if visualize:
                    webbrowser.open(f"file://{os.path.abspath(report_path)}")
            elif visualize:
                # Open quick visualization
                plot_combined_metrics(csv_file)
                
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)


@cli.command()
@click.argument('pid', type=int)
@click.option('--output', '-o', help='Output CSV file path')
@click.option('--interval', '-i', type=float, default=1.0, help='Sampling interval in seconds')
@click.option('--live', is_flag=True, help='Show live monitoring UI instead of saving to CSV')
def attach(pid, output, interval, live):
    """Attach to an existing process and profile it by PID."""
    if live:
        try:
            click.echo(f"Starting live monitoring for process {pid}...")
            monitor_process(pid, refresh_rate=interval)
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)
    else:
        profiler = PerfProfiler(output_file=output)
        try:
            csv_file = profiler.profile_process(pid, interval)
            click.echo(f"Performance data saved to: {csv_file}")
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)


@cli.command()
@click.argument('csv_file', type=click.Path(exists=True))
@click.option('--output', '-o', help='Output image file path')
@click.option('--type', '-t', 
              type=click.Choice(['cpu', 'memory', 'combined', 'advanced']), 
              default='combined', 
              help='Type of visualization to generate')
@click.option('--show/--no-show', default=True, help='Whether to display the plot')
def visualize(csv_file, output, type, show):
    """Generate visualizations from performance data."""
    try:
        if type == 'cpu':
            plot_cpu_usage(csv_file, output, show)
        elif type == 'memory':
            plot_memory_usage(csv_file, output, show)
        elif type == 'advanced':
            plot_advanced_metrics(csv_file, output, show)
        else:  # combined
            plot_combined_metrics(csv_file, output, show)
            
        if output:
            click.echo(f"Visualization saved to: {output}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('csv_file', type=click.Path(exists=True))
@click.option('--output-dir', '-o', help='Output directory for the report')
@click.option('--open/--no-open', default=True, help='Open the report in a web browser')
def report(csv_file, output_dir, open):
    """Generate a comprehensive HTML report from performance data."""
    try:
        report_path = generate_html_report(csv_file, output_dir)
        click.echo(f"HTML report generated: {report_path}")
        
        if open:
            webbrowser.open(f"file://{os.path.abspath(report_path)}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('csv_file', type=click.Path(exists=True))
def stats(csv_file):
    """Print statistical summary of performance data."""
    try:
        profiler = PerfProfiler(output_file=csv_file)
        summary = profiler.generate_stats_summary()
        
        # Print a nicely formatted summary
        click.echo("\nPerformance Statistics Summary:")
        click.echo("=" * 80)
        
        for metric, values in summary.items():
            click.echo(f"\n{metric}:")
            click.echo("-" * 40)
            for stat, value in values.items():
                click.echo(f"  {stat.ljust(10)}: {value:.2f}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('pid', type=int, required=False)
@click.option('--refresh-rate', '-r', type=float, default=1.0, help='UI refresh rate in seconds')
def live(pid, refresh_rate):
    """
    Live terminal-based monitoring of a process.
    If PID is not provided, monitors the current Python process.
    """
    try:
        monitor_process(pid, refresh_rate)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()