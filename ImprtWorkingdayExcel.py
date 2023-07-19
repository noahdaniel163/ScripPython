import pandas as pd
import xlsxwriter

# Đọc dữ liệu từ tệp Excel hiện có
df = pd.read_excel('e:/1.xlsx')

# Chuyển đổi cột A thành định dạng ngày
df['A'] = pd.to_datetime(df['A'], format='%d/%m/%Y')

# Tạo một danh sách các tháng duy nhất từ cột A
months = df['A'].dt.month.unique()

# Tạo tệp Excel mới với định dạng ngày là dd/mm/yyyy
writer = pd.ExcelWriter('e:/book1_with_sheets.xlsx', engine='xlsxwriter', date_format='dd/mm/yyyy')

for month in months:
    # Lọc dữ liệu cho tháng hiện tại
    month_df = df[df['A'].dt.month == month]
    
    # Tạo tên sheet từ tháng và năm
    sheet_name = month_df['A'].dt.strftime('%B %Y').iloc[0]
    
    # Ghi dữ liệu vào sheet mới với định dạng ngày là dd/mm/yyyy
    month_df.to_excel(writer, sheet_name=sheet_name, index=False)

# Lưu tệp Excel mới
writer.save()
