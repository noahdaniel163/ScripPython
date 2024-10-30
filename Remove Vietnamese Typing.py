import os
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
from unidecode import unidecode

# Thiết lập biến môi trường để khắc phục cảnh báo về QT_DEVICE_PIXEL_RATIO
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

class ExcelProcessor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Excel Vietnamese Diacritic Remover')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.btn_select_file = QPushButton('Chọn tệp Excel', self)
        self.btn_select_file.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.btn_select_file)

        self.btn_save_file = QPushButton('Lưu tệp Excel', self)
        self.btn_save_file.clicked.connect(self.save_file_dialog)
        self.btn_save_file.setEnabled(False)
        layout.addWidget(self.btn_save_file)

        self.setLayout(layout)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn tệp Excel", "", 
                                                  "Excel Files (*.xls *.xlsx);;All Files (*)", 
                                                  options=options)
        if file_path:
            self.file_path = file_path
            self.btn_save_file.setEnabled(True)

    def save_file_dialog(self):
        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self, "Lưu tệp Excel", "", 
                                                   "Excel Files (*.xlsx);;All Files (*)", 
                                                   options=options)
        if save_path:
            self.process_excel(self.file_path, save_path)
            QMessageBox.information(self, "Thành công", "Tệp đã được lưu thành công!")

    def process_excel(self, file_path, save_path):
        # Kiểm tra định dạng tệp
        if file_path.endswith('.xls'):
            df = pd.read_excel(file_path)
        else:  # .xlsx
            df = pd.read_excel(file_path, engine='openpyxl')

        # Loại bỏ dấu tiếng Việt trong từng ô dữ liệu
        df = df.applymap(lambda x: unidecode(str(x)) if isinstance(x, str) else x)

        # Lưu lại tệp Excel mới
        df.to_excel(save_path, index=False, engine='openpyxl')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ExcelProcessor()
    ex.show()
    sys.exit(app.exec_())
