# Tên file: frontend/styles.py
# CHANGELOG:
# - 2024-08-03: [TÁI CẤU TRÚC] Chuyển toàn bộ giao diện sang Light Theme để cải thiện độ đọc. (AI Studio)
# - 2024-08-02: [NÂNG CẤP] Thêm style cho các ô lọc (.filterLineEdit). (AI Studio)
# - 2024-08-01: [NÂNG CẤP] Thêm style cho tiêu đề thư viện (#libraryTitleLabel). (AI Studio)
# - 2024-07-31: [NÂNG CẤP] Cập nhật style cho banner đa ảnh và placeholder. (AI Studio)
# - 2024-07-31: [NÂNG CẤP] Thêm style cho banner và QScrollArea. (AI Studio)
# - 2024-07-30: [NÂNG CẤP] Thêm stylesheet cho giao diện dark mode chuyên nghiệp. (AI Studio)
# - 2024-07-29: [KHỞI TẠO] Tạo file để quản lý QSS (CSS cho Qt) trong tương lai. (AI Studio)

STYLESHEET = """
QWidget {
    background-color: #f0f0f0;
    color: #222222;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 14px;
}

QMainWindow {
    background-color: #e9e9e9;
}

#bannerScrollArea {
    background-color: #ffffff;
    border-radius: 5px;
    border: 1px solid #dcdcdc;
    margin-bottom: 10px;
}

#bannerPlaceholder {
    color: #888888;
    font-size: 22px;
    font-weight: bold;
}

#libraryTitleLabel {
    color: #005a9e;
    font-size: 18px;
    font-weight: bold;
    font-family: "Segoe Script", "Brush Script MT", cursive;
}

QPushButton {
    background-color: #0078d7;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 5px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #005a9e;
}

QPushButton:disabled {
    background-color: #dcdcdc;
    color: #888888;
}

QLineEdit {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 5px;
    padding: 8px;
}

QTableWidget {
    background-color: #ffffff;
    border: 1px solid #dcdcdc;
    gridline-color: #e0e0e0;
}

QTableWidget::item {
    padding: 5px;
    vertical-align: middle;
    border-bottom: 1px solid #e0e0e0;
}

QTableWidget::item:selected {
    background-color: #cce5ff;
    color: #222222;
}

QHeaderView::section {
    background-color: #e9e9e9;
    color: #005a9e;
    padding: 8px;
    border: 1px solid #dcdcdc;
    font-weight: bold;
}

QStatusBar {
    background-color: #e9e9e9;
    color: #333333;
    font-weight: bold;
}

QScrollBar:vertical {
    border: none;
    background: #e0e0e0;
    width: 14px;
    margin: 0px 0px 0px 0px;
}
QScrollBar::handle:vertical {
    background: #b0b0b0;
    min-height: 20px;
    border-radius: 7px;
}
QScrollBar:horizontal {
    border: none;
    background: #e0e0e0;
    height: 14px;
    margin: 0px 0px 0px 0px;
}
QScrollBar::handle:horizontal {
    background: #b0b0b0;
    min-width: 20px;
    border-radius: 7px;
}

QListWidget {
    background-color: #ffffff;
    border: 1px solid #dcdcdc;
}

QListWidget::item {
    background-color: #f9f9f9;
    color: #222222;
    border-radius: 5px;
    padding: 5px;
    margin: 5px;
    border: 1px solid #e0e0e0;
}

QDialog {
    background-color: #f8f8f8;
}

QTextEdit {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 5px;
}

QScrollArea {
    border: none;
}

QMenu {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    color: #222222;
}

QMenu::item:selected {
    background-color: #0078d7;
    color: #ffffff;
}

QSplitter::handle {
    background-color: #dcdcdc;
}
"""