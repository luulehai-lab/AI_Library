import json

data_file = "D:/CloudStation/CODE/PYTHON_APP/22_THU_VIEN_AI_LOCAL_1212/_tools/book_data.json"
with open(data_file, "r", encoding="utf-8") as f:
    books = json.load(f)

new_books = [
    {
        "image_path": "images_input/IMG_20260224_135834.jpg",
        "Tên sách": "Đoàn binh Tây Tiến (Bản trùng)",
        "Tác giả": "Quang Dũng",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Hồi ký,Lịch sử",
        "Lứa tuổi": "Thanh thiếu niên",
        "NXB": "Nhà xuất bản Kim Đồng",
        "Năm xuất bản": 2019,
        "Số trang": 124,
        "Điểm Goodreads": 4.5,
        "Review": "Hồi ký chân thật và hào hùng của nhà thơ Quang Dũng về lực lượng Tây Tiến. Tác phẩm kể về những ngày tháng gian bôn, hành quân qua núi rừng Tây Bắc hiểm trở, lưu giữ vẻ đẹp bi tráng của người lính trong kháng chiến chống Pháp. (Ghi chú: Lặp ảnh)",
        "Giá Tiki": 50000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_135843.jpg",
        "Tên sách": "Những người Châu Âu ở nước An Nam (Bản trùng)",
        "Tác giả": "Charles B. Maybon",
        "Quốc gia": "Pháp",
        "Thể loại": "Lịch sử,Khảo cứu",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Thế Giới",
        "Năm xuất bản": 2018,
        "Số trang": 318,
        "Điểm Goodreads": 4.0,
        "Review": "Cuốn sách khảo cứu chi tiết về sự hiện diện và hoạt động của người Châu Âu tại An Nam từ thời tiền thuộc địa. Tác giả đã tổng hợp nhiều tài liệu lịch sử quan trọng, giúp đánh giá khách quan về những tương tác văn hóa, chính trị đầu tiên giữa phương Tây và Đại Nam. (Ghi chú: Lặp ảnh)",
        "Giá Tiki": 130000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_135851.jpg",
        "Tên sách": "Cuộc chiến bí mật: Hồ sơ lực lượng biệt quân ngụy (Bản trùng)",
        "Tác giả": "Vũ Đình Hiếu",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Lịch sử,Tư liệu",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Lao Động",
        "Năm xuất bản": 2018,
        "Số trang": 320,
        "Điểm Goodreads": 3.9,
        "Review": "Dựa trên các tài liệu giải mật từ Lầu Năm Góc qua nguyên bản của John L. Plaster và Kenneth Conboy, cuốn sách cung cấp góc nhìn về các chiến dịch ngầm và lực lượng biệt kích của VNCH trong chiến tranh Việt Nam. (Ghi chú: Lặp ảnh)",
        "Giá Tiki": 95000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_135952.jpg",
        "Tên sách": "Hành trình của một sinh viên Sài Gòn (Bản trùng)",
        "Tác giả": "Nguyễn Hữu Thái",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Lịch sử,Hồi ký",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Alphabooks",
        "Năm xuất bản": 2013,
        "Số trang": 496,
        "Điểm Goodreads": 4.2,
        "Review": "Tập hồi ký sống động của cựu chủ tịch Tổng hội Sinh viên Sài Gòn Nguyễn Hữu Thái. Cuốn sách tái hiện phong trào thanh niên Sài Gòn phản chiến, những trăn trở của trí thức trẻ đô thị miền Nam và quá trình thay đổi nhận thức lịch sử. (Ghi chú: Lặp ảnh)",
        "Giá Tiki": 150000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_140121.jpg",
        "Tên sách": "Mẹ ơi ở đâu con mới được an toàn (Bản trùng)",
        "Tác giả": "Nhiều Tác Giả",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Kỹ năng sống,Nuôi dạy con",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Thanh Niên",
        "Năm xuất bản": 2019,
        "Số trang": 248,
        "Điểm Goodreads": 4.0,
        "Review": "Cuốn sách cung cấp những kiến thức thực tế, kỹ năng cần thiết cho phụ huynh nhằm bảo vệ con trẻ trước các rủi ro xã hội, xâm hại và bạo lực học đường. Lời tư vấn đến từ các chuyên gia giáo dục uy tín và những người làm cha mẹ. (Ghi chú: Lặp ảnh)",
        "Giá Tiki": 70000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_140625.jpg",
        "Tên sách": "Lược sử nước Mỹ (Bản trùng tập 3)",
        "Tác giả": "Cơ Quan Thông Tin Mỹ",
        "Quốc gia": "Hoa Kỳ",
        "Thể loại": "Lịch sử",
        "Lứa tuổi": "Thanh thiếu niên",
        "NXB": "Nhà xuất bản Tổng Hợp Thành Phố Hồ Chí Minh",
        "Năm xuất bản": 2010,
        "Số trang": 435,
        "Điểm Goodreads": 3.9,
        "Review": "Cung cấp cái nhìn toàn cảnh và tóm lược quá trình hình thành, xây dựng và phát triển tư bản của Hợp chúng quốc Hoa Kỳ từ buổi sơ khai đến kỷ nguyên hiện đại. Cuốn sách là nguồn tham khảo nền tảng cho ai muốn tìm hiểu nhanh về nước Mỹ. (Ghi chú: Lặp ảnh lần 3)",
        "Giá Tiki": 160000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_140737.jpg",
        "Tên sách": "Truyện Thông sử Trung Quốc (Quyển thượng)",
        "Tác giả": "Nhiều Tác Giả",
        "Quốc gia": "Trung Quốc",
        "Thể loại": "Lịch sử",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Văn hóa - Thông tin",
        "Năm xuất bản": 2000,
        "Số trang": 685,
        "Điểm Goodreads": 4.0,
        "Review": "Tập đầu tiên trong bộ thông sử vĩ đại giới thiệu một cách toàn diện về lịch sử Trung Hoa. Sách cung cấp những ghi chép, truyền thuyết lịch sử và diễn biến chính trị, quân sự của các triều đại cổ đại gắn liền với nền văn minh huy hoàng bậc nhất phương Đông.",
        "Giá Tiki": 120000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_140745.jpg",
        "Tên sách": "Truyện Thông sử Trung Quốc (Quyển thượng) (Bản trùng)",
        "Tác giả": "Nhiều Tác Giả",
        "Quốc gia": "Trung Quốc",
        "Thể loại": "Lịch sử",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Văn hóa - Thông tin",
        "Năm xuất bản": 2000,
        "Số trang": 685,
        "Điểm Goodreads": 4.0,
        "Review": "Tập đầu tiên trong bộ thông sử vĩ đại giới thiệu một cách toàn diện về lịch sử Trung Hoa. Sách cung cấp những ghi chép, truyền thuyết lịch sử và diễn biến chính trị, quân sự của các triều đại cổ đại gắn liền với nền văn minh huy hoàng bậc nhất phương Đông. (Ghi chú: Ảnh trùng)",
        "Giá Tiki": 120000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_140954.jpg",
        "Tên sách": "Lịch sử thế giới cổ đại",
        "Tác giả": "Lương Ninh, Nguyễn Gia Phu",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Lịch sử,Giáo trình",
        "Lứa tuổi": "Sinh viên, Người lớn",
        "NXB": "Nhà xuất bản Giáo dục",
        "Năm xuất bản": 1998,
        "Số trang": 272,
        "Điểm Goodreads": 3.8,
        "Review": "Giáo trình chuẩn cung cấp kiến thức nền tảng và hệ thống về quá trình phát sinh, hình thành, phát triển và tan rã của các nhà nước cổ đại trên thế giới, bao quát từ các nền văn minh phương Đông cổ đại đến phương Tây.",
        "Giá Tiki": 50000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_141245.jpg",
        "Tên sách": "Nghìn ngày nước Ý, nghìn ngày yêu",
        "Tác giả": "Trương Anh Ngọc",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Du ký,Tản văn",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Hội Nhà Văn",
        "Năm xuất bản": 2017,
        "Số trang": 212,
        "Điểm Goodreads": 3.7,
        "Review": "Tuyển tập những đoạn ghi chép, tản văn đầy chất thơ và suy nghiệm chân thực của nhà báo Trương Anh Ngọc trong hơn một ngàn ngày sinh sống, gắn bó tại nước Ý rực mỡ sắc màu và phóng khoáng tình người.",
        "Giá Tiki": 85000,
        "Xoay ảnh": 0
    }
]

books.extend(new_books)
with open(data_file, "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, indent=4)
print(f"Updated book_data.json with {len(new_books)} more books successfully")
