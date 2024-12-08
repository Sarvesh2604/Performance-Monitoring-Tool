import psutil
import time
import tkinter as tk
from tkinter import messagebox

# Function to get CPU usage
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

# Function to get memory usage
def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.percent, memory.used, memory.total

# Function to get disk usage
def get_disk_usage():
    disk = psutil.disk_usage('/')
    return disk.percent, disk.used, disk.total

# Function to get network usage
def get_network_usage():
    net_io = psutil.net_io_counters()
    return net_io.bytes_sent, net_io.bytes_recv

# Function to trigger alert
def alert(threshold, value, metric):
    if value > threshold:
        messagebox.showwarning("Alert", f"{metric} usage exceeded! Current: {value}%")

# GUI Update Function
def update_gui():
    cpu_usage = get_cpu_usage()
    memory_usage, memory_used, memory_total = get_memory_usage()
    disk_usage, disk_used, disk_total = get_disk_usage()
    network_sent, network_recv = get_network_usage()

    # Update labels with current stats
    cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
    memory_label.config(text=f"Memory Usage: {memory_usage}% ({memory_used}/{memory_total})")
    disk_label.config(text=f"Disk Usage: {disk_usage}% ({disk_used}/{disk_total})")
    network_label.config(text=f"Network - Sent: {network_sent} bytes, Received: {network_recv} bytes")

    # Check for thresholds and trigger alerts
    alert(thresholds['cpu'], cpu_usage, 'CPU')
    alert(thresholds['memory'], memory_usage, 'Memory')
    alert(thresholds['disk'], disk_usage, 'Disk')

    # Update every 5 seconds
    root.after(5000, update_gui)

# Initialize thresholds for alerts
thresholds = {
    'cpu': 80,     # Set CPU threshold to 80%
    'memory': 80,  # Set Memory threshold to 80%
    'disk': 90     # Set Disk threshold to 90%
}

# GUI Setup
root = tk.Tk()
root.title("System Monitor")

# Create and position labels
cpu_label = tk.Label(root, text="CPU Usage: ", font=("Arial", 14))
cpu_label.pack(pady=10)

memory_label = tk.Label(root, text="Memory Usage: ", font=("Arial", 14))
memory_label.pack(pady=10)

disk_label = tk.Label(root, text="Disk Usage: ", font=("Arial", 14))
disk_label.pack(pady=10)

network_label = tk.Label(root, text="Network Usage: ", font=("Arial", 14))
network_label.pack(pady=10)

# Start monitoring and updating GUI
update_gui()

# Run the Tkinter event loop
root.mainloop()
