# Tên file: frontend/components/book_table_widget.py
# CHANGELOG:
# - 2024-08-06: [NÂNG CẤP] Thêm action "Làm mới ảnh bìa" vào menu chuột phải và phát tín hiệu thumbnail_refresh_requested. (AI Studio)
# - 2024-08-06: [TÁI CẤU TRÚC] Lấy danh sách cột và tiêu đề từ data_model.py thay vì hard-code. (AI Studio)
# - 2024-08-06: [VÁ LỖI] Sửa lỗi crash khi lọc. Thay vì truy cập self.parent(), widget sẽ phát ra tín hiệu header_filter_applied để MainWindow xử lý. (AI Studio)
# - 2024-08-06: [TỐI ƯU] Sửa logic hiển thị ảnh để load từ thumbnail cache thay vì ảnh gốc, giúp tăng tốc độ render. (AI Studio)
# - 2024-08-06: [KHỞI TẠO] Tách toàn bộ logic và UI của bảng hiển thị sách từ MainWindow vào widget riêng biệt này. (AI Studio)

import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel,
                             QHeaderView, QMenu, QInputDialog, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QAction
from backend.database import (update_book_field, delete_book, get_distinct_column_values, get_book_by_id)
from backend.rag_service import embed_and_store_book, remove_book_from_chroma
from backend.utils import get_thumbnail_path
from backend.data_model import get_db_columns, get_column_headers

