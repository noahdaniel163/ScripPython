import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QHeaderView
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt

import pandas as pd
import sqlite3

class Dictionary(QMainWindow):
    def __init__(self):
        super().__init__()
        self.abbreviations = ()
        self.abbreviations_table = None
        # Add this line to initialize the "tab_widget" attribute
        self.tab_widget = QTabWidget()

        # Thiết lập giao diện người dùng cho tab "Từ điển"
        self.init_dictionary_ui()

        # Khởi tạo cơ sở dữ liệu SQLite
        self.init_database()

        # Load dữ liệu vào bảng từ điển
        self.dictionary_load_data()
        self.abbreviation_load_data()
        # Thiết lập giao diện người dùng cho tab "Từ viết tắt"
        self.init_abbreviations_ui()

        # Add this line to set the central widget
        self.setCentralWidget(self.tab_widget)


    def init_database(self):
        # Kết nối tới cơ sở dữ liệu
        self.conn = sqlite3.connect('dictionary.db')

        # Tạo bảng từ điển nếu chưa có
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS dictionary
            (id INTEGER PRIMARY KEY,
            word TEXT UNIQUE,
            definition TEXT);
        ''')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS abbreviation
            (id INTEGER PRIMARY KEY,
            abbreviation TEXT UNIQUE,
            full_form TEXT,
            definition TEXT);
        ''')



    def dictionary_load_data(self):
        # Lấy tất cả các từ trong bảng và hiển thị trên bảng từ điển
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM dictionary ORDER BY word ASC')
        results = cursor.fetchall()
        self.dictionary_table.setRowCount(0)
        for row_number, row_data in enumerate(results):
            self.dictionary_table.insertRow(row_number)
            self.dictionary_table.setItem(row_number, 0, QTableWidgetItem(row_data[1]))
            self.dictionary_table.setItem(row_number, 1, QTableWidgetItem(row_data[2]))


    def abbreviation_load_data(self):

        # Lấy tất cả các từ trong bảng và hiển thị trên bảng từ điển
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM abbreviation ORDER BY abbreviation ASC')
        results = cursor.fetchall()
        if self.abbreviations_table is None:
           self.abbreviations_table = QTableWidget()
        self.abbreviations_table.setRowCount(0)
        for row_number, row_data in enumerate(results):
            self.abbreviations_table.insertRow(row_number)
            self.abbreviations_table.setItem(row_number, 0, QTableWidgetItem(row_data[1]))
            self.abbreviations_table.setItem(row_number, 1, QTableWidgetItem(row_data[2]))
            self.abbreviations_table.setItem(row_number, 2, QTableWidgetItem(row_data[3]))

    def init_dictionary_ui(self):
        # Thiết lập giao diện cho tab "Từ điển"
        dictionary_tab = QWidget()
        self.tab_widget.addTab(dictionary_tab, "Từ điển")
        self.setFixedSize(1000, 600)
        dictionary_layout = QVBoxLayout()

        # Khởi tạo các widget
        self.dictionary_search_label = QLabel('Tìm kiếm:')
        self.dictionary_search_box = QLineEdit()
        self.dictionary_search_box.returnPressed.connect(self.search_word)
        self.dictionary_search_button = QPushButton('Tìm kiếm')
        self.dictionary_search_button.clicked.connect(self.search_word)

        self.dictionary_add_label = QLabel('Thêm từ:')
        self.dictionary_add_word_box = QLineEdit()
        self.dictionary_add_definition_box = QLineEdit()
        self.dictionary_add_button = QPushButton('Thêm từ')
        self.dictionary_add_word_box.returnPressed.connect(self.dictionary_add_definition_box.setFocus) 
        self.dictionary_add_definition_box.returnPressed.connect(self.add_word) 
        self.dictionary_add_button.clicked.connect(self.add_word)

        self.dictionary_delete_label = QLabel('Xoá từ:')
        self.dictionary_delete_box = QLineEdit()
        self.dictionary_delete_button = QPushButton('Xoá từ')
        self.dictionary_delete_button.clicked.connect(self.delete_word)

        self.dictionary_modify_label = QLabel('Sửa từ:')
        self.dictionary_modify_word_box = QLineEdit()
        self.dictionary_modify_definition_box = QLineEdit()
        self.dictionary_modify_button = QPushButton('Sửa từ')
        self.dictionary_modify_button.clicked.connect(self.modify_word)

        self.dictionary_table = QTableWidget()
        self.dictionary_table.setColumnCount(2)
        self.dictionary_table.setHorizontalHeaderLabels(['Từ', 'Định nghĩa'])
        self.dictionary_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.dictionary_table.setColumnWidth(0, 210) 
        self.dictionary_table.setColumnWidth(1, 690)

        # Thêm các widget vào layout
        dictionary_search_layout = QHBoxLayout()
        dictionary_search_layout.addWidget(self.dictionary_search_label)
        dictionary_search_layout.addWidget(self.dictionary_search_box)
        dictionary_search_layout.addWidget(self.dictionary_search_button)

        dictionary_add_layout = QHBoxLayout()
        dictionary_add_layout.addWidget(self.dictionary_add_label)
        dictionary_add_layout.addWidget(self.dictionary_add_word_box)
        dictionary_add_layout.addWidget(self.dictionary_add_definition_box)
        dictionary_add_layout.addWidget(self.dictionary_add_button)

        dictionary_delete_layout = QHBoxLayout()
        dictionary_delete_layout.addWidget(self.dictionary_delete_label)
        dictionary_delete_layout.addWidget(self.dictionary_delete_box)
        dictionary_delete_layout.addWidget(self.dictionary_delete_button)
        
        dictionary_modify_layout = QHBoxLayout()
        dictionary_modify_layout.addWidget(self.dictionary_modify_label)
        dictionary_modify_layout.addWidget(self.dictionary_modify_word_box)
        dictionary_modify_layout.addWidget(self.dictionary_modify_definition_box)
        dictionary_modify_layout.addWidget(self.dictionary_modify_button)

        dictionary_layout.addLayout(dictionary_search_layout)
        dictionary_layout.addLayout(dictionary_add_layout)
        dictionary_layout.addLayout(dictionary_delete_layout)
        dictionary_layout.addLayout(dictionary_modify_layout)
        dictionary_layout.addWidget(self.dictionary_table)
        dictionary_tab.setLayout(dictionary_layout)

    def init_abbreviations_ui(self):

        # Thiết lập giao diện cho tab "Từ điển"
        abbreviations_tab = QWidget()
        self.tab_widget.addTab(abbreviations_tab, "Từ viết tắt")
        
        self.setFixedSize(1000, 600)
        abbreviations_layout = QVBoxLayout()

        # Khởi tạo các widget
        self.abbreviations_search_label = QLabel('Tìm kiếm:')
        self.abbreviations_search_box = QLineEdit()
        self.abbreviations_search_box.returnPressed.connect(self.search_abbreviation)
        self.abbreviations_search_button = QPushButton('Tìm kiếm')
        self.abbreviations_search_button.clicked.connect(self.search_abbreviation)

        self.abbreviations_add_label = QLabel('Thêm từ:')
        self.abbreviations_add_abbreviation_box = QLineEdit()
        self.abbreviations_add_abbreviation_box.setFixedWidth(100)
        self.abbreviations_add_full_form_box = QLineEdit()
        self.abbreviations_add_full_form_box.setFixedWidth(340)
        self.abbreviations_add_definition_box = QLineEdit()
        self.abbreviations_add_definition_box.setFixedWidth(340)
        self.abbreviations_add_button = QPushButton('Thêm từ')
        self.abbreviations_add_button.clicked.connect(self.add_abbreviation)

        self.abbreviations_delete_label = QLabel('Xoá từ:')
        self.abbreviations_delete_box = QLineEdit()
        self.abbreviations_delete_button = QPushButton('Xoá từ')
        self.abbreviations_delete_button.clicked.connect(self.delete_abbreviation)


        self.abbreviations_table = QTableWidget()
        self.abbreviations_table.setColumnCount(3)
        self.abbreviations_table.setHorizontalHeaderLabels(['Từ','Từ đầy đủ', 'Định nghĩa'])
        self.abbreviations_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.abbreviations_table.setColumnWidth(0, 90) 
        self.abbreviations_table.setColumnWidth(1, 420)
        self.abbreviations_table.setColumnWidth(2, 420)


        # Thêm các widget vào layout
        abbreviations_search_layout = QHBoxLayout()
        abbreviations_search_layout.addWidget(self.abbreviations_search_label)
        abbreviations_search_layout.addWidget(self.abbreviations_search_box)
        abbreviations_search_layout.addWidget(self.abbreviations_search_button)
        abbreviations_layout.addLayout(abbreviations_search_layout)



        abbreviations_add_layout = QHBoxLayout()
        abbreviations_add_layout.addWidget(self.abbreviations_add_label)
        abbreviations_add_layout.addWidget(self.abbreviations_add_abbreviation_box)
        abbreviations_add_layout.addWidget(self.abbreviations_add_full_form_box)
        abbreviations_add_layout.addWidget(self.abbreviations_add_definition_box)
        abbreviations_add_layout.addWidget(self.abbreviations_add_button)
        abbreviations_layout.addLayout(abbreviations_add_layout)


        abbreviations_delete_layout = QHBoxLayout()
        abbreviations_delete_layout.addWidget(self.abbreviations_delete_label)
        abbreviations_delete_layout.addWidget(self.abbreviations_delete_box)
        abbreviations_delete_layout.addWidget(self.abbreviations_delete_button)
        abbreviations_layout.addLayout(abbreviations_delete_layout)

        
        abbreviations_layout.addWidget(self.abbreviations_table)
        abbreviations_tab.setLayout(abbreviations_layout)


        
    def search_abbreviation(self):
        # Lấy từ khóa tìm kiếm
       
        word = self.abbreviations_search_box.text().strip()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM abbreviation WHERE abbreviation LIKE ?", ('%' + word + '%',))
        results = cursor.fetchall()

        if results:
            # Nếu có kết quả tìm kiếm, hiển thị các kết quả trên bảng từ điển
            self.abbreviations_table.setRowCount(0)
            for row_number, row_data in enumerate(results):
                self.abbreviations_table.insertRow(row_number)
                self.abbreviations_table.setItem(row_number, 0, QTableWidgetItem(row_data[1]))
                self.abbreviations_table.setItem(row_number, 1, QTableWidgetItem(row_data[2]))
                self.abbreviations_table.setItem(row_number, 2, QTableWidgetItem(row_data[3]))
            self.abbreviations_table.sortItems(0, Qt.AscendingOrder)  # Sắp xếp theo thứ tự abc
        else:
            # Nếu không có kết quả tìm kiếm, thông báo không tìm thấy
            QMessageBox.information(self, 'Kết quả tìm kiếm', 'Không tìm thấy từ này.')
        self.abbreviations_search_box.clear()
        abbreviation = self.abbreviations_search_box.text().strip().lower()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM abbreviation WHERE abbreviation LIKE ?", ('%' + word + '%',))
        results = cursor.fetchall()

        if results:
            # Nếu có kết quả tìm kiếm, hiển thị các kết quả trên bảng từ điển
            self.abbreviations_table.setRowCount(0)
            for row_number, row_data in enumerate(results):
                self.abbreviations_table.insertRow(row_number)
                self.abbreviations_table.setItem(row_number, 0, QTableWidgetItem(row_data[1]))
                self.abbreviations_table.setItem(row_number, 1, QTableWidgetItem(row_data[2]))
                self.abbreviations_table.setItem(row_number, 2, QTableWidgetItem(row_data[3]))
            self.abbreviations_table.sortItems(0, Qt.AscendingOrder)  # Sắp xếp theo thứ tự abc
            self.abbreviations_table.setCurrentCell(0, 0)  
        else:
            # Nếu không có kết quả tìm kiếm, thông báo không tìm thấy
            QMessageBox.information(self, 'Kết quả tìm kiếm', 'Không tìm thấy từ này.')
        self.abbreviations_search_box.clear()

    def add_abbreviation(self):
        # Thêm từ mới vào cơ sở dữ liệu
        abbreviation = self.abbreviations_add_abbreviation_box.text().strip()
        full_form = self.abbreviations_add_full_form_box.text().strip()
        definition = self.abbreviations_add_definition_box.text().strip()

        if abbreviation and full_form and definition:
            # Nếu từ và định nghĩa không rỗng, thêm vào cơ sở dữ liệu
            cursor = self.conn.cursor()
            try:
                cursor.execute("SELECT * FROM abbreviation WHERE abbreviation=?", (abbreviation,))
                result = cursor.fetchone()
                if result: # kiểm tra xem từ đã tồn tại trong cơ sở dữ liệu chưa
                    if result[1] == full_form: # nếu giống nhau thì hiện thông báo và kết thúc hàm
                        QMessageBox.information(self, 'Thông báo', 'Từ này đã tồn tại trong từ điển.')
                        return
                    else: # nếu khác nhau thì hiện hộp thoại hỏi xem có muốn lưu không
                        msg_box = QMessageBox()
                        msg_box.setIcon(QMessageBox.Question)
                        msg_box.setText(f"Từ {abbreviation} hiện đã có trong từ điển với định nghĩa là '{result[2]}'. Bạn có muốn lưu lại từ này với định nghĩa mới không?")
                        msg_box.setWindowTitle("Xác nhận")
                        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        button_yes = msg_box.button(QMessageBox.Yes)
                        button_yes.setText('Lưu lại')
                        button_no = msg_box.button(QMessageBox.No)
                        button_no.setText('Huỷ bỏ')
                        msg_box.exec_()
                        if msg_box.clickedButton() == button_yes: # nếu người dùng chọn 'Lưu lại' thì thêm từ mới vào cơ sở dữ liệu
                            new_abbreviation = f"{abbreviation} "
                            while True:
                                cursor.execute("SELECT * FROM abbreviation WHERE abbreviation=?", (new_abbreviation,))
                                result = cursor.fetchone()
                                if not result: # nếu không tìm thấy từ mới trong cơ sở dữ liệu thì thêm từ mới vào cơ sở dữ liệu
                                    break
                                new_abbreviation += " "
                            cursor.execute("INSERT INTO abbreviation (abbreviation, full_form, definition) VALUES (?, ?, ?)", (new_abbreviation, full_form, definition))
                            self.conn.commit()
                            QMessageBox.information(self, 'Thông báo', 'Thêm từ thành công.')
                            self.abbreviation_load_data()  # Load lại dữ liệu vào bảng từ điển
                            self.abbreviations_add_abbreviation_box.setText('')
                            self.abbreviations_add_full_form_box.setText('')
                            self.abbreviations_add_definition_box.setText('')
                            self.abbreviations_add_abbreviation_box.setFocus()
                else: # nếu từ chưa tồn tại trong cơ sở dữ liệu thì thêm từ mới vào cơ sở dữ liệu
                    cursor.execute("INSERT INTO abbreviation (abbreviation, full_form, definition) VALUES (?, ?, ?)", (abbreviation, full_form, definition))
                    self.conn.commit()
                    QMessageBox.information(self, 'Thông báo', 'Thêm từ thành công.')
                    self.abbreviation_load_data()  # Load lại dữ liệu vào bảng từ điển
                    self.abbreviations_add_abbreviation_box.setText('')
                    self.abbreviations_add_full_form_box.setText('')
                    self.abbreviations_add_definition_box.setText('')
                    self.abbreviations_add_abbreviation_box.setFocus()
            except sqlite3.Error:
                QMessageBox.warning(self, 'Lỗi', 'Có lỗi xảy ra khi thêm từ vào cơ sở dữ liệu.')
        else:
            # Nếu từ hoặc định nghĩa rỗng, thông báo lỗi
            QMessageBox.warning(self, 'Lỗi', 'Vui lòng nhập từ và định nghĩa.')

        # Xoá dữ liệu trong các ô nhập để nhập dữ liệu mới
        self.abbreviations_add_abbreviation_box.setText('')
        self.abbreviations_add_full_form_box.setText('')
        self.abbreviations_add_definition_box.setText('')


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            current_focus = self.focusWidget()
            if current_focus == self.abbreviations_add_abbreviation_box:
                self.abbreviations_add_full_form_box.setFocus()
            elif current_focus == self.abbreviations_add_full_form_box:
                self.abbreviations_add_definition_box.setFocus()
            elif current_focus == self.abbreviations_add_definition_box:
                self.add_abbreviation()




    def search_word(self):
    # Tìm kiếm từ trong cơ sở dữ liệu
        word = self.dictionary_search_box.text().strip().lower()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM dictionary WHERE word LIKE ?", ('%' + word + '%',))
        results = cursor.fetchall()

        if results:
            # Nếu có kết quả tìm kiếm, hiển thị các kết quả trên bảng từ điển
            self.dictionary_table.setRowCount(0)
            for row_number, row_data in enumerate(results):
                self.dictionary_table.insertRow(row_number)
                self.dictionary_table.setItem(row_number, 0, QTableWidgetItem(row_data[1]))
                self.dictionary_table.setItem(row_number, 1, QTableWidgetItem(row_data[2]))
            self.dictionary_table.sortItems(0, Qt.AscendingOrder)  # Sắp xếp theo thứ tự abc
 # Di chuyển con trỏ đến ô đầu tiên của kết quả tìm kiếm
            self.dictionary_table.setCurrentCell(0, 0)
        else:
            # Nếu không có kết quả tìm kiếm, thông báo không tìm thấy
            QMessageBox.information(self, 'Kết quả tìm kiếm', 'Không tìm thấy từ này.')
        self.dictionary_search_box.clear()


    def add_word(self):
        # Thêm từ mới vào cơ sở dữ liệu
        word = self.dictionary_add_word_box.text().strip()
        definition = self.dictionary_add_definition_box.text().strip()

        if word and definition:
            # Nếu từ và định nghĩa không rỗng, thêm vào cơ sở dữ liệu
            cursor = self.conn.cursor()
            try:
                cursor.execute("INSERT INTO dictionary (word, definition) VALUES (?, ?)", (word, definition))
                self.conn.commit()
                QMessageBox.information(self, 'Thông báo', 'Thêm từ thành công.')
                self.dictionary_load_data()  # Load lại dữ liệu vào bảng từ điển
                self.dictionary_add_word_box.setText('')
                self.dictionary_add_definition_box.setText('')
                self.dictionary_add_word_box.setFocus()
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, 'Lỗi', 'Từ này đã tồn tại trong từ điển.')
        else:
            # Nếu từ hoặc định nghĩa rỗng, thông báo lỗi
            QMessageBox.warning(self, 'Lỗi', 'Vui lòng nhập từ và định nghĩa.')

    def delete_word(self):
    # Lấy từ cần xoá từ ô nhập liệu
        word = self.dictionary_delete_box.text().strip()

        # Hiển thị hộp thoại xác nhận
        confirm = QMessageBox.question(self, 'Xác nhận', f'Bạn có chắc muốn xoá từ "{word}"?', QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.Yes:
            # Xoá từ khỏi cơ sở dữ liệu nếu người dùng xác nhận
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM dictionary WHERE word=?", (word,))
            if cursor.rowcount > 0:
                # Nếu xoá thành công, hiển thị thông báo và load lại dữ liệu vào bảng từ điển
                self.conn.commit()
                QMessageBox.information(self, 'Thông báo', 'Xoá từ thành công.')
                self.dictionary_load_data()
                self.dictionary_delete_box.setText('')
            else:
                # Nếu từ không tồn tại, hiển thị thông báo lỗi
                QMessageBox.warning(self, 'Lỗi', 'Không tìm thấy từ này trong từ điển.')
        else:
            # Nếu người dùng không xác nhận việc xoá từ, không làm gì cả
            pass

            

    def delete_abbreviation(self):
    # Lấy từ cần xoá từ ô nhập liệu
        abbreviation = self.abbreviations_delete_box.text().strip()

        # Hiển thị hộp thoại xác nhận trước khi xoá từ
        reply = QMessageBox.question(self, 'Xác nhận', f"Bạn có muốn xoá từ '{abbreviation}' không?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Xoá từ khỏi cơ sở dữ liệu
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM abbreviation WHERE full_form=?", (abbreviation,))
            if cursor.rowcount > 0:
                # Nếu xoá thành công, hiển thị thông báo và load lại dữ liệu vào bảng từ điển
                self.conn.commit()
                QMessageBox.information(self, 'Thông báo', 'Xoá từ thành công.')
                self.abbreviation_load_data()
                self.abbreviations_delete_box.setText('')
            else:
                # Nếu từ không tồn tại, hiển thị thông báo lỗi
                QMessageBox.warning(self, 'Lỗi', 'Không tìm thấy từ này trong từ điển.')
        else:
            # Nếu người dùng không xác nhận việc xoá từ, không làm gì cả
            pass

                
    def modify_word(self):
        # Sửa định nghĩa của một từ trong cơ sở dữ liệu
        word = self.dictionary_modify_word_box.text()
        definition = self.dictionary_modify_definition_box.text()

        if word == '' or definition == '':
            QMessageBox.warning(self, 'Lỗi', 'Từ hoặc định nghĩa không được để trống.')
            return
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM dictionary WHERE word=?', (word,))
        result = cursor.fetchone()

        if result is None:
            QMessageBox.warning(self, 'Lỗi', 'Từ không có trong từ điển.')
            return

    # Hiển thị hộp thoại xác nhận việc sửa đổi
        confirm_box = QMessageBox()
        confirm_box.setIcon(QMessageBox.Question)
        confirm_box.setText(f'Bạn có chắc muốn sửa định nghĩa của từ "{word}"?')
        confirm_box.setWindowTitle('Xác nhận sửa đổi')
        confirm_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_box.setDefaultButton(QMessageBox.Yes)
        button_clicked = confirm_box.exec()

        if button_clicked == QMessageBox.Yes:
            cursor.execute('UPDATE dictionary SET definition=? WHERE word=?', (definition, word))
            self.conn.commit()
            self.dictionary_load_data()
            self.dictionary_modify_word_box.setText('')
            self.dictionary_modify_definition_box.setText('')
            QMessageBox.information(self, 'Thành công', 'Định nghĩa của từ đã được sửa đổi.')
   
    def closeEvent(self, event):
        # Đóng kết nối đến cơ sở dữ liệu khi thoát chương trình
        self.conn.close()
        event.accept()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dict_window = Dictionary()
    dict_window.abbreviation_load_data()
    dict_window.show()
    sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QHeaderView
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt

import pandas as pd
import sqlite3

class Dictionary(QMainWindow):
    def __init__(self):
        super().__init__()
        self.abbreviations = ()
        self.abbreviations_table = None
        # Add this line to initialize the "tab_widget" attribute
        self.tab_widget = QTabWidget()

        # Thiết lập giao diện người dùng cho tab "Từ điển"
        self.init_dictionary_ui()

        # Khởi tạo cơ sở dữ liệu SQLite
        self.init_database()

        # Load dữ liệu vào bảng từ điển
        self.dictionary_load_data()
        self.abbreviation_load_data()
        # Thiết lập giao diện người dùng cho tab "Từ viết tắt"
        self.init_abbreviations_ui()

        # Add this line to set the central widget
        self.setCentralWidget(self.tab_widget)


    def init_database(self):
        # Kết nối tới cơ sở dữ liệu
        self.conn = sqlite3.connect('dictionary.db')

        # Tạo bảng từ điển nếu chưa có
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS dictionary
            (id INTEGER PRIMARY KEY,
            word TEXT UNIQUE,
            definition TEXT);
        ''')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS abbreviation
            (id INTEGER PRIMARY KEY,
            abbreviation TEXT UNIQUE,
            full_form TEXT,
            definition TEXT);
        ''')



    def dictionary_load_data(self):
        # Lấy tất cả các từ trong bảng và hiển thị trên bảng từ điển
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM dictionary ORDER BY word ASC')
        results = cursor.fetchall()
        self.dictionary_table.setRowCount(0)
        for row_number, row_data in enumerate(results):
            self.dictionary_table.insertRow(row_number)
            self.dictionary_table.setItem(row_number, 0, QTableWidgetItem(row_data[1]))
            self.dictionary_table.setItem(row_number, 1, QTableWidgetItem(row_data[2]))


    def abbreviation_load_data(self):

        # Lấy tất cả các từ trong bảng và hiển thị trên bảng từ điển
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM abbreviation ORDER BY abbreviation ASC')
        results = cursor.fetchall()
        if self.abbreviations_table is None:
           self.abbreviations_table = QTableWidget()
        self.abbreviations_table.setRowCount(0)
        for row_number, row_data in enumerate(results):
            self.abbreviations_table.insertRow(row_number)
            self.abbreviations_table.setItem(row_number, 0, QTableWidgetItem(row_data[1]))
            self.abbreviations_table.setItem(row_number, 1, QTableWidgetItem(row_data[2]))
            self.abbreviations_table.setItem(row_number, 2, QTableWidgetItem(row_data[3]))

    def init_dictionary_ui(self):
        # Thiết lập giao diện cho tab "Từ điển"
        dictionary_tab = QWidget()
        self.tab_widget.addTab(dictionary_tab, "Từ điển")
        self.setFixedSize(1000, 600)
        dictionary_layout = QVBoxLayout()

        # Khởi tạo các widget
        self.dictionary_search_label = QLabel('Tìm kiếm:')
        self.dictionary_search_box = QLineEdit()
        self.dictionary_search_box.returnPressed.connect(self.search_word)
        self.dictionary_search_button = QPushButton('Tìm kiếm')
        self.dictionary_search_button.clicked.connect(self.search_word)

        self.dictionary_add_label = QLabel('Thêm từ:')
        self.dictionary_add_word_box = QLineEdit()
        self.dictionary_add_definition_box = QLineEdit()
        self.dictionary_add_button = QPushButton('Thêm từ')
        self.dictionary_add_word_box.returnPressed.connect(self.dictionary_add_definition_box.setFocus) 
        self.dictionary_add_definition_box.returnPressed.connect(self.add_word) 
        self.dictionary_add_button.clicked.connect(self.add_word)

        self.dictionary_delete_label = QLabel('Xoá từ:')
        self.dictionary_delete_box = QLineEdit()
        self.dictionary_delete_button = QPushButton('Xoá từ')
        self.dictionary_delete_button.clicked.connect(self.delete_word)

        self.dictionary_modify_label = QLabel('Sửa từ:')
        self.dictionary_modify_word_box = QLineEdit()
        self.dictionary_modify_definition_box = QLineEdit()
        self.dictionary_modify_button = QPushButton('Sửa từ')
        self.dictionary_modify_button.clicked.connect(self.modify_word)

        self.dictionary_table = QTableWidget()
        self.dictionary_table.setColumnCount(2)
        self.dictionary_table.setHorizontalHeaderLabels(['Từ', 'Định nghĩa'])
        self.dictionary_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.dictionary_table.setColumnWidth(0, 210) 
        self.dictionary_table.setColumnWidth(1, 690)

        # Thêm các widget vào layout
        dictionary_search_layout = QHBoxLayout()
        dictionary_search_layout.addWidget(self.dictionary_search_label)
        dictionary_search_layout.addWidget(self.dictionary_search_box)
        dictionary_search_layout.addWidget(self.dictionary_search_button)

        dictionary_add_layout = QHBoxLayout()
        dictionary_add_layout.addWidget(self.dictionary_add_label)
        dictionary_add_layout.addWidget(self.dictionary_add_word_box)
        dictionary_add_layout.addWidget(self.dictionary_add_definition_box)
        dictionary_add_layout.addWidget(self.dictionary_add_button)

        dictionary_delete_layout = QHBoxLayout()
        dictionary_delete_layout.addWidget(self.dictionary_delete_label)
        dictionary_delete_layout.addWidget(self.dictionary_delete_box)
        dictionary_delete_layout.addWidget(self.dictionary_delete_button)
        
        dictionary_modify_layout = QHBoxLayout()
        dictionary_modify_layout.addWidget(self.dictionary_modify_label)
        dictionary_modify_layout.addWidget(self.dictionary_modify_word_box)
        dictionary_modify_layout.addWidget(self.dictionary_modify_definition_box)
        dictionary_modify_layout.addWidget(self.dictionary_modify_button)

        dictionary_layout.addLayout(dictionary_search_layout)
        dictionary_layout.addLayout(dictionary_add_layout)
        dictionary_layout.addLayout(dictionary_delete_layout)
        dictionary_layout.addLayout(dictionary_modify_layout)
        dictionary_layout.addWidget(self.dictionary_table)
        dictionary_tab.setLayout(dictionary_layout)

    def init_abbreviations_ui(self):

        # Thiết lập giao diện cho tab "Từ điển"
        abbreviations_tab = QWidget()
        self.tab_widget.addTab(abbreviations_tab, "Từ viết tắt")
        
        self.setFixedSize(1000, 600)
        abbreviations_layout = QVBoxLayout()

        # Khởi tạo các widget
        self.abbreviations_search_label = QLabel('Tìm kiếm:')
        self.abbreviations_search_box = QLineEdit()
        self.abbreviations_search_box.returnPressed.connect(self.search_abbreviation)
        self.abbreviations_search_button = QPushButton('Tìm kiếm')
        self.abbreviations_search_button.clicked.connect(self.search_abbreviation)

        self.abbreviations_add_label = QLabel('Thêm từ:')
        self.abbreviations_add_abbreviation_box = QLineEdit()
        self.abbreviations_add_abbreviation_box.setFixedWidth(100)
        self.abbreviations_add_full_form_box = QLineEdit()
        self.abbreviations_add_full_form_box.setFixedWidth(340)
        self.abbreviations_add_definition_box = QLineEdit()
        self.abbreviations_add_definition_box.setFixedWidth(340)
        self.abbreviations_add_button = QPushButton('Thêm từ')
        self.abbreviations_add_button.clicked.connect(self.add_abbreviation)

        self.abbreviations_delete_label = QLabel('Xoá từ:')
        self.abbreviations_delete_box = QLineEdit()
        self.abbreviations_delete_button = QPushButton('Xoá từ')
        self.abbreviations_delete_button.clicked.connect(self.delete_abbreviation)


        self.abbreviations_table = QTableWidget()
        self.abbreviations_table.setColumnCount(3)
        self.abbreviations_table.setHorizontalHeaderLabels(['Từ','Từ đầy đủ', 'Định nghĩa'])
        self.abbreviations_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.abbreviations_table.setColumnWidth(0, 90) 
        self.abbreviations_table.setColumnWidth(1, 420)
        self.abbreviations_table.setColumnWidth(2, 420)


        # Thêm các widget vào layout
        abbreviations_search_layout = QHBoxLayout()
        abbreviations_search_layout.addWidget(self.abbreviations_search_label)
        abbreviations_search_layout.addWidget(self.abbreviations_search_box)
        abbreviations_search_layout.addWidget(self.abbreviations_search_button)
        abbreviations_layout.addLayout(abbreviations_search_layout)



        abbreviations_add_layout = QHBoxLayout()
        abbreviations_add_layout.addWidget(self.abbreviations_add_label)
        abbreviations_add_layout.addWidget(self.abbreviations_add_abbreviation_box)
        abbreviations_add_layout.addWidget(self.abbreviations_add_full_form_box)
        abbreviations_add_layout.addWidget(self.abbreviations_add_definition_box)
        abbreviations_add_layout.addWidget(self.abbreviations_add_button)
        abbreviations_layout.addLayout(abbreviations_add_layout)


        abbreviations_delete_layout = QHBoxLayout()
        abbreviations_delete_layout.addWidget(self.abbreviations_delete_label)
        abbreviations_delete_layout.addWidget(self.abbreviations_delete_box)
        abbreviations_delete_layout.addWidget(self.abbreviations_delete_button)
        abbreviations_layout.addLayout(abbreviations_delete_layout)

        
        abbreviations_layout.addWidget(self.abbreviations_table)
        abbreviations_tab.setLayout(abbreviations_layout)


        
    def search_abbreviation(self):
        # Lấy từ khóa tìm kiếm
       
        word = self.abbreviations_search_box.text().strip()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM abbreviation WHERE abbreviation LIKE ?", ('%' + word + '%',))
        results = cursor.fetchall()

        if results:
            # Nếu có kết quả tìm kiếm, hiển thị các kết quả trên bảng từ điển
            self.abbreviations_table.setRowCount(0)
            for row_number, row_data in enumerate(results):
                self.abbreviations_table.insertRow(row_number)
                self.abbreviations_table.setItem(row_number, 0, QTableWidgetItem(row_data[1]))
                self.abbreviations_table.setItem(row_number, 1, QTableWidgetItem(row_data[2]))
                self.abbreviations_table.setItem(row_number, 2, QTableWidgetItem(row_data[3]))
            self.abbreviations_table.sortItems(0, Qt.AscendingOrder)  # Sắp xếp theo thứ tự abc
        else:
            # Nếu không có kết quả tìm kiếm, thông báo không tìm thấy
            QMessageBox.information(self, 'Kết quả tìm kiếm', 'Không tìm thấy từ này.')
        self.abbreviations_search_box.clear()
        abbreviation = self.abbreviations_search_box.text().strip().lower()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM abbreviation WHERE abbreviation LIKE ?", ('%' + word + '%',))
        results = cursor.fetchall()

        if results:
            # Nếu có kết quả tìm kiếm, hiển thị các kết quả trên bảng từ điển
            self.abbreviations_table.setRowCount(0)
            for row_number, row_data in enumerate(results):
                self.abbreviations_table.insertRow(row_number)
                self.abbreviations_table.setItem(row_number, 0, QTableWidgetItem(row_data[1]))
                self.abbreviations_table.setItem(row_number, 1, QTableWidgetItem(row_data[2]))
                self.abbreviations_table.setItem(row_number, 2, QTableWidgetItem(row_data[3]))
            self.abbreviations_table.sortItems(0, Qt.AscendingOrder)  # Sắp xếp theo thứ tự abc
            self.abbreviations_table.setCurrentCell(0, 0)  
        else:
            # Nếu không có kết quả tìm kiếm, thông báo không tìm thấy
            QMessageBox.information(self, 'Kết quả tìm kiếm', 'Không tìm thấy từ này.')
        self.abbreviations_search_box.clear()

    def add_abbreviation(self):
        # Thêm từ mới vào cơ sở dữ liệu
        abbreviation = self.abbreviations_add_abbreviation_box.text().strip()
        full_form = self.abbreviations_add_full_form_box.text().strip()
        definition = self.abbreviations_add_definition_box.text().strip()

        if abbreviation and full_form and definition:
            # Nếu từ và định nghĩa không rỗng, thêm vào cơ sở dữ liệu
            cursor = self.conn.cursor()
            try:
                cursor.execute("SELECT * FROM abbreviation WHERE abbreviation=?", (abbreviation,))
                result = cursor.fetchone()
                if result: # kiểm tra xem từ đã tồn tại trong cơ sở dữ liệu chưa
                    if result[1] == full_form: # nếu giống nhau thì hiện thông báo và kết thúc hàm
                        QMessageBox.information(self, 'Thông báo', 'Từ này đã tồn tại trong từ điển.')
                        return
                    else: # nếu khác nhau thì hiện hộp thoại hỏi xem có muốn lưu không
                        msg_box = QMessageBox()
                        msg_box.setIcon(QMessageBox.Question)
                        msg_box.setText(f"Từ {abbreviation} hiện đã có trong từ điển với định nghĩa là '{result[2]}'. Bạn có muốn lưu lại từ này với định nghĩa mới không?")
                        msg_box.setWindowTitle("Xác nhận")
                        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        button_yes = msg_box.button(QMessageBox.Yes)
                        button_yes.setText('Lưu lại')
                        button_no = msg_box.button(QMessageBox.No)
                        button_no.setText('Huỷ bỏ')
                        msg_box.exec_()
                        if msg_box.clickedButton() == button_yes: # nếu người dùng chọn 'Lưu lại' thì thêm từ mới vào cơ sở dữ liệu
                            new_abbreviation = f"{abbreviation} "
                            while True:
                                cursor.execute("SELECT * FROM abbreviation WHERE abbreviation=?", (new_abbreviation,))
                                result = cursor.fetchone()
                                if not result: # nếu không tìm thấy từ mới trong cơ sở dữ liệu thì thêm từ mới vào cơ sở dữ liệu
                                    break
                                new_abbreviation += " "
                            cursor.execute("INSERT INTO abbreviation (abbreviation, full_form, definition) VALUES (?, ?, ?)", (new_abbreviation, full_form, definition))
                            self.conn.commit()
                            QMessageBox.information(self, 'Thông báo', 'Thêm từ thành công.')
                            self.abbreviation_load_data()  # Load lại dữ liệu vào bảng từ điển
                            self.abbreviations_add_abbreviation_box.setText('')
                            self.abbreviations_add_full_form_box.setText('')
                            self.abbreviations_add_definition_box.setText('')
                            self.abbreviations_add_abbreviation_box.setFocus()
                else: # nếu từ chưa tồn tại trong cơ sở dữ liệu thì thêm từ mới vào cơ sở dữ liệu
                    cursor.execute("INSERT INTO abbreviation (abbreviation, full_form, definition) VALUES (?, ?, ?)", (abbreviation, full_form, definition))
                    self.conn.commit()
                    QMessageBox.information(self, 'Thông báo', 'Thêm từ thành công.')
                    self.abbreviation_load_data()  # Load lại dữ liệu vào bảng từ điển
                    self.abbreviations_add_abbreviation_box.setText('')
                    self.abbreviations_add_full_form_box.setText('')
                    self.abbreviations_add_definition_box.setText('')
                    self.abbreviations_add_abbreviation_box.setFocus()
            except sqlite3.Error:
                QMessageBox.warning(self, 'Lỗi', 'Có lỗi xảy ra khi thêm từ vào cơ sở dữ liệu.')
        else:
            # Nếu từ hoặc định nghĩa rỗng, thông báo lỗi
            QMessageBox.warning(self, 'Lỗi', 'Vui lòng nhập từ và định nghĩa.')

        # Xoá dữ liệu trong các ô nhập để nhập dữ liệu mới
        self.abbreviations_add_abbreviation_box.setText('')
        self.abbreviations_add_full_form_box.setText('')
        self.abbreviations_add_definition_box.setText('')


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            current_focus = self.focusWidget()
            if current_focus == self.abbreviations_add_abbreviation_box:
                self.abbreviations_add_full_form_box.setFocus()
            elif current_focus == self.abbreviations_add_full_form_box:
                self.abbreviations_add_definition_box.setFocus()
            elif current_focus == self.abbreviations_add_definition_box:
                self.add_abbreviation()




    def search_word(self):
    # Tìm kiếm từ trong cơ sở dữ liệu
        word = self.dictionary_search_box.text().strip().lower()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM dictionary WHERE word LIKE ?", ('%' + word + '%',))
        results = cursor.fetchall()

        if results:
            # Nếu có kết quả tìm kiếm, hiển thị các kết quả trên bảng từ điển
            self.dictionary_table.setRowCount(0)
            for row_number, row_data in enumerate(results):
                self.dictionary_table.insertRow(row_number)
                self.dictionary_table.setItem(row_number, 0, QTableWidgetItem(row_data[1]))
                self.dictionary_table.setItem(row_number, 1, QTableWidgetItem(row_data[2]))
            self.dictionary_table.sortItems(0, Qt.AscendingOrder)  # Sắp xếp theo thứ tự abc
 # Di chuyển con trỏ đến ô đầu tiên của kết quả tìm kiếm
            self.dictionary_table.setCurrentCell(0, 0)
        else:
            # Nếu không có kết quả tìm kiếm, thông báo không tìm thấy
            QMessageBox.information(self, 'Kết quả tìm kiếm', 'Không tìm thấy từ này.')
        self.dictionary_search_box.clear()


    def add_word(self):
        # Thêm từ mới vào cơ sở dữ liệu
        word = self.dictionary_add_word_box.text().strip()
        definition = self.dictionary_add_definition_box.text().strip()

        if word and definition:
            # Nếu từ và định nghĩa không rỗng, thêm vào cơ sở dữ liệu
            cursor = self.conn.cursor()
            try:
                cursor.execute("INSERT INTO dictionary (word, definition) VALUES (?, ?)", (word, definition))
                self.conn.commit()
                QMessageBox.information(self, 'Thông báo', 'Thêm từ thành công.')
                self.dictionary_load_data()  # Load lại dữ liệu vào bảng từ điển
                self.dictionary_add_word_box.setText('')
                self.dictionary_add_definition_box.setText('')
                self.dictionary_add_word_box.setFocus()
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, 'Lỗi', 'Từ này đã tồn tại trong từ điển.')
        else:
            # Nếu từ hoặc định nghĩa rỗng, thông báo lỗi
            QMessageBox.warning(self, 'Lỗi', 'Vui lòng nhập từ và định nghĩa.')

    def delete_word(self):
    # Lấy từ cần xoá từ ô nhập liệu
        word = self.dictionary_delete_box.text().strip()

        # Hiển thị hộp thoại xác nhận
        confirm = QMessageBox.question(self, 'Xác nhận', f'Bạn có chắc muốn xoá từ "{word}"?', QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.Yes:
            # Xoá từ khỏi cơ sở dữ liệu nếu người dùng xác nhận
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM dictionary WHERE word=?", (word,))
            if cursor.rowcount > 0:
                # Nếu xoá thành công, hiển thị thông báo và load lại dữ liệu vào bảng từ điển
                self.conn.commit()
                QMessageBox.information(self, 'Thông báo', 'Xoá từ thành công.')
                self.dictionary_load_data()
                self.dictionary_delete_box.setText('')
            else:
                # Nếu từ không tồn tại, hiển thị thông báo lỗi
                QMessageBox.warning(self, 'Lỗi', 'Không tìm thấy từ này trong từ điển.')
        else:
            # Nếu người dùng không xác nhận việc xoá từ, không làm gì cả
            pass

            

    def delete_abbreviation(self):
    # Lấy từ cần xoá từ ô nhập liệu
        abbreviation = self.abbreviations_delete_box.text().strip()

        # Hiển thị hộp thoại xác nhận trước khi xoá từ
        reply = QMessageBox.question(self, 'Xác nhận', f"Bạn có muốn xoá từ '{abbreviation}' không?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Xoá từ khỏi cơ sở dữ liệu
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM abbreviation WHERE abbreviation=?", (abbreviation,))
            if cursor.rowcount > 0:
                # Nếu xoá thành công, hiển thị thông báo và load lại dữ liệu vào bảng từ điển
                self.conn.commit()
                QMessageBox.information(self, 'Thông báo', 'Xoá từ thành công.')
                self.abbreviation_load_data()
                self.abbreviations_delete_box.setText('')
            else:
                # Nếu từ không tồn tại, hiển thị thông báo lỗi
                QMessageBox.warning(self, 'Lỗi', 'Không tìm thấy từ này trong từ điển.')
        else:
            # Nếu người dùng không xác nhận việc xoá từ, không làm gì cả
            pass

                
    def modify_word(self):
        # Sửa định nghĩa của một từ trong cơ sở dữ liệu
        word = self.dictionary_modify_word_box.text()
        definition = self.dictionary_modify_definition_box.text()

        if word == '' or definition == '':
            QMessageBox.warning(self, 'Lỗi', 'Từ hoặc định nghĩa không được để trống.')
            return
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM dictionary WHERE word=?', (word,))
        result = cursor.fetchone()

        if result is None:
            QMessageBox.warning(self, 'Lỗi', 'Từ không có trong từ điển.')
            return

    # Hiển thị hộp thoại xác nhận việc sửa đổi
        confirm_box = QMessageBox()
        confirm_box.setIcon(QMessageBox.Question)
        confirm_box.setText(f'Bạn có chắc muốn sửa định nghĩa của từ "{word}"?')
        confirm_box.setWindowTitle('Xác nhận sửa đổi')
        confirm_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_box.setDefaultButton(QMessageBox.Yes)
        button_clicked = confirm_box.exec()

        if button_clicked == QMessageBox.Yes:
            cursor.execute('UPDATE dictionary SET definition=? WHERE word=?', (definition, word))
            self.conn.commit()
            self.dictionary_load_data()
            self.dictionary_modify_word_box.setText('')
            self.dictionary_modify_definition_box.setText('')
            QMessageBox.information(self, 'Thành công', 'Định nghĩa của từ đã được sửa đổi.')
   
    def closeEvent(self, event):
        # Đóng kết nối đến cơ sở dữ liệu khi thoát chương trình
        self.conn.close()
        event.accept()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dict_window = Dictionary()
    dict_window.abbreviation_load_data()
    dict_window.show()
    sys.exit(app.exec_())
