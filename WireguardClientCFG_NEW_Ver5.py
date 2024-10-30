import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import ttkthemes
import subprocess

def generate_keys():
    try:
        client_privkey = subprocess.check_output(["wg", "genkey"]).strip().decode('utf-8')
        client_pubkey = subprocess.check_output(["wg", "pubkey"], input=client_privkey.encode()).strip().decode('utf-8')
        return client_privkey, client_pubkey
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Key generation failed: {e}")
        return None, None

def generate_config():
    listen_port = listen_port_entry.get().strip()
    cidr = cidr_entry.get().strip()
    allowed_ips = allowed_ips_entry.get().strip()
    endpoint = endpoint_entry.get().strip()
    dns = dns_entry.get().strip()
    client_pubkey = client_pubkey_entry.get().strip()
    server_pubkey = server_pubkey_entry.get().strip()
    client_privkey = client_privkey_entry.get().strip()
    preshared_key = preshared_key_entry.get().strip()
    persistent_keepalive = persistent_keepalive_entry.get().strip()

    if not client_privkey or not client_pubkey or not server_pubkey:
        messagebox.showerror("Error", "Client and Server keys are required.")
        return

    config = "[Interface]\n"
    config += f"PrivateKey = {client_privkey}\n"
    if listen_port:
        config += f"ListenPort = {listen_port}\n"
    config += f"Address = {cidr}\n"
    if dns:
        config += f"DNS = {dns}\n"

    config += "\n[Peer]\n"
    config += f"PublicKey = {server_pubkey}\n"
    if preshared_key:
        config += f"PresharedKey = {preshared_key}\n"
    config += f"AllowedIPs = {allowed_ips}\n"
    if endpoint:
        config += f"Endpoint = {endpoint}\n"
    if persistent_keepalive:
        config += f"PersistentKeepalive = {persistent_keepalive}\n"

    result_window = tk.Toplevel(root)
    result_window.title("WireGuard Config")
    result_window.geometry("800x600")

    result_text = tk.Text(result_window, height=30, width=100)
    result_text.pack(expand=True, fill='both')
    result_text.insert(tk.END, config)

    save_button = ttk.Button(result_window, text="Save Config", command=lambda: save_config(config))
    save_button.pack(pady=10)

def save_config(config):
    file_path = filedialog.asksaveasfilename(defaultextension=".conf", filetypes=[("Config files", "*.conf"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(config)
        messagebox.showinfo("Success", f"Configuration saved to {file_path}")

def generate_new_keys():
    client_privkey, client_pubkey = generate_keys()
    if client_privkey and client_pubkey:
        client_privkey_entry.delete(0, tk.END)
        client_privkey_entry.insert(0, client_privkey)
        client_pubkey_entry.delete(0, tk.END)
        client_pubkey_entry.insert(0, client_pubkey)

root = ttkthemes.ThemedTk(theme="arc")
root.title("WireGuard Config Generator")
root.geometry("1054x738")

row = 0
listen_port_label = ttk.Label(root, text="Listen Port:")
listen_port_label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
listen_port_entry = ttk.Entry(root, width=50)
listen_port_entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
row += 1

cidr_label = ttk.Label(root, text="CIDR:")
cidr_label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
cidr_entry = ttk.Entry(root, width=50)
cidr_entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
row += 1

allowed_ips_label = ttk.Label(root, text="Client Allowed IPs:")
allowed_ips_label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
allowed_ips_entry = ttk.Entry(root, width=50)
allowed_ips_entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
row += 1

endpoint_label = ttk.Label(root, text="Endpoint (Optional):")
endpoint_label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
endpoint_entry = ttk.Entry(root, width=50)
endpoint_entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
row += 1

dns_label = ttk.Label(root, text="DNS (Optional):")
dns_label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
dns_entry = ttk.Entry(root, width=50)
dns_entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
row += 1

client_pubkey_label = ttk.Label(root, text="Client Public Key:")
client_pubkey_label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
client_pubkey_entry = ttk.Entry(root, width=50)
client_pubkey_entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
row += 1

server_pubkey_label = ttk.Label(root, text="Server Public Key:")
server_pubkey_label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
server_pubkey_entry = ttk.Entry(root, width=50)
server_pubkey_entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
row += 1

client_privkey_label = ttk.Label(root, text="Client Private Key:")
client_privkey_label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
client_privkey_entry = ttk.Entry(root, width=50)
client_privkey_entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
row += 1

preshared_key_label = ttk.Label(root, text="Preshared Key:")
preshared_key_label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
preshared_key_entry = ttk.Entry(root, width=50)
preshared_key_entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
row += 1

persistent_keepalive_label = ttk.Label(root, text="Persistent Keepalive (Optional):")
persistent_keepalive_label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
persistent_keepalive_entry = ttk.Entry(root, width=50)
persistent_keepalive_entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
row += 1

row += 1
generate_button = ttk.Button(root, text="Generate Config", command=generate_config)
generate_button.grid(row=row, column=0, padx=5, pady=5, sticky="ew")

generate_keys_button = ttk.Button(root, text="Generate New Keys", command=generate_new_keys)
generate_keys_button.grid(row=row, column=1, padx=5, pady=5, sticky="ew")

root.mainloop()
