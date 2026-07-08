# Tên file: frontend/components/chat_widget.py
# CHANGELOG:
# - 2024-08-06: [KHỞI TẠO] Tách toàn bộ logic và UI của khu vực chat từ MainWindow vào widget riêng biệt này để tái cấu trúc. (AI Studio)

import markdown
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTextEdit, QLineEdit, QPushButton)
from PyQt6.QtCore import QThread
from backend.rag_service import ChatWorker

class ChatWidget(QWidget):
    """
    Widget quản lý toàn bộ giao diện và logic cho khu vực trò chuyện với AI.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.chat_thread = None
        self.chat_worker = None
        self.initUI()

    def initUI(self):
        """Khởi tạo giao diện người dùng cho widget chat."""
        chat_layout = QVBoxLayout(self)
        chat_layout.addWidget(QLabel("Trò chuyện với Thư viện AI:"))
        
        self.chat_history_view = QTextEdit()
        self.chat_history_view.setReadOnly(True)
        chat_layout.addWidget(self.chat_history_view)

        chat_input_layout = QHBoxLayout()
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Hỏi AI về sách trong thư viện...")
        self.chat_input.returnPressed.connect(self.send_chat_message)
        chat_input_layout.addWidget(self.chat_input)

        self.send_chat_button = QPushButton("Gửi")
        self.send_chat_button.clicked.connect(self.send_chat_message)
        chat_input_layout.addWidget(self.send_chat_button)
        chat_layout.addLayout(chat_input_layout)
        
        self.setLayout(chat_layout)

    def send_chat_message(self):
        """Gửi tin nhắn của người dùng đến AI và bắt đầu worker."""
        user_query = self.chat_input.text().strip()
        if not user_query:
            return

        self.chat_history_view.append(f"<b>Bạn:</b> {user_query}")
        self.chat_input.clear()
        self.chat_input.setEnabled(False)
        self.send_chat_button.setEnabled(False)

        chat_history = self.chat_history_view.toPlainText()

        # Sử dụng self làm parent cho QThread để quản lý vòng đời
        self.chat_thread = QThread(self)
        self.chat_worker = ChatWorker(user_query, chat_history)
        self.chat_worker.moveToThread(self.chat_thread)

        self.chat_thread.started.connect(self.chat_worker.run)
        self.chat_worker.finished.connect(self.on_chat_response)
        self.chat_worker.error.connect(self.on_chat_error)
        
        # Dọn dẹp khi hoàn thành
        self.chat_worker.finished.connect(self.chat_thread.quit)
        self.chat_worker.finished.connect(self.chat_worker.deleteLater)
        self.chat_thread.finished.connect(self.chat_thread.deleteLater)

        self.chat_thread.start()

    def on_chat_response(self, response):
        """Xử lý và hiển thị phản hồi thành công từ AI."""
        html_response = markdown.markdown(response)
        self.chat_history_view.append(f"<b>AI:</b> {html_response}")
        self.chat_input.setEnabled(True)
        self.send_chat_button.setEnabled(True)
        self.chat_input.setFocus()

    def on_chat_error(self, error_message):
        """Hiển thị thông báo lỗi khi có sự cố với AI chat."""
        self.chat_history_view.append(f"<p style='color:red;'><b>Lỗi:</b> {error_message}</p>")
        self.chat_input.setEnabled(True)
        self.send_chat_button.setEnabled(True)