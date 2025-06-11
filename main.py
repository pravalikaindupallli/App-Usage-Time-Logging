import time
import csv
import psutil
import pygetwindow as gw
import pywinauto
from datetime import datetime
from pynput import keyboard

def get_active_window_title():
    try:
        active_window = gw.getActiveWindow()
        if active_window:
            return active_window.title
        
        
    except:
        return None

def get_active_process_name(window_title):
    try:
        app = pywinauto.Application().connect(title=window_title)
        pid = app.process
        return psutil.Process(pid).name()
    except:
        return "Unknown"

def log_app_usage(log_file='app_usage_log.csv', interval=5):
    current_app = None
    start_time = None

    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['App Name', 'Window Title', 'Start Time', 'End Time'])

        while True:
            window_title = get_active_window_title()
            if window_title:
                app_name = get_active_process_name(window_title)
                if window_title != current_app:
                    if current_app is not None:
                        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        writer.writerow([previous_app_name, current_app, start_time, end_time])
                        file.flush()

                    current_app = window_title
                    previous_app_name = app_name
                    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            time.sleep(interval)

if __name__ == "__main__":
    log_app_usage()




stop_flag = False

def on_press(key):
    global stop_flag
    if key == keyboard.Key.esc:
        stop_flag = True
        print("Exit key pressed. Stopping logging...")

# Start listener in a separate thread
listener = keyboard.Listener(on_press=on_press)
listener.start()
