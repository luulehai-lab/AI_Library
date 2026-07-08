# Tên file: frontend/components/add_book_dialog.py
# CHANGELOG:
# - 2024-08-06: [TÁI CẤU TRÚC] Tự động sinh form nhập liệu từ data_model.py thay vì hard-code. (AI Studio)
# - 2024-08-06: [TÁI CẤU TRÚC] Sửa get_book_data để trả về key là tên cột DB (vd: 'ten_sach'), nhất quán với hàm add_book mới. (AI Studio)
# - 2024-08-06: [VÁ LỖI] Sửa hàm get_book_data để trả về dictionary với key là Tiếng Việt có dấu (ví dụ: 'Tên sách'), khớp với định dạng mà hàm database.add_book yêu cầu. (AI Studio)
# - 2024-08-06: [KHỞI TẠO] Tạo dialog cho phép người dùng nhập thông tin sách mới một cách thủ công. (AI Studio)

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, 
                             QSpinBox, QDoubleSpinBox, QDialogButtonBox, QMessageBox)
from backend.data_model import get_form_fields

class AddBookDialog(QDialog):
    """
    Dialog để thêm một cuốn sách mới vào thư viện bằng cách nhập liệu thủ công.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm sách mới thủ công")
        self.setMinimumSize(600, 700)

        self.fields = {}
        self.initUI()

    def initUI(self):
        """Khởi tạo giao diện người dùng của dialog."""
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        form_fields = get_form_fields()

        for db_key, details in form_fields.items():
            widget_class = details["widget"]
            props = details["widget_props"]
            label = details["label"]
            
            widget = widget_class()
            if isinstance(widget, QLineEdit):
                if "placeholder" in props:
                    widget.setPlaceholderText(props["placeholder"])
                if "text" in props:
                    widget.setText(props["text"])
            elif isinstance(widget, QSpinBox):
                widget.setRange(props["range"][0], props["range"][1])
                widget.setValue(props["value"])
            elif isinstance(widget, QDoubleSpinBox):
                widget.setRange(props["range"][0], props["range"][1])
                widget.setValue(props["value"])
                widget.setDecimals(props["decimals"])
            elif isinstance(widget, QTextEdit):
                widget.setMinimumHeight(80)
            
            self.fields[db_key] = widget
            form_layout.addRow(f"{label}:", widget)

        layout.addLayout(form_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.on_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def on_accept(self):
        """Kiểm tra dữ liệu trước khi chấp nhận dialog."""
        if not self.fields['ten_sach'].text().strip():
            QMessageBox.warning(self, "Thiếu thông tin", "Tên sách là trường bắt buộc.")
            return
        self.accept()

    def get_book_data(self):
        """Lấy dữ liệu từ các trường và trả về dict với key là tên cột DB."""
        data = {}
        for db_key, widget in self.fields.items():
            value = None
            if isinstance(widget, QLineEdit):
                value = widget.text().strip()
            elif isinstance(widget, QTextEdit):
                value = widget.toPlainText().strip()
            elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                value = widget.value()
            
            data[db_key] = value if value else None
        
        return data