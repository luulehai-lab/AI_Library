# Tên file: frontend/main_window.py
# CHỨC NĂNG: Cửa sổ giao diện chính điều phối toàn bộ các widget và luồng xử lý thư viện sách.
# CHANGELOG:
# - 10:28:00 08/07/2026: [REFACTOR] Tách các widget Banner, Gallery, DetailDialog, ExcelWorker và làm sạch code. (Antigravity)
# - 2024-08-06: [NÂNG CẤP] Thêm slot on_thumbnail_refresh_requested và xử lý logic xoay ảnh trong on_processing_finished. (AI Studio)
# - 2024-08-06: [NÂNG CẤP] Tích hợp DashboardWidget vào giao diện chính và thêm nút chuyển đổi. (AI Studio)
# - 2024-08-06: [VÁ LỖI] Thêm slot on_header_filter_applied và kết nối với tín hiệu từ BookTableWidget để xử lý logic lọc, sửa lỗi crash. (AI Studio)
# - 2024-08-06: [TỐI ƯU] Cập nhật luồng xử lý AI và thủ công để tạo thumbnail sau khi thêm sách, giúp tăng tốc độ tải. (AI Studio)
# - 2024-08-06: [VÁ LỖI] Chuẩn hóa việc truyền dữ liệu cho hàm add_book, đảm bảo luồng AI và thủ công đều dùng key là tên cột DB. (AI Studio)
# - 2024-08-06: [NÂNG CẤP] Thêm nút "Thêm sách thủ công" và logic để mở dialog, xử lý dữ liệu trả về, và lưu sách mới. (AI Studio)
# - 2024-08-06: [TÁI CẤU TRÚC] Tách toàn bộ logic và UI của bảng hiển thị sách ra BookTableWidget. MainWindow giờ chỉ quản lý và kết nối tín hiệu. (AI Studio)
# - 2024-08-06: [TÁI CẤU TRÚC] Tách toàn bộ logic và UI của khu vực chat ra ChatWidget riêng biệt. MainWindow chỉ còn nhiệm vụ khởi tạo và thêm widget này. (AI Studio)
# - 2024-08-06: [NÂNG CẤP] Cập nhật phiên bản lên 1.7.0. (AI Studio)

import os
import shutil
import re
from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QProgressBar,
    QLabel,
    QMessageBox,
    QLineEdit,
    QStatusBar,
    QStackedWidget,
    QDialog,
    QScrollArea,
    QSplitter,
)
from PyQt6.QtCore import QThread, Qt, QSettings, QTimer, QUrl
from PyQt6.QtGui import QDesktopServices, QPixmap
from typing import Any

from backend.ai_service import AIServiceWorker
from backend.database import (
    get_filtered_books,
    add_book,
    get_library_stats,
    get_book_by_id,
)
from backend.rag_service import embed_and_store_book
from backend.utils import find_cover_image, create_thumbnail, rotate_image_file
from backend.data_model import get_ai_to_db_key_map
from config import APP_NAME, APP_VERSION, SETTINGS_ORGANIZATION, SETTINGS_APP_NAME

from .styles import STYLESHEET
from .components.chat_widget import ChatWidget
from .components.book_table_widget import BookTableWidget
from .components.add_book_dialog import AddBookDialog
from .components.dashboard_widget import DashboardWidget
from .components.banner_widget import BannerWidget
from .components.book_gallery_widget import BookGalleryWidget
from .components.book_detail_dialog import BookDetailDialog
from .excel_worker import ExcelExportWorker


