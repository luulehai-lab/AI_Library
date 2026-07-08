# Tên file: main.py
# CHANGELOG:
# - 2024-08-06: [TÁI CẤU TRÚC] Tích hợp SplashScreen và StartupWorker để xử lý khởi động nặng trong luồng nền, tránh treo UI. (AI Studio)
# - 2024-08-05: [NÂNG CẤP] Thêm lệnh gọi hàm dọn dẹp CSDL khi khởi động. (AI Studio)
# - 2024-08-02: [NÂNG CẤP] Thêm lệnh gọi đồng bộ hóa ChromaDB khi khởi động. (AI Studio)
# - 2024-07-31: [NÂNG CẤP] Thêm logic tạo thư mục 'assets/custom_banners' khi khởi động. (AI Studio)
# - 2024-07-30: [NÂNG CẤP] Gọi hàm khởi tạo cơ sở dữ liệu khi ứng dụng bắt đầu. (AI Studio)
# - 2024-07-29: [KHỞI TẠO] File chính để khởi chạy ứng dụng PyQt6. (AI Studio)

import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QThread

from frontend.main_window import MainWindow
from frontend.splash_screen import SplashScreen
from backend.startup_worker import StartupWorker

class ApplicationController:
    """
    Lớp điều phối quá trình khởi động và chạy ứng dụng.
    """
    def __init__(self, app):
        self.app = app
        self.main_window = None
        self.splash = None
        self.worker_thread = None
        self.startup_worker = None

    def run(self):
        self.splash = SplashScreen()
        self.splash.show()

        self.worker_thread = QThread()
        self.startup_worker = StartupWorker()
        self.startup_worker.moveToThread(self.worker_thread)

        # Kết nối tín hiệu từ worker
        self.startup_worker.progress_updated.connect(self.splash.update_progress)
        self.startup_worker.finished.connect(self.on_startup_finished)
        self.startup_worker.error.connect(self.on_startup_error)
        
        # Bắt đầu worker khi thread chạy
        self.worker_thread.started.connect(self.startup_worker.run)
        
        self.worker_thread.start()

    def on_startup_finished(self):
        """
        Được gọi khi worker khởi động hoàn tất.
        """
        print("Khởi động hoàn tất. Đang mở cửa sổ chính...")
        self.main_window = MainWindow()
        self.main_window.show()
        self.splash.close()
        
        # Dọn dẹp thread
        self.worker_thread.quit()
        self.worker_thread.wait()

    def on_startup_error(self, error_message):
        """
        Được gọi khi có lỗi xảy ra trong quá trình khởi động.
        """
        self.splash.close()
        QMessageBox.critical(None, "Lỗi Khởi Động", f"Không thể khởi động ứng dụng:\n{error_message}")
        self.app.quit()

def main():
    """
    Hàm chính để khởi tạo và chạy ứng dụng.
    """
    app = QApplication(sys.argv)
    
    controller = ApplicationController(app)
    controller.run()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()