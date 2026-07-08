import sys
import io

# Cấu hình encoding cho console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from backend.rag_service import sync_database_with_chroma

if __name__ == "__main__":
    print("Bắt đầu đồng bộ SQLite với ChromaDB...")
    sync_database_with_chroma()
    print("Đồng bộ hoàn tất.")
