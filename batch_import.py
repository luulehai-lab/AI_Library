# Tên file: batch_import.py
# CHỨC NĂNG: Nhập hàng loạt sách từ file JSON vào hệ thống.
# CHANGELOG:
# - 10:28:00 08/07/2026: [REFACTOR] Chia nhỏ hàm batch_import hạ Radon CC và thêm Type Hints. (Antigravity)

import os
import json
import shutil
import sys
from datetime import datetime
from typing import Any

# Thêm đường dẫn gốc vào sys.path để có thể import các module trong backend
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Cấu hình encoding cho console để in được tiếng Việt trên Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

try:
    from backend.database import add_book, init_db
    from backend.data_model import get_ai_to_db_key_map
    from backend.utils import rotate_image_file, create_thumbnail
    from backend.rag_service import embed_and_store_book
except ImportError as e:
    print(f"Lỗi import: {e}")
    print("Vui lòng đảm bảo script này được chạy từ thư mục gốc của ứng dụng.")
    sys.exit(1)


def _read_books_json(json_path: str) -> list[dict[str, Any]]:
    """Đọc dữ liệu sách từ file JSON.

    Args:
        json_path: Đường dẫn tới file JSON dữ liệu sách.

    Returns:
        Danh sách chứa thông tin của từng cuốn sách dưới dạng dictionary.
    """
    if not os.path.exists(json_path):
        print(f"Lỗi: Không tìm thấy file dữ liệu {json_path}")
        return []

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            print("Lỗi: Dữ liệu JSON không đúng định dạng danh sách.")
            return []
    except (json.JSONDecodeError, OSError) as e:
        print(f"Lỗi khi đọc file JSON: {e}")
        return []


def _prepare_book_image(
    book: dict[str, Any], index: int, total_count: int, processed_dir: str
) -> str | None:
    """Xử lý xoay ảnh nếu cần, tạo tên file an toàn và di chuyển ảnh tới thư mục xử lý.

    Args:
        book: Dictionary chứa thông tin sách.
        index: Thứ tự hiện tại đang xử lý.
        total_count: Tổng số cuốn sách cần xử lý.
        processed_dir: Thư mục lưu trữ ảnh đã xử lý.

    Returns:
        Đường dẫn ảnh bìa mới sau khi di chuyển, hoặc None nếu thất bại.
    """
    image_path = book.get("image_path")
    if not image_path or not os.path.exists(image_path):
        print(f"[{index}/{total_count}] Bỏ qua: Không tìm thấy ảnh {image_path}")
        return None

    book_title = book.get("Tên sách", "Không tên")

    # 1. Xoay ảnh nếu AI yêu cầu
    rotation_angle = book.get("Xoay ảnh", 0)
    if rotation_angle != 0:
        try:
            rotate_image_file(image_path, rotation_angle)
        except Exception as e:
            print(f"    Lỗi khi xoay ảnh {image_path}: {e}")

    # 2. Chuẩn bị tên file mới (safe_title)
    safe_title = "".join(
        c for c in book_title if c.isalnum() or c in (" ", ".", "_")
    ).strip()
    _, extension = os.path.splitext(image_path)
    new_filename = f"{safe_title}{extension}"
    destination_path = os.path.join(processed_dir, new_filename)

    # Xử lý trường hợp trùng tên file (thêm timestamp)
    if os.path.exists(destination_path):
        timestamp = datetime.now().strftime("%H%M%S")
        new_filename = f"{safe_title}_{timestamp}{extension}"
        destination_path = os.path.join(processed_dir, new_filename)

    # 3. Di chuyển file ảnh sang thư mục processed
    try:
        shutil.move(image_path, destination_path)
        return destination_path
    except OSError as e:
        print(f"    Lỗi khi di chuyển file: {e}")
        return None


def _import_single_book(
    book: dict[str, Any],
    key_map: dict[str, str],
    cover_path: str | None,
    index: int,
    total_count: int,
) -> bool:
    """Ánh xạ dữ liệu, lưu vào database, tạo ảnh thu nhỏ (thumbnail) và lưu embedding.

    Args:
        book: Dữ liệu cuốn sách gốc từ JSON.
        key_map: Bản đồ map key của AI sang key của database.
        cover_path: Đường dẫn ảnh bìa đã được xử lý.
        index: Chỉ số xử lý hiện tại.
        total_count: Tổng số sách cần import.

    Returns:
        True nếu import thành công hoàn toàn, ngược lại là False.
    """
    book_title = book.get("Tên sách", "Không tên")
    print(f"[{index}/{total_count}] Đang xử lý: {book_title}")

    # Chuyển đổi dữ liệu sang định dạng database
    db_book_data = {db_key: book.get(ai_key) for ai_key, db_key in key_map.items()}
    db_book_data["cover_path"] = cover_path

    try:
        # Thêm vào SQLite
        book_id = add_book(db_book_data)
        print(f"    -> Đã thêm vào SQLite (ID: {book_id})")

        # Tạo Thumbnail
        if cover_path:
            thumb_path = create_thumbnail(cover_path, book_id)
            if thumb_path:
                print("    -> Đã tạo thumbnail")

        # Embedding và lưu vào ChromaDB
        try:
            print("    -> Đang tạo embedding cho ChromaDB...")
            embed_and_store_book(book_id)
            print("    -> Thành công!")
        except Exception as e:
            print(f"    -> Lỗi embedding: {e}")

        return True
    except Exception as e:
        print(f"    Lỗi khi ghi database: {e}")
        return False


def batch_import(json_path: str) -> None:
    """Nhập hàng loạt sách từ file JSON vào hệ thống.

    Args:
        json_path: Đường dẫn tới file JSON.
    """
    # 1. Khởi tạo DB nếu chưa có
    init_db()

    books_data = _read_books_json(json_path)
    if not books_data:
        return

    key_map = get_ai_to_db_key_map()
    processed_count = 0
    total_count = len(books_data)

    print(f"Bắt đầu import {total_count} cuốn sách...")

    processed_dir = "images_processed"
    os.makedirs(processed_dir, exist_ok=True)

    for i, book in enumerate(books_data, 1):
        cover_path = _prepare_book_image(book, i, total_count, processed_dir)
        if not cover_path:
            continue

        success = _import_single_book(book, key_map, cover_path, i, total_count)
        if success:
            processed_count += 1

    print("\n========================================")
    print(f"KẾT QUẢ: Đã nạp thành công {processed_count}/{total_count} cuốn sách.")
    print("========================================")


if __name__ == "__main__":
    # Thay đổi đường dẫn đến file JSON của bạn ở đây
    DATA_JSON = os.path.join(os.path.dirname(__file__), "_tools", "book_data.json")
    batch_import(DATA_JSON)
