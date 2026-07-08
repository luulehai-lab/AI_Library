import os
import shutil
import sqlite3
import sys

# Thêm đường dẫn hiện tại vào sys.path để import config
sys.path.append(os.getcwd())

# Cấu hình encoding cho console để in được tiếng Việt trên Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

try:
    from config import DATABASE_FILE
except ImportError:
    DATABASE_FILE = "library.db"

def restore():
    # 1. Delete from SQLite
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        # Kiểm tra xem ID 325 có tồn tại không
        res = conn.execute("SELECT id FROM books WHERE id = 325").fetchone()
        if res:
            conn.execute("DELETE FROM books WHERE id = 325")
            conn.commit()
            print("Đã xóa sách ID 325 khỏi SQLite.")
        else:
            print("Sách ID 325 không tồn tại hoặc đã bị xóa.")
        conn.close()
    except Exception as e:
        print(f"Lỗi khi xử lý SQLite: {e}")

    # 2. Di chuyển file ảnh trở lại
    src = os.path.join("images_processed", "Ăn dặm không nước mắt.jpg")
    dst = os.path.join("images_input", "IMG_20260224_122419.jpg")
    
    if os.path.exists(src):
        try:
            shutil.move(src, dst)
            print(f"Đã di chuyển {src} về {dst}")
        except Exception as e:
            print(f"Lỗi khi di chuyển file: {e}")
    else:
        # Thử tìm file tương tự nếu tên có chút khác biệt (ví dụ andamkhongnuocmat.jpg)
        print(f"Không tìm thấy file chính xác: {src}")
        
if __name__ == "__main__":
    restore()
