# Tên file: backend/utils.py
# CHANGELOG:
# - 2024-08-06: [NÂNG CẤP] Thêm hàm rotate_image_file để tự động xoay ảnh theo góc chỉ định. (AI Studio)
# - 2024-08-06: [NÂNG CẤP] Thêm hàm create_thumbnail để tạo và cache ảnh thu nhỏ, giúp tăng tốc độ tải giao diện. (AI Studio)
# - 2024-08-06: [KHỞI TẠO] Tạo file utils và thêm hàm find_cover_image để tìm ảnh bìa dựa trên tên sách. (AI Studio)

import os
from PIL import Image

THUMBNAIL_DIR = os.path.join(".cache", "thumbnails")
THUMBNAIL_SIZE = (90, 120)

def find_cover_image(book_title):
    """
    Tìm kiếm file ảnh trong thư mục 'images_processed' có tên trùng với tên sách.
    """
    if not book_title:
        return None
        
    processed_dir = "images_processed"
    valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.webp']
    
    try:
        for filename in os.listdir(processed_dir):
            name_without_ext, ext = os.path.splitext(filename)
            if name_without_ext.lower() == book_title.lower() and ext.lower() in valid_extensions:
                return os.path.join(processed_dir, filename)
    except FileNotFoundError:
        print(f"Lỗi: Thư mục '{processed_dir}' không tồn tại.")
        return None
        
    return None

def create_thumbnail(original_image_path, book_id):
    """
    Tạo một ảnh thu nhỏ từ ảnh gốc và lưu vào thư mục cache.
    """
    if not original_image_path or not os.path.exists(original_image_path):
        return None

    os.makedirs(THUMBNAIL_DIR, exist_ok=True)
    
    try:
        img = Image.open(original_image_path)
        img.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
        
        # Lấy phần mở rộng của file gốc để lưu thumbnail
        _, ext = os.path.splitext(original_image_path)
        thumbnail_filename = f"{book_id}{ext}"
        thumbnail_path = os.path.join(THUMBNAIL_DIR, thumbnail_filename)
        
        img.save(thumbnail_path)
        return thumbnail_path
    except Exception as e:
        print(f"Lỗi khi tạo thumbnail cho {original_image_path}: {e}")
        return None

def get_thumbnail_path(book_id, original_cover_path):
    """
    Lấy đường dẫn đến thumbnail. Nếu không tồn tại, sẽ thử tạo nó.
    """
    if not book_id or not original_cover_path:
        return None

    # Tìm kiếm thumbnail với các phần mở rộng phổ biến
    base_name = str(book_id)
    for ext in ['.jpg', '.png', '.jpeg', '.bmp', '.webp']:
        potential_path = os.path.join(THUMBNAIL_DIR, base_name + ext)
        if os.path.exists(potential_path):
            return potential_path
            
    # Nếu không tìm thấy, có thể thumbnail chưa được tạo
    # Thử tạo lại từ đường dẫn gốc
    return create_thumbnail(original_cover_path, book_id)

def rotate_image_file(image_path, angle):
    """
    Xoay file ảnh theo góc chỉ định và ghi đè lên file gốc.
    """
    if not angle or angle not in [90, 180, 270]:
        return
        
    try:
        img = Image.open(image_path)
        # Pillow xoay ngược chiều kim đồng hồ, nên ta cần đảo dấu góc
        rotated_img = img.rotate(-angle, expand=True)
        rotated_img.save(image_path)
        print(f"Đã xoay ảnh {os.path.basename(image_path)} một góc {angle} độ.")
    except Exception as e:
        print(f"Lỗi khi xoay ảnh {image_path}: {e}")