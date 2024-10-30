import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import ThemedTk
import pandas as pd

def merge_csv_files():
    # Chọn các file CSV cần ghép
    files = filedialog.askopenfilenames(title="Chọn các file CSV cần ghép", filetypes=[("CSV files", "*.csv")])
    if not files:
        return

    # Ghép các file CSV
    combined_csv = pd.concat([pd.read_csv(f) for f in files])

    # Chọn vị trí lưu file ghép
    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if not save_path:
        return

    # Lưu file ghép dưới dạng file Excel (XLSX)
    combined_csv.to_excel(save_path, index=False)
    print("Đã ghép và lưu file thành công.")

def view_csv_files():
    # Chọn file CSV cần xem
    files = filedialog.askopenfilenames(title="Chọn các file CSV cần xem", filetypes=[("CSV files", "*.csv")])
    if not files:
        return

    # Hiển thị nội dung của các file CSV
    display_csv_files(files)

def display_csv_files(file_paths):
    # Đọc dữ liệu từ các file CSV và ghép chúng
    dfs = [pd.read_csv(file) for file in file_paths]
    combined_df = pd.concat(dfs)

    # Tạo cửa sổ mới để hiển thị dữ liệu
    view_window = tk.Toplevel(root)
    view_window.title("Xem nội dung file CSV đã ghép")
    view_window.geometry("800x600")

    # Tạo frame để chứa Treeview và Scrollbar
    frame = ttk.Frame(view_window)
    frame.pack(fill=tk.BOTH, expand=True)

    # Tạo Treeview để hiển thị dữ liệu
    tree = ttk.Treeview(frame)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Tạo Scrollbar dọc và liên kết với Treeview
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    vsb.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=vsb.set)

    # Tạo Scrollbar ngang và liên kết với Treeview
    hsb = ttk.Scrollbar(view_window, orient="horizontal", command=tree.xview)
    hsb.pack(side=tk.BOTTOM, fill=tk.X)
    tree.configure(xscrollcommand=hsb.set)

    # Thiết lập các cột cho Treeview
    tree["columns"] = list(combined_df.columns)
    tree["show"] = "headings"

    for column in combined_df.columns:
        tree.heading(column, text=column)
        tree.column(column, anchor=tk.CENTER)

    # Thêm dữ liệu vào Treeview
    for index, row in combined_df.iterrows():
        tree.insert("", tk.END, values=list(row))

    # Bind left and right arrow keys to scroll horizontally
    tree.bind("<Left>", lambda e: tree.xview_scroll(-1, "units"))
    tree.bind("<Right>", lambda e: tree.xview_scroll(1, "units"))

# Tạo giao diện
root = ThemedTk(theme="breeze")
root.title("Ghép và xem file CSV")
root.geometry("300x150")

merge_button = tk.Button(root, text="Ghép file CSV và lưu thành Excel", command=merge_csv_files)
merge_button.pack(pady=10)

view_button = tk.Button(root, text="Xem file CSV", command=view_csv_files)
view_button.pack(pady=10)

root.mainloop()
