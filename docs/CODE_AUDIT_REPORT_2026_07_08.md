# 📊 BÁO CÁO KIỂM TOÁN CHẤT LƯỢNG MÃ NGUỒN (CODE AUDIT REPORT)
**Thời gian thực hiện**: 10:07 08/07/2026  
**Dự án**: Thư viện AI Local (`22_THU_VIEN_AI_LOCAL_1212`)  
**Người kiểm duyệt**: Lê Thanh Vân (Senior Software Architect / Antigravity)  

---

## 🏆 TỔNG QUAN ĐIỂM SỐ CHẤT LƯỢNG (QUALITY SCORE SUMMARY)

*   **Điểm chất lượng mã nguồn (AST Clean Code)**: 🟢 **10.0 / 10.0** (Không có Lỗi nặng / Blocker)
*   **Độ bao phủ Type Hints**: 🔴 **2.5%** (Chỉ 3 trên 120 hàm có Type Hints đầy đủ)
*   **Chỉ số Xenon CI/CD Gate**: 🔴 **FAIL** (Phát hiện module `batch_import.py` đạt Rank C, vượt ngưỡng cho phép là B)
*   **Độ phức tạp Cyclomatic trung bình (Radon CC)**: 🟡 **Grade C (12.5)** đối với các khối phức tạp
*   **Cognitive Complexity lớn nhất (Complexipy)**: 🟡 **51** (`scripts/generate_codebase_graph.py`), **31** (`frontend/main_window.py` -> `ExcelExportWorker::run`)
*   **Tổng số Cảnh báo Linter (Ruff)**: **94 lỗi** (Chủ yếu là unused imports, style E701)
*   **Tổng số Dead Code tiềm ẩn (Vulture 60%)**: **49 cảnh báo**
*   **Tổng số Cảnh báo Clean Code AST**: **246 cảnh báo** (Hầu hết là thiếu Type Hints và Docstrings)

---

## 🚨 CÁC VI PHẠM NGHIÊM TRỌNG (CRITICAL VIOLATIONS)

### 1. File phình to vượt giới hạn cứng (Hard Limit 800 Lines)
*   **File bị ảnh hưởng**: [frontend/main_window.py](file:///d:/CloudStation/CODE/PYTHON_APP/22_THU_VIEN_AI_LOCAL_1212/frontend/main_window.py) (**816 dòng**)
*   **Trạng thái**: 🚨 **CẤM SỬA TRỰC TIẾP** (Bị khóa theo Hiến pháp Master Rules do vượt quá 800 dòng).
*   **Phân tích**: File này chứa cả luồng xuất Excel (`ExcelExportWorker`) và toàn bộ UI điều khiển chính của MainWindow. Điểm khớp nối (Coupling Score) lên tới **137.5** (cực kỳ cao so với ngưỡng an toàn là 25).
*   *Giải pháp*: Bắt buộc phải tách `ExcelExportWorker` và các widget phụ trợ ra khỏi `main_window.py`.

### 2. Thất bại tại Xenon CI/CD Gate (Độ phức tạp Cyclomatic cao)
*   **File bị ảnh hưởng**: [batch_import.py](file:///d:/CloudStation/CODE/PYTHON_APP/22_THU_VIEN_AI_LOCAL_1212/batch_import.py)
*   **Chi tiết**: Hàm `batch_import` có độ phức tạp Radon CC đạt **14 (Grade C)**.
*   **Hậu quả**: Xenon chặn CI/CD với thông báo: `ERROR:xenon:module 'batch_import.py' has a rank of C`.
*   *Giải pháp*: Tách nhỏ hàm `batch_import` thành các hàm helper thực thi đơn chức năng.

### 3. Rủi ro rò rỉ kết nối Database (Database connection leak)
*   **File bị ảnh hưởng**: [backend/database.py](file:///d:/CloudStation/CODE/PYTHON_APP/22_THU_VIEN_AI_LOCAL_1212/backend/database.py)
*   **Chi tiết**: Tất cả các hàm thực thi SQLite3 đều mở kết nối bằng `conn = get_db_connection()` và đóng thủ công bằng `conn.close()` ở cuối hàm.
*   **Hậu quả**: Khi có lỗi runtime ném ra giữa hàm (ví dụ: lỗi SQL syntax hoặc lỗi định dạng dữ liệu), luồng chạy sẽ thoát trước khi tới `conn.close()`, gây khóa database SQLite (`Database is locked`).
*   *Giải pháp*: Sử dụng context manager `with` hoặc khối `try...finally` để đảm bảo đóng kết nối 100% khi xảy ra lỗi. Kích hoạt **WAL mode** (`PRAGMA journal_mode=WAL;`) để tăng tốc độ ghi/đọc đồng thời.

---

## 📈 CHI TIẾT KẾT QUẢ PHÂN TÍCH (DETAILED AUDIT RESULTS)

### 📊 1. Modularity & Coupling (scripts/check_modularity.py)
| File | Tổng dòng | Lớp | Hàm | Imports | Khớp nối (Coupling) | Trạng thái |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `frontend/main_window.py` | **816** | 2 | 43 | 67 | **137.5** | 🚨 CẤM SỬA TRỰC TIẾP |
| `scripts/audit_code_quality.py` | **775** | 2 | 21 | 9 | **46.5** | ⚠️ Nguy cơ phình |
| `scripts/generate_codebase_graph.py` | **637** | 3 | 20 | 5 | **44.0** | ⚠️ Nguy cơ phình |
| `frontend/components/dashboard_widget.py` | 282 | 4 | 13 | 16 | **47.5** | ⚠️ Khớp nối cao & > 1 Class |
| `frontend/components/book_table_widget.py` | 247 | 1 | 12 | 23 | **44.0** | ⚠️ Khớp nối cao |

### 🧠 2. Độ phức tạp nhận thức (Cognitive Complexity - Complexipy)
Các hàm nghiệp vụ chính có độ phức tạp Cognitive lớn (vượt ngưỡng Google Standard <= 15):
1.  `frontend/main_window.py` -> `ExcelExportWorker::run` (**31**) - *Do chứa nhiều vòng lặp định dạng ô Excel*.
2.  `frontend/components/book_table_widget.py` -> `BookTableWidget::add_book_to_table` (**23**) - *Do nhiều khối rẽ nhánh tạo widget trong bảng*.
3.  `frontend/main_window.py` -> `MainWindow::display_book_dialog` (**18**) - *Do xử lý kiểm tra các loại widget popup*.

### 🔍 3. Ruff Linter (94 Errors) & Vulture Dead Code (49 Warnings)
*   **Unused Imports (F401)**: Nhiều thư viện như `markdown` trong `frontend/main_window.py` và `Border`, `Side` trong `openpyxl` được import nhưng không dùng.
*   **Multiple Statements on One Line (E701)**: Xuất hiện nhiều đoạn mã viết gộp như `if col == 'id': continue` hoặc `try: os.remove(path)`.
*   **Unused Variables (F841)**: Biến cục bộ như `btn_close` trong `main_window.py` và `checked` trong các hàm Qt được gán nhưng không bao giờ sử dụng.

---

## 🛠️ PHÂN TÍCH TỪ TECH LEAD (ARCHITECTURAL INSIGHTS)

1.  **Thiết kế Lớp giao diện và Backend**:
    *   Sự tách biệt giữa UI (`frontend/`) và DAO (`backend/database.py`) tương đối tốt. Frontend không import trực tiếp `sqlite3`.
    *   Tuy nhiên, `frontend/main_window.py` đang import trực tiếp `openpyxl` để thực hiện tác vụ export. Theo đúng thiết kế "Separation of Concerns", toàn bộ logic làm việc với file (`openpyxl`) nên được đóng gói vào một module độc lập ở `backend/` (ví dụ: `backend/excel_service.py`), UI chỉ gọi Worker để chạy luồng ngầm.
2.  **Quản lý luồng ngầm (Multi-threading)**:
    *   Sử dụng `QThread` (`ExcelExportWorker`) rất tốt để tránh treo UI. Nhưng nên đưa class này ra file riêng để giảm tải cho `main_window.py`.
3.  **An toàn API Key**:
    *   API Key của Gemini được lấy từ `config.py` thông qua `get_api_key()` (đọc từ file `.env`), không bị hard-code trong mã nguồn. Đạt chuẩn bảo mật.

---

## 📝 BẢNG HÀNH ĐỘNG ĐỀ XUẤT (ACTION PLAN)

| Thứ tự | Ưu tiên | Tác vụ | File ảnh hưởng | Mô tả chi tiết |
| :---: | :---: | :--- | :--- | :--- |
| **1** | 🔥 **Cực cao** | Khóa Git Guard & Sửa Xenon | `batch_import.py` | Tách nhỏ hàm `batch_import` để hạ độ phức tạp Cyclomatic (từ C xuống A/B), đảm bảo pass Xenon Gate. |
| **2** | 🔥 **Cực cao** | Áp dụng Modularity First | `frontend/main_window.py` | Tách lớp `ExcelExportWorker` ra file riêng `backend/excel_service.py` hoặc `frontend/workers.py`. Đưa các menu xử lý banner ra component riêng để giảm số dòng của `main_window.py` xuống < 600 dòng. |
| **3** | ⚡ **Cao** | Đảm bảo an toàn Database | `backend/database.py` | Refactor kết nối database sử dụng context manager `with sqlite3.connect` để đảm bảo giải phóng tài nguyên. Bật **WAL mode**. |
| **4** | ⚡ **Cao** | Tự động hóa Ruff Format | Toàn bộ codebase | Chạy `ruff format .` và `ruff check --fix .` để giải quyết 94 lỗi style một cách tự động. |
| **5** | 📅 **Trung bình** | Hoàn thiện Type Hints & Docstrings | Vùng `core/` & `backend/` | Nâng tỷ lệ bao phủ Type Hints từ 2.5% lên tối thiểu 80% theo đúng Google-style docstrings. |
| **6** | 📅 **Thấp** | Dọn dẹp Dead Code | Toàn bộ codebase | Lọc các cảnh báo Vulture và cập nhật `vulture_whitelist.py` để loại bỏ các Qt Callback (được Qt gọi ngầm nhưng Vulture hiểu nhầm là dead code). |

---
> [!NOTE]  
> Báo cáo này đã được lưu chính thức tại [docs/CODE_AUDIT_REPORT_2026_07_08.md](file:///d:/CloudStation/CODE/PYTHON_APP/22_THU_VIEN_AI_LOCAL_1212/docs/CODE_AUDIT_REPORT_2026_07_08.md).  
> Đồ thị cấu trúc codebase được cập nhật trực tiếp tại [docs/architecture/MAP_GRAPH.md](file:///d:/CloudStation/CODE/PYTHON_APP/22_THU_VIEN_AI_LOCAL_1212/docs/architecture/MAP_GRAPH.md).
