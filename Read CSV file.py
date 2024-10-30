import tkinter as tk
from tkinter import filedialog, scrolledtext
import pandas as pd

def open_files():
    filepaths = filedialog.askopenfilenames(
        title="Open CSV Files",
        initialdir="/",
        filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
    )
    
    if filepaths:
        read_and_display_files(filepaths)

def read_and_display_files(filepaths):
    text_box.delete('1.0', tk.END)  # Clear the text box

    for filepath in filepaths:
        try:
            df = pd.read_csv(filepath)
            text_box.insert(tk.END, f"File: {filepath}\n\n")
            text_box.insert(tk.END, df.to_string(index=False))
            text_box.insert(tk.END, "\n\n")
        except Exception as e:
            text_box.insert(tk.END, f"Error reading file {filepath}: {str(e)}\n\n")

root = tk.Tk()
root.title("CSV File Reader")

open_button = tk.Button(root, text="Open CSV Files", command=open_files)
open_button.pack(pady=10)

text_box = scrolledtext.ScrolledText(root, width=80, height=20)
text_box.pack()

root.mainloop()