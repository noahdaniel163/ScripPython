import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime, timedelta
from ttkthemes import ThemedTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Hàm tính toán thời gian thức dậy hợp lý dựa trên chu kỳ REM
def calculate_wake_up_times(sleep_time):
    rem_cycle = 90  # 90 phút cho một chu kỳ REM
    sleep_time = datetime.strptime(sleep_time, "%H:%M")
    wake_up_times = []

    # Tính toán các thời gian thức dậy hợp lý
    for i in range(1, 8):  # 7 chu kỳ REM
        wake_up_time = sleep_time + timedelta(minutes=rem_cycle * i)
        wake_up_times.append(wake_up_time.strftime("%H:%M"))

    return wake_up_times

# Hàm xử lý khi nhấn nút "Tính toán"
def on_calculate():
    sleep_time = entry_sleep_time.get()
    try:
        wake_up_times = calculate_wake_up_times(sleep_time)
        result = "Thời gian thức dậy hợp lý:\n" + "\n".join(wake_up_times)
        messagebox.showinfo("Kết quả", result)
        display_chart(wake_up_times)
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập giờ ngủ theo định dạng HH:MM")

# Hàm hiển thị biểu đồ
def display_chart(wake_up_times):
    # Xóa biểu đồ hiện tại nếu có
    for widget in chart_frame.winfo_children():
        widget.destroy()

    # Tạo dữ liệu cho biểu đồ
    cycles = list(range(1, len(wake_up_times) + 1))
    times = [datetime.strptime(t, "%H:%M") for t in wake_up_times]
    times_in_minutes = [(t.hour * 60 + t.minute) for t in times]

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(cycles, times_in_minutes, marker='o', linestyle='-', color='b')

    ax.set_xlabel('Chu kỳ REM')
    ax.set_ylabel('Thời gian thức dậy (phút từ 00:00)')
    ax.set_title('Thời gian thức dậy hợp lý dựa trên chu kỳ REM')
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Tạo giao diện đồ họa
root = ThemedTk(theme="arc")  # Sử dụng theme "arc"
root.title("Tính Toán Thời Gian Thức Dậy Hợp Lý Dựa Theo Chu Kỳ REM")
root.geometry("600x400")

frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

label_sleep_time = ttk.Label(frame, text="Giờ đi ngủ (HH:MM):")
label_sleep_time.pack(pady=5)

entry_sleep_time = ttk.Entry(frame)
entry_sleep_time.pack(pady=5)

button_calculate = ttk.Button(frame, text="Tính toán", command=on_calculate)
button_calculate.pack(pady=10)

chart_frame = ttk.Frame(frame)
chart_frame.pack(fill=tk.BOTH, expand=True, pady=10)

root.mainloop()
