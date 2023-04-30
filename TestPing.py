import subprocess
import time
import tkinter as tk
def ping_ip():
    try:
        ping_result = subprocess.check_output(['ping', '-n', '1', '-w', '500', ip_entry.get()])
        result_label.config(text=ping_result.decode('utf-8'))
    except subprocess.TimeoutExpired:
        result_label.config(text="Request timed out")
    # update result label every 2 seconds
    result_label.after(2000, ping_ip)


#create the GUI window
window = tk.Tk()
window.title("Ping Utility")
#create input label and entry
ip_label = tk.Label(window, text="IP address:")
ip_entry = tk.Entry(window)
ip_label.grid(row=0, column=0)
ip_entry.grid(row=0, column=1)
#create ping button and ping result label
ping_button = tk.Button(window, text="Ping", command=ping_ip)
result_label = tk.Label(window)
ping_button.grid(row=1, column=0)
result_label.grid(row=1, column=1)
#start the main event loop
window.mainloop()

