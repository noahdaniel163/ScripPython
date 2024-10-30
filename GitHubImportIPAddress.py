import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # For better styling
from github import Github
import base64
import requests

# Function to load data from the GitHub raw file and display in the text field
def load_from_github():
    try:
        # Fetch raw content from GitHub
        raw_url = "https://raw.githubusercontent.com/noahdaniel163/blank-text/refs/heads/main/AllowList"
        response = requests.get(raw_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            raw_content = response.text
            text_field.delete("1.0", tk.END)  # Clear the text field
            text_field.insert(tk.END, raw_content)  # Insert the current content into the text field
            messagebox.showinfo("Success", "Data refreshed successfully!")
        else:
            messagebox.showerror("Error", "Failed to load data from GitHub.")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to save content to GitHub
def save_to_github():
    try:
        # Get the content from the text field
        new_content = text_field.get("1.0", tk.END).strip()

        # Authenticate with the GitHub token
        g = Github(token)

        # Get the repository and file
        repo = g.get_repo(repo_name)
        file = repo.get_contents(file_path, ref="main")

        # Update the file on GitHub with the new content
        commit_message = "Updated AllowList with new content via GUI"
        repo.update_file(file.path, commit_message, new_content, file.sha, branch="main")

        # Show a success message
        messagebox.showinfo("Success", "File updated successfully on GitHub!")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to get the public IP address of the user
def get_public_ip():
    try:
        response = requests.get('https://httpbin.org/ip')
        ip_data = response.json()
        return ip_data['origin']
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch IP address: {str(e)}")
        return None

# Function to insert the public IP into the text field
def add_ip():
    public_ip = get_public_ip()
    if public_ip:
        text_field.insert(tk.END, f"{public_ip}\n")  # Insert only the IP address

# Function to clear the text field
def clear_content():
    text_field.delete("1.0", tk.END)

# Function to add new content based on user input
def add_content():
    # Create a new window (popup) for user input
    input_window = tk.Toplevel(root)
    input_window.title("Add New Content")
    input_window.configure(bg='#f2f2f2')

    # Label and entry field for user input
    label = ttk.Label(input_window, text="Enter new content:")
    label.pack(pady=5)

    user_input = ttk.Entry(input_window, width=50)
    user_input.pack(pady=5)

    # Function to insert the input content into the main text field
    def insert_content():
        new_content = user_input.get().strip()
        if new_content:
            text_field.insert(tk.END, "\n" + new_content)
        input_window.destroy()  # Close the input window after insertion

    # Button to confirm and insert content
    submit_button = ttk.Button(input_window, text="Add", command=insert_content)
    submit_button.pack(pady=5)

# GitHub details (replace with your actual details)
token = "ghp_CoNgcOhm3hiU44ExG8"  # Replace with your GitHub Personal Access Token
repo_name = "noahdaniel163/blank-text"  # Replace with your repository name
file_path = "AllowList"  # Replace with the path to your file in the repository

# Initialize the main window
root = tk.Tk()
root.title("GitHub File Editor")
root.geometry("600x500")
root.configure(bg='#e6f2f2')  # Light background color for the window

# Create a frame for the text area and buttons
frame = ttk.Frame(root, padding="10 10 10 10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Add a label
label = ttk.Label(frame, text="Edit AllowList File Content:", font=("Helvetica", 14))
label.grid(row=0, column=0, columnspan=4, pady=10)

# Add a text field for editing file content
text_field = tk.Text(frame, height=15, width=60, wrap='word', font=("Helvetica", 12))
text_field.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

# Add "Add IP" button (to append public IP to the content)
add_ip_button = ttk.Button(frame, text="Add IP", command=add_ip)
add_ip_button.grid(row=2, column=0, padx=10, pady=10, sticky=(tk.W))

# Add "Add" button (to append new content via user input)
add_button = ttk.Button(frame, text="Add", command=add_content)
add_button.grid(row=2, column=1, padx=10, pady=10)

# Add "Delete" button (to clear content)
delete_button = ttk.Button(frame, text="Delete", command=clear_content)
delete_button.grid(row=2, column=2, padx=10, pady=10)

# Add "Save" button (to update content on GitHub)
save_button = ttk.Button(frame, text="Save", command=save_to_github)
save_button.grid(row=2, column=3, padx=10, pady=10, sticky=(tk.E))

# Add "Refresh" button (to load the latest content from GitHub)
refresh_button = ttk.Button(frame, text="Refresh", command=load_from_github)
refresh_button.grid(row=2, column=4, padx=10, pady=10, sticky=(tk.E))

# Make the elements resize properly
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.columnconfigure(2, weight=1)
frame.columnconfigure(3, weight=1)
frame.rowconfigure(1, weight=1)

# Load content from GitHub at the start
load_from_github()

# Run the application
root.mainloop()
