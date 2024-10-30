import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
import librouteros as ros
import qrcode

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WireGuard VPN Setup")
        self.setGeometry(100, 100, 400, 300)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.public_key_label = QLabel("Public Key:")
        self.public_key_input = QLineEdit()
        layout.addWidget(self.public_key_label)
        layout.addWidget(self.public_key_input)

        self.private_key_label = QLabel("Private Key:")
        self.private_key_input = QLineEdit()
        layout.addWidget(self.private_key_label)
        layout.addWidget(self.private_key_input)

        self.wan_ip_label = QLabel("WAN IP:")
        self.wan_ip_input = QLineEdit()
        layout.addWidget(self.wan_ip_label)
        layout.addWidget(self.wan_ip_input)

        self.lan_ip_label = QLabel("LAN IP Range:")
        self.lan_ip_input = QLineEdit()
        layout.addWidget(self.lan_ip_label)
        layout.addWidget(self.lan_ip_input)

        self.ip_tunnel_label = QLabel("IP Tunnel:")
        self.ip_tunnel_input = QLineEdit()
        layout.addWidget(self.ip_tunnel_label)
        layout.addWidget(self.ip_tunnel_input)

        self.generate_qr_button = QPushButton("Generate QR Code")
        self.generate_qr_button.clicked.connect(self.generate_qr_code)
        layout.addWidget(self.generate_qr_button)

        self.setLayout(layout)

    def generate_qr_code(self):
        # Get input values
        public_key = self.public_key_input.text()
        private_key = self.private_key_input.text()
        wan_ip = self.wan_ip_input.text()
        lan_ip_range = self.lan_ip_input.text()
        ip_tunnel = self.ip_tunnel_input.text()

        # Generate WireGuard config
        wireguard_config = f"""
            [Interface]
            PrivateKey = {private_key}
            Address = {lan_ip_range}
            
            [Peer]
            PublicKey = {public_key}
            AllowedIPs = 0.0.0.0/0
            Endpoint = {wan_ip}
        """

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(wireguard_config)
        qr.make(fit=True)

        # Display QR code (you'll need to implement this)
        # For simplicity, we'll just print the wireguard_config
        print(wireguard_config)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
