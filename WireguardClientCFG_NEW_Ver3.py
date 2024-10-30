import tkinter as tk
from tkinter import ttk
import ttkthemes
import subprocess
import qrcode
from PIL import Image, ImageTk

def generate_keys():
    client_privkey = subprocess.check_output("wg genkey", shell=True).strip().decode('utf-8')
    client_pubkey = subprocess.check_output(f"echo {client_privkey} | wg pubkey", shell=True).strip().decode('utf-8')
    return client_privkey, client_pubkey

def generate_config():
    listen_port = listen_port_entry.get()
    cidr = cidr_entry.get()
    allowed_ips = allowed_ips_entry.get()
    endpoint = endpoint_entry.get()
    dns = dns_entry.get()
    client_pubkey = client_pubkey_entry.get()
    server_pubkey = server_pubkey_entry.get()
    client_privkey = client_privkey_entry.get()
    preshared_key = preshared_key_entry.get()
    persistent_keepalive = persistent_keepalive_entry.get()
    address = cidr

    # Tạo file cấu hình mẫu
    config = "[Interface]\n"
    config += f"PrivateKey = {client_privkey}\n"
    if listen_port:
        config += f"ListenPort = {listen_port}\n"
    config += f"Address = {address}\n"
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

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(config)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    # Resize QR code to 200x200
    img = img.resize((200, 200), Image.ANTIALIAS)

    # Display the result and QR code in a new window
    result_window = tk.Toplevel(root)
    result_window.title("WireGuard Config and QR Code")
    result_window.geometry("1054x738")

    result_text = tk.Text(result_window, height=30, width=100)
    result_text.pack(expand=True, fill='both')
    result_text.insert(tk.END, config)

    qr_frame = ttk.Frame(result_window)
    qr_frame.pack(pady=10)

    img = ImageTk.PhotoImage(img)
    qr_label = ttk.Label(qr_frame, image=img)
    qr_label.image = img  # Keep a reference to avoid garbage collection
    qr_label.pack()

def generate_new_keys():
    client_privkey, client_pubkey = generate_keys()
    client_privkey_entry.delete(0, tk.END)
    client_privkey_entry.insert(0, client_privkey)
    client_pubkey_entry.delete(0, tk.END)
    client_pubkey_entry.insert(0, client_pubkey)

root = ttkthemes.ThemedTk(theme="arc")
root.title("WireGuard Config Generator")
root.geometry("1054x738")

# Create input fields
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

# Create the "Generate Config" button
generate_button = ttk.Button(root, text="Generate Config", command=generate_config)
generate_button.grid(row=row, column=0, padx=5, pady=5, sticky="ew")

# Create the "Generate New Keys" button
generate_keys_button = ttk.Button(root, text="Generate New Keys", command=generate_new_keys)
generate_keys_button.grid(row=row, column=1, padx=5, pady=5, sticky="ew")

root.mainloop()
