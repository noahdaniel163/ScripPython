import tkinter as tk
from tkinter import messagebox
import subprocess

def generate_wireguard_config(interface, ip, peer_public_key, peer_allowed_ips):
    config = f"""
[Interface]
Address = {ip}
PrivateKey = <private_key>

[Peer]
PublicKey = {peer_public_key}
AllowedIPs = {peer_allowed_ips}
"""

    return config

def generate_qr_code(text, output_file):
    subprocess.run(['qrencode', '-o', output_file, text])

def generate_config_and_qr():
    interface = interface_entry.get()
    ip = ip_entry.get()
    peer_public_key = peer_public_key_entry.get()
    peer_allowed_ips = peer_allowed_ips_entry.get()

    config = generate_wireguard_config(interface, ip, peer_public_key, peer_allowed_ips)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, config)

    qr_code_text = config.replace('\n', '\\n')
    generate_qr_code(qr_code_text, 'wireguard_qr.png')

    messagebox.showinfo("QR Code", "QR code generated successfully.")

# GUI setup
root = tk.Tk()
root.title("WireGuard Configuration Generator")

# Interface
interface_label = tk.Label(root, text="Interface:")
interface_label.pack()
interface_entry = tk.Entry(root)
interface_entry.pack()

# IP Address
ip_label = tk.Label(root, text="IP Address:")
ip_label.pack()
ip_entry = tk.Entry(root)
ip_entry.pack()

# Peer Public Key
peer_public_key_label = tk.Label(root, text="Peer Public Key:")
peer_public_key_label.pack()
peer_public_key_entry = tk.Entry(root)
peer_public_key_entry.pack()

# Peer Allowed IPs
peer_allowed_ips_label = tk.Label(root, text="Peer Allowed IPs:")
peer_allowed_ips_label.pack()
peer_allowed_ips_entry = tk.Entry(root)
peer_allowed_ips_entry.pack()

# Button to generate config and QR code
generate_button = tk.Button(root, text="Generate Config and QR Code", command=generate_config_and_qr)
generate_button.pack()

# Result text area
result_text = tk.Text(root, height=10, width=50)
result_text.pack()

root.mainloop()
