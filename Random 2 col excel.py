import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import random
import time

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Chương trình quay thưởng")
root.geometry("800x500")
root.configure(bg="black")

# Biến toàn cục
candidates_a = []
candidates_b = []
winners = {"A": set(), "B": set()}  # Dùng Set để tránh trùng
running = False

# Tạo Canvas để hiển thị pháo hoa nhưng không che giao diện
canvas = tk.Canvas(root, bg="black", highlightthickness=0)
canvas.place(x=0, y=0, relwidth=1, relheight=1)
canvas.lower("all")  # Đưa canvas xuống dưới

# Hàm tải danh sách từ file Excel
def load_excel():
    global candidates_a, candidates_b
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    
    if file_path:
        try:
            df = pd.read_excel(file_path)
            candidates_a = set(df.iloc[:, 0].dropna().tolist())  # Dùng set để tránh trùng
            candidates_b = set(df.iloc[:, 1].dropna().tolist())
            winners["A"].clear()
            winners["B"].clear()
            messagebox.showinfo("Thành công", "Đã tải danh sách thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {e}")

# Hàm tạo pháo hoa
def create_firework():
    fireworks = []
    for _ in range(15):  # Tạo 15 tia sáng
        x, y = 400, 200  # Vị trí trung tâm pháo hoa
        dx, dy = random.randint(-8, 8), random.randint(-8, 8)  # Hướng bắn
        color = random.choice(["red", "yellow", "white", "blue", "purple", "orange"])
        particle = canvas.create_oval(x, y, x+6, y+6, fill=color, outline=color)
        fireworks.append((particle, dx, dy))

    animate_firework(fireworks)

def animate_firework(fireworks, step=0):
    if step > 20:  # Sau 20 bước thì xóa pháo hoa
        for particle, _, _ in fireworks:
            canvas.delete(particle)
        return

    for particle, dx, dy in fireworks:
        canvas.move(particle, dx, dy)  # Di chuyển từng hạt pháo hoa
    root.after(50, lambda: animate_firework(fireworks, step + 1))  # Tiếp tục animation

# Hàm quay thưởng (KHÔNG CHO TRÙNG)
def start_spin(category):
    global running

    if running:
        return

    candidates = candidates_a if category == "A" else candidates_b
    available_candidates = list(candidates - winners[category])  # Lọc người chưa trúng

    if not available_candidates:
        messagebox.showinfo("Lỗi", "Tất cả đã trúng thưởng!")
        return

    running = True

    for _ in range(30):  # Quay số ngẫu nhiên 30 lần
        random_name = random.choice(available_candidates)
        result_label.config(text=random_name, fg="white", font=("Arial", 40, "bold"))
        root.update()
        time.sleep(0.1)

    winner = random.choice(available_candidates)
    winners[category].add(winner)  # Lưu vào danh sách trúng thưởng

    # Hiển thị kết quả với hiệu ứng viền màu
    for _ in range(3):
        result_label.config(text=winner, fg="yellow", font=("Arial", 50, "bold"))
        result_frame.config(bg="gold")
        root.update()
        time.sleep(0.3)
        result_label.config(text=winner, fg="red", font=("Arial", 50, "bold"))
        result_frame.config(bg="red")
        root.update()
        time.sleep(0.3)

    result_frame.config(bg="goldenrod")  # Giữ khung viền sau khi chọn xong
    create_firework()  # Kích hoạt pháo hoa
    running = False

# Hàm lưu danh sách người trúng thưởng
def save_winners():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt")],
                                             title="Lưu danh sách trúng thưởng")
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("Danh sách trúng thưởng:\n\n")
            f.write("🔵 Nhóm A:\n" + "\n".join(winners["A"]) + "\n\n")
            f.write("🔴 Nhóm B:\n" + "\n".join(winners["B"]))
        messagebox.showinfo("Lưu thành công", f"Danh sách đã được lưu tại:\n{file_path}")

# Hàm hiển thị tổng kết danh sách trúng thưởng
def show_summary():
    summary_text = "🔵 Nhóm A:\n" + "\n".join(winners["A"]) + "\n\n🔴 Nhóm B:\n" + "\n".join(winners["B"])
    messagebox.showinfo("Tổng kết", summary_text)

# Thiết kế giao diện tối giản
frame_controls = tk.Frame(root, bg="black")
frame_controls.pack(side="left", fill="y", padx=5, pady=5)

frame_display = tk.Frame(root, bg="black")
frame_display.pack(side="right", expand=True, fill="both")

# Nút tải file
btn_load = tk.Button(frame_controls, text="📂", command=load_excel, font=("Arial", 12),
                     bg="#4CAF50", fg="white", padx=10, pady=5, width=2)
btn_load.pack(pady=3)

# Nút quay thưởng nhóm A
btn_spin_a = tk.Button(frame_controls, text="🔵", command=lambda: start_spin("A"), font=("Arial", 12),
                       bg="blue", fg="white", padx=10, pady=5, width=2)
btn_spin_a.pack(pady=3)

# Nút quay thưởng nhóm B
btn_spin_b = tk.Button(frame_controls, text="🔴", command=lambda: start_spin("B"), font=("Arial", 12),
                       bg="red", fg="white", padx=10, pady=5, width=2)
btn_spin_b.pack(pady=3)

# Nút tổng kết
btn_summary = tk.Button(frame_controls, text="📜", command=show_summary, font=("Arial", 12),
                        bg="gray", fg="white", padx=10, pady=5, width=2)
btn_summary.pack(pady=3)

# Nút lưu kết quả
btn_save = tk.Button(frame_controls, text="💾", command=save_winners, font=("Arial", 12),
                     bg="purple", fg="white", padx=10, pady=5, width=2)
btn_save.pack(pady=3)

# Khung hiển thị kết quả
result_frame = tk.Frame(frame_display, bg="goldenrod", bd=5, relief="ridge")
result_frame.pack(expand=True, fill="both", padx=20, pady=20)

# Khu vực hiển thị kết quả
result_label = tk.Label(result_frame, text="Đang chờ...", font=("Arial", 50, "bold"), bg="black", fg="white")
result_label.pack(expand=True, fill="both")

# Chạy ứng dụng
root.mainloop()
