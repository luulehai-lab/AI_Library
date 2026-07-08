import json

data_file = "D:/CloudStation/CODE/PYTHON_APP/22_THU_VIEN_AI_LOCAL_1212/_tools/book_data.json"
with open(data_file, "r", encoding="utf-8") as f:
    books = json.load(f)

new_books = [
    {
        "image_path": "images_input/IMG_20260224_141835.jpg",
        "Tên sách": "Không thể chuộc lỗi",
        "Tác giả": "Allen Hassan",
        "Quốc gia": "Hoa Kỳ",
        "Thể loại": "Tiểu thuyết,Chiến tranh",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Trẻ",
        "Năm xuất bản": 2006,
        "Số trang": 272,
        "Điểm Goodreads": 4.1,
        "Review": "Hồi ký xúc động của bác sĩ chiến trường người Mỹ Allen Hassan trong chiến tranh Việt Nam. Tác phẩm kể về những góc khuất, sự tàn khốc của chiến tranh cũng như nỗi ám ảnh về trách nhiệm, lương tri con người trước những vết thương không thể nào hàn gắn.",
        "Giá Tiki": 65000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_141841.jpg",
        "Tên sách": "Việt Nam qua tuần san Indochine 1941-1944",
        "Tác giả": "Lưu Đình Tuân",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Lịch sử,Văn hóa",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Thế Giới",
        "Năm xuất bản": 2019,
        "Số trang": 376,
        "Điểm Goodreads": 3.9,
        "Review": "Tập hợp và tuyển dịch từ tạp chí Indochine, cuốn sách là bức tranh tư liệu quý giá về đời sống văn hóa, xã hội, phong tục tập quán của Việt Nam thời kỳ thuộc Pháp trong những năm đầu thập niên 1940.",
        "Giá Tiki": 125000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_142020.jpg",
        "Tên sách": "Chiến tranh không có một khuôn mặt phụ nữ",
        "Tác giả": "Svetlana Alexievich",
        "Quốc gia": "Belarus",
        "Thể loại": "Lịch sử,Hồi ký",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Hà Nội",
        "Năm xuất bản": 2018,
        "Số trang": 464,
        "Điểm Goodreads": 4.4,
        "Review": "Tác phẩm đoạt giải Nobel Văn học, tái hiện sinh động chiến tranh Vệ quốc vĩ đại qua góc nhìn của những hồng quân nữ giới Liên Xô. Một bản cáo trạng sắc bén và thấm đẫm tình người về nỗi đau tột cùng của phái nữ giữa bom đạn lịch sử.",
        "Giá Tiki": 160000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_142029.jpg",
        "Tên sách": "Việt-Pháp bang giao sử lược",
        "Tác giả": "Phan Khoang",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Lịch sử",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Khoa Học Xã Hội",
        "Năm xuất bản": 2017,
        "Số trang": 330,
        "Điểm Goodreads": 4.0,
        "Review": "Nghiên cứu sử học hệ thống và giá trị của nhà nghiên cứu Phan Khoang về mối quan hệ ngoại giao phức tạp giữa Việt Nam và Pháp từ thế kỷ 17 đến đầu thế kỷ 20, góp phần làm rõ bối cảnh mất nước vào tay thực dân Pháp.",
        "Giá Tiki": 95000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_142036.jpg",
        "Tên sách": "Biên bản chiến tranh 1-2-3-4.75",
        "Tác giả": "Trần Mai Hạnh",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Lịch sử,Tiểu thuyết tư liệu",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Chính trị quốc gia Sự thật",
        "Năm xuất bản": 2014,
        "Số trang": 612,
        "Điểm Goodreads": 4.1,
        "Review": "Cuốn tiểu thuyết tư liệu lịch sử đồ sộ thuật lại từng diễn biến chi tiết, căng thẳng dẫn đến sự sụp đổ của chế độ cũ Sài Gòn trong 4 tháng cuối cùng của cuộc kháng chiến chống Mỹ cứu nước.",
        "Giá Tiki": 180000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_142232.jpg",
        "Tên sách": "1491 Những khám phá mới về châu Mỹ",
        "Tác giả": "Charles C. Mann",
        "Quốc gia": "Hoa Kỳ",
        "Thể loại": "Lịch sử,Khảo cổ",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Đại Học Kinh Tế Quốc Dân",
        "Năm xuất bản": 2005,
        "Số trang": 480,
        "Điểm Goodreads": 4.1,
        "Review": "Tác phẩm làm thay đổi nhận thức lịch sử khi tái dựng lại nền văn minh quy mô, đông đúc và vô cùng tinh vi của cư dân bản địa châu Mỹ ngay thời kỳ trước khi Columbus đến vào năm 1492.",
        "Giá Tiki": 140000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_142240.jpg",
        "Tên sách": "1493 Diện mạo tân thế giới của Columbus",
        "Tác giả": "Charles C. Mann",
        "Quốc gia": "Hoa Kỳ",
        "Thể loại": "Lịch sử",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Dân Trí",
        "Năm xuất bản": 2011,
        "Số trang": 560,
        "Điểm Goodreads": 4.2,
        "Review": "Tiếp nối '1491', sách phân tích sâu sắc khái niệm 'trao đổi Columbus' đã thay đổi mãi mãi thế giới sinh thái, kinh tế và dân cư toàn cầu kể từ thế kỷ 16 như thế nào.",
        "Giá Tiki": 150000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_142431.jpg",
        "Tên sách": "TẾT!",
        "Tác giả": "Don Oberdorfer",
        "Quốc gia": "Hoa Kỳ",
        "Thể loại": "Lịch sử,Chiến tranh",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Tổng hợp Thành phố Hồ Chí Minh",
        "Năm xuất bản": 2018,
        "Số trang": 234,
        "Điểm Goodreads": 4.0,
        "Review": "Công trình ghi chép lịch sử xuất sắc từ góc nhìn của một ký giả Mỹ, phân tích toàn diện về cuộc Tổng tiến công và nổi dậy Mậu Thân 1968, một bước ngoặt quyết định thay đổi thế giới quan nước Mỹ về chiến tranh Việt Nam.",
        "Giá Tiki": 75000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_142437.jpg",
        "Tên sách": "Một thời Rừng Sác (Tập 1)",
        "Tác giả": "Lê Bá Ước",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Lịch sử,Hồi ký",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Văn hóa Văn nghệ",
        "Năm xuất bản": 2012,
        "Số trang": 351,
        "Điểm Goodreads": 4.0,
        "Review": "Bản hùng ca chân thực và đầy tự hào của thế hệ những chiến sĩ đặc công Rừng Sác huyền thoại nơi cửa ngõ phía Nam, với bao gian khó, hy sinh, mưu trí và dũng cảm (Tập 1).",
        "Giá Tiki": 60000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_142443.jpg",
        "Tên sách": "Một thời Rừng Sác (Tập 2)",
        "Tác giả": "Lê Bá Ước",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Lịch sử,Hồi ký",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Văn hóa Văn nghệ",
        "Năm xuất bản": 2012,
        "Số trang": 264,
        "Điểm Goodreads": 4.0,
        "Review": "Phần tiếp theo của tác phẩm ghi lại những góc nhìn sống động, khí tiết hào hùng của nghĩa quân Rừng Sác anh dũng và thủy chung trong cuộc chiến tranh vĩ đại (Tập 2).",
        "Giá Tiki": 55000,
        "Xoay ảnh": 0
    }
]

books.extend(new_books)
with open(data_file, "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, indent=4)
print(f"Updated book_data.json with {len(new_books)} more books successfully")
