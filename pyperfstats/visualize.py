"""
Visualization utilities for performance data.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


def load_perfstats(csv_file):
    """
    Load performance statistics from a CSV file.
    
    Args:
        csv_file (str): Path to the CSV file.
        
    Returns:
        pandas.DataFrame: DataFrame containing the performance stats.
    """
    df = pd.read_csv(csv_file)
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Ensure numeric columns are properly typed
    numeric_cols = df.columns.difference(['timestamp'])
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    return df


def plot_metric(df, metric, title, color, ax=None, fill=True):
    """Utility function to plot a single metric."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))
    
    ax.plot(df['timestamp'], df[metric], color=color, linewidth=2)
    if fill:
        ax.fill_between(df['timestamp'], df[metric], alpha=0.2, color=color)
    
    ax.set_title(title)
    ax.set_ylabel(title)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Format x-axis to show time clearly
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    
    return ax


def plot_cpu_usage(csv_file, output_file=None, show=True):
    """
    Plot CPU usage over time.
    
    Args:
        csv_file (str): Path to the CSV file.
        output_file (str, optional): If provided, save the plot to this file.
        show (bool): Whether to display the plot.
    """
    df = load_perfstats(csv_file)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    plot_metric(df, 'cpu_percent', 'CPU Usage (%)', 'b', ax)
    
    plt.xlabel('Time')
    plt.gcf().autofmt_xdate()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_memory_usage(csv_file, output_file=None, show=True):
    """
    Plot memory usage over time.
    
    Args:
        csv_file (str): Path to the CSV file.
        output_file (str, optional): If provided, save the plot to this file.
        show (bool): Whether to display the plot.
    """
    df = load_perfstats(csv_file)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    plot_metric(df, 'memory_mb', 'Memory Usage (MB)', 'g', ax)
    
    plt.xlabel('Time')
    plt.gcf().autofmt_xdate()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_combined_metrics(csv_file, output_file=None, show=True):
    """
    Plot multiple metrics on separate subplots.
    
    Args:
        csv_file (str): Path to the CSV file.
        output_file (str, optional): If provided, save the plot to this file.
        show (bool): Whether to display the plot.
    """
    df = load_perfstats(csv_file)
    
    fig, axes = plt.subplots(2, 1, figsize=(10, 10), sharex=True)
    
    # CPU subplot
    plot_metric(df, 'cpu_percent', 'CPU Usage (%)', 'b', axes[0])
    
    # Memory subplot
    plot_metric(df, 'memory_mb', 'Memory Usage (MB)', 'g', axes[1])
    axes[1].set_xlabel('Time')
    
    # Format x-axis to show time clearly
    axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    fig.autofmt_xdate()
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_advanced_metrics(csv_file, output_file=None, show=True):
    """
    Plot advanced metrics including disk and network I/O.
    
    Args:
        csv_file (str): Path to the CSV file.
        output_file (str, optional): If provided, save the plot to this file.
        show (bool): Whether to display the plot.
    """
    df = load_perfstats(csv_file)
    
    fig, axes = plt.subplots(4, 1, figsize=(10, 16), sharex=True)
    
    # CPU subplot
    plot_metric(df, 'cpu_percent', 'CPU Usage (%)', 'b', axes[0])
    
    # Memory subplot
    plot_metric(df, 'memory_mb', 'Memory Usage (MB)', 'g', axes[1])
    
    # Disk I/O subplot
    axes[2].plot(df['timestamp'], df['disk_read_mb'], 'r-', linewidth=2, label='Read')
    axes[2].plot(df['timestamp'], df['disk_write_mb'], 'b-', linewidth=2, label='Write')
    axes[2].set_title('Disk I/O Over Time')
    axes[2].set_ylabel('MB')
    axes[2].grid(True, linestyle='--', alpha=0.7)
    axes[2].legend()
    
    # Thread count subplot
    plot_metric(df, 'num_threads', 'Thread Count', 'purple', axes[3], fill=False)
    axes[3].set_xlabel('Time')
    
    # Format x-axis to show time clearly
    axes[3].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    fig.autofmt_xdate()
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    else:
        plt.close()


def generate_html_report(csv_file, output_dir=None):
    """
    Generate a complete HTML report with all visualizations.
    
    Args:
        csv_file (str): Path to the CSV file.
        output_dir (str, optional): Directory to save the report and images.
            If None, uses the same directory as the CSV file.
            
    Returns:
        str: Path to the generated HTML report.
    """
    import base64
    from io import BytesIO
    
    # Set up output directory
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(csv_file)) or '.'
    os.makedirs(output_dir, exist_ok=True)
    
    # Load data and calculate statistics
    df = load_perfstats(csv_file)
    
    # Calculate summary statistics
    stats = {}
    for col in df.columns:
        if col == 'timestamp':
            continue
        try:
            numeric_data = pd.to_numeric(df[col])
            stats[col] = {
                'min': f"{numeric_data.min():.2f}",
                'max': f"{numeric_data.max():.2f}",
                'mean': f"{numeric_data.mean():.2f}",
                'median': f"{numeric_data.median():.2f}",
                'p95': f"{numeric_data.quantile(0.95):.2f}",
                'p99': f"{numeric_data.quantile(0.99):.2f}"
            }
        except:
            pass
    
    # Generate plots and convert to base64 for embedding in HTML
    plot_images = {}
    
    # CPU plot
    plt.figure(figsize=(10, 5))
    plot_metric(df, 'cpu_percent', 'CPU Usage (%)', 'b')
    plt.xlabel('Time')
    plt.gcf().autofmt_xdate()
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    plot_images['cpu'] = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    # Memory plot
    plt.figure(figsize=(10, 5))
    plot_metric(df, 'memory_mb', 'Memory Usage (MB)', 'g')
    plt.xlabel('Time')
    plt.gcf().autofmt_xdate()
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    plot_images['memory'] = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    # Thread count plot
    plt.figure(figsize=(10, 5))
    plot_metric(df, 'num_threads', 'Thread Count', 'purple', fill=False)
    plt.xlabel('Time')
    plt.gcf().autofmt_xdate()
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    plot_images['threads'] = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    # Build HTML report
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>PyPerfStats Report - {os.path.basename(csv_file)}</title>
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{ 
                max-width: 1200px; 
                margin: 0 auto; 
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            h1, h2, h3 {{ color: #333; }}
            .section {{ margin-bottom: 30px; }}
            .plot-img {{ 
                width: 100%; 
                max-width: 1000px; 
                height: auto; 
                margin: 10px 0;
                border: 1px solid #ddd;
                border-radius: 4px;
            }}
            table {{ 
                border-collapse: collapse; 
                width: 100%; 
                margin: 20px 0;
            }}
            th, td {{ 
                border: 1px solid #ddd; 
                padding: 8px; 
                text-align: right;
            }}
            th {{ 
                background-color: #f2f2f2; 
                text-align: center;
            }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>PyPerfStats Performance Report</h1>
            <div class="section">
                <h2>Summary</h2>
                <p>File analyzed: {os.path.basename(csv_file)}</p>
                <p>Data points: {len(df)}</p>
                <p>Time range: {df['timestamp'].min().strftime('%Y-%m-%d %H:%M:%S')} to {df['timestamp'].max().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="section">
                <h2>Statistics Summary</h2>
                <table>
                    <tr>
                        <th>Metric</th>
                        <th>Min</th>
                        <th>Max</th>
                        <th>Mean</th>
                        <th>Median</th>
                        <th>95th %ile</th>
                        <th>99th %ile</th>
                    </tr>
    """
    
    # Add rows for each metric in the statistics table
    for metric, values in stats.items():
        html += f"""
                    <tr>
                        <td>{metric}</td>
                        <td>{values['min']}</td>
                        <td>{values['max']}</td>
                        <td>{values['mean']}</td>
                        <td>{values['median']}</td>
                        <td>{values['p95']}</td>
                        <td>{values['p99']}</td>
                    </tr>
        """
    
    html += """
                </table>
            </div>
    """
    
    # Add CPU section
    html += f"""
            <div class="section">
                <h2>CPU Usage</h2>
                <img src="data:image/png;base64,{plot_images['cpu']}" class="plot-img" alt="CPU Usage">
            </div>
    """
    
    # Add Memory section
    html += f"""
            <div class="section">
                <h2>Memory Usage</h2>
                <img src="data:image/png;base64,{plot_images['memory']}" class="plot-img" alt="Memory Usage">
            </div>
    """
    
    # Add Thread Count section
    html += f"""
            <div class="section">
                <h2>Thread Count</h2>
                <img src="data:image/png;base64,{plot_images['threads']}" class="plot-img" alt="Thread Count">
            </div>
    """
    
    # Close HTML
    html += """
        </div>
    </body>
    </html>
    """
    
    # Write HTML to file
    report_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(csv_file))[0]}_report.html")
    with open(report_path, 'w') as f:
        f.write(html)
    
    return report_path