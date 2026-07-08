import json

data_file = "D:/CloudStation/CODE/PYTHON_APP/22_THU_VIEN_AI_LOCAL_1212/_tools/book_data.json"
with open(data_file, "r", encoding="utf-8") as f:
    books = json.load(f)

new_books = [
    {
        "image_path": "images_input/IMG_20260224_141254.jpg",
        "Tên sách": "Nụ hôn thành Rome",
        "Tác giả": "DiLi",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Du ký,Tản văn",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Dân Trí",
        "Năm xuất bản": 2015,
        "Số trang": 291,
        "Điểm Goodreads": 3.8,
        "Review": "Cuốn sách du ký thứ hai của DiLi sau 'Đảo thiên đường'. Bằng giọng văn tinh tế và lãng mạn, tác giả dẫn dắt người đọc qua những miền đất châu Âu đầy thơ mộng, cổ kính, đặc biệt là những trải nghiệm sâu sắc và ngọt ngào tại Rome.",
        "Giá Tiki": 70000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_141304.jpg",
        "Tên sách": "Ngẫm ngợi phố phường",
        "Tác giả": "Đỗ Phấn",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Tạp bút",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Trẻ",
        "Năm xuất bản": 2016,
        "Số trang": 326,
        "Điểm Goodreads": 3.5,
        "Review": "Tập tạp bút ghi lại những quan sát, suy ngẫm trầm lắng của họa sĩ, nhà văn Đỗ Phấn về những đổi thay của phố phường Hà Nội, những nét văn hóa đang dần mai một và tâm thức của người Tràng An giữa nhịp sống hiện đại.",
        "Giá Tiki": 80000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_141311.jpg",
        "Tên sách": "Gái phượt",
        "Tác giả": "Yếm Đào Lẳng Lơ",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Du ký,Hồi ký",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Hội Nhà Văn",
        "Năm xuất bản": 2017,
        "Số trang": 255,
        "Điểm Goodreads": 3.8,
        "Review": "Hành trình xê dịch dọc ngang của một cô gái trẻ đam mê khám phá. Cuốn sách không chỉ là những chuyến đi 'say đường' mà còn chứa đựng chuyện 'say nắng' và hành trình làm mẹ đơn thân đầy bản lĩnh, truyền cảm hứng sống mãnh liệt.",
        "Giá Tiki": 65000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_141317.jpg",
        "Tên sách": "Hướng nào Hà Nội cũng sông",
        "Tác giả": "Hồ Anh Thái",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Tiểu luận,Tạp văn",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Văn Nghệ",
        "Năm xuất bản": 2009,
        "Số trang": 208,
        "Điểm Goodreads": 3.6,
        "Review": "Tập hợp những bài tiểu luận, góc nhìn đặc sắc của nhà văn Hồ Anh Thái về văn hóa, lịch sử và con người Hà Nội. Sách viết với sự sắc sảo, hóm hỉnh nhưng cũng không kém phần thâm trầm của một người gắn bó máu thịt với Thủ đô.",
        "Giá Tiki": 55000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_141350.jpg",
        "Tên sách": "Miền Tây lạ lắm à nghen",
        "Tác giả": "Trương Chí Hùng",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Du ký,Văn hóa",
        "Lứa tuổi": "Thanh thiếu niên",
        "NXB": "Nhà xuất bản Kim Đồng",
        "Năm xuất bản": 2020,
        "Số trang": 100,
        "Điểm Goodreads": 3.9,
        "Review": "Một cuốn sách nhỏ gọn, xinh xắn dẫn dắt người đọc khám phá những nét văn hóa miệt vườn độc đáo, từ cảnh vật thiên nhiên đến tính cách phóng khoáng, chân chất của người dân Đồng bằng sông Cửu Long.",
        "Giá Tiki": 45000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_141404.jpg",
        "Tên sách": "Phút 90++",
        "Tác giả": "Trương Anh Ngọc",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Ký sự,Du ký",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Hội Nhà Văn",
        "Năm xuất bản": 2013,
        "Số trang": 260,
        "Điểm Goodreads": 3.8,
        "Review": "Ký sự đầy đam mê của nhà báo thể thao Trương Anh Ngọc về những chuyến tát nghiệp tại các kỳ World Cup ở Nam Phi và EURO ở Ukraina, đan xen cùng những suy nghiệm sau 10 nghìn cây số di chuyển xuyên qua các miền văn hóa.",
        "Giá Tiki": 70000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_141414.jpg",
        "Tên sách": "Người tình Havana",
        "Tác giả": "Đinh Hằng",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Du ký",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Hội Nhà Văn",
        "Năm xuất bản": 2020,
        "Số trang": 233,
        "Điểm Goodreads": 4.1,
        "Review": "Cuốn sách kể về hành trình trải nghiệm ở đất nước Cuba xinh đẹp của tác giả gốc Việt. Bằng góc nhìn hoài niệm, lãng mạn, cuốn sách vừa là bức tranh sống động về Havana, vừa là những tự sự cá nhân sâu thẳm về tình yêu và tuổi thanh xuân.",
        "Giá Tiki": 90000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_141553.jpg",
        "Tên sách": "Mệnh lệnh lưỡi lê",
        "Tác giả": "Nick Turse",
        "Quốc gia": "Hoa Kỳ",
        "Thể loại": "Lịch sử,Chính trị",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Trẻ",
        "Năm xuất bản": 2013,
        "Số trang": 370,
        "Điểm Goodreads": 4.5,
        "Review": "Dựa trên những hồ sơ giải mật chưa từng công bố, nhà báo Nick Turse phơi bày một khía cạnh tàn khốc, có tính hệ thống về những tội ác chiến tranh của quân đội Mỹ tại Việt Nam, vượt xa những vụ án lác đác từng được biết đến.",
        "Giá Tiki": 110000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_141821.jpg",
        "Tên sách": "Trực thăng vận Mạt vận ở đường 9",
        "Tác giả": "Báo Quân đội Nhân dân",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Lịch sử,Quân sự",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Quân đội nhân dân",
        "Năm xuất bản": 2005,
        "Số trang": 288,
        "Điểm Goodreads": 3.8,
        "Review": "Tập bình luận thời chiến tranh tập 3, phân tích chi tiết về sự phá sản của chiến lược 'Trực thăng vận' và 'Thiết xa vận' của Mỹ - Ngụy trong chiến dịch Đường 9 - Nam Lào, một mốc son chói lọi trong lịch sử kháng chiến chống Mỹ.",
        "Giá Tiki": 60000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_141827.jpg",
        "Tên sách": "Tài hoa ra trận",
        "Tác giả": "Hoàng Thượng Lân",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Nhật ký,Lịch sử",
        "Lứa tuổi": "Thanh thiếu niên",
        "NXB": "Nhà xuất bản Hội Nhà Văn",
        "Năm xuất bản": 2005,
        "Số trang": 316,
        "Điểm Goodreads": 4.0,
        "Review": "Nằm trong Tủ sách Mãi mãi tuổi hai mươi. Cuốn sổ nhật ký chiến trường chan chứa nhiệt huyết, lý tưởng nhưng cũng đượm buồn về cuộc sống, tình yêu, sự hy sinh của liệt sĩ Hoàng Thượng Lân - một người thanh niên tài hoa thế hệ chống Mỹ.",
        "Giá Tiki": 65000,
        "Xoay ảnh": 0
    }
]

books.extend(new_books)
with open(data_file, "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, indent=4)
print(f"Updated book_data.json with {len(new_books)} more books successfully")
