import tkinter as tk
from tkinter import filedialog, messagebox
import openpyxl
import os
import win32net
import win32netcon

def get_user_list():
    try:
        user_info = win32net.NetUserEnum(None, 2)
        users = [user['name'] for user in user_info[0]]
        return users
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve user list: {e}")
        return []

def share_folders():
    # Open Excel file
    excel_file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if not excel_file_path:
        return
    workbook = openpyxl.load_workbook(excel_file_path)
    sheet = workbook.active

    # Get list of users on the device
    users = get_user_list()
    if not users:
        return

    # Create GUI
    root = tk.Tk()
    root.title("Folder Sharing Tool")

    # Create user selection dropdown
    user_var = tk.StringVar(root)
    user_var.set(users[0])  # Set default user

    user_label = tk.Label(root, text="Select user:")
    user_label.pack()

    user_dropdown = tk.OptionMenu(root, user_var, *users)
    user_dropdown.pack()

    # Iterate over rows in Excel file
    result_message = ""
    for row in sheet.iter_rows(values_only=True):
        folder_path, share_name = row
        if not folder_path or not share_name:
            continue

        # Check if folder path exists
        if not os.path.exists(folder_path):
            result_message += f"Folder '{folder_path}' does not exist.\n"
            continue

        # Create shared folder
        try:
            win32net.NetShareAdd(None, 2, {
                'netname': share_name,
                'path': folder_path,
                'remark': f"Shared folder for {user_var.get()}",
                'permissions': win32netcon.ACCESS_ALL,
                'max_uses': -1,
                'current_uses': 0,
                'path_type': 0,
                'passwd': None
            })
            result_message += f"Folder '{folder_path}' shared as '{share_name}' for user '{user_var.get()}'\n"
        except Exception as e:
            result_message += f"Failed to share folder '{folder_path}': {e}\n"

    # Close Excel file
    workbook.close()

    # Display result message
    messagebox.showinfo("Sharing Result", result_message)

    # Start GUI main loop
    root.mainloop()

# Create GUI
root = tk.Tk()
root.title("Folder Sharing Tool")

# Create browse button
browse_button = tk.Button(root, text="Browse Excel File", command=share_folders)
browse_button.pack(pady=20)

# Create execute button
execute_button = tk.Button(root, text="Execute", command=share_folders)
execute_button.pack(pady=10)

# Start GUI main loop
root.mainloop()
