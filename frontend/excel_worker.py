# Tên file: frontend/excel_worker.py
# CHỨC NĂNG: Worker chạy luồng ngầm PyQt để xuất dữ liệu ra Excel.
# CHANGELOG:
# - 10:28:00 08/07/2026: [NEW] Khởi tạo excel_worker. (Antigravity)

from PyQt6.QtCore import QObject, pyqtSignal
from typing import Any
from backend.excel_service import export_to_excel_file


class ExcelExportWorker(QObject):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(
        self,
        file_path: str,
        headers: list[str],
        db_columns: list[str],
        book_data: list[dict[str, Any]],
    ):
        """Khởi tạo Worker xuất Excel.

        Args:
            file_path: Đường dẫn file Excel đích.
            headers: Danh sách tiêu đề Excel.
            db_columns: Danh sách cột DB tương ứng.
            book_data: Danh sách dữ liệu sách.
        """
        super().__init__()
        self.file_path = file_path
        self.headers = headers
        self.db_columns = db_columns
        self.book_data = book_data

    def run(self) -> None:
        """Thực thi xuất file Excel trong luồng phụ."""
        try:
            export_to_excel_file(
                self.file_path, self.headers, self.db_columns, self.book_data
            )
            self.finished.emit(self.file_path)
        except Exception as e:
            self.error.emit(f"Lỗi khi xuất file Excel: {str(e)}")
