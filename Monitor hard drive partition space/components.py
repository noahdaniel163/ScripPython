import tkinter as tk
from tkinter import ttk
from utils import get_disk_partitions, get_partition_usage

class DiskUsageTable(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.treeview = ttk.Treeview(self, columns=("Total", "Used", "Free", "Percent"))
        self.treeview.heading("#0", text="Device")
        self.treeview.heading("Total", text="Total")
        self.treeview.heading("Used", text="Used")
        self.treeview.heading("Free", text="Free")
        self.treeview.heading("Percent", text="Percent")

        partitions = get_disk_partitions()

        for partition in partitions:
            partition_usage = get_partition_usage(partition)
            self.treeview.insert("", "end", text=partition.device,
                                 values=(partition_usage.total, partition_usage.used,
                                         partition_usage.free, partition_usage.percent))

        self.treeview.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)
        scrollbar.pack(side="right", fill="y")
        self.treeview.configure(yscrollcommand=scrollbar.set)
