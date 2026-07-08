# Tên file: backend/rag_service.py
# CHANGELOG:
# - 2024-08-06: [BẢO TRÌ] Thêm code để ẩn cảnh báo FutureWarning từ thư viện google.generativeai. (AI Studio)
# - 2024-08-06: [VÁ LỖI] Đổi lại import thành `google.generativeai` để tương thích với phiên bản package mới nhất (>=0.8.0). (AI Studio)
# - 2024-08-06: [BẢO TRÌ] Chuyển sang sử dụng thư viện google.genai mới thay cho google.generativeai đã bị ngừng hỗ trợ. (AI Studio)
# - 2024-08-02: [TÁI CẤU TRÚC] Loại bỏ sentence-transformers, chuyển sang sử dụng Google Embedding API để tạo vector. (AI Studio)
# - 2024-08-02: [KHỞI TẠO] Tạo service cho RAG, bao gồm embedding, lưu trữ ChromaDB, và logic chat. (AI Studio)

import warnings
# Bỏ qua cảnh báo cụ thể từ thư viện google.generativeai
warnings.filterwarnings("ignore", category=FutureWarning, module='google.generativeai')

import chromadb
import google.generativeai as genai
from PyQt6.QtCore import QObject, pyqtSignal
from config import CHROMA_PATH, CHROMA_COLLECTION, get_api_key, EMBEDDING_MODEL
from .database import get_db_connection, get_book_by_id

# Cấu hình API key cho Google một lần
try:
    genai.configure(api_key=get_api_key())
except ValueError as e:
    print(f"Lỗi cấu hình Google API: {e}")
    # Xử lý lỗi hoặc thông báo cho người dùng

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name=CHROMA_COLLECTION)

def embed_and_store_book(book_id):
    """Tạo embedding cho một cuốn sách bằng Google API và lưu vào ChromaDB."""
    book = get_book_by_id(book_id)
    if not book:
        return

    book_dict = dict(book)
    content = (
        f"Tên sách: {book_dict.get('ten_sach', '')}. "
        f"Tác giả: {book_dict.get('tac_gia', '')}. "
        f"Thể loại: {book_dict.get('the_loai', '')}. "
        f"Review: {book_dict.get('review', '')}. "
        f"Đánh giá cá nhân: {book_dict.get('danh_gia_ca_nhan', '')}."
    )
    
    # Gọi API của Google để tạo embedding
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=content,
        task_type="RETRIEVAL_DOCUMENT"
    )
    embedding = result['embedding']
    
    collection.upsert( # Dùng upsert để an toàn hơn, có thể thêm mới hoặc cập nhật
        ids=[str(book_id)],
        embeddings=[embedding],
        metadatas=[{"id": book_id}]
    )

def remove_book_from_chroma(book_id):
    """Xóa một cuốn sách khỏi chỉ mục ChromaDB."""
    collection.delete(ids=[str(book_id)])

def sync_database_with_chroma():
    """Đồng bộ hóa toàn bộ CSDL SQLite với ChromaDB."""
    conn = get_db_connection()
    all_book_ids_sqlite = {str(row['id']) for row in conn.execute("SELECT id FROM books").fetchall()}
    conn.close()

    all_book_ids_chroma = set(collection.get(include=[])['ids'])

    ids_to_add = all_book_ids_sqlite - all_book_ids_chroma
    ids_to_delete = all_book_ids_chroma - all_book_ids_sqlite

    if ids_to_add:
        print(f"Tìm thấy {len(ids_to_add)} sách mới cần lập chỉ mục...")
        for book_id in ids_to_add:
            try:
                embed_and_store_book(int(book_id))
            except Exception as e:
                print(f"Lỗi khi lập chỉ mục cho sách ID {book_id}: {e}")
    
    if ids_to_delete:
        print(f"Tìm thấy {len(ids_to_delete)} sách đã bị xóa cần loại bỏ khỏi chỉ mục...")
        collection.delete(ids=list(ids_to_delete))

def query_relevant_books(user_query, n_results=5):
    """Tìm kiếm các sách liên quan trong ChromaDB và trả về thông tin từ SQLite."""
    # Gọi API của Google để tạo embedding cho câu hỏi
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=user_query,
        task_type="RETRIEVAL_QUERY"
    )
    query_embedding = result['embedding']

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    book_ids = results['ids'][0]
    relevant_books = []
    for book_id in book_ids:
        book = get_book_by_id(int(book_id))
        if book:
            relevant_books.append(dict(book))
    return relevant_books

class ChatWorker(QObject):
    """Worker chạy trong luồng riêng để xử lý chat AI."""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, user_query, chat_history):
        super().__init__()
        self.user_query = user_query
        self.chat_history = chat_history

    def run(self):
        try:
            # Bước 1: Truy vấn sách liên quan (Retrieval)
            relevant_books = query_relevant_books(self.user_query)
            
            if not relevant_books:
                context = "Không tìm thấy cuốn sách nào trong thư viện phù hợp với câu hỏi."
            else:
                context = "Dưới đây là một số cuốn sách có liên quan từ thư viện:\n\n"
                for book in relevant_books:
                    context += (
                        f"- Tên sách: {book.get('ten_sach')}\n"
                        f"  Tác giả: {book.get('tac_gia')}\n"
                        f"  Thể loại: {book.get('the_loai')}\n"
                        f"  Review: {book.get('review')}\n\n"
                    )

            # Bước 2: Tạo prompt và sinh câu trả lời (Generation)
            model = genai.GenerativeModel('gemini-flash-latest')

            prompt = (
                "Bạn là một trợ lý thư viện thông thái và hữu ích. "
                "Nhiệm vụ của bạn là trả lời câu hỏi của người dùng dựa trên thông tin về các cuốn sách được cung cấp trong thư viện. "
                "Hãy trả lời một cách tự nhiên, thân thiện và chỉ dựa vào thông tin trong phần 'CONTEXT'. "
                "Nếu không có sách nào phù hợp, hãy nói như vậy một cách lịch sự.\n\n"
                f"CONTEXT:\n{context}\n\n"
                f"LỊCH SỬ TRÒ CHUYỆN:\n{self.chat_history}\n\n"
                f"CÂU HỎI CỦA NGƯỜI DÙNG: {self.user_query}\n\n"
                "TRẢ LỜI CỦA BẠN:"
            )

            response = model.generate_content(prompt)
            self.finished.emit(response.text)

        except Exception as e:
            self.error.emit(f"Lỗi khi trò chuyện với AI: {str(e)}")