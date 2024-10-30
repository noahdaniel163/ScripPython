import pandas as pd

# Đọc file Excel
file_path = r"E:\1\1.xlsx"
df = pd.read_excel(file_path)

# Chia file thành nhiều file với 200 dòng mỗi file
chunk_size = 200
for i, chunk in enumerate(range(0, len(df), chunk_size)):
    df_chunk = df.iloc[chunk:chunk + chunk_size]
    output_file = f"E:\\1\\File_{i+1:02}.xlsx"
    df_chunk.to_excel(output_file, index=False)

print("Chia file hoàn tất.")
