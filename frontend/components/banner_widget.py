# Tên file: frontend/components/banner_widget.py
# CHỨC NĂNG: Widget quản lý và hiển thị banner cuộn ảnh bìa.
# CHANGELOG:
# - 10:28:00 08/07/2026: [NEW] Khởi tạo banner widget riêng biệt. (Antigravity)

import os
import shutil
from datetime import datetime
from PyQt6.QtWidgets import (
    QScrollArea,
    QWidget,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QFileDialog,
)
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QPixmap
from config import SETTINGS_ORGANIZATION, SETTINGS_APP_NAME


class BannerWidget(QScrollArea):
    """Widget hiển thị một dải banner ảnh bìa có thể cuộn ngang, thêm mới hoặc xóa bỏ."""

    def __init__(self, parent: QWidget | None = None):
        """Khởi tạo BannerWidget.

        Args:
            parent: Widget cha quản lý banner.
        """
        super().__init__(parent)
        self.initUI()
        self.load_banner_images()

    def initUI(self) -> None:
        """Khởi tạo cấu trúc giao diện."""
        self.setObjectName("bannerScrollArea")
        self.setWidgetResizable(True)
        self.setFixedHeight(150)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.banner_widget = QWidget()
        self.banner_layout = QHBoxLayout(self.banner_widget)
        self.banner_layout.setContentsMargins(0, 0, 0, 0)
        self.banner_layout.setSpacing(5)

        self.setWidget(self.banner_widget)

    def add_banner_images(self) -> None:
        """Mở hộp thoại chọn nhiều ảnh và lưu vào thư mục custom banners để hiển thị."""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Chọn ảnh bìa", "", "Image Files (*.png *.jpg *.jpeg)"
        )
        if not file_paths:
            return

        settings = QSettings(SETTINGS_ORGANIZATION, SETTINGS_APP_NAME)
        current_paths = settings.value("bannerPaths", [], type=list)
        banner_storage_path = os.path.join("assets", "custom_banners")
        os.makedirs(banner_storage_path, exist_ok=True)

        for path in file_paths:
            try:
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
                _, extension = os.path.splitext(path)
                new_filename = f"banner_{timestamp}{extension}"
                destination_path = os.path.join(banner_storage_path, new_filename)
                shutil.copy(path, destination_path)
                current_paths.append(destination_path)
            except OSError as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể sao chép file ảnh: {e}")

        settings.setValue("bannerPaths", current_paths)
        self.load_banner_images()

    def clear_banner_images(self) -> None:
        """Xóa tất cả các ảnh bìa custom khỏi cấu hình và bộ nhớ đĩa."""
        reply = QMessageBox.question(
            self,
            "Xác nhận",
            "Bạn có chắc muốn xóa tất cả ảnh bìa?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.No:
            return

        settings = QSettings(SETTINGS_ORGANIZATION, SETTINGS_APP_NAME)
        paths_to_delete = settings.value("bannerPaths", [], type=list)

        for path in paths_to_delete:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError as e:
                    QMessageBox.critical(self, "Lỗi", f"Không thể xóa file: {e}")

        settings.setValue("bannerPaths", [])
        self.load_banner_images()

    def load_banner_images(self) -> None:
        """Tải và vẽ các ảnh bìa lên layout từ QSettings."""
        # Xóa các widget cũ
        while self.banner_layout.count():
            child = self.banner_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        settings = QSettings(SETTINGS_ORGANIZATION, SETTINGS_APP_NAME)
        banner_paths = settings.value("bannerPaths", [], type=list)

        if not banner_paths:
            placeholder = QLabel(
                "Thư Viện Sách Cá Nhân\n(Nhấn 'Thêm ảnh bìa...' để bắt đầu)"
            )
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            placeholder.setObjectName("bannerPlaceholder")
            self.banner_layout.addWidget(placeholder)
            return

        for path in banner_paths:
            if os.path.exists(path):
                pixmap = QPixmap(path)
                if not pixmap.isNull():
                    label = QLabel()
                    # Scale chiều cao tương ứng chiều cao widget trừ khoảng đệm
                    scaled_pixmap = pixmap.scaledToHeight(
                        self.height() - 20, Qt.TransformationMode.SmoothTransformation
                    )
                    label.setPixmap(scaled_pixmap)
                    self.banner_layout.addWidget(label)
        self.banner_layout.addStretch(1)

    def refresh_banner(self) -> None:
        """Phương thức hỗ trợ MainWindow gọi lại khi resize cửa sổ."""
        self.load_banner_images()
