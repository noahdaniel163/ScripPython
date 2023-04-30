import os
import tkinter as tk

def shutdown():
    os.system("shutdown /s /t 15")

def cancel_shutdown():
    os.system("shutdown /a")

root = tk.Tk()
root.geometry("300x200")
root.title("Tự động tắt máy tính")
tk.Label(root, text="Nhấn nút để tắt máy tính sau 15 giây").pack(pady=20)
tk.Button(root, text="Tắt máy", command=shutdown).pack(pady=10)
tk.Button(root, text="Huỷ", command=cancel_shutdown).pack(pady=10)
root.mainloop()