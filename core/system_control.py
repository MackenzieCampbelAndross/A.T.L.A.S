import os, subprocess, psutil, pyautogui

def open_app(app_name):
    try:
        subprocess.Popen(app_name)
    except Exception:
        os.system(f"start {app_name}")

def system_stats():
    battery = psutil.sensors_battery()
    return f"Battery: {battery.percent}% | CPU: {psutil.cpu_percent()}%"
