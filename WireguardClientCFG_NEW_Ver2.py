import tkinter as tk
from tkinter import ttk
import ttkthemes

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
    address = cidr  # Sử dụng giá trị CIDR làm Address

    # Tạo file cấu hình mẫu
    config = "[Interface]\n"
    config += f"PrivateKey = {client_privkey}\n"
    config += f"ListenPort = {listen_port}\n"
    config += f"Address = {address}\n"
    if dns:
        config += f"DNS = {dns}\n"

    config += "\n[Peer]\n"
    config += f"PublicKey = {server_pubkey}\n"
    config += f"PresharedKey = {preshared_key}\n"
    config += f"AllowedIPs = {allowed_ips}\n"
    if endpoint:
        config += f"Endpoint = {endpoint}\n"
    config += "PersistentKeepalive = 9000\n"

    # Hiển thị kết quả trong cửa sổ mới
    result_window = tk.Toplevel(root)
    result_window.title("WireGuard Config")
    result_window.geometry("1054x738")

    result_text = tk.Text(result_window, height=30, width=100)
    result_text.pack(expand=True, fill='both')
    result_text.insert(tk.END, config)

root = ttkthemes.ThemedTk(theme="arc")
root.title("WireGuard Config Generator")
root.geometry("1054x738")

# Tạo các trường nhập liệu
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

# Tạo nút "Generate Config"
generate_button = ttk.Button(root, text="Generate Config", command=generate_config)
generate_button.grid(row=row, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()