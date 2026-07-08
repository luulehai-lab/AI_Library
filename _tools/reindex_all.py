import sys
import io
import time
import google.generativeai as genai
import chromadb
from config import CHROMA_PATH, CHROMA_COLLECTION, get_api_key, EMBEDDING_MODEL
from backend.database import get_db_connection

# Cấu hình encoding cho console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Cấu hình Google AI
genai.configure(api_key=get_api_key())

def reindex_all():
    # 1. Khởi tạo ChromaDB
    print(f"Khởi tạo ChromaDB tại: {CHROMA_PATH}")
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = chroma_client.get_or_create_collection(name=CHROMA_COLLECTION)

    # 2. Lấy tất cả sách từ SQLite
    print("Đang lấy dữ liệu từ SQLite...")
    conn = get_db_connection()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    
    total = len(books)
    print(f"Tìm thấy {total} cuốn sách. Bắt đầu indexing...")

    batch_size = 50 # Google Batch API hỗ trợ lên đến 100
    for i in range(0, total, batch_size):
        batch = books[i:i + batch_size]
        ids = [str(b['id']) for b in batch]
        metadatas = [{"id": b['id']} for b in batch]
        
        contents = []
        for b in batch:
            text = (
                f"Tên sách: {b['ten_sach']}. "
                f"Tác giả: {b['tac_gia']}. "
                f"Thể loại: {b['the_loai']}. "
                f"Review: {b['review']}. "
                f"Đánh giá cá nhân: {b['danh_gia_ca_nhan']}."
            )
            contents.append(text)

        print(f"Đang xử lý batch {i//batch_size + 1}/{(total-1)//batch_size + 1} ({len(batch)} cuốn)...")
        
        try:
            # Gọi API Batch Embedding
            result = genai.embed_content(
                model=EMBEDDING_MODEL,
                content=contents,
                task_type="RETRIEVAL_DOCUMENT"
            )
            embeddings = result['embedding']

            # Lưu vào ChromaDB
            collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas
            )
            print(f"  -> Xong batch.")
            
            # Nghỉ một chút để tránh rate limit nếu cần
            if i + batch_size < total:
                time.sleep(2) 
        except Exception as e:
            print(f"  -> LỖI tại batch này: {e}")

if __name__ == "__main__":
    start_time = time.time()
    reindex_all()
    duration = time.time() - start_time
    print(f"Hoàn tất re-index toàn bộ {total_books if 'total_books' in locals() else 'thư viện'} sách.")
    print(f"Thời gian thực hiện: {duration:.2f} giây.")
