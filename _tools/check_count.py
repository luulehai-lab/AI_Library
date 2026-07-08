import sqlite3
import os

db_path = "library.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM books")
    count = cursor.fetchone()[0]
    conn.close()
    print(f"Total books in SQLite: {count}")
else:
    print("Không tìm thấy file database library.db")