class MainWindow(QMainWindow):
    """Cửa sổ chính điều khiển giao diện ứng dụng quản lý thư viện."""

    def __init__(self):
        super().__init__()
        self.thread = None
        self.worker = None
        self.export_thread = None
        self.export_worker = None
        self.image_queue = []
        self.total_images_in_queue = 0
        self.active_filters = {}
        self.sort_column = None
        self.sort_order = Qt.SortOrder.AscendingOrder

        self.filter_timer = QTimer(self)
        self.filter_timer.setSingleShot(True)
        self.filter_timer.timeout.connect(self.trigger_filter)

        self.grand_total_stats = {}

        self.initUI()
        self.load_settings()
        self.load_books_from_db()

    def initUI(self) -> None:
        """Khởi tạo và sắp xếp giao diện cửa sổ."""
        self.setWindowTitle(f"{APP_NAME} - v{APP_VERSION}")
        self.setGeometry(100, 100, 1800, 1000)
        self.setStyleSheet(STYLESHEET)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # BannerArea đã được module hóa
        self.banner_widget = BannerWidget(self)
        self.layout.addWidget(self.banner_widget)

        self.setup_control_bar()

        main_splitter = QSplitter(Qt.Orientation.Vertical)
        self.layout.addWidget(main_splitter)

        # Setup view container (Table, Gallery, Dashboard)
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        self.stacked_widget = QStackedWidget()
        top_layout.addWidget(self.stacked_widget)
        main_splitter.addWidget(top_widget)

        # 1. BookTableWidget
        self.book_table_widget = BookTableWidget(self)
        self.stacked_widget.addWidget(self.book_table_widget)

        # 2. BookGalleryWidget
        self.gallery_widget = BookGalleryWidget(self)
        self.stacked_widget.addWidget(self.gallery_widget)

        # 3. DashboardWidget
        self.dashboard_widget = DashboardWidget(self)
        self.stacked_widget.addWidget(self.dashboard_widget)

        # ChatWidget
        self.chat_widget = ChatWidget(self)
        main_splitter.addWidget(self.chat_widget)
        main_splitter.setSizes([800, 250])

        self.setup_status_area()
        self.connect_signals()

    def setup_control_bar(self) -> None:
        """Thiết lập thanh công cụ điều khiển chính."""
        control_layout = QHBoxLayout()
        self.add_banner_button = QPushButton("Thêm ảnh bìa...")
        control_layout.addWidget(self.add_banner_button)

        self.clear_banner_button = QPushButton("Xóa ảnh bìa")
        control_layout.addWidget(self.clear_banner_button)

        self.library_title = QLabel("THƯ VIỆN GIA ĐÌNH LÊ HẢI LƯU")
        self.library_title.setObjectName("libraryTitleLabel")
        control_layout.addWidget(self.library_title, 0, Qt.AlignmentFlag.AlignCenter)
        control_layout.addStretch(1)

        self.add_manual_button = QPushButton("Thêm sách thủ công...")
        control_layout.addWidget(self.add_manual_button)

        self.upload_button = QPushButton("Xử lý thư mục Input")
        control_layout.addWidget(self.upload_button)

        self.export_button = QPushButton("Xuất Excel...")
        self.setup_export_menu()
        control_layout.addWidget(self.export_button)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm chung...")
        control_layout.addWidget(self.search_input)

        self.view_toggle_button = QPushButton("Xem dạng Lưới")
        control_layout.addWidget(self.view_toggle_button)

        # Nút chuyển sang Dashboard
        self.dashboard_button = QPushButton("Dashboard")
        self.dashboard_button.clicked.connect(self.toggle_dashboard)
        control_layout.addWidget(self.dashboard_button)

        self.layout.addLayout(control_layout)

    def setup_status_area(self) -> None:
        """Thiết lập khu vực hiển thị trạng thái và thanh tiến trình."""
        self.status_label = QLabel("Sẵn sàng.")
        self.layout.addWidget(self.status_label)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.layout.addWidget(self.progress_bar)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def connect_signals(self) -> None:
        """Kết nối các tín hiệu chính giữa MainWindow và các components con."""
        # Điều phối Banner
        self.add_banner_button.clicked.connect(self.banner_widget.add_banner_images)
        self.clear_banner_button.clicked.connect(self.banner_widget.clear_banner_images)

        # Nút chức năng
        self.add_manual_button.clicked.connect(self.show_add_manual_dialog)
        self.upload_button.clicked.connect(self.start_processing)
        self.search_input.textChanged.connect(self.apply_filters_debounced)
        self.view_toggle_button.clicked.connect(self.toggle_view)

        # Tín hiệu từ BookTableWidget
        self.book_table_widget.table.horizontalHeader().sectionClicked.connect(
            self.on_header_clicked
        )
        self.book_table_widget.data_changed.connect(self.update_status_bar)
        self.book_table_widget.filter_triggered.connect(self.trigger_filter)
        self.book_table_widget.view_image_requested.connect(self.show_full_size_image)
        self.book_table_widget.status_message_changed.connect(
            lambda msg: self.status_bar.showMessage(msg, 3000)
        )
        self.book_table_widget.header_filter_applied.connect(
            self.on_header_filter_applied
        )
        self.book_table_widget.thumbnail_refresh_requested.connect(
            self.on_thumbnail_refresh_requested
        )

        # Tín hiệu từ BookGalleryWidget (Đã module hóa)
        self.gallery_widget.book_selected.connect(self.display_book_dialog)
        self.gallery_widget.view_image_requested.connect(self.show_full_size_image)

    def on_thumbnail_refresh_requested(self, book_id: int) -> None:
        """Slot để làm mới thumbnail khi người dùng yêu cầu."""
        book = get_book_by_id(book_id)
        if book and book["cover_path"]:
            create_thumbnail(book["cover_path"], book_id)
            self.status_bar.showMessage(
                f"Đã làm mới ảnh bìa cho sách ID {book_id}", 3000
            )
            self.trigger_filter()  # Tải lại để hiển thị ảnh mới
        else:
            self.status_bar.showMessage(
                f"Không tìm thấy ảnh bìa để làm mới cho sách ID {book_id}", 3000
            )

    def on_header_filter_applied(self, column: str, value: Any) -> None:
        """Slot để xử lý khi người dùng chọn một bộ lọc từ header."""
        if value is None:
            self.active_filters.pop(column, None)
        else:
            self.active_filters[column] = value
        self.trigger_filter()

    def show_add_manual_dialog(self) -> None:
        """Mở dialog để thêm sách thủ công và xử lý kết quả."""
        dialog = AddBookDialog(self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            book_data = dialog.get_book_data()

            book_title = book_data.get("ten_sach")
            cover_path = find_cover_image(book_title)
            book_data["cover_path"] = cover_path

            try:
                book_id = add_book(book_data)
                if cover_path:
                    create_thumbnail(cover_path, book_id)

                embed_and_store_book(book_id)
                self.trigger_filter()
                self.status_bar.showMessage(
                    f"Đã thêm thành công sách '{book_title}'", 5000
                )
            except Exception as e:
                self.show_error(f"Lỗi khi lưu sách mới: {e}")

    def setup_export_menu(self) -> None:
        """Thiết lập menu xuất dữ liệu Excel."""
        from PyQt6.QtGui import QAction
        from PyQt6.QtWidgets import QMenu

        menu = QMenu(self)
        action_export_selected = QAction("Xuất các sách đã chọn", self)
        action_export_selected.triggered.connect(self.export_selected_to_excel)
        menu.addAction(action_export_selected)

        action_export_all = QAction("Xuất toàn bộ thư viện", self)
        action_export_all.triggered.connect(self.export_all_to_excel)
        menu.addAction(action_export_all)

        self.export_button.setMenu(menu)

    def on_header_clicked(self, logical_index: int) -> None:
        """Sắp xếp danh sách sách khi nhấp vào tiêu đề cột của bảng."""
        db_col = self.book_table_widget.db_columns[logical_index]
        if db_col in ["id", "cover_path"]:
            return

        if self.sort_column == db_col:
            self.sort_order = (
                Qt.SortOrder.DescendingOrder
                if self.sort_order == Qt.SortOrder.AscendingOrder
                else Qt.SortOrder.AscendingOrder
            )
        else:
            self.sort_column = db_col
            self.sort_order = Qt.SortOrder.AscendingOrder

        self.book_table_widget.table.horizontalHeader().setSortIndicator(
            logical_index, self.sort_order
        )
        self.trigger_filter()

    def toggle_view(self) -> None:
        """Chuyển đổi giữa các chế độ xem: Bảng <-> Lưới."""
        current_index = self.stacked_widget.currentIndex()
        if current_index == 2:
            self.stacked_widget.setCurrentIndex(0)
            self.view_toggle_button.setText("Xem dạng Lưới")
            self.dashboard_button.setEnabled(True)
        elif current_index == 0:
            self.stacked_widget.setCurrentIndex(1)
            self.view_toggle_button.setText("Xem dạng Bảng")
        else:
            self.stacked_widget.setCurrentIndex(0)
            self.view_toggle_button.setText("Xem dạng Lưới")

    def toggle_dashboard(self) -> None:
        """Chuyển sang chế độ xem Dashboard."""
        self.stacked_widget.setCurrentIndex(2)  # Index 2 là DashboardWidget
        self.dashboard_widget.refresh_data()  # Cập nhật dữ liệu mới nhất
        self.view_toggle_button.setText("Quay lại Thư viện")
        self.dashboard_button.setEnabled(
            False
        )  # Vô hiệu hóa nút Dashboard khi đang xem nó

    def load_books_from_db(self, books: list[Any] | None = None) -> None:
        """Tải dữ liệu từ DB và cập nhật cho Table View và Gallery View."""
        if books is None:
            self.grand_total_stats = get_library_stats()
            sort_order_str = (
                "ASC" if self.sort_order == Qt.SortOrder.AscendingOrder else "DESC"
            )
            books = get_filtered_books(
                self.active_filters,
                self.search_input.text(),
                self.sort_column,
                sort_order_str,
            )

        # Cập nhật cả hai view
        self.book_table_widget.display_books(books)
        self.gallery_widget.display_books(books)
        self.update_status_bar(books)

    def apply_filters_debounced(self) -> None:
        """Độ trễ xử lý lọc tìm kiếm (debouncing) tránh lag UI."""
        self.filter_timer.start(400)

    def trigger_filter(self) -> None:
        """Thực thi lọc tìm kiếm."""
        sort_order_str = (
            "ASC" if self.sort_order == Qt.SortOrder.AscendingOrder else "DESC"
        )
        books = get_filtered_books(
            self.active_filters,
            self.search_input.text(),
            self.sort_column,
            sort_order_str,
        )
        self.load_books_from_db(books)

    def start_processing(self) -> None:
        """Quét thư mục ảnh images_input và đưa các ảnh vào hàng đợi AI để xử lý."""
        if not self.upload_button.isEnabled():
            return

        input_dir = "images_input"
        valid_extensions = [".png", ".jpg", ".jpeg", ".bmp"]

        try:
            all_files = os.listdir(input_dir)
            image_files = [
                os.path.join(input_dir, f)
                for f in all_files
                if os.path.splitext(f)[1].lower() in valid_extensions
            ]
        except FileNotFoundError:
            self.show_error(f"Thư mục '{input_dir}' không tồn tại.")
            return

        if not image_files:
            QMessageBox.information(
                self,
                "Thông báo",
                f"Không tìm thấy ảnh nào trong thư mục '{input_dir}'.\n\nVui lòng sao chép ảnh bạn muốn xử lý vào đó.",
            )
            return

        self.image_queue.clear()
        self.image_queue.extend(image_files)

        self.total_images_in_queue = len(self.image_queue)
        self.upload_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.process_next_in_queue()

    def process_next_in_queue(self) -> None:
        """Lấy ảnh tiếp theo trong queue để chạy QThread AI."""
        if not self.image_queue:
            self.status_label.setText("Hoàn tất xử lý tất cả các ảnh!")
            self.upload_button.setEnabled(True)
            self.progress_bar.setVisible(False)
            self.grand_total_stats = get_library_stats()
            self.update_status_bar()
            return

        current_path = self.image_queue.pop(0)
        current_count = self.total_images_in_queue - len(self.image_queue)
        self.status_label.setText(
            f"Đang xử lý ảnh {current_count} trên {self.total_images_in_queue}..."
        )
        self.progress_bar.setValue(0)

        self.thread = QThread(self)
        self.worker = AIServiceWorker(current_path)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_processing_finished)
        self.worker.error.connect(self.on_error)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def update_progress(self, value: int, message: str) -> None:
        """Cập nhật giá trị thanh tiến trình."""
        self.progress_bar.setValue(value)
        self.status_label.setText(
            f"Ảnh {self.total_images_in_queue - len(self.image_queue) + 1}/{self.total_images_in_queue}: {message}"
        )

    def on_error(self, message: str) -> None:
        """Báo lỗi khi thread gặp ngoại lệ."""
        self.show_error(message)
        self.process_next_in_queue()

    def on_processing_finished(
        self, data_from_ai: dict[str, Any], rotation_angle: int
    ) -> None:
        """Xử lý kết quả trả về từ AI (xoay ảnh, lưu DB, tạo thumbnail và ChromaDB)."""
        source_path = self.worker.image_path

        # Xoay ảnh gốc trước khi xử lý
        if rotation_angle != 0:
            rotate_image_file(source_path, rotation_angle)

        processed_path = self.process_image_file(data_from_ai)

        key_map = get_ai_to_db_key_map()
        book_data = {
            db_key: data_from_ai.get(ai_key) for ai_key, db_key in key_map.items()
        }
        book_data["cover_path"] = processed_path

        book_id = add_book(book_data)
        if processed_path:
            create_thumbnail(processed_path, book_id)

        embed_and_store_book(book_id)
        self.trigger_filter()
        self.process_next_in_queue()

    def process_image_file(self, data: dict[str, Any]) -> str | None:
        """Di chuyển file ảnh bìa sang thư mục ảnh đã xử lý."""
        path_to_process = self.worker.image_path
        book_title = data.get(
            "Tên sách", f"unknown_book_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )
        safe_title = "".join(
            c for c in book_title if c.isalnum() or c in (" ", ".", "_")
        ).rstrip()

        if path_to_process and os.path.exists(path_to_process):
            _, extension = os.path.splitext(path_to_process)
            new_filename = f"{safe_title}{extension}"
            destination_path = os.path.join("images_processed", new_filename)
            try:
                shutil.move(path_to_process, destination_path)
                return destination_path
            except OSError as e:
                self.show_error(f"Không thể di chuyển/đổi tên file ảnh: {e}")
        return None

    def update_status_bar(self, filtered_books: list[Any] | None = None) -> None:
        """Cập nhật thống kê chi tiết hiển thị ở thanh StatusBar phía dưới cùng."""
        if filtered_books is None:
            stats = get_library_stats()
            self.grand_total_stats = stats
            self.status_bar.showMessage(
                f"Tổng sách: {stats.get('total_books', 0)} | Tổng trang: {stats.get('total_pages', 0):,} | Đang đọc: {stats.get('total_pages_reading', 0):,} trang | Tổng giá trị: {stats.get('total_price', 0):,.0f} VNĐ"
            )
            return

        filtered_count = len(filtered_books)
        filtered_pages = 0
        filtered_price = 0
        filtered_reading = 0

        for book in filtered_books:
            try:
                filtered_pages += int(book["so_trang"] or 0)
            except (ValueError, TypeError):
                pass
            try:
                filtered_price += int(book["gia_tiki"] or 0)
            except (ValueError, TypeError):
                pass
            if book["status"] and book["status"].startswith("Đang đọc"):
                match = re.search(r"\((\d+)/", book["status"])
                if match:
                    try:
                        filtered_reading += int(match.group(1))
                    except (ValueError, IndexError):
                        continue

        gt = self.grand_total_stats
        msg = (
            f"Hiển thị: {filtered_count}/{gt.get('total_books', 0)} sách | "
            f"Trang: {filtered_pages:,}/{gt.get('total_pages', 0):,} | "
            f"Đang đọc: {filtered_reading:,}/{gt.get('total_pages_reading', 0):,} | "
            f"Giá trị: {filtered_price:,.0f}/{gt.get('total_price', 0):,.0f} VNĐ"
        )
        self.status_bar.showMessage(msg)

    def display_book_dialog(self, book_id: int) -> None:
        """Mở dialog xem chi tiết thông tin sách."""
        book_data = get_book_by_id(book_id)
        if not book_data:
            self.show_error("Không tìm thấy thông tin sách.")
            return

        # Sử dụng Dialog đã tách rời module
        dialog = BookDetailDialog(dict(book_data), self)
        dialog.view_image_requested.connect(self.show_full_size_image)
        dialog.exec()

    def show_full_size_image(self, image_path: str) -> None:
        """Hiển thị ảnh bìa phóng to đầy đủ."""
        if not image_path or not os.path.exists(image_path):
            self.show_error("Không tìm thấy file ảnh.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle(os.path.basename(image_path))

        pixmap = QPixmap(image_path)
        label = QLabel()
        label.setPixmap(pixmap)

        scroll_area = QScrollArea()
        scroll_area.setWidget(label)

        layout = QVBoxLayout(dialog)
        layout.addWidget(scroll_area)

        dialog.resize(min(pixmap.width() + 40, 1200), min(pixmap.height() + 40, 800))
        dialog.exec()

    def show_error(self, message: str) -> None:
        """Hiển thị thông báo lỗi popup."""
        QMessageBox.critical(self, "Lỗi", message)

    def resizeEvent(self, event: Any) -> None:
        """Xử lý sự kiện thay đổi kích thước cửa sổ."""
        super().resizeEvent(event)
        self.banner_widget.refresh_banner()

    def closeEvent(self, event: Any) -> None:
        """Lưu cài đặt hình học của cửa sổ trước khi tắt."""
        self.save_settings()
        super().closeEvent(event)

    def save_settings(self) -> None:
        """Lưu kích thước và trạng thái layout cửa sổ chính."""
        settings = QSettings(SETTINGS_ORGANIZATION, SETTINGS_APP_NAME)
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        settings.setValue(
            "tableHeaderState",
            self.book_table_widget.table.horizontalHeader().saveState(),
        )

    def load_settings(self) -> None:
        """Nạp lại cấu hình hình học cửa sổ chính."""
        settings = QSettings(SETTINGS_ORGANIZATION, SETTINGS_APP_NAME)
        geometry = settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)

        state = settings.value("windowState")
        if state:
            self.restoreState(state)

        header_state = settings.value("tableHeaderState")
        if header_state:
            self.book_table_widget.table.horizontalHeader().restoreState(header_state)

    def export_selected_to_excel(self) -> None:
        """Xuất các dòng được bôi xanh trong bảng ra file Excel."""
        selected_rows = sorted(
            list(
                set(
                    index.row()
                    for index in self.book_table_widget.table.selectedIndexes()
                )
            )
        )
        if not selected_rows:
            QMessageBox.information(
                self, "Thông báo", "Vui lòng chọn ít nhất một hàng để xuất."
            )
            return

        table = self.book_table_widget.table
        db_cols = self.book_table_widget.db_columns
        book_ids = [
            table.item(row, db_cols.index("id")).data(Qt.ItemDataRole.UserRole)
            for row in selected_rows
        ]
        books_data = [
            dict(get_book_by_id(bid)) for bid in book_ids if get_book_by_id(bid)
        ]
        self.export_to_excel(books_data)

    def export_all_to_excel(self) -> None:
        """Xuất toàn bộ thư viện sách ra file Excel."""
        sort_order_str = (
            "ASC" if self.sort_order == Qt.SortOrder.AscendingOrder else "DESC"
        )
        books_data = [
            dict(book)
            for book in get_filtered_books(
                self.active_filters,
                self.search_input.text(),
                self.sort_column,
                sort_order_str,
            )
        ]
        self.export_to_excel(books_data)

    def export_to_excel(self, book_data: list[dict[str, Any]]) -> None:
        """Khởi động QThread xuất Excel dưới nền để tránh treo UI."""
        if not book_data:
            QMessageBox.information(self, "Thông báo", "Không có dữ liệu để xuất.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Lưu file Excel", "", "Excel Files (*.xlsx)"
        )
        if not file_path:
            return

        self.status_label.setText("Đang chuẩn bị xuất ra file Excel...")
        self.upload_button.setEnabled(False)
        self.export_button.setEnabled(False)

        headers = [h for h in self.book_table_widget.column_headers if h != "ID"]
        db_cols = [c for c in self.book_table_widget.db_columns if c != "id"]

        self.export_thread = QThread(self)
        self.export_worker = ExcelExportWorker(file_path, headers, db_cols, book_data)
        self.export_worker.moveToThread(self.export_thread)

        self.export_thread.started.connect(self.export_worker.run)
        self.export_worker.finished.connect(self.on_export_finished)
        self.export_worker.error.connect(self.on_export_error)

        self.export_worker.finished.connect(self.export_thread.quit)
        self.export_worker.finished.connect(self.export_worker.deleteLater)
        self.export_thread.finished.connect(self.export_thread.deleteLater)

        self.export_thread.start()

    def on_export_finished(self, file_path: str) -> None:
        """Slot xử lý khi xuất Excel thành công."""
        self.status_label.setText(
            f"Đã xuất thành công ra file: {os.path.basename(file_path)}"
        )
        self.upload_button.setEnabled(True)
        self.export_button.setEnabled(True)

        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText("Xuất file Excel thành công!")
        msg_box.setInformativeText(f"File đã được lưu tại:\n{file_path}")

        btn_open_file = msg_box.addButton("Mở File", QMessageBox.ButtonRole.ActionRole)
        btn_open_folder = msg_box.addButton(
            "Mở Thư mục", QMessageBox.ButtonRole.ActionRole
        )
        msg_box.addButton("Đóng", QMessageBox.ButtonRole.RejectRole)

        msg_box.exec()

        if msg_box.clickedButton() == btn_open_file:
            QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.abspath(file_path)))
        elif msg_box.clickedButton() == btn_open_folder:
            QDesktopServices.openUrl(
                QUrl.fromLocalFile(os.path.dirname(os.path.abspath(file_path)))
            )

    def on_export_error(self, error_message: str) -> None:
        """Slot xử lý khi xuất Excel thất bại."""
        self.show_error(error_message)
        self.status_label.setText("Xuất file thất bại.")
        self.upload_button.setEnabled(True)
        self.export_button.setEnabled(True)
