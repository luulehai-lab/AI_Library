# Tên file: backend/ai_service.py
# CHANGELOG:
# - 2024-08-06: [NÂNG CẤP] Thêm trường 'Xoay ảnh' vào prompt và cập nhật tín hiệu finished để trả về góc xoay. (AI Studio)
# - 2024-08-06: [BẢO TRÌ] Thêm code để ẩn cảnh báo FutureWarning từ thư viện google.generativeai. (AI Studio)
# - 2024-08-06: [VÁ LỖI] Đổi lại import thành `google.generativeai` để tương thích với phiên bản package mới nhất (>=0.8.0). (AI Studio)
# - 2024-08-06: [BẢO TRÌ] Chuyển sang sử dụng thư viện google.genai mới thay cho google.generativeai đã bị ngừng hỗ trợ. (AI Studio)
# - 2024-08-05: [TỐI ƯU] Thêm quy tắc chuẩn hóa viết hoa cho NXB và Tác giả vào prompt. Thêm hàm chuẩn hóa bằng Python sau khi nhận kết quả. (AI Studio)
# - 2024-08-03: [TỐI ƯU] "Gia cố" prompt để AI trả về thể loại nhất quán hơn (ví dụ: "Thiếu nhi" thay vì "Thiếunhi"). (AI Studio)
# - 2024-07-29: [KHỞI TẠO] Tạo service xử lý logic AI với Gemini trong một luồng riêng biệt. (AI Studio)

import warnings
# Bỏ qua cảnh báo cụ thể từ thư viện google.generativeai
warnings.filterwarnings("ignore", category=FutureWarning, module='google.generativeai')

import google.generativeai as genai
from PyQt6.QtCore import QObject, pyqtSignal
from PIL import Image
from config import get_api_key

def normalize_data(data):
    """Chuẩn hóa dữ liệu trả về từ AI."""
    for key, value in data.items():
        if isinstance(value, str):
            # Chuẩn hóa viết hoa cho các trường cụ thể
            if key in ["Tác giả", "NXB", "Quốc gia"]:
                # Xử lý đặc biệt cho NXB
                if key == "NXB" and "Nhà Xuất Bản" in value:
                    value = value.replace("Nhà Xuất Bản", "Nhà xuất bản")
                
                # Áp dụng title() cho các từ còn lại
                words = value.split()
                capitalized_words = [word.capitalize() for word in words]
                data[key] = " ".join(capitalized_words)

            # Loại bỏ khoảng trắng thừa
            data[key] = value.strip()
    return data

class AIServiceWorker(QObject):
    """
    Worker chạy trong một luồng riêng để xử lý các tác vụ AI nặng,
    tránh làm treo giao diện chính.
    """
    finished = pyqtSignal(dict, int) # data, rotation_angle
    error = pyqtSignal(str)
    progress = pyqtSignal(int, str)

    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.is_running = True

    def run(self):
        """
        Thực thi tác vụ phân tích hình ảnh sách.
        """
        try:
            self.progress.emit(10, "Đang khởi tạo AI...")
            api_key = get_api_key()
            genai.configure(api_key=api_key)

            generation_config = {
                "temperature": 0.2,
                "top_p": 1,
                "top_k": 32,
                "max_output_tokens": 4096,
            }

            model = genai.GenerativeModel(
                model_name="gemini-flash-latest",
                generation_config=generation_config,
            )

            self.progress.emit(30, "Đang tải và phân tích hình ảnh...")
            
            image = Image.open(self.image_path)

            prompt_parts = [
                "Phân tích hình ảnh bìa sách này và trích xuất thông tin chi tiết. Sau đó, tìm kiếm thông tin bổ sung trên Goodreads và các nguồn đáng tin cậy khác. Trả về kết quả dưới dạng một chuỗi duy nhất, mỗi trường thông tin trên một dòng, theo định dạng 'Key: Value'.",
                "\nQUY TẮC CỰC KỲ QUAN TRỌNG:",
                "1. CHUẨN HÓA VIẾT HOA: Luôn viết hoa chữ cái đầu của mỗi từ cho các danh từ riêng như 'Tác giả', 'Quốc gia'. RIÊNG 'NXB', chỉ viết hoa chữ cái đầu của tên riêng, ví dụ: 'Nhà xuất bản Kim Đồng', 'Nhà xuất bản Phụ Nữ Việt Nam'.",
                "2. ĐÚNG CHÍNH TẢ: Luôn viết đúng chính tả Tiếng Việt có dấu. Ví dụ, với thể loại 'Thiếu nhi', phải viết là 'Thiếu nhi' (có khoảng trắng), TUYỆT ĐỐI KHÔNG viết 'Thiếunhi' (liền nhau).",
                "3. ĐỊNH DẠNG THỂ LOẠI: Cột 'Thể loại' phải ngăn cách bởi dấu phẩy, KHÔNG có khoảng trắng giữa các thể loại (ví dụ: Kinh điển,Tiểu thuyết,Triết học).",
                "\nCÁC TRƯỜNG THÔNG TIN BẮT BUỘC:",
                "Tên sách: [Tên sách đầy đủ, bao gồm cả tên tiếng Anh trong ngoặc nếu có]",
                "Tác giả: [Tên tác giả, tuân thủ quy tắc viết hoa]",
                "Quốc gia: [Quốc gia của tác giả, tuân thủ quy tắc viết hoa]",
                "Thể loại: [Liệt kê các thể loại, tuân thủ quy tắc ở trên]",
                "Lứa tuổi: [Ví dụ: Thiếu nhi, Thanh thiếu niên, Người lớn]",
                "NXB: [Nhà xuất bản, tuân thủ quy tắc viết hoa]",
                "Năm xuất bản: [Năm xuất bản]",
                "Số trang: [Số trang của sách]",
                "Điểm Goodreads: [Chỉ ghi số thập phân, ví dụ: 4.08]",
                "Review: [Lấy 2-3 câu review nổi bật từ Goodreads, mang tính khái quát, không chứa số tham chiếu hoặc trích dẫn.]",
                "Giá Tiki: [Giá bán tham khảo trên Tiki, nếu có, ghi dạng số. Ví dụ: 120000]",
                "Xoay ảnh: [Chỉ trả về một trong các số: 0, 90, 180, 270. 0 là đúng hướng, 90 là xoay 90 độ theo chiều kim đồng hồ để chữ đọc được.]",
                "\nBẮT ĐẦU PHÂN TÍCH:",
                image,
            ]
            
            self.progress.emit(60, "AI đang xử lý yêu cầu...")
            response = model.generate_content(prompt_parts)
            
            self.progress.emit(90, "Đang định dạng dữ liệu trả về...")
            
            if not response.text:
                raise ValueError("AI không trả về dữ liệu văn bản.")

            data = {}
            lines = response.text.strip().split('\n')
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    data[key.strip()] = value.strip()
            
            # Lấy và xử lý góc xoay
            rotation_str = data.pop('Xoay ảnh', '0').strip()
            try:
                rotation_angle = int(rotation_str)
                if rotation_angle not in [0, 90, 180, 270]:
                    rotation_angle = 0
            except (ValueError, TypeError):
                rotation_angle = 0

            normalized_data = normalize_data(data)
            
            self.progress.emit(100, "Hoàn tất!")
            self.finished.emit(normalized_data, rotation_angle)

        except Exception as e:
            self.error.emit(f"Lỗi trong quá trình xử lý AI: {str(e)}")