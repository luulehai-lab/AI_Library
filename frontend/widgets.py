# Tên file: frontend/widgets.py
# CHANGELOG:
# - 2024-08-04: [NÂNG CẤP] Tạo widget GalleryItemWidget để tùy chỉnh hiển thị và tương tác trong chế độ Lưới. (AI Studio)
# - 2024-07-31: [NÂNG CẤP] Tạo widget ClickableLabel để xử lý sự kiện nháy đúp chuột cho ảnh. (AI Studio)
# - 2024-07-29: [KHỞI TẠO] Tạo file cho các widget tùy chỉnh trong tương lai. (AI Studio)

import os
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap

class ClickableLabel(QLabel):
    """
    Một QLabel tùy chỉnh có thể phát ra tín hiệu khi được nháy đúp chuột.
    """
    doubleClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def mouseDoubleClickEvent(self, event):
        """
        Bắt sự kiện nháy đúp chuột và phát tín hiệu.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.doubleClicked.emit()
        super().mouseDoubleClickEvent(event)

class GalleryItemWidget(QWidget):
    """
    Widget tùy chỉnh để hiển thị một mục trong chế độ xem Lưới.
    Bao gồm ảnh bìa có thể nháy đúp và tiêu đề sách.
    """
    def __init__(self, cover_path, title, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        self.image_label = ClickableLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setToolTip("Nháy đúp để phóng to ảnh")
        
        if cover_path and os.path.exists(cover_path):
            pixmap = QPixmap(cover_path)
            scaled_pixmap = pixmap.scaled(150, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
        else:
            # Hiển thị ảnh placeholder nếu không có bìa
            self.image_label.setText("Không có ảnh")
            self.image_label.setFixedSize(150, 200)

        self.text_label = QLabel(title)
        self.text_label.setWordWrap(True)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setToolTip("Nháy đúp để xem chi tiết sách")

        layout.addWidget(self.image_label)
        layout.addWidget(self.text_label)
        self.setLayout(layout)