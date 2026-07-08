# Tên file: backend/startup_worker.py
# CHANGELOG:
# - 2024-08-06: [KHỞI TẠO] Tạo worker để xử lý các tác vụ khởi động nặng (tạo thư mục, init DB, cleanup, sync Chroma) trong luồng nền. (AI Studio)

import os
from PyQt6.QtCore import QObject, pyqtSignal
from backend.database import init_db, run_database_cleanup
from backend.rag_service import sync_database_with_chroma

class StartupWorker(QObject):
    """
    Worker thực hiện các tác vụ khởi tạo nặng nề khi ứng dụng bắt đầu,
    tránh làm treo giao diện chính.
    """
    progress_updated = pyqtSignal(str, int) # message, percent
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        """
        Thực thi tuần tự các tác vụ khởi động.
        """
        try:
            # 1. Tạo cấu trúc thư mục (10%)
            self.progress_updated.emit("Đang kiểm tra cấu trúc thư mục...", 10)
            os.makedirs("images_input", exist_ok=True)
            os.makedirs("images_processed", exist_ok=True)
            os.makedirs(os.path.join("assets", "custom_banners"), exist_ok=True)
            os.makedirs("chroma_db", exist_ok=True)

            # 2. Khởi tạo cơ sở dữ liệu SQLite (25%)
            self.progress_updated.emit("Đang khởi tạo cơ sở dữ liệu...", 25)
            init_db()

            # 3. Dọn dẹp và chuẩn hóa CSDL (50%)
            self.progress_updated.emit("Đang dọn dẹp và chuẩn hóa dữ liệu...", 50)
            run_database_cleanup()

            # 4. Đồng bộ hóa với ChromaDB (90%)
            self.progress_updated.emit("Đang đồng bộ hóa với thư viện vector...", 90)
            sync_database_with_chroma()

            # 5. Hoàn tất (100%)
            self.progress_updated.emit("Hoàn tất!", 100)
            self.finished.emit()

        except Exception as e:
            self.error.emit(f"Lỗi trong quá trình khởi tạo: {str(e)}")