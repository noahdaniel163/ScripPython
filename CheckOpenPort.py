import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QMessageBox
import socket

class PortChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Port Checker')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.input_label = QLabel('Enter IP Address or Domain:')
        layout.addWidget(self.input_label)
        self.input_edit = QLineEdit()
        layout.addWidget(self.input_edit)

        self.result_label = QLabel('')
        layout.addWidget(self.result_label)

        self.ip_label = QLabel('IP Address:')
        layout.addWidget(self.ip_label)
        self.ip_edit = QLineEdit()
        self.ip_edit.setReadOnly(True)
        layout.addWidget(self.ip_edit)

        self.port_label = QLabel('Port:')
        layout.addWidget(self.port_label)
        self.port_edit = QLineEdit()
        layout.addWidget(self.port_edit)

        self.protocol_label = QLabel('Protocol:')
        layout.addWidget(self.protocol_label)
        self.protocol_combo = QComboBox()
        self.protocol_combo.addItems(['TCP', 'UDP'])
        layout.addWidget(self.protocol_combo)

        self.check_button = QPushButton('Check')
        self.check_button.clicked.connect(self.check_port)
        layout.addWidget(self.check_button)

        self.setLayout(layout)

    def check_port(self):
        ip_or_domain = self.input_edit.text()
        try:
            ip = socket.gethostbyname(ip_or_domain)
            self.ip_edit.setText(ip)
        except socket.gaierror:
            QMessageBox.warning(self, 'Error', 'Invalid IP address or domain')
            return

        port = int(self.port_edit.text())
        protocol = socket.SOCK_STREAM if self.protocol_combo.currentText() == 'TCP' else socket.SOCK_DGRAM
        sock = socket.socket(socket.AF_INET, protocol)
        sock.settimeout(2)  # Timeout là 2 giây
        result = sock.connect_ex((ip, port))
        sock.close()

        if result == 0:
            QMessageBox.information(self, 'Result', f'<b>Port {port} is open</b>')
        else:
            QMessageBox.warning(self, 'Result', f'<b>Port {port} is closed</b>')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PortChecker()
    window.show()
    sys.exit(app.exec_())
