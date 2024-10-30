import os
from openpyxl import load_workbook

folder_path = r'E:\1\R'

# Lặp qua từng file trong thư mục
for filename in os.listdir(folder_path):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(folder_path, filename)
        
        # Mở workbook
        wb = load_workbook(file_path)
        
        # Lấy sheet đầu tiên
        sheet = wb.active
        
        # Đọc giá trị của ô C12
        cell_value = sheet['C12'].value
        
        # Thay thế chuỗi "R" thành "N"
        if cell_value:
            new_value = cell_value.replace('R', 'N')
            sheet['C12'] = new_value
        
        # Lưu workbook với tên file tương ứng
        wb.save(file_path)
