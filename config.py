# Tên file: config.py
# CHANGELOG:
# - 2024-08-06: [NÂNG CẤP] Cập nhật phiên bản lên 2.3.0 sau khi thêm tính năng tự động xoay ảnh và làm mới thumbnail. (AI Studio)
# - 2024-08-06: [TÁI CẤU TRÚC] Cập nhật phiên bản lên 2.1.0 sau khi tập trung hóa mô hình dữ liệu vào data_model.py. (AI Studio)
# - 2024-08-06: [NÂNG CẤP] Cập nhật phiên bản lên 2.0.0 sau khi thêm tính năng thêm sách thủ công. (AI Studio)
# - 2024-08-06: [TÁI CẤU TRÚC] Cập nhật phiên bản lên 1.9.0 sau khi tách BookTableWidget ra khỏi MainWindow. (AI Studio)
# - 2024-08-06: [TÁI CẤU TRÚC] Cập nhật phiên bản lên 1.8.0 sau khi tách ChatWidget ra khỏi MainWindow. (AI Studio)
# - 2024-08-06: [NÂNG CẤP] Cập nhật phiên bản lên 1.7.0 sau khi tái cấu trúc logic khởi động. (AI Studio)
# - 2024-08-05: [NÂNG CẤP] Cập nhật phiên bản lên 1.6.3. (AI Studio)
# - 2024-08-05: [VÁ LỖI] Cập nhật phiên bản lên 1.6.2. (AI Studio)
# - 2024-08-05: [VÁ LỖI] Cập nhật phiên bản lên 1.6.1 sau khi sửa lỗi thiếu import QObject. (AI Studio)
# - 2024-08-05: [NÂNG CẤP] Cập nhật phiên bản lên 1.6.0. (AI Studio)
# - 2024-08-04: [VÁ LỖI] Cập nhật phiên bản lên 1.5.7 sau khi sửa lỗi TypeError trong hàm tính toán thống kê. (AI Studio)
# - 2024-08-04: [NÂNG CẤP] Cập nhật phiên bản lên 1.5.6 sau khi tối ưu hóa hiệu năng lọc. (AI Studio)
# - 2024-08-04: [NÂNG CẤP] Cập nhật phiên bản lên 1.5.5 sau khi cải tiến Gallery View. (AI Studio)
# - 2024-08-04: [NÂNG CẤP] Cập nhật phiên bản lên 1.5.4 sau khi thay đổi logic xử lý ảnh. (AI Studio)
# - 2024-08-03: [VÁ LỖI] Cập nhật phiên bản lên 1.5.3 sau khi sửa lỗi QThread crash. (AI Studio)
# - 2024-08-03: [VÁ LỖI] Cập nhật phiên bản lên 1.5.2 sau khi sửa lỗi cú pháp. (AI Studio)
# - 2024-08-03: [NÂNG CẤP] Cập nhật phiên bản ứng dụng lên 1.5.1. (AI Studio)
# - 2024-08-03: [NÂNG CẤP] Cập nhật phiên bản ứng dụng lên 1.5.0. (AI Studio)
# - 2024-08-02: [VÁ LỖI] Cập nhật phiên bản lên 1.4.2 sau khi sửa lỗi thiếu progress bar. (AI Studio)
# - 2024-08-02: [NÂNG CẤP] Thêm hằng số EMBEDDING_MODEL cho Google API và cập nhật phiên bản. (AI Studio)
# - 2024-08-02: [NÂNG CẤP] Thêm cấu hình cho ChromaDB và cập nhật phiên bản. (AI Studio)
# - 2024-08-01: [NÂNG CẤP] Cập nhật phiên bản ứng dụng lên 1.3.0. (AI Studio)
# - 2024-07-31: [NÂNG CẤP] Thêm các hằng số cho QSettings để lưu trạng thái giao diện. (AI Studio)
# - 2024-07-30: [NÂNG CẤP] Thêm biến cấu hình cho tên file database. (AI Studio)
# - 2024-07-29: [KHỞI TẠO] Tạo file cấu hình để tải và quản lý API key. (AI Studio)

import os
from dotenv import load_dotenv

def get_api_key():
    """
    Tải biến môi trường từ file .env và trả về API key.
    Ném ra một ValueError nếu không tìm thấy key.
    """
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "YOUR_GOOGLE_API_KEY_HERE":
        raise ValueError("Không tìm thấy GOOGLE_API_KEY. Vui lòng kiểm tra file .env của bạn.")
    return api_key

# Các cấu hình khác
APP_NAME = "Trợ Lý Thư Viện Sách AI"
APP_VERSION = "2.3.0"
DATABASE_FILE = "library.db"

# Cấu hình cho QSettings
SETTINGS_ORGANIZATION = "MyCompany"
SETTINGS_APP_NAME = "BookCatalogAI"

# Cấu hình cho ChromaDB và Embedding
CHROMA_PATH = "chroma_db"
CHROMA_COLLECTION = "book_collection"
EMBEDDING_MODEL = "models/gemini-embedding-001"