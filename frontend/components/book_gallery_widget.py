# Tên file: frontend/components/book_gallery_widget.py
# CHỨC NĂNG: Widget hiển thị thư viện sách dưới dạng lưới ảnh (Gallery).
# CHANGELOG:
# - 10:28:00 08/07/2026: [NEW] Khởi tạo book gallery widget riêng biệt. (Antigravity)

import sqlite3
from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from backend.utils import get_thumbnail_path
from ..widgets import GalleryItemWidget


class BookGalleryWidget(QListWidget):
    """Widget hiển thị lưới sách (Gallery View) sử dụng QListWidget ở IconMode."""

    book_selected = pyqtSignal(
        int
    )  # Phát ra ID sách khi nhấp đúp vào item để xem chi tiết
    view_image_requested = pyqtSignal(
        str
    )  # Phát ra đường dẫn ảnh bìa khi nhấp đúp vào nhãn ảnh

    def __init__(self, parent: QWidget | None = None):
        """Khởi tạo BookGalleryWidget.

        Args:
            parent: Widget cha quản lý widget này.
        """
        super().__init__(parent)
        self.initUI()

    def initUI(self) -> None:
        """Thiết lập các thuộc tính hiển thị dạng lưới."""
        self.setViewMode(QListWidget.ViewMode.IconMode)
        self.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.setWordWrap(True)
        self.setSpacing(20)

        # Kết nối sự kiện nhấp đúp vào dòng/cột để xem chi tiết sách
        self.itemDoubleClicked.connect(self._on_item_double_clicked)

    def display_books(self, books: list[sqlite3.Row]) -> None:
        """Cập nhật dữ liệu hiển thị danh sách sách dạng lưới.

        Args:
            books: Danh sách các bản ghi sách từ database SQLite.
        """
        self.clear()

        for book_row in books:
            book_dict = dict(book_row)
            book_id = book_dict.get("id")
            cover_path = book_dict.get("cover_path", "")
            title = book_dict.get("ten_sach", "Không có tên")

            if book_id is None:
                continue

            item = QListWidgetItem(self)
            item.setData(Qt.ItemDataRole.UserRole, book_id)

            thumbnail_path = get_thumbnail_path(book_id, cover_path)
            item_widget = GalleryItemWidget(thumbnail_path, title)

            # Kết nối sự kiện double click vào ảnh bìa để phát tín hiệu phóng to ảnh
            item_widget.image_label.doubleClicked.connect(
                lambda path=cover_path: self.view_image_requested.emit(path)
            )

            item.setSizeHint(item_widget.sizeHint())
            self.addItem(item)
            self.setItemWidget(item, item_widget)

    def _on_item_double_clicked(self, item: QListWidgetItem) -> None:
        """Slot nội bộ điều hướng sự kiện nhấp đúp xem chi tiết.

        Args:
            item: QListWidgetItem được click.
        """
        book_id = item.data(Qt.ItemDataRole.UserRole)
        if book_id is not None:
            self.book_selected.emit(book_id)
