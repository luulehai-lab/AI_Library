# RULES.MD — Quy Tắc Làm Việc: Trợ Lý Thư Viện Sách AI

> **Người dùng:** Anh Lưu (Lê Hải Lưu)  
> **Ngôn ngữ giao tiếp:** Tiếng Việt  
> **Cập nhật lần cuối:** 2026-02-25

---

## 1. Hiểu Biết Về App

### Tổng quan
App là **Thư Viện Sách AI cá nhân** (v2.3.0), dùng PyQt6 + SQLite + Google Gemini AI + ChromaDB.

### Luồng xử lý chính
```
images_input/ (ảnh bìa sách chụp bằng điện thoại)
    ↓ AIServiceWorker (Gemini AI phân tích bìa sách)
    ↓ add_book() → ghi vào SQLite (library.db, bảng books)
    ↓ create_thumbnail() → cache ảnh nhỏ (.cache/thumbnails/)
    ↓ embed_and_store_book() → lưu vào ChromaDB (tìm kiếm ngữ nghĩa)
    ↓ shutil.move() → chuyển ảnh sang images_processed/
```

### Cấu trúc thư mục
| Thư mục | Mục đích |
|---------|---------|
| `images_input/` | Nơi đặt ảnh bìa sách MỚI để xử lý |
| `images_processed/` | Ảnh đã qua xử lý, đặt tên = tên sách |
| `.cache/thumbnails/` | Thumbnail (90x120px) theo book_id |
| `chroma_db/` | Vector database cho tìm kiếm AI |
| `assets/custom_banners/` | Ảnh banner giao diện |
| `library.db` | SQLite database chính |

### Database — Bảng `books`
| Cột DB | Nhãn UI | Kiểu | Ghi chú |
|--------|---------|------|---------|
| `id` | ID | INTEGER PK AUTOINCREMENT | Auto |
| `cover_path` | Bìa sách | TEXT | Đường dẫn ảnh đã xử lý |
| `ten_sach` | Tên sách | TEXT | Có thể kèm tên tiếng Anh |
| `tac_gia` | Tác giả | TEXT | |
| `quoc_gia` | Quốc gia | TEXT | Quốc gia tác giả |
| `the_loai` | Thể loại | TEXT | Ngăn cách bởi dấu phẩy (không dấu cách) |
| `lua_tuoi` | Lứa tuổi | TEXT | Thiếu nhi / Thanh thiếu niên / Người lớn |
| `nxb` | NXB | TEXT | Tên đầy đủ, ví dụ: "Nhà xuất bản Kim Đồng" |
| `diem_goodreads` | Điểm Goodreads | REAL | 0.0 – 5.0 |
| `review` | Review | TEXT | 2-3 câu review từ Goodreads |
| `danh_gia_ca_nhan` | Đánh giá cá nhân | TEXT | |
| `vi_tri` | Vị trí | TEXT | Ví dụ: "Kệ A, ngăn 2" |
| `status` | Status | TEXT | Default: "Chưa đọc" |
| `nam_xuat_ban` | Năm xuất bản | INTEGER | |
| `gia_tiki` | Giá Tiki | INTEGER | Đơn vị VNĐ |
| `so_trang` | Số trang | INTEGER | |
| `chat_luong_sach` | Chất lượng sách | TEXT | Tốt, Bìa cứng... |

---

## 2. Quy Tắc Ghi Database

### Chuẩn hóa dữ liệu
- **Tên sách:** Đầy đủ, ưu tiên tên tiếng Việt, thêm tên gốc trong ngoặc nếu có (ví dụ: `Trăm Năm Cô Đơn (Cien años de soledad)`)
- **Tác giả / Quốc gia:** Viết hoa chữ cái đầu mỗi từ (Title Case)
- **NXB:** Chỉ viết hoa chữ cái đầu tên riêng (ví dụ: `Nhà xuất bản Kim Đồng`, KHÔNG phải `Nhà Xuất Bản Kim Đồng`)
- **Thể loại:** Ngăn cách bởi dấu phẩy, KHÔNG có khoảng trắng giữa các thể loại (ví dụ: `Kinh điển,Tiểu thuyết`)
- **Lứa tuổi:** Dùng đúng 3 giá trị chuẩn: `Thiếu nhi` / `Thanh thiếu niên` / `Người lớn`
- **Status mặc định:** `Chưa đọc`

### Quy trình thêm sách từ ảnh (batch import)
1. Đặt ảnh vào `images_input/`
2. Nhấn "Xử lý thư mục Input" trong app (hoặc chạy script thủ công)
3. AI tự động phân tích, ghi DB, di chuyển ảnh sang `images_processed/`

### Quy trình thêm sách thủ công (qua script)
Khi cần ghi thủ công vào DB, dùng hàm `add_book()` từ `backend/database.py`:
```python
from backend.database import add_book
from backend.utils import create_thumbnail
from backend.rag_service import embed_and_store_book

book_data = {
    "ten_sach": "Tên sách",
    "tac_gia": "Tên tác giả",
    "quoc_gia": "Việt Nam",
    "the_loai": "Tiểu thuyết,Lịch sử",
    "lua_tuoi": "Người lớn",
    "nxb": "Nhà xuất bản Trẻ",
    "diem_goodreads": 4.05,
    "review": "...",
    "nam_xuat_ban": 2020,
    "gia_tiki": 120000,
    "so_trang": 300,
    "status": "Chưa đọc",
    "cover_path": "images_processed/Ten_sach.jpg",  # hoặc None
}
book_id = add_book(book_data)
create_thumbnail(book_data["cover_path"], book_id)
embed_and_store_book(book_id)
```

---

## 3. Quy Tắc Viết Code

### Chuẩn code chung
- **Ngôn ngữ:** Python 3.x
- **Framework UI:** PyQt6
- **Header mỗi file:** Có `# Tên file:` và `# CHANGELOG:` theo format chuẩn
- **Comment:** Viết bằng Tiếng Việt
- **Changelog format:**
  ```python
  # CHANGELOG:
  # - YYYY-MM-DD: [LOẠI] Mô tả thay đổi. (AI Studio)
  ```
  Các LOẠI: `[KHỞI TẠO]`, `[NÂNG CẤP]`, `[VÁ LỖI]`, `[TÁI CẤU TRÚC]`, `[TỐI ƯU]`, `[BẢO TRÌ]`

### Quy tắc kiến trúc
- **Single Source of Truth:** Cấu trúc bảng DB định nghĩa trong `backend/data_model.py` (`BOOK_FIELDS`)
- **Không hard-code tên cột:** Luôn dùng `get_db_columns()`, `get_ai_to_db_key_map()`, v.v.
- **AI worker:** Luôn chạy trong QThread riêng để không treo UI
- **Tín hiệu/Slot:** Dùng PyQt signals để kết nối các component

### Xử lý ảnh
- **Ảnh đầu vào:** `images_input/` — bất kỳ tên file nào
- **Ảnh đầu ra:** `images_processed/{TenSach}.{ext}` — tên file = tên sách (safe chars)
- **Thumbnail:** `.cache/thumbnails/{book_id}.{ext}` — kích thước 90×120px
- Ảnh được tự động xoay nếu AI phát hiện sai hướng

---

## 4. Quy Tắc Giao Tiếp Với AI (Antigravity)

- **Ngôn ngữ:** Luôn trả lời bằng Tiếng Việt
- **Xưng hô:** Anh Lưu = người dùng; em = AI trợ lý
- **Trước khi code:** Đọc và hiểu toàn bộ codebase liên quan
- **Khi thêm tính năng:** Cập nhật `CHANGELOG` trong file được sửa
- **Khi sửa bug:** Ghi rõ nguyên nhân và cách sửa trong CHANGELOG
- **Không làm thay đổi dữ liệu thật** nếu không được phép (luôn test trước với dữ liệu thử)

---

## 5. Quy Tắc Làm Việc Hằng Ngày

- Mỗi buổi làm việc: Ghi `work_log.md` với ngày và những việc đã làm
- Backup DB trước khi thực hiện thao tác hàng loạt (batch operations)
- Sau mỗi batch import ảnh lớn: Kiểm tra số bản ghi trong DB
- Khi chạy script xử lý ảnh thủ công: Đảm bảo đang ở đúng thư mục gốc project (`22_THU_VIEN_AI_LOCAL_1212/`)

---

## 6. Quy Trình Batch Import Thủ Công (Qua AI Assistant)

> **Workflow chính thức:** Dùng lệnh `/batch-import-books` để gọi file mô tả quy trình ở thư mục `.agent/workflows/batch-import-books.md`.

### Tóm tắt cốt lõi
**Mục tiêu chính:** Tiết kiệm chi phí gọi Gemini API. Mọi thao tác trích xuất, nhận diện ảnh, tìm kiếm Google đều do AI Assistant (Antigravity) làm 100%. Tuyệt đối KHÔNG chạy code gọi API Gemini từ trong thư viện ứng dụng để nhận diện chữ cho bước này, trừ khi được yêu cầu rõ ràng.

### Tóm tắt JSON Data Format
File `_tools/book_data.json` sử dụng mảng Array of Objects.
Mỗi đối tượng phải bao gồm các key bắt buộc viết bằng Tiếng Việt (chữ có dấu):
* `image_path` (đường dẫn tương đối: `images_input/xxx.jpg`)
* `Tên sách`, `Tác giả`, `Quốc gia`, `Thể loại`, `Lứa tuổi`, `NXB`, `Năm xuất bản`, `Số trang`, `Điểm Goodreads`, `Review`, `Giá Tiki`, `Xoay ảnh` (int: 0, 90, 180, 270)

---

*File này là căn cứ làm việc định hướng thiết kế và quản lý dự án Thư Viện AI. Những workflow thường quy đã được tách file riêng.*
