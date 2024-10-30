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
        
        # Gán tên file vào ô C12
        sheet['C12'] = filename
        
        # Lưu workbook với tên file tương ứng
        wb.save(file_path)
