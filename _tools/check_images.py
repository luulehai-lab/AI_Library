import json
import os
import sys

# Configure UTF-8 for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

json_path = r"C:\Users\luule\.gemini\antigravity\brain\7dbb3c43-8629-4e14-8219-0e6cc9b21709\book_data.json"
base_dir = r"d:\CloudStation\CODE\PYTHON_APP\22_THU_VIEN_AI_LOCAL_1212"

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Chỉ kiểm tra 20 cuốn cuối cùng (Batch 4)
batch4 = data[-20:]

print("Checking Batch 4 (last 20 books):")
for book in batch4:
    path = os.path.join(base_dir, book['image_path'])
    if not os.path.exists(path):
        print(f"MISSING: {book['image_path']} - {book.get('Tên sách', 'N/A')}")
    else:
        print(f"EXISTS: {book['image_path']}")
