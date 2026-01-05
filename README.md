# PyPerfStats

[![PyPI Downloads](https://static.pepy.tech/personalized-badge/pyperfstats?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/pyperfstats)

**Lightweight Python Performance Profiler**  
📊 Real-time metrics · 💻 Interactive terminal UI · 📈 Visual reports · 🧠 Built-in analysis

[![PyPI version](https://img.shields.io/pypi/v/pyperfstats.svg)](https://pypi.org/project/pyperfstats/)
[![License](https://img.shields.io/github/license/anish-reddy-k/pyperfstats.svg)](LICENSE)
[![Buy Me a Coffee](https://img.shields.io/badge/☕-Buy%20me%20a%20coffee-orange)](https://www.buymeacoffee.com/anishreddyk)

---
## Demo Video

👉 **Watch the 1-minute demo video:**  
[<img width="1842" alt="Screenshot 2025-04-12 at 11 50 35 PM" src="https://github.com/user-attachments/assets/f2d2c043-a76a-4916-9194-2047651333f6" />](https://youtu.be/7bUqttXzHgI?si=Ecu7TBdqbtr3ZoDE)

---
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

---
## 🔧 Installation

```bash
pip install pyperfstats
````
---

## **Quick Start**

### **📂 Profile a Python Script**

```
pyperfstats profile your_script.py
```
Profiles a script with default settings and outputs a live summary.

<img width="728" alt="Screenshot 2025-04-12 at 11 51 22 PM" src="https://github.com/user-attachments/assets/2e327e77-2959-4dac-ad51-9d734c07bb0c" />

---

### **📺 Live Monitoring (Terminal UI)**

```
pyperfstats profile your_script.py --live
```

Displays an interactive terminal UI while the script runs.

<img width="1350" alt="Screenshot 2025-04-12 at 11 51 53 PM" src="https://github.com/user-attachments/assets/5f6983ff-0474-41c5-9f79-76db201d5a6d" />

---

### **📄 Export to CSV**

```
pyperfstats profile your_script.py --output stats.csv
```

Saves performance metrics to a CSV file for later analysis.

<img width="1067" alt="Screenshot 2025-04-13 at 12 03 33 AM" src="https://github.com/user-attachments/assets/6acb2a3f-3ea0-4aaa-bef1-7c6242866edb" />

---

### **📈 Visualize Performance**

```
pyperfstats visualize stats.csv
```

Generates time-series plots (CPU, memory, etc.) from CSV data.

<img width="818" alt="Screenshot 2025-04-12 at 11 52 16 PM" src="https://github.com/user-attachments/assets/46c50be8-f324-428b-a146-1dfa10788d56" />

---

### **🌐 Generate HTML Report**

```
pyperfstats report stats.csv
```

Creates a full HTML dashboard with graphs and stats summary.

<img width="1069" alt="Screenshot 2025-04-12 at 11 52 49 PM" src="https://github.com/user-attachments/assets/795e63d2-7f8f-43d9-99d6-5aca133f8c30" />

---

## **🔍 All Features & CLI Options**

Each feature is fully modular and can be combined or used standalone.

---

### **🔹 Basic Profiling**

```
pyperfstats profile your_script.py
```

Run and profile a Python script.

---

### **🔹 Set Sampling Rate**

```
pyperfstats profile your_script.py --interval 0.5
```

Control how frequently stats are collected (in seconds).

---

### **🔹 Save CSV Output**

```
pyperfstats profile your_script.py --output stats.csv
```

  

---

### **🔹 Pass Arguments to Script**

```
pyperfstats profile your_script.py --args "arg1,arg2"
```

  

---

### **🔹 Live Dashboard While Running**

```
pyperfstats profile your_script.py --live
```

  

---

### **🔹 Automatically Visualize After Run**

```
pyperfstats profile your_script.py --visualize
```

  

---

### **🔹 Automatically Generate Report**

```
pyperfstats profile your_script.py --report
```

  

---

### **🔹 Attach to Running Process**

```
pyperfstats attach <PID>
```

Collect stats from any running process.

---

### **🔹 Attach + Live View**

```
pyperfstats attach <PID> --live
```

---

### **🔹 Monitor by PID (Live Only)**

```
pyperfstats live <PID>
```

---

### **🔹 Monitor Current Python Process**
```
pyperfstats live
```

---

### **🔹 Visualize CSV**
```
pyperfstats visualize stats.csv
```

---

### **🔹 Visualize Specific Metric**
```
pyperfstats visualize stats.csv --type cpu
```

---

### **🔹 Save Visualization to File**
```
pyperfstats visualize stats.csv --output perf_chart.png
```

---

### **🔹 Generate HTML Report**
```
pyperfstats report stats.csv
```

---
### **🔹 View Stats Summary**

```
pyperfstats stats stats.csv
```
Shows min/max/avg/median/percentiles for each metric.

---
## **🐍 Python API**

Use programmatically in your scripts:

```
from pyperfstats import PerfProfiler, plot_combined_metrics, monitor_process, generate_html_report

# Profile and save to CSV
profiler = PerfProfiler(output_file="stats.csv")
profiler.profile_script("your_script.py")

# Visualize results
plot_combined_metrics("stats.csv")

# Generate report
generate_html_report("stats.csv")

# Real-time monitor (terminal UI)
monitor_process(pid=1234)
```

---
## **📊 Example Use Case**

> After optimizing using PyPerfStats, I reduced server resource usage by ~50%.

> Now I can serve 2× more users with the same infrastructure.

<img width="2108" alt="Screenshot 2025-04-12 at 11 34 49 PM" src="https://github.com/user-attachments/assets/9b51451a-03cc-4aa4-9345-6ab55bfe36b5" />


---

## **❤️ Support the Project**
If you find PyPerfStats useful, consider supporting it:
☕ [Buy Me a Coffee](https://buymeacoffee.com/anishreddyk)

---
## **📄 License**
MIT License © [Anish Reddy]

---

## **🔗 Related Projects**
- [psutil](https://github.com/giampaolo/psutil)
- [matplotlib](https://matplotlib.org/)
- [rich](https://github.com/Textualize/rich)
