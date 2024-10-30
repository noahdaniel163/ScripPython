import tkinter as tk
from tkinter import filedialog
import os
import shutil
import time
def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

def organize_files():
    scan_path = folder_entry.get()
    for filename in os.listdir(scan_path):
        if filename.endswith(".pdf"):
            creation_time = os.path.getctime(os.path.join(scan_path, filename))
            year, month = time.localtime(creation_time)[:2]
            destination_folder = os.path.join(scan_path, f"{year}-{month:02}")
            os.makedirs(destination_folder, exist_ok=True)
            shutil.move(os.path.join(scan_path, filename), destination_folder)
    status_label.config(text="Tổ chức file hoàn tất.")

# Tạo cửa sổ chính
window = tk.Tk()
window.title("Tổ chức file PDF")

# Tạo các thành phần giao diện
folder_label = tk.Label(window, text="Thư mục quét:")
folder_entry = tk.Entry(window, width=50)
browse_button = tk.Button(window, text="Tìm", command=browse_folder)
organize_button = tk.Button(window, text="Tổ chức file", command=organize_files)
status_label = tk.Label(window, text="")

# Đặt vị trí các thành phần
folder_label.grid(row=0, column=0, padx=5, pady=5)
folder_entry.grid(row=0, column=1, padx=5, pady=5)
browse_button.grid(row=0, column=2, padx=5, pady=5)
organize_button.grid(row=1, column=1, padx=5, pady=5)
status_label.grid(row=2, column=1, padx=5, pady=5)

# Chạy ứng dụng
window.mainloop()