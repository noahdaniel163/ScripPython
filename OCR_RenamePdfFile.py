import os
import fitz  # PyMuPDF
import pandas as pd
import pytesseract
import easyocr
import numpy as np
from fuzzywuzzy import process
from PIL import Image
import io

# Đường dẫn thư mục PDF và file Excel
pdf_folder = r"E:\1"
excel_file = r"E:\1\Name.xlsx"

# Chọn thư viện OCR
use_easyocr = True  # Dùng EasyOCR
use_tesseract = False  # Dùng Tesseract
use_fuzzy_matching = True  # Bật fuzzy matching

# Đọc danh sách tên từ file Excel (Không có tiêu đề cột)
def load_company_list(excel_file):
    df = pd.read_excel(excel_file, header=None, dtype=str)
    print("📌 Dữ liệu trong file Excel:\n", df.head())

    if df.shape[1] < 2:
        raise ValueError("⚠️ File Excel cần có ít nhất 2 cột!")

    company_dict = dict(zip(df[0].str.lower().str.strip(), df[1].str.strip()))
    return company_dict

# Chuyển PDF thành ảnh bằng PyMuPDF (fitz) - CHỈ LẤY TRANG ĐẦU TIÊN
def extract_first_page_image(pdf_path):
    doc = fitz.open(pdf_path)
    if len(doc) == 0:
        return None  # Trả về None nếu file PDF không có trang nào
    
    pix = doc[0].get_pixmap()  # Chỉ lấy trang đầu tiên
    img = Image.open(io.BytesIO(pix.tobytes("png")))  # Chuyển thành ảnh
    return img

# Dùng OCR để đọc nội dung từ hình ảnh - CHỈ LẤY 3 DÒNG ĐẦU
def extract_text_from_image(image):
    text = ""

    if use_easyocr:
        reader = easyocr.Reader(["vi", "en"])
        img_np = np.array(image)  # Chuyển đổi từ PIL.Image sang NumPy array
        result = reader.readtext(img_np)
        
        # Chỉ lấy 3 dòng đầu tiên
        text_lines = [detection[1] for detection in result[:3]]
        text = "\n".join(text_lines)

    elif use_tesseract:
        text = pytesseract.image_to_string(image, lang="eng+vie")
        text_lines = text.split("\n")[:3]  # Chỉ lấy 3 dòng đầu tiên
        text = "\n".join(text_lines)

    return text.strip()

# Tìm tên công ty trong nội dung OCR
def find_company_name(text, company_dict):
    text_lines = text.lower().split("\n")  # Tách thành từng dòng
    for line in text_lines:
        if line in company_dict:
            return company_dict[line]

    # Nếu không tìm thấy, thử fuzzy matching
    if use_fuzzy_matching:
        for line in text_lines:
            match = process.extractOne(line, company_dict.keys(), score_cutoff=80)
            if match:
                return company_dict[match[0]]

    return None

# Xử lý đổi tên file PDF
def process_pdfs(pdf_folder, excel_file):
    company_dict = load_company_list(excel_file)

    for file_name in os.listdir(pdf_folder):
        if file_name.lower().endswith(".pdf"):
            file_path = os.path.join(pdf_folder, file_name)
            print(f"🔍 Đọc file: {file_name}")

            image = extract_first_page_image(file_path)  # CHỈ lấy trang đầu tiên
            if image is None:
                print(f"⚠️ File PDF {file_name} không có nội dung!")
                continue

            text = extract_text_from_image(image)  # NHẬN DIỆN CHỈ 3 DÒNG ĐẦU
            new_name = find_company_name(text, company_dict)  # Tìm tên mới

            if new_name:
                new_file_name = new_name.replace(" ", "_") + ".pdf"
                new_file_path = os.path.join(pdf_folder, new_file_name)

                os.rename(file_path, new_file_path)
                print(f"✅ Đổi tên: {file_name} ➝ {new_file_name}")
            else:
                print(f"⚠️ Không tìm thấy tên trong {file_name}")

# Chạy chương trình
process_pdfs(pdf_folder, excel_file)
