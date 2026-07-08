import sqlite3
import json
import os
import sys

# Thêm đường dẫn gốc vào sys.path để có thể import các module trong backend
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from backend.data_model import get_ai_to_db_key_map
from backend.rag_service import embed_and_store_book
from config import DATABASE_FILE

def update_metadata(json_path):
    if not os.path.exists(json_path):
        print(f"Lỗi: Không tìm thấy file {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        books_data = json.load(f)

    # Lấy map ánh xạ từ key AI sang key DB
    key_map = get_ai_to_db_key_map()
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    updated_count = 0
    
    # Bắt đầu xử lý từ Batch 5 (cuốn "Phương pháp nuôi dạy con trong năm đầu")
    # Hoặc đơn giản là duyệt qua toàn bộ, nếu thấy trùng tên thì cập nhật.
    
    for i, book in enumerate(books_data, 1):
        title = book.get("Tên sách")
        if not title:
            continue
            
        # Tìm sách trong DB theo tên
        cursor.execute("SELECT id FROM books WHERE ten_sach = ?", (title,))
        result = cursor.fetchone()
        
        if result:
            book_id = result[0]
            print(f"[{i}] Cập nhật: {title} (ID: {book_id})")
            
            # Chuẩn bị dữ liệu cập nhật
            update_fields = []
            update_values = []
            
            for ai_key, db_key in key_map.items():
                if ai_key in book:
                    value = book[ai_key]
                    update_fields.append(f"{db_key} = ?")
                    update_values.append(value)
            
            if update_fields:
                sql = f"UPDATE books SET {', '.join(update_fields)} WHERE id = ?"
                update_values.append(book_id)
                cursor.execute(sql, update_values)
                
                # Re-index trong ChromaDB để cập nhật thông tin tìm kiếm
                try:
                    embed_and_store_book(book_id)
                    print(f"    -> Đã cập nhật metadata và re-index ChromaDB.")
                except Exception as e:
                    print(f"    -> Lỗi khi re-index ChromaDB: {e}")
                
                updated_count += 1
        else:
            # print(f"[{i}] Không tìm thấy trong DB: {title}")
            pass

    conn.commit()
    conn.close()
    print(f"\nHoàn tất! Đã cập nhật {updated_count} cuốn sách.")

if __name__ == "__main__":
    if sys.platform == "win32":
        import codecs
        sys.stdout.reconfigure(encoding='utf-8')
        
    DATA_JSON = r"C:\Users\luule\.gemini\antigravity\brain\7dbb3c43-8629-4e14-8219-0e6cc9b21709\book_data.json"
    update_metadata(DATA_JSON)
