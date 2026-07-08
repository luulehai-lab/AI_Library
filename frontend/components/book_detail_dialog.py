# Tên file: frontend/components/book_detail_dialog.py
# CHỨC NĂNG: Hộp thoại hiển thị thông tin chi tiết của một cuốn sách.
# CHANGELOG:
# - 10:28:00 08/07/2026: [NEW] Khởi tạo dialog hiển thị chi tiết sách. (Antigravity)

import os
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QScrollArea,
    QWidget,
    QFormLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from ..widgets import ClickableLabel
from typing import Any


class BookDetailDialog(QDialog):
    """Hộp thoại chi tiết sách hiển thị tất cả các trường dữ liệu của một cuốn sách."""

    view_image_requested = pyqtSignal(str)

    def __init__(self, book_data: dict[str, Any], parent: QWidget | None = None):
        """Khởi tạo dialog chi tiết sách.

        Args:
            book_data: Dictionary chứa thông tin chi tiết của cuốn sách từ SQLite.
            parent: Widget cha quản lý dialog này.
        """
        super().__init__(parent)
        self.book_data = book_data
        self.initUI()

    def initUI(self) -> None:
        """Thiết lập giao diện dialog."""
        self.setWindowTitle(self.book_data.get("ten_sach", "Chi tiết sách"))
        self.setMinimumSize(800, 700)

        dialog_layout = QVBoxLayout(self)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        dialog_layout.addWidget(scroll_area)

        scroll_content = QWidget()
        scroll_area.setWidget(scroll_content)

        form_layout = QFormLayout(scroll_content)
        form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)

        for key, value in self.book_data.items():
            if key == "id":
                continue
            display_key = key.replace("_", " ").title()

            if key == "cover_path":
                label = QLabel("Bìa sách (nháy đúp để phóng to):")
                pixmap_label = ClickableLabel()
                if value and os.path.exists(str(value)):
                    pixmap = QPixmap(str(value))
                    pixmap_label.setPixmap(
                        pixmap.scaledToWidth(
                            200, Qt.TransformationMode.SmoothTransformation
                        )
                    )
                    pixmap_label.doubleClicked.connect(
                        lambda path=str(value): self.view_image_requested.emit(path)
                    )
                form_layout.addRow(label, pixmap_label)
            elif key in ["review", "danh_gia_ca_nhan"]:
                field = QTextEdit(str(value if value is not None else ""))
                field.setReadOnly(True)
                field.setMinimumHeight(100)
                form_layout.addRow(QLabel(f"{display_key}:"), field)
            else:
                field = QLineEdit(str(value if value is not None else ""))
                field.setReadOnly(True)
                form_layout.addRow(QLabel(f"{display_key}:"), field)
