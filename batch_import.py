import os
import json
import shutil
import sys
from datetime import datetime

# Thêm đường dẫn gốc vào sys.path để có thể import các module trong backend
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Cấu hình encoding cho console để in được tiếng Việt trên Windows
if sys.platform == "win32":
    import codecs
    sys.stdout.reconfigure(encoding='utf-8')

try:
    from backend.database import add_book, init_db
    from backend.data_model import get_ai_to_db_key_map
    from backend.utils import rotate_image_file, create_thumbnail
    from backend.rag_service import embed_and_store_book
except ImportError as e:
    print(f"Lỗi import: {e}")
    print("Vui lòng đảm bảo script này được chạy từ thư mục gốc của ứng dụng.")
    sys.exit(1)

def batch_import(json_path):
    """
    Nhập hàng loạt sách từ file JSON vào hệ thống.
    """
    # 1. Khởi tạo DB nếu chưa có
    init_db()
    
    if not os.path.exists(json_path):
        print(f"Lỗi: Không tìm thấy file dữ liệu {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        books_data = json.load(f)
        
    key_map = get_ai_to_db_key_map()
    processed_count = 0
    total_count = len(books_data)
    
    print(f"Bắt đầu import {total_count} cuốn sách...")
    
    processed_dir = "images_processed"
    os.makedirs(processed_dir, exist_ok=True)
    
    for i, book in enumerate(books_data, 1):
        image_path = book.get('image_path')
        # Kiểm tra đường dẫn ảnh (có thể là đường dẫn tương đối từ gốc app)
        if not os.path.exists(image_path):
            print(f"[{i}/{total_count}] Bỏ qua: Không tìm thấy ảnh {image_path}")
            continue
            
        book_title = book.get("Tên sách", "Không tên")
        print(f"[{i}/{total_count}] Đang xử lý: {book_title}")
        
        # 2. Xoay ảnh nếu AI yêu cầu
        rotation_angle = book.get('Xoay ảnh', 0)
        if rotation_angle != 0:
            rotate_image_file(image_path, rotation_angle)
            
        # 3. Chuẩn bị tên file mới (safe_title)
        safe_title = "".join(c for c in book_title if c.isalnum() or c in (' ', '.', '_')).strip()
        _, extension = os.path.splitext(image_path)
        new_filename = f"{safe_title}{extension}"
        destination_path = os.path.join(processed_dir, new_filename)
        
        # Xử lý trường hợp trùng tên file (thêm timestamp hoặc hậu tố)
        if os.path.exists(destination_path):
            timestamp = datetime.now().strftime("%H%M%S")
            new_filename = f"{safe_title}_{timestamp}{extension}"
            destination_path = os.path.join(processed_dir, new_filename)

        # 4. Di chuyển file ảnh sang thư mục processed
        try:
            shutil.move(image_path, destination_path)
        except Exception as e:
            print(f"    Lỗi khi di chuyển file: {e}")
            continue
            
        # 5. Chuyển đổi dữ liệu sang định dạng database
        db_book_data = {db_key: book.get(ai_key) for ai_key, db_key in key_map.items()}
        db_book_data['cover_path'] = destination_path
        
        # 6. Thêm vào SQLite
        try:
            book_id = add_book(db_book_data)
            print(f"    -> Đã thêm vào SQLite (ID: {book_id})")
            
            # 7. Tạo Thumbnail
            thumb_path = create_thumbnail(destination_path, book_id)
            if thumb_path:
                print(f"    -> Đã tạo thumbnail")
                
            # 8. Embedding và lưu vào ChromaDB
            try:
                print(f"    -> Đang tạo embedding cho ChromaDB...")
                embed_and_store_book(book_id)
                print(f"    -> Thành công!")
            except Exception as e:
                print(f"    -> Lỗi embedding: {e}")
                
            processed_count += 1
        except Exception as e:
            print(f"    Lỗi khi ghi database: {e}")
        
    print(f"\n========================================")
    print(f"KẾT QUẢ: Đã nạp thành công {processed_count}/{total_count} cuốn sách.")
    print(f"========================================")

if __name__ == "__main__":
    # Thay đổi đường dẫn đến file JSON của bạn ở đây
    DATA_JSON = os.path.join(os.path.dirname(__file__), "_tools", "book_data.json")
    batch_import(DATA_JSON)
