# Tên file: frontend/components/dashboard_widget.py
# CHANGELOG:
# - 2024-08-06: [VÁ LỖI] Sửa lỗi crash trong plot_genres do ax.pie trả về số lượng giá trị khác nhau khi autopct là None. (AI Studio)
# - 2024-08-06: [NÂNG CẤP] Tái cấu trúc Dashboard: Sử dụng ChartPreviewCard để hiển thị thumbnail và ChartDetailDialog để xem full-screen. Thêm biểu đồ Quốc gia. (AI Studio)
# - 2024-08-06: [KHỞI TẠO] Tạo widget Dashboard chứa các biểu đồ thống kê sử dụng Matplotlib. (AI Studio)

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QScrollArea, QLabel, 
                             QFrame, QDialog, QPushButton, QHBoxLayout)
from PyQt6.QtCore import Qt, pyqtSignal
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from backend.database import get_dashboard_stats

# Cấu hình font chữ cho Matplotlib
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'Tahoma']
plt.rcParams['font.size'] = 9

class ChartCanvas(FigureCanvasQTAgg):
    """Lớp bao đóng FigureCanvas của Matplotlib."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)

class ChartDetailDialog(QDialog):
    """Dialog hiển thị biểu đồ kích thước lớn với đầy đủ tính năng."""
    def __init__(self, title, plot_callback, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(1000, 700)
        
        layout = QVBoxLayout(self)
        
        # Canvas lớn
        self.canvas = ChartCanvas(self, width=10, height=8, dpi=100)
        
        # Toolbar của Matplotlib (Zoom, Pan, Save...)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        # Vẽ biểu đồ
        plot_callback(self.canvas.axes, data, is_preview=False)
        self.canvas.draw()
        
        # Nút đóng
        close_btn = QPushButton("Đóng")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, 0, Qt.AlignmentFlag.AlignRight)

class ChartPreviewCard(QFrame):
    """Widget hiển thị thumbnail của biểu đồ, có thể click để phóng to."""
    clicked = pyqtSignal()

    def __init__(self, title, plot_callback, data, parent=None):
        super().__init__(parent)
        self.title = title
        self.plot_callback = plot_callback
        self.data = data
        
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setStyleSheet("""
            ChartPreviewCard {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
            }
            ChartPreviewCard:hover {
                border: 1px solid #0078d7;
                background-color: #f8faff;
            }
        """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout(self)
        
        # Tiêu đề
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("font-weight: bold; font-size: 14px; color: #333; border: none; background: transparent;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        # Canvas nhỏ (Preview)
        self.canvas = ChartCanvas(self, width=4, height=3, dpi=80)
        self.canvas.setStyleSheet("background: transparent; border: none;")
        # Vô hiệu hóa tương tác chuột trên canvas để sự kiện click truyền lên Card
        self.canvas.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        layout.addWidget(self.canvas)
        
        # Vẽ preview
        self.plot_callback(self.canvas.axes, self.data, is_preview=True)
        self.canvas.draw()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

class DashboardWidget(QWidget):
    """
    Widget hiển thị bảng điều khiển với các biểu đồ thống kê dạng lưới.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Tiêu đề
        title = QLabel("Thống Kê Thư Viện")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #005a9e; margin-bottom: 15px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Khu vực cuộn
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll_area.setStyleSheet("background-color: #f0f0f0;")
        
        content_widget = QWidget()
        self.grid_layout = QGridLayout(content_widget)
        self.grid_layout.setSpacing(20)
        self.grid_layout.setContentsMargins(20, 20, 20, 20)
        
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        # Load dữ liệu lần đầu
        self.refresh_data()

    def refresh_data(self):
        """Lấy dữ liệu mới nhất từ DB và vẽ lại các thẻ biểu đồ."""
        # Xóa các widget cũ
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        stats = get_dashboard_stats()
        
        # Định nghĩa danh sách các biểu đồ
        charts = [
            ("Phân bố Thể loại (Top 8)", self.plot_genres, stats.get("genres", {})),
            ("Trạng thái Đọc", self.plot_status, stats.get("status", {})),
            ("Top 5 Tác giả", self.plot_authors, stats.get("authors", {})),
            ("Sách theo Năm xuất bản", self.plot_years, stats.get("years", {})),
            ("Sách theo Quốc gia (Top 8)", self.plot_countries, stats.get("countries", {}))
        ]

        # Thêm các thẻ vào lưới (2 cột)
        row, col = 0, 0
        for title, func, data in charts:
            card = ChartPreviewCard(title, func, data)
            card.clicked.connect(lambda t=title, f=func, d=data: self.show_detail(t, f, d))
            self.grid_layout.addWidget(card, row, col)
            
            col += 1
            if col > 1:
                col = 0
                row += 1

    def show_detail(self, title, func, data):
        """Mở dialog chi tiết."""
        dialog = ChartDetailDialog(title, func, data, self)
        dialog.exec()

    # --- CÁC HÀM VẼ BIỂU ĐỒ (STATIC LOGIC) ---
    
    def plot_genres(self, ax, data, is_preview=False):
        ax.clear()
        if not data:
            ax.text(0.5, 0.5, "Chưa có dữ liệu", ha='center')
            return
        
        labels = list(data.keys())
        values = list(data.values())
        
        # Nếu là preview, ẩn bớt label nhỏ để đỡ rối
        if is_preview and len(labels) > 5:
             autopct = None 
        else:
             autopct = '%1.1f%%'

        # SỬA LỖI: Xử lý kết quả trả về linh hoạt
        pie_data = ax.pie(values, labels=labels, autopct=autopct, startangle=90, 
                          colors=plt.cm.Pastel1.colors, labeldistance=1.1)
        
        if autopct is None:
            wedges, texts = pie_data
            autotexts = None
        else:
            wedges, texts, autotexts = pie_data
        
        if is_preview:
            plt.setp(texts, fontsize=8)
            if autotexts:
                plt.setp(autotexts, fontsize=7)
        
        ax.axis('equal')  # Đảm bảo hình tròn
        ax.figure.tight_layout()

    def plot_status(self, ax, data, is_preview=False):
        ax.clear()
        if not data:
            ax.text(0.5, 0.5, "Chưa có dữ liệu", ha='center')
            return
            
        labels = list(data.keys())
        values = list(data.values())
        
        wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, 
                                          pctdistance=0.85, colors=plt.cm.Set3.colors)
        
        centre_circle = plt.Circle((0,0), 0.70, fc='white')
        ax.add_artist(centre_circle)
        ax.axis('equal')
        ax.figure.tight_layout()

    def plot_authors(self, ax, data, is_preview=False):
        ax.clear()
        if not data:
            ax.text(0.5, 0.5, "Chưa có dữ liệu", ha='center')
            return
            
        authors = list(data.keys())
        counts = list(data.values())
        y_pos = range(len(authors))
        
        ax.barh(y_pos, counts, align='center', color='#0078d7')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(authors)
        ax.invert_yaxis()
        
        if not is_preview:
            ax.set_xlabel('Số lượng sách')
            
        ax.figure.tight_layout()

    def plot_years(self, ax, data, is_preview=False):
        ax.clear()
        if not data:
            ax.text(0.5, 0.5, "Chưa có dữ liệu", ha='center')
            return
            
        years = [str(y) for y in data.keys()]
        counts = list(data.values())
        
        ax.bar(years, counts, color='#28a745')
        if not is_preview:
            ax.set_ylabel('Số lượng sách')
            
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
        ax.figure.tight_layout()

    def plot_countries(self, ax, data, is_preview=False):
        ax.clear()
        if not data:
            ax.text(0.5, 0.5, "Chưa có dữ liệu", ha='center')
            return
            
        countries = list(data.keys())
        counts = list(data.values())
        
        # Vẽ biểu đồ cột đứng cho quốc gia
        ax.bar(countries, counts, color='#ff7f0e')
        
        if not is_preview:
            ax.set_ylabel('Số lượng sách')
            
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
        ax.figure.tight_layout()