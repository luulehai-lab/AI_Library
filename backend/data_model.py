# Tên file: backend/data_model.py
# CHANGELOG:
# - 2024-08-06: [KHỞI TẠO] Tạo file định nghĩa mô hình dữ liệu tập trung (Single Source of Truth) cho ứng dụng. (AI Studio)

from collections import OrderedDict
from PyQt6.QtWidgets import QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox
from datetime import datetime

# Sử dụng OrderedDict để đảm bảo thứ tự các cột là nhất quán
BOOK_FIELDS = OrderedDict({
    "id": {
        "label": "ID",
        "db_type": "INTEGER PRIMARY KEY AUTOINCREMENT",
    },
    "cover_path": {
        "label": "Bìa sách",
        "db_type": "TEXT",
    },
    "ten_sach": {
        "label": "Tên sách",
        "ai_key": "Tên sách",
        "db_type": "TEXT",
        "widget": QLineEdit,
        "widget_props": {"placeholder": "Nhập tên sách đầy đủ..."}
    },
    "tac_gia": {
        "label": "Tác giả",
        "ai_key": "Tác giả",
        "db_type": "TEXT",
        "widget": QLineEdit,
        "widget_props": {"placeholder": "Nhập tên tác giả..."}
    },
    "quoc_gia": {
        "label": "Quốc gia",
        "ai_key": "Quốc gia",
        "db_type": "TEXT",
        "widget": QLineEdit,
        "widget_props": {"placeholder": "Quốc gia của tác giả..."}
    },
    "the_loai": {
        "label": "Thể loại",
        "ai_key": "Thể loại",
        "db_type": "TEXT",
        "widget": QLineEdit,
        "widget_props": {"placeholder": "Cách nhau bởi dấu phẩy, vd: Kinh điển,Tiểu thuyết"}
    },
    "lua_tuoi": {
        "label": "Lứa tuổi",
        "ai_key": "Lứa tuổi",
        "db_type": "TEXT",
        "widget": QLineEdit,
        "widget_props": {"placeholder": "Thiếu nhi, Người lớn..."}
    },
    "nxb": {
        "label": "NXB",
        "ai_key": "NXB",
        "db_type": "TEXT",
        "widget": QLineEdit,
        "widget_props": {"placeholder": "Nhà xuất bản..."}
    },
    "diem_goodreads": {
        "label": "Điểm Goodreads",
        "ai_key": "Điểm Goodreads",
        "db_type": "REAL",
        "widget": QDoubleSpinBox,
        "widget_props": {"range": (0.0, 5.0), "value": 0.0, "decimals": 2}
    },
    "review": {
        "label": "Review",
        "ai_key": "Review",
        "db_type": "TEXT",
        "widget": QTextEdit,
        "widget_props": {}
    },
    "danh_gia_ca_nhan": {
        "label": "Đánh giá cá nhân",
        "db_type": "TEXT",
        "widget": QTextEdit,
        "widget_props": {}
    },
    "vi_tri": {
        "label": "Vị trí",
        "db_type": "TEXT",
        "widget": QLineEdit,
        "widget_props": {"placeholder": "Kệ sách A, ngăn 2..."}
    },
    "status": {
        "label": "Status",
        "db_type": "TEXT DEFAULT 'Chưa đọc'",
        "widget": QLineEdit,
        "widget_props": {"text": "Chưa đọc"}
    },
    "nam_xuat_ban": {
        "label": "Năm xuất bản",
        "ai_key": "Năm xuất bản",
        "db_type": "INTEGER",
        "widget": QSpinBox,
        "widget_props": {"range": (1800, datetime.now().year), "value": datetime.now().year}
    },
    "gia_tiki": {
        "label": "Giá Tiki",
        "ai_key": "Giá Tiki",
        "db_type": "INTEGER",
        "widget": QSpinBox,
        "widget_props": {"range": (0, 10000000), "value": 0}
    },
    "so_trang": {
        "label": "Số trang",
        "ai_key": "Số trang",
        "db_type": "INTEGER",
        "widget": QSpinBox,
        "widget_props": {"range": (0, 10000), "value": 0}
    },
    "chat_luong_sach": {
        "label": "Chất lượng sách",
        "db_type": "TEXT",
        "widget": QLineEdit,
        "widget_props": {"placeholder": "Tốt, Bìa cứng..."}
    }
})

def get_db_columns():
    """Trả về danh sách tên các cột trong database."""
    return list(BOOK_FIELDS.keys())

def get_column_headers():
    """Trả về danh sách các tiêu đề cột để hiển thị trên UI."""
    return [details["label"] for details in BOOK_FIELDS.values()]

def get_ai_to_db_key_map():
    """Trả về một dictionary để ánh xạ key từ AI sang key của DB."""
    return {details["ai_key"]: db_key for db_key, details in BOOK_FIELDS.items() if "ai_key" in details}

def get_form_fields():
    """Trả về một OrderedDict các trường cần hiển thị trên form nhập liệu."""
    return OrderedDict({
        db_key: details for db_key, details in BOOK_FIELDS.items() 
        if "widget" in details and db_key != "id"
    })