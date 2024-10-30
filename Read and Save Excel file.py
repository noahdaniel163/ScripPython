import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog

class FileSelectorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Selector")
        self.setGeometry(100, 100, 400, 200)

        self.button_select_file = QPushButton("Chọn File", self)
        self.button_select_file.clicked.connect(self.select_file)
        self.button_select_file.setGeometry(100, 50, 200, 50)

        self.show()

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn File", "", "All Files (*);;Excel Files (*.xlsx)", options=options)
        if file_path:
            print(f"File đã chọn: {file_path}")

            save_path, _ = QFileDialog.getSaveFileName(self, "Chọn Vị Trí Lưu", "", "All Files (*);;Excel Files (*.xlsx)", options=options)
            if save_path:
                print(f"Vị trí lưu mới: {save_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileSelectorWindow()
    sys.exit(app.exec_())
