---
description: Quy trình nạp sách hàng loạt từ ảnh bìa vào database (batch import books)
---
Quy trình này sử dụng AI Vision và Web Search để lấy metadata sách tự động, tiết kiệm chi phí Gemini API, sau đó nạp chung vào database bằng script Python theo lô (batch).

## CÁC BƯỚC THỰC HIỆN DÀNH CHO AI ASSISTANT:

1. **Xác định lô ảnh cần xử lý (Batch X):** 
Nên dùng PowerShell `Get-ChildItem -Path images_input -File | Select-Object -First 10` để xem nhanh danh sách ảnh. Chỉ xử lý từng lô 10 ảnh để đảm bảo độ chính xác và tránh quá tải cho AI context length.

2. **Xem ảnh (Vision Analysis):** 
Dùng công cụ `view_file` (gọi song song 10 ảnh nếu cần) để đọc bìa sách. Hãy phân tích các thông số có thể nhìn thấy: `Tên sách`, `Tác giả`, `Nhà xuất bản`. Nếu ảnh bị ngang/ngược, hãy thêm cờ `"Xoay ảnh": 90` (hoặc góc xoay tương ứng) vào dữ liệu, vì script của user sẽ tự động xử lý.

3. **Tra cứu Web (Web Search):** 
Tuyệt đối không tự bịa các thông tin bị thiếu (ảo giác dữ liệu). Sử dụng công cụ `search_web` (chạy song song cho nhiều sách) để tra Google thông tin về `Số trang`, `Năm xuất bản`, và một đoạn văn ngắn lấp vào cột `Review` (dựa trên Goodreads/Tiki/Vinabook).

4. **Biên soạn dữ liệu vào JSON trung gian:** 
Mở file `_tools/book_data.json` và bổ sung toàn bộ sách của lô vừa phân tích vào cuối mảng cấp 1 (Array of Objects). 
Sử dụng công cụ `replace_file_content` MỘT LẦN thay vì ghi lẻ tẻ từng cuốn. Đảm bảo file cấu trúc đúng định dạng JSON chuẩn.

5. **Chạy script Import:** 
// turbo
Chạy lệnh `python batch_import.py` từ thư mục gốc của dự án. Script sẽ làm việc: Đọc `book_data.json` -> Tạo Thumbnail -> Parse DB -> Embedding ChromaDB -> Di chuyển ảnh sang `images_processed/`.
(Sau khi chạy, danh sách `book_data.json` tự động bị script làm cạn, AI không cần xóa file JSON).

6. **Log tiến độ:** 
Tiến hành cập nhật file check-list `task.md` đánh dấu (`[x]`) hoàn thành lô.
Ghi log vào file `work_log.md` tổng kết lô đã chạy.
