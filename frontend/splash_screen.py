# Tên file: frontend/splash_screen.py
# CHANGELOG:
# - 2024-08-06: [KHỞI TẠO] Tạo màn hình chờ (Splash Screen) để hiển thị tiến trình khởi động của ứng dụng. (AI Studio)

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QApplication
from PyQt6.QtCore import Qt
from config import APP_NAME, APP_VERSION

class SplashScreen(QWidget):
    """
    Màn hình chờ hiển thị trong khi các tác vụ nền đang được thực thi.
    """
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(450, 250)
        
        self.setup_ui()
        self.center_on_screen()

    def setup_ui(self):
        """Thiết lập giao diện người dùng cho màn hình chờ."""
        main_layout = QVBoxLayout(self)
        
        # Tạo một widget nền để có thể bo góc và đổ màu
        background_widget = QWidget(self)
        background_widget.setObjectName("splashBackground")
        background_widget.setStyleSheet("""
            #splashBackground {
                background-color: #f0f0f0;
                border-radius: 10px;
                border: 1px solid #dcdcdc;
            }
        """)
        
        layout = QVBoxLayout(background_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.title_label = QLabel(APP_NAME)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #005a9e;")
        layout.addWidget(self.title_label)

        self.version_label = QLabel(f"Phiên bản {APP_VERSION}")
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.version_label.setStyleSheet("font-size: 14px; color: #555;")
        layout.addWidget(self.version_label)
        
        layout.addStretch(1)

        self.status_label = QLabel("Đang khởi tạo...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 13px; color: #333;")
        layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #e0e0e0;
                height: 12px;
            }
            QProgressBar::chunk {
                background-color: #0078d7;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        main_layout.addWidget(background_widget)
        self.setLayout(main_layout)

    def center_on_screen(self):
        """Canh giữa cửa sổ trên màn hình."""
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def update_progress(self, message, percent):
        """Cập nhật thanh tiến trình và thông điệp trạng thái."""
        self.status_label.setText(message)
        self.progress_bar.setValue(percent)
        QApplication.processEvents() # Đảm bảo UI được cập nhật