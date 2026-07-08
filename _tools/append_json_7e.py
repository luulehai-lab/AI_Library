import json

data_file = "D:/CloudStation/CODE/PYTHON_APP/22_THU_VIEN_AI_LOCAL_1212/_tools/book_data.json"
with open(data_file, "r", encoding="utf-8") as f:
    books = json.load(f)

new_books = [
    {
        "image_path": "images_input/IMG_20260224_132800.jpg",
        "Tên sách": "Đoàn binh Tây Tiến",
        "Tác giả": "Quang Dũng",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Hồi ký,Lịch sử",
        "Lứa tuổi": "Thanh thiếu niên",
        "NXB": "Nhà xuất bản Kim Đồng",
        "Năm xuất bản": 2019,
        "Số trang": 124,
        "Điểm Goodreads": 4.5,
        "Review": "Hồi ký chân thật và hào hùng của nhà thơ Quang Dũng về lực lượng Tây Tiến. Tác phẩm kể về những ngày tháng gian bôn, hành quân qua núi rừng Tây Bắc hiểm trở, lưu giữ vẻ đẹp bi tráng của người lính trong kháng chiến chống Pháp.",
        "Giá Tiki": 50000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_134846.jpg",
        "Tên sách": "Những người Châu Âu ở nước An Nam",
        "Tác giả": "Charles B. Maybon",
        "Quốc gia": "Pháp",
        "Thể loại": "Lịch sử,Khảo cứu",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Thế Giới",
        "Năm xuất bản": 2018,
        "Số trang": 318,
        "Điểm Goodreads": 4.0,
        "Review": "Cuốn sách khảo cứu chi tiết về sự hiện diện và hoạt động của người Châu Âu tại An Nam từ thời tiền thuộc địa. Tác giả đã tổng hợp nhiều tài liệu lịch sử quan trọng, giúp đánh giá khách quan về những tương tác văn hóa, chính trị đầu tiên giữa phương Tây và Đại Nam.",
        "Giá Tiki": 130000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_134907.jpg",
        "Tên sách": "Cuộc chiến bí mật: Hồ sơ lực lượng biệt quân ngụy",
        "Tác giả": "Vũ Đình Hiếu",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Lịch sử,Tư liệu",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Công An Nhân Dân",
        "Năm xuất bản": 2018,
        "Số trang": 320,
        "Điểm Goodreads": 3.9,
        "Review": "Dựa trên các tài liệu giải mật từ Lầu Năm Góc qua nguyên bản của John L. Plaster và Kenneth Conboy, cuốn sách cung cấp góc nhìn về các chiến dịch ngầm và lực lượng biệt kích của VNCH trong chiến tranh Việt Nam.",
        "Giá Tiki": 95000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_134951.jpg",
        "Tên sách": "Hành trình của một sinh viên Sài Gòn",
        "Tác giả": "Nguyễn Hữu Thái",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Lịch sử,Hồi ký",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Trẻ",
        "Năm xuất bản": 2013,
        "Số trang": 496,
        "Điểm Goodreads": 4.2,
        "Review": "Tập hồi ký sống động của cựu chủ tịch Tổng hội Sinh viên Sài Gòn Nguyễn Hữu Thái. Cuốn sách tái hiện phong trào thanh niên Sài Gòn phản chiến, những trăn trở của trí thức trẻ đô thị miền Nam và quá trình thay đổi nhận thức lịch sử.",
        "Giá Tiki": 150000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_140237.jpg",
        "Tên sách": "Mẹ ơi ở đâu con mới được an toàn",
        "Tác giả": "Nhiều Tác Giả",
        "Quốc gia": "Việt Nam",
        "Thể loại": "Kỹ năng sống,Nuôi dạy con",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Lao Động",
        "Năm xuất bản": 2019,
        "Số trang": 248,
        "Điểm Goodreads": 4.0,
        "Review": "Cuốn sách cung cấp những kiến thức thực tế, kỹ năng cần thiết cho phụ huynh nhằm bảo vệ con trẻ trước các rủi ro xã hội, xâm hại và bạo lực học đường. Lời tư vấn đến từ các chuyên gia giáo dục uy tín và những người làm cha mẹ.",
        "Giá Tiki": 70000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_140305.jpg",
        "Tên sách": "Nền văn minh Lục Địa Đen",
        "Tác giả": "Graham Connah",
        "Quốc gia": "Anh",
        "Thể loại": "Lịch sử,Khảo cứu",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Từ Điển Bách Khoa",
        "Năm xuất bản": 2012,
        "Số trang": 520,
        "Điểm Goodreads": 4.1,
        "Review": "Khảo cứu sâu sắc về quá trình hình thành và phát triển của các nền văn minh cổ đại tại cõi châu Phi hùng vĩ. Một công trình dân tộc học - khảo cổ học quy mô, làm mờ đi định kiến về sự non trẻ của Lục địa Đen dưới góc nhìn lịch sử toàn cầu.",
        "Giá Tiki": 180000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_140313.jpg",
        "Tên sách": "Những nhân chứng cuối cùng: Solo cho giọng trẻ em",
        "Tác giả": "Svetlana Alexievich",
        "Quốc gia": "Belarus",
        "Thể loại": "Lịch sử,Phóng sự",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Phụ Nữ",
        "Năm xuất bản": 2020,
        "Số trang": 326,
        "Điểm Goodreads": 4.5,
        "Review": "Tác phẩm đoạt giải Nobel Văn chương năm 2015, là tập hợp những ký ức đầy đau thương của những đứa trẻ tận mắt chứng kiến sự tàn khốc của Chiến tranh thế giới thứ hai. Những lời kể ngây thơ nhưng đẫm nước mắt làm chấn động lương tri loài người.",
        "Giá Tiki": 120000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_140329.jpg",
        "Tên sách": "Anh em nhà Himmler",
        "Tác giả": "Katrin Himmler",
        "Quốc gia": "Đức",
        "Thể loại": "Lịch sử,Tiểu sử",
        "Lứa tuổi": "Người lớn",
        "NXB": "Nhà xuất bản Thế Giới",
        "Năm xuất bản": 2015,
        "Số trang": 382,
        "Điểm Goodreads": 3.8,
        "Review": "Dưới ngòi bút của chính cháu gái Heinrich Himmler, cuốn sách bóc trần sự thật về gia đình trùm SS. Đây là cuộc đối mặt đầy đau xót và dũng cảm với di sản đen tối mà dòng họ này để lại qua những tội ác vô tiền khoáng hậu chống lại nhân loại.",
        "Giá Tiki": 110000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_140338.jpg",
        "Tên sách": "Lược sử nước Mỹ",
        "Tác giả": "Cơ Quan Thông Tin Mỹ",
        "Quốc gia": "Hoa Kỳ",
        "Thể loại": "Lịch sử",
        "Lứa tuổi": "Thanh thiếu niên",
        "NXB": "Nhà xuất bản Tổng Hợp Thành Phố Hồ Chí Minh",
        "Năm xuất bản": 2010,
        "Số trang": 435,
        "Điểm Goodreads": 3.9,
        "Review": "Cung cấp cái nhìn toàn cảnh và tóm lược quá trình hình thành, xây dựng và phát triển tư bản của Hợp chúng quốc Hoa Kỳ từ buổi sơ khai đến kỷ nguyên hiện đại. Cuốn sách là nguồn tham khảo nền tảng cho ai muốn tìm hiểu nhanh về nước Mỹ.",
        "Giá Tiki": 160000,
        "Xoay ảnh": 0
    },
    {
        "image_path": "images_input/IMG_20260224_140552.jpg",
        "Tên sách": "Lược sử nước Mỹ (Bản trùng)",
        "Tác giả": "Cơ Quan Thông Tin Mỹ",
        "Quốc gia": "Hoa Kỳ",
        "Thể loại": "Lịch sử",
        "Lứa tuổi": "Thanh thiếu niên",
        "NXB": "Nhà xuất bản Tổng Hợp Thành Phố Hồ Chí Minh",
        "Năm xuất bản": 2010,
        "Số trang": 435,
        "Điểm Goodreads": 3.9,
        "Review": "Cung cấp cái nhìn toàn cảnh và tóm lược quá trình hình thành, xây dựng và phát triển tư bản của Hợp chúng quốc Hoa Kỳ từ buổi sơ khai đến kỷ nguyên hiện đại. Cuốn sách là nguồn tham khảo nền tảng cho ai muốn tìm hiểu nhanh về nước Mỹ. (Ghi chú: Ảnh trùng lặp)",
        "Giá Tiki": 160000,
        "Xoay ảnh": 0
    }
]

books.extend(new_books)
with open(data_file, "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, indent=4)
print(f"Updated book_data.json with {len(new_books)} more books successfully")
