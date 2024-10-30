import os
import secrets
import ipaddress
import tkinter as tk
from tkinter import ttk, scrolledtext

def generate_client_config(server_public_key, server_ip, server_listen_port, client_private_key, client_public_key, client_ip, client_subnet_mask, client_port, client_dns, client_preshared_key):
    config = f"""[Interface]
PrivateKey = {client_private_key}
Address = {client_ip}/{client_subnet_mask}
DNS = {client_dns}
ListenPort = {client_port}

[Peer]
PublicKey = {server_public_key}
PresharedKey = {client_preshared_key}
AllowedIPs = 0.0.0.0/0
Endpoint = {server_ip}:{server_listen_port}
"""
    return config

def generate_server_config(server_private_key, server_public_key, server_ip, server_listen_port, client_public_key, client_ip, client_subnet_mask, client_port):
    config = f"""[Interface]
PrivateKey = {server_private_key}
Address = {server_ip}/24
ListenPort = {server_listen_port}

[Peer]
PublicKey = {client_public_key}
AllowedIPs = {client_ip}/{client_subnet_mask}
Endpoint = {client_ip}:{client_port}
"""
    return config

def generate_configs():
    server_ip = server_ip_entry.get()
    server_listen_port = server_port_entry.get()
    client_ip = client_ip_entry.get()
    client_subnet_mask = client_subnet_mask_entry.get()
    server_public_key = server_public_key_entry.get()
    client_public_key = client_public_key_entry.get()
    client_private_key = client_private_key_entry.get()
    client_port = client_listen_port_entry.get()
    client_dns = client_dns_entry.get()
    client_preshared_key = client_preshared_key_entry.get()

    client_config = generate_client_config(server_public_key, server_ip, server_listen_port, client_private_key, client_public_key, client_ip, client_subnet_mask, client_port, client_dns, client_preshared_key)
    server_config = generate_server_config(client_private_key, server_public_key, server_ip, server_listen_port, client_public_key, client_ip, client_subnet_mask, client_port)

    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "Client Configuration:\n\n" + client_config + "\n\nServer Configuration:\n\n" + server_config)

root = tk.Tk()
root.title("WireGuard Config Generator")
root.geometry("856x450")  # Đặt kích thước cửa sổ

# Server IP
server_ip_label = ttk.Label(root, text="Server IP:")
server_ip_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
server_ip_entry = ttk.Entry(root)
server_ip_entry.grid(row=0, column=1, padx=5, pady=5)

# Server Listen Port
server_port_label = ttk.Label(root, text="Server Listen Port:")
server_port_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
server_port_entry = ttk.Entry(root)
server_port_entry.grid(row=1, column=1, padx=5, pady=5)

# Client IP
client_ip_label = ttk.Label(root, text="Client IP:")
client_ip_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
client_ip_entry = ttk.Entry(root)
client_ip_entry.grid(row=2, column=1, padx=5, pady=5)

# Client Subnet Mask
client_subnet_mask_label = ttk.Label(root, text="Client Subnet Mask:")
client_subnet_mask_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
client_subnet_mask_entry = ttk.Entry(root)
client_subnet_mask_entry.grid(row=3, column=1, padx=5, pady=5)

# Server Public Key
server_public_key_label = ttk.Label(root, text="Server Public Key:")
server_public_key_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
server_public_key_entry = ttk.Entry(root)
server_public_key_entry.grid(row=4, column=1, padx=5, pady=5)

# Client Public Key
client_public_key_label = ttk.Label(root, text="Client Public Key:")
client_public_key_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
client_public_key_entry = ttk.Entry(root)
client_public_key_entry.grid(row=5, column=1, padx=5, pady=5)

# Client Private Key
client_private_key_label = ttk.Label(root, text="Client Private Key:")
client_private_key_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
client_private_key_entry = ttk.Entry(root)
client_private_key_entry.grid(row=6, column=1, padx=5, pady=5)

# Client Port
client_listen_port_label = ttk.Label(root, text="Client Port:")
client_listen_port_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
client_listen_port_entry = ttk.Entry(root)
client_listen_port_entry.grid(row=7, column=1, padx=5, pady=5)

# Client DNS
client_dns_label = ttk.Label(root, text="Client DNS:")
client_dns_label.grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)
client_dns_entry = ttk.Entry(root)
client_dns_entry.grid(row=8, column=1, padx=5, pady=5)

# Client PresharedKey
client_preshared_key_label = ttk.Label(root, text="Client PresharedKey:")
client_preshared_key_label.grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)
client_preshared_key_entry = ttk.Entry(root)
client_preshared_key_entry.grid(row=9, column=1, padx=5, pady=5)

# Generate Configs Button
generate_button = ttk.Button(root, text="Generate Configs", command=generate_configs)
generate_button.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

# Result Text Area
result_text = scrolledtext.ScrolledText(root, width=100, height=20)
result_text.grid(row=11, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()