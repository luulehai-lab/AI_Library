# Tên file: backend/database.py
# CHANGELOG:
# - 2024-08-06: [NÂNG CẤP] Thêm thống kê 'countries' vào get_dashboard_stats. (AI Studio)
# - 2024-08-06: [NÂNG CẤP] Thêm hàm get_dashboard_stats để tổng hợp dữ liệu cho biểu đồ (thể loại, tác giả, trạng thái...). (AI Studio)
# - 2024-08-06: [TÁI CẤU TRÚC] Tự động tạo câu lệnh CREATE TABLE từ data_model.py thay vì hard-code. (AI Studio)
# - 2024-08-06: [TÁI CẤU TRÚC] Chuẩn hóa hàm add_book để chỉ chấp nhận key là tên cột DB (vd: 'ten_sach'), thay vì key tiếng Việt ('Tên sách'). (AI Studio)
# - 2024-08-05: [TỐI ƯU] Loại bỏ PRAGMA check trong get_filtered_books để tăng tốc độ sort và tránh lỗi logic. (AI Studio)
# - 2024-08-05: [NÂNG CẤP] Cải thiện run_database_cleanup với danh sách chuẩn hóa NXB chi tiết hơn. (AI Studio)
# - 2024-08-05: [NÂNG CẤP] Thêm hàm run_database_cleanup để chuẩn hóa dữ liệu NXB. Cập nhật logic lọc và lấy giá trị cho 'lua_tuoi'. Thêm tham số sắp xếp vào get_filtered_books. (AI Studio)
# - 2024-08-03: [NÂNG CẤP] Cập nhật get_distinct_column_values để xử lý các tag thể loại riêng lẻ. (AI Studio)
# - 2024-08-02: [NÂNG CẤP] Thêm hàm delete_book và get_distinct_column_values. (AI Studio)
# - 2024-08-02: [TÁI CẤU TRÚC] Thay thế search_books bằng get_filtered_books để hỗ trợ lọc đa điều kiện. Cập nhật get_library_stats để tính số trang đang đọc. (AI Studio)
# - 2024-08-01: [NÂNG CẤP] Mở rộng hàm get_library_stats để tính cả tổng giá tiền sách. (AI Studio)
# - 2024-07-31: [NÂNG CẤP] Thêm hàm get_library_stats để lấy thống kê tổng số sách và số trang. (AI Studio)
# - 2024-07-30: [KHỞI TẠO] Tạo module quản lý cơ sở dữ liệu SQLite cho thư viện sách. (AI Studio)

import sqlite3
import re
from collections import Counter
from config import DATABASE_FILE
from .data_model import BOOK_FIELDS, get_db_columns

def get_db_connection():
    """Tạo và trả về một kết nối đến cơ sở dữ liệu."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Khởi tạo bảng sách trong cơ sở dữ liệu nếu chưa tồn tại."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tự động tạo câu lệnh CREATE TABLE từ data_model
    columns_sql = ", ".join([f"{name} {details['db_type']}" for name, details in BOOK_FIELDS.items()])
    create_table_sql = f"CREATE TABLE IF NOT EXISTS books ({columns_sql})"
    
    cursor.execute(create_table_sql)
    conn.commit()
    conn.close()

def run_database_cleanup():
    """Quét và chuẩn hóa dữ liệu không nhất quán trong CSDL."""
    conn = get_db_connection()
    cursor = conn.cursor()
    books = cursor.execute("SELECT id, nxb FROM books WHERE nxb IS NOT NULL").fetchall()
    
    nxb_mapping = {
        "hội nhà văn": "Nhà xuất bản Hội Nhà văn",
        "phụ nữ": "Nhà xuất bản Phụ Nữ Việt Nam",
        "kim đồng": "Nhà xuất bản Kim Đồng",
        "trẻ": "Nhà xuất bản Trẻ",
        "lao động": "Nhà xuất bản Lao Động",
        "văn học": "Nhà xuất bản Văn Học",
        "dân trí": "Nhà xuất bản Dân Trí",
        "thế giới": "Nhà xuất bản Thế Giới",
        "nhã nam": "Nhã Nam",
    }

    updates = []
    for book in books:
        original_nxb = book['nxb'].strip()
        cleaned_nxb = original_nxb
        lower_nxb = original_nxb.lower()

        for key, standard_value in nxb_mapping.items():
            if key in lower_nxb and cleaned_nxb != standard_value:
                cleaned_nxb = standard_value
                break 
        
        if "nhà xuất bản" in lower_nxb and "Nhà xuất bản" not in cleaned_nxb:
             cleaned_nxb = re.sub(r'nhà xuất bản', 'Nhà xuất bản', cleaned_nxb, flags=re.IGNORECASE)

        if cleaned_nxb != original_nxb:
            updates.append((cleaned_nxb, book['id']))

    if updates:
        cursor.executemany("UPDATE books SET nxb = ? WHERE id = ?", updates)
        conn.commit()
        print(f"Đã chuẩn hóa {len(updates)} bản ghi NXB.")
    conn.close()

def add_book(book_data):
    """Thêm một cuốn sách mới vào cơ sở dữ liệu và trả về ID của nó."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    db_columns = get_db_columns()
    # Bỏ 'id' vì nó là AUTOINCREMENT
    columns_to_insert = [col for col in db_columns if col != 'id']
    
    columns_str = ", ".join(columns_to_insert)
    placeholders_str = ", ".join(["?"] * len(columns_to_insert))
    
    values = [book_data.get(col) for col in columns_to_insert]
    
    insert_sql = f"INSERT INTO books ({columns_str}) VALUES ({placeholders_str})"
    
    cursor.execute(insert_sql, values)
    book_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return book_id

def get_book_by_id(book_id):
    """Lấy thông tin một cuốn sách bằng ID."""
    conn = get_db_connection()
    book = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    conn.close()
    return book

def get_filtered_books(filters, general_search="", sort_column=None, sort_order="ASC"):
    """Lấy sách từ DB dựa trên bộ lọc, tìm kiếm và sắp xếp."""
    conn = get_db_connection()
    query = "SELECT * FROM books"
    conditions = []
    params = []

    for column, value in filters.items():
        if value:
            if column in ['the_loai', 'lua_tuoi']:
                conditions.append(f"({column} LIKE ? OR {column} LIKE ? OR {column} LIKE ? OR {column} = ?)")
                params.extend([f"%{value},%", f"{value},%", f"%,{value}%", value])
            else:
                conditions.append(f"{column} = ?")
                params.append(value)
    
    if general_search:
        search_term = f"%{general_search}%"
        search_conditions = " OR ".join([f"{col} LIKE ?" for col in ['ten_sach', 'tac_gia', 'the_loai', 'nxb', 'review']])
        conditions.append(f"({search_conditions})")
        params.extend([search_term] * 5)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    if sort_column:
        query += f" ORDER BY {sort_column} {sort_order}"
    else:
        query += " ORDER BY id DESC"
    
    books = conn.execute(query, params).fetchall()
    conn.close()
    return books

def update_book_field(book_id, field_name, value):
    """Cập nhật một trường cụ thể của một cuốn sách."""
    conn = get_db_connection()
    cursor = conn.cursor()
    if isinstance(value, str) and not value.strip():
        db_value = None
    else:
        db_value = value
        
    cursor.execute(f"UPDATE books SET {field_name} = ? WHERE id = ?", (db_value, book_id))
    conn.commit()
    conn.close()

def delete_book(book_id):
    """Xóa một cuốn sách khỏi cơ sở dữ liệu."""
    conn = get_db_connection()
    conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

