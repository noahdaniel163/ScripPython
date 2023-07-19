import tkinter as tk
import random

def generate_filenames(num_files):
    filenames = []
    for _ in range(num_files):
        random_number = random.randint(100000000000000, 999999999999999)
        filename = f"IMG_{random_number}"
        filenames.append(filename)
    return filenames

def save_filenames(filenames):
    file_path = "E:/Name_Rand.txt"
    with open(file_path, "w") as file:
        for filename in filenames:
            file.write(filename + "\n")

def generate_and_save_files():
    num_files = int(entry.get())
    filenames = generate_filenames(num_files)
    save_filenames(filenames)
    tk.messagebox.showinfo("Success", f"{num_files} filenames have been saved to E:/Name_Rand.txt.")

# Tạo cửa sổ Tkinter
window = tk.Tk()
window.title("Generate Files")

# Tạo nhãn và hộp văn bản để nhập số lượng tên file
label = tk.Label(window, text="Enter the number of filenames:")
label.pack()
entry = tk.Entry(window)
entry.pack()

# Tạo nút "Generate Files"
button = tk.Button(window, text="Generate Files", command=generate_and_save_files)
button.pack()

# Chạy giao diện đồ hoạ
window.mainloop()