class BookTableWidget(QWidget):
    """
    Widget chuyên quản lý việc hiển thị và tương tác với bảng dữ liệu sách.
    """
    data_changed = pyqtSignal()
    filter_triggered = pyqtSignal()
    view_image_requested = pyqtSignal(str)
    status_message_changed = pyqtSignal(str)
    header_filter_applied = pyqtSignal(str, object)
    thumbnail_refresh_requested = pyqtSignal(int) # book_id

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_loading_data = False
        self.db_columns = get_db_columns()
        self.column_headers = get_column_headers()
        self.initUI()

    def initUI(self):
        """Khởi tạo giao diện người dùng cho widget bảng."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setSortingEnabled(False)
        
        self.table.setColumnCount(len(self.column_headers))
        self.table.setHorizontalHeaderLabels(self.column_headers)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnHidden(self.db_columns.index('id'), True)
        self.table.setWordWrap(True)
        self.table.cellChanged.connect(self.on_cell_changed)
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_row_context_menu)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setStretchLastSection(False)
        header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        header.customContextMenuRequested.connect(self.show_header_context_menu)
        
        layout.addWidget(self.table)
        self.setLayout(layout)

    def display_books(self, books):
        """Xóa bảng và hiển thị danh sách sách mới."""
        self.is_loading_data = True
        self.table.setRowCount(0)
        for book_dict in books:
            self.add_book_to_table(dict(book_dict))
        self.table.resizeRowsToContents()
        self.is_loading_data = False

    def add_book_to_table(self, book_dict, at_top=False):
        """Thêm một hàng sách vào bảng."""
        row_position = 0 if at_top else self.table.rowCount()
        self.table.insertRow(row_position)
        
        for col_idx, db_col in enumerate(self.db_columns):
            value = book_dict.get(db_col)
            
            if db_col == 'cover_path' and value:
                book_id = book_dict.get('id')
                thumbnail_path = get_thumbnail_path(book_id, value)
                if thumbnail_path and os.path.exists(thumbnail_path):
                    pixmap = QPixmap(thumbnail_path)
                    if not pixmap.isNull():
                        label = QLabel()
                        label.setPixmap(pixmap) # Không cần scale vì thumbnail đã đúng kích thước
                        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.table.setCellWidget(row_position, col_idx, label)
                        self.table.setRowHeight(row_position, 130)
            else:
                item = QTableWidgetItem(str(value) if value is not None else "")
                if db_col == 'id':
                    item.setData(Qt.ItemDataRole.UserRole, value)
                
                if db_col in ["status", "cover_path"]:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

                self.table.setItem(row_position, col_idx, item)

    def show_header_context_menu(self, pos):
        """Hiển thị menu ngữ cảnh cho header để lọc."""
        header = self.table.horizontalHeader()
        column_index = header.logicalIndexAt(pos)
        db_col = self.db_columns[column_index]

        if db_col in ["id", "cover_path", "review", "danh_gia_ca_nhan"]:
            return

        menu = QMenu(self)
        
        action_clear = QAction("Xóa bộ lọc này", self)
        action_clear.triggered.connect(lambda: self.header_filter_applied.emit(db_col, None))
        menu.addAction(action_clear)
        menu.addSeparator()

        values = get_distinct_column_values(db_col)
        for value in values[:30]:
            action = QAction(str(value), self)
            action.triggered.connect(lambda checked=False, c=db_col, v=value: self.header_filter_applied.emit(c, v))
            menu.addAction(action)
        
        menu.exec(header.mapToGlobal(pos))

    def show_row_context_menu(self, pos):
        """Hiển thị menu ngữ cảnh cho một hàng (xóa sách)."""
        row = self.table.rowAt(pos.y())
        if row < 0:
            return
            
        book_id_item = self.table.item(row, self.db_columns.index('id'))
        if not book_id_item:
            return
        book_id = book_id_item.data(Qt.ItemDataRole.UserRole)

        menu = QMenu(self)
        
        action_refresh_cover = QAction("Làm mới ảnh bìa", self)
        action_refresh_cover.triggered.connect(lambda: self.thumbnail_refresh_requested.emit(book_id))
        menu.addAction(action_refresh_cover)
        
        menu.addSeparator()

        action_delete = QAction("Xóa sách này", self)
        action_delete.triggered.connect(lambda: self.delete_selected_book(row))
        menu.addAction(action_delete)
        
        menu.exec(self.table.viewport().mapToGlobal(pos))

    def delete_selected_book(self, row):
        """Xử lý logic xóa sách."""
        book_id_item = self.table.item(row, self.db_columns.index('id'))
        if not book_id_item:
            return
        book_id = book_id_item.data(Qt.ItemDataRole.UserRole)
        book_title = self.table.item(row, self.db_columns.index('ten_sach')).text()

        reply = QMessageBox.question(self, "Xác nhận xóa", f"Bạn có chắc muốn xóa vĩnh viễn cuốn sách:\n'{book_title}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            delete_book(book_id)
            remove_book_from_chroma(book_id)
            self.filter_triggered.emit()
            self.status_message_changed.emit(f"Đã xóa sách '{book_title}'")

    def on_cell_changed(self, row, column):
        """Xử lý khi dữ liệu trong một ô bị thay đổi."""
        if self.is_loading_data:
            return
        
        db_col = self.db_columns[column]
        if db_col in ["id", "cover_path", "status"]:
            return

        book_id_item = self.table.item(row, self.db_columns.index('id'))
        if not book_id_item:
            return
        
        book_id = book_id_item.data(Qt.ItemDataRole.UserRole)
        new_value = self.table.item(row, column).text()
        
        update_book_field(book_id, db_col, new_value)
        embed_and_store_book(book_id)
        self.status_message_changed.emit(f"Đã cập nhật '{self.column_headers[column]}'")
        self.data_changed.emit()

    def on_cell_double_clicked(self, row, column):
        """Xử lý khi một ô được nháy đúp."""
        db_col = self.db_columns[column]
        if db_col == "status":
            self.show_status_menu(row)
        elif db_col == "cover_path":
            book_id_item = self.table.item(row, self.db_columns.index('id'))
            if not book_id_item:
                return
            book_id = book_id_item.data(Qt.ItemDataRole.UserRole)
            book = get_book_by_id(book_id)
            if book and book['cover_path']:
                self.view_image_requested.emit(book['cover_path'])
        else:
            item = self.table.item(row, column)
            if item and item.flags() & Qt.ItemFlag.ItemIsEditable:
                self.table.editItem(item)

    def show_status_menu(self, row):
        """Hiển thị menu để thay đổi trạng thái đọc sách."""
        book_id_item = self.table.item(row, self.db_columns.index('id'))
        if not book_id_item:
            return
        book_id = book_id_item.data(Qt.ItemDataRole.UserRole)

        menu = QMenu(self)
        action_unread = QAction("Chưa đọc", self)
        action_unread.triggered.connect(lambda: self.update_status(book_id, row, "Chưa đọc"))
        menu.addAction(action_unread)

        action_reading = QAction("Đang đọc", self)
        action_reading.triggered.connect(lambda: self.update_status_reading(book_id, row))
        menu.addAction(action_reading)

        action_read = QAction("Đã đọc", self)
        action_read.triggered.connect(lambda: self.update_status(book_id, row, "Đã đọc"))
        menu.addAction(action_read)
        menu.exec(self.cursor().pos())

    def update_status(self, book_id, row, status):
        """Cập nhật trạng thái và giao diện."""
        update_book_field(book_id, 'status', status)
        self.table.item(row, self.db_columns.index('status')).setText(status)
        embed_and_store_book(book_id)
        self.status_message_changed.emit("Đã cập nhật trạng thái")
        self.data_changed.emit()

    def update_status_reading(self, book_id, row):
        """Cập nhật trạng thái 'Đang đọc' với số trang."""
        total_pages_item = self.table.item(row, self.db_columns.index('so_trang'))
        total_pages = int(total_pages_item.text()) if total_pages_item and total_pages_item.text().isdigit() else 0
        
        new_status = "Đang đọc"
        if total_pages > 0:
            current_page, ok = QInputDialog.getInt(self, "Tiến độ đọc", f"Đã đọc đến trang (trên tổng số {total_pages}):", 0, 0, total_pages)
            if ok:
                new_status = f"Đang đọc ({current_page}/{total_pages})"
        
        self.update_status(book_id, row, new_status)