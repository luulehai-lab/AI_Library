<!--
File: README.md
Description: Tài liệu giới thiệu, cài đặt và vận hành ứng dụng Trợ Lý Thư Viện Sách AI
CHANGELOG:
- 10:18:00 08/07/2026: [NEW] Khởi tạo tài liệu README.md chi tiết và chuyên nghiệp (Antigravity)
-->

# 📚 Trợ Lý Thư Viện Sách AI (AI Library Assistant)

Ứng dụng Desktop cao cấp xây dựng bằng **PyQt6** và tích hợp công nghệ **Generative AI (Gemini Flash)** giúp tự động hóa quá trình số hóa, quản lý và tương tác thông minh với thư viện sách cá nhân.

<p align="center">
  <img src="assets/logo.png" alt="AI Library Logo" width="200"/>
</p>

---

## ✨ Các Tính Năng Nổi Bật (Key Features)

*   📷 **Quét ảnh bìa trích xuất thông tin tự động**: Chỉ cần tải lên ảnh bìa sách, Gemini AI sẽ tự động phân tích và trích xuất 100% dữ liệu chi tiết (Tên sách, Tác giả, Nhà xuất bản, Thể loại, Năm xuất bản, Điểm Goodreads, Tiki Price, và Review tóm tắt).
*   🔄 **Tự động xoay ảnh thông minh**: AI tự động phát hiện hướng của bìa sách và xoay ảnh về đúng chiều dọc để người dùng dễ đọc.
*   📊 **Dashboard trực quan hóa dữ liệu**: Tích hợp các biểu đồ Matplotlib hiện đại hiển thị thống kê chi tiết của thư viện sách theo Thể loại, Trạng thái đọc, Top tác giả, Năm xuất bản và Quốc gia.
*   💬 **RAG AI Chatbot (Hỏi đáp cùng sách)**: Tích hợp hệ thống tìm kiếm ngữ nghĩa ChromaDB (Vector Database) cho phép bạn chat trực tiếp và đặt câu hỏi về các cuốn sách đã lưu trữ trong thư viện.
*   📥 **Nạp sách hàng loạt (Batch Import)**: Hỗ trợ script nhập hàng loạt hàng trăm cuốn sách từ thư mục ảnh bìa có sẵn, tự động hóa toàn bộ quy trình.
*   📑 **Xuất báo cáo Excel**: Hỗ trợ xuất dữ liệu sách ra file Excel được định dạng màu sắc premium bằng openpyxl.

---

## 🛠️ Công Nghệ Sử Dụng (Tech Stack)

*   **GUI Framework**: PyQt6
*   **AI Engine**: Google Gemini API (`google.generativeai` với model `gemini-flash-latest`)
*   **Vector DB (RAG)**: ChromaDB (sử dụng model `gemini-embedding-001`)
*   **Database**: SQLite 3
*   **Data Export**: openpyxl
*   **Visualizations**: Matplotlib
*   **Image Processing**: Pillow (PIL)

---

## 🚀 Hướng Dẫn Cài Đặt (Installation)

### 1. Yêu cầu hệ thống
*   Python 3.10 trở lên.
*   Git cài đặt trên hệ thống.

### 2. Cài đặt các thư viện phụ thuộc
Di chuyển vào thư mục dự án và cài đặt thông qua `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Cấu hình khóa API (Environment Setup)
Tạo file `.env` tại thư mục gốc của dự án và khai báo khóa API của Google Gemini:
```env
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE
```

---

## 📂 Hướng Dẫn Sử Dụng (Usage)

### 1. Khởi chạy ứng dụng chính
Chạy tệp `main.py` để mở giao diện đồ họa chính của ứng dụng:
```bash
python main.py
```
*Giao diện sẽ hiển thị màn hình chờ (Splash Screen) để chuẩn bị cơ sở dữ liệu SQLite, dọn dẹp dữ liệu rác và đồng bộ hóa ChromaDB trước khi mở cửa sổ chính.*

### 2. Sử dụng công cụ nhập sách hàng loạt (Batch Import Tool)
Nếu bạn có một thư mục chứa nhiều ảnh bìa sách muốn nhập đồng thời vào hệ thống:
1.  Đặt toàn bộ ảnh bìa vào thư mục `images_input/`.
2.  Chạy script nạp sách hàng loạt:
    ```bash
    python batch_import.py
    ```
3.  Script sẽ quét toàn bộ ảnh, gửi qua Gemini AI phân tích, lưu thông tin vào SQLite, embed nội dung vào ChromaDB và chuyển ảnh đã xử lý sang thư mục `images_processed/`.

---

## 🏗️ Kiến Trúc Hệ Thống (System Architecture)

Ứng dụng tuân thủ kiến trúc phân lớp rõ ràng:
*   `frontend/`: Chứa giao diện chính và các Component UI tách biệt (Bảng sách, Chatbot RAG, Dashboard thống kê, Hộp thoại).
*   `backend/`:
    *   `ai_service.py`: Xử lý giao tiếp với Gemini API để phân tích ảnh bìa sách.
    *   `rag_service.py`: Giao tiếp với ChromaDB để lưu trữ vector embeddings và thực hiện truy vấn RAG.
    *   `database.py`: DAO (Data Access Object) tương tác trực tiếp với SQLite để lưu trữ thông tin thực tế.
    *   `data_model.py`: Định nghĩa cấu trúc dữ liệu chung của Sách.
*   `scripts/`: Các công cụ kiểm định chất lượng mã nguồn tự động (`check_modularity.py`, `audit_code_quality.py`, `git_guard.py`).

Sơ đồ Mermaid chi tiết về liên kết gọi hàm và tham chiếu trong codebase được cập nhật trực tiếp tại: [docs/architecture/MAP_GRAPH.md](file:///d:/CloudStation/CODE/PYTHON_APP/22_THU_VIEN_AI_LOCAL_1212/docs/architecture/MAP_GRAPH.md)

---

## 📝 Nhật Ký Thay Đổi & Kiểm Toán (Changelog & Audit)
*   **Báo cáo kiểm toán chất lượng mã nguồn gần nhất**: Xem tại [docs/CODE_AUDIT_REPORT_2026_07_08.md](file:///d:/CloudStation/CODE/PYTHON_APP/22_THU_VIEN_AI_LOCAL_1212/docs/CODE_AUDIT_REPORT_2026_07_08.md)
*   **Lịch sử nhật ký nghiệp vụ**: Xem tại thư mục `docs/work_logs/`

---
*Phát triển và vận hành bởi luulehai-lab & Antigravity (Senior Software Architect).*
