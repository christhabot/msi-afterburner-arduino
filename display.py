import time
import serial
import os
import sys
import threading
import tkinter as tk
from pystray import Icon, MenuItem, Menu
from PIL import Image
from datetime import datetime

# Change these
total_ram = 16000
icon_path = r"your path to the .png file"




os.chdir(os.path.dirname(os.path.abspath(__file__)))

ser = serial.Serial('COM3', 9600)
time.sleep(2)

file_path = r"C:\Program Files (x86)\MSI Afterburner\HardwareMonitoring.hml"

def get_log_entry_from_file():
    if not os.path.exists(file_path):
        print(f"File does not exist: {file_path}")
        return None
    file_size = os.path.getsize(file_path)
    if file_size > 512 * 1024:  
        print(f"File exceeds 512 Kb, deleting {file_path}...")
        os.remove(file_path)
        return None
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if lines:
                return lines[-1].strip()  
            else:
                print("The file is empty.")
                return None
    except Exception as e:
        print(f"Error reading the log file: {e}")
        return None

def parse_log(log):
    values = log.split(',')[1:]  
    def safe_float(value):
        try:
            return float(value.strip())
        except ValueError:
            return 0.0  
    return {
        "gpu_temp": safe_float(values[1]),
        "gpu_usage": safe_float(values[2]),
        "memory_usage": safe_float(values[3]),
        "cpu_temp": safe_float(values[4]),
        "cpu_usage": safe_float(values[5]),
        "ram_usage": safe_float(values[6]),
        "fps": safe_float(values[7])  
    }

def get_gpu_temp():
    log_entry = get_log_entry_from_file()  
    if log_entry:
        data = parse_log(log_entry)
        return data["gpu_temp"]
    return None

def get_cpu_temp():
    log_entry = get_log_entry_from_file()  
    if log_entry:
        data = parse_log(log_entry)
        return data["cpu_temp"]
    return None

def get_gpu_usage():
    log_entry = get_log_entry_from_file()  
    if log_entry:
        data = parse_log(log_entry)
        return data["gpu_usage"]
    return None

def get_cpu_usage():
    log_entry = get_log_entry_from_file()  
    if log_entry:
        data = parse_log(log_entry)
        return data["cpu_usage"]
    return None

def get_ram_usage():
    log_entry = get_log_entry_from_file()  
    if log_entry:
        data = parse_log(log_entry)
        ram_usage_percentage = (data["ram_usage"] / total_ram) * 100
        if ram_usage_percentage >= 100:
            ram_usage_percentage = 99
        return ram_usage_percentage
    return None

def get_fps():
    log_entry = get_log_entry_from_file()  
    if log_entry:
        data = parse_log(log_entry)
        return data["fps"]
    return None

def get_system_stats():
    fps = get_fps() or 0
    gpu_temp = get_gpu_temp() or 0
    gpu_usage = get_gpu_usage() or 0
    cpu_temp = get_cpu_temp() or 0
    cpu_usage = get_cpu_usage() or 0
    ram_usage = get_ram_usage() or 0
    data = (
        f"G:{int(gpu_usage):3}% {int(gpu_temp):2}c "
        f"F:{int(fps):3}"
        f"C:{int(cpu_usage):3}% {int(cpu_temp):2}c "
        f"R:{int(ram_usage):2}%"
    )
    return data

def on_quit(icon, item):
    print("Exiting the program...")
    icon.stop()
    os._exit(0)

def monitor_system():
    counter = 0
    while True:
        system_data = get_system_stats()
        if system_data:
            ser.write(system_data.encode())
            ser.write(b'\n')
        counter += 1
        if counter >= 6000:
            get_log_entry_from_file()  
            counter = 0  
        time.sleep(0.1)

def setup_tray():
    image = Image.open(icon_path)  # Open icon image
    icon = Icon("System Monitor", image, menu=Menu(MenuItem('Exit', on_quit)))  # Exit stops the tray and quits the program
    icon.run()

def show_window():
    root = tk.Tk()
    root.title("Arduino monitoring")
    root.geometry("400x300")
    
    label = tk.Label(root, text="Sends system information to arduino")
    label.pack()
    
    def update_label():
        system_data = get_system_stats()
        label.config(text=system_data)
        root.after(1000, update_label)
    
    update_label()
    
    # Handling minimize and close actions
    def on_close():
        root.iconify()  # Minimize to tray
        root.withdraw()  # Hide window, still running in background

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

def open_window(icon, item):
    threading.Thread(target=show_window).start()

if __name__ == "__main__":
    tray_thread = threading.Thread(target=setup_tray)
    tray_thread.daemon = True
    tray_thread.start()

    monitor_thread = threading.Thread(target=monitor_system)
    monitor_thread.daemon = True
    monitor_thread.start()

    tray_thread.join()
    monitor_thread.join()