def get_distinct_column_values(column_name):
    """Lấy danh sách các giá trị duy nhất từ một cột."""
    conn = get_db_connection()
    values = conn.execute(f"SELECT DISTINCT {column_name} FROM books WHERE {column_name} IS NOT NULL").fetchall()
    conn.close()
    
    if column_name in ['the_loai', 'lua_tuoi']:
        all_tags = set()
        for row in values:
            tags = [tag.strip() for tag in row[0].split(',') if tag.strip()]
            all_tags.update(tags)
        return sorted(list(all_tags))
    
    return sorted([row[0] for row in values])

def get_library_stats():
    """Lấy các số liệu thống kê của thư viện."""
    conn = get_db_connection()
    
    overall_stats = conn.execute("SELECT COUNT(id), SUM(so_trang), SUM(gia_tiki) FROM books").fetchone()
    total_books = overall_stats[0] if overall_stats[0] is not None else 0
    total_pages = overall_stats[1] if overall_stats[1] is not None else 0
    total_price = overall_stats[2] if overall_stats[2] is not None else 0

    reading_books = conn.execute("SELECT status FROM books WHERE status LIKE 'Đang đọc (%)'").fetchall()
    total_pages_reading = 0
    for book in reading_books:
        match = re.search(r'\((\d+)/', book['status'])
        if match:
            try: total_pages_reading += int(match.group(1))
            except (ValueError, IndexError): continue

    conn.close()
    return {
        "total_books": total_books, 
        "total_pages": total_pages, 
        "total_price": total_price,
        "total_pages_reading": total_pages_reading
    }

def get_dashboard_stats():
    """
    Tổng hợp dữ liệu chi tiết để vẽ biểu đồ Dashboard.
    """
    conn = get_db_connection()
    
    # 1. Thống kê thể loại (xử lý chuỗi ngăn cách dấu phẩy)
    all_genres = conn.execute("SELECT the_loai FROM books WHERE the_loai IS NOT NULL").fetchall()
    genre_counter = Counter()
    for row in all_genres:
        genres = [g.strip() for g in row['the_loai'].split(',') if g.strip()]
        genre_counter.update(genres)
    
    # 2. Thống kê trạng thái đọc
    status_data = conn.execute("""
        SELECT 
            CASE 
                WHEN status LIKE 'Đang đọc%' THEN 'Đang đọc'
                ELSE status 
            END as clean_status,
            COUNT(*) 
        FROM books 
        GROUP BY clean_status
    """).fetchall()
    status_stats = {row[0]: row[1] for row in status_data}

    # 3. Top 5 Tác giả
    author_data = conn.execute("""
        SELECT tac_gia, COUNT(*) as count 
        FROM books 
        WHERE tac_gia IS NOT NULL 
        GROUP BY tac_gia 
        ORDER BY count DESC 
        LIMIT 5
    """).fetchall()
    top_authors = {row['tac_gia']: row['count'] for row in author_data}

    # 4. Sách theo năm xuất bản (chỉ lấy 10 năm gần nhất có sách)
    year_data = conn.execute("""
        SELECT nam_xuat_ban, COUNT(*) as count
        FROM books
        WHERE nam_xuat_ban IS NOT NULL AND nam_xuat_ban > 1900
        GROUP BY nam_xuat_ban
        ORDER BY nam_xuat_ban DESC
        LIMIT 10
    """).fetchall()
    books_by_year = {row['nam_xuat_ban']: row['count'] for row in reversed(year_data)}

    # 5. Thống kê theo Quốc gia (Top 8)
    country_data = conn.execute("""
        SELECT quoc_gia, COUNT(*) as count
        FROM books
        WHERE quoc_gia IS NOT NULL
        GROUP BY quoc_gia
        ORDER BY count DESC
        LIMIT 8
    """).fetchall()
    books_by_country = {row['quoc_gia']: row['count'] for row in country_data}

    conn.close()
    
    return {
        "genres": dict(genre_counter.most_common(8)),
        "status": status_stats,
        "authors": top_authors,
        "years": books_by_year,
        "countries": books_by_country
    }