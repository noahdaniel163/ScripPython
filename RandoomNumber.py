import random
import tkinter as tk

class LotteryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lottery Number Generator")
        self.root.geometry("300x200")
        self.root.configure(bg="white")

        self.option = tk.StringVar()
        self.option.set("645")

        self.create_widgets()

    def create_widgets(self):
        tk.Radiobutton(self.root, text="6/45", variable=self.option, value="645", bg="white").pack()
        tk.Radiobutton(self.root, text="6/55", variable=self.option, value="655", bg="white").pack()
        tk.Button(self.root, text="Generate Numbers", command=self.generate_numbers, bg="white").pack()
        self.result_label = tk.Label(self.root, text="", bg="yellow", width=40, height=5)
        self.result_label.pack(pady=20)

    def generate_numbers(self):
        if self.option.get() == "645":
            numbers = sorted(random.sample(range(1, 46), 6), reverse=True)
        elif self.option.get() == "655":
            numbers = sorted(random.sample(range(1, 56), 6), reverse=True)
        self.result_label.config(text=', '.join(map(str, numbers)))

if __name__ == "__main__":
    root = tk.Tk()
    app = LotteryApp(root)
    root.mainloop()