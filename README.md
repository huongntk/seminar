Vietnamese Sentiment Assistant
Một hệ thống phân loại cảm xúc tiếng Việt thông minh sử dụng mô hình PhoBERT và giao diện web tương tác.
GIỚI THIỆU
Vietnamese Sentiment Assistant là công cụ phân tích cảm xúc tự động cho văn bản tiếng Việt. Hệ thống kết hợp sức mạnh của mô hình ngôn ngữ Transformer (PhoBERT) với các quy tắc xử lý ngôn ngữ đặc thù để đạt độ chính xác cao trong việc nhận diện cảm xúc (Tích cực/Tiêu cực/Trung lập).
TÍNH NĂNG NỔI BẬT
- Phân loại cảm xúc: Sử dụng PhoBERT được fine-tune cho tiếng Việt
- Tiền xử lý thông minh: Xử lý từ viết tắt, tiếng lóng, chuẩn hóa văn bản
- Giao diện trực quan: Web app với Streamlit, dễ sử dụng
- Lưu trữ lịch sử: SQLite database để theo dõi kết quả phân tích
- Tối ưu hiệu suất: Cache mô hình, xử lý nhanh chóng
- Quy tắc bổ sung: Kết hợp rule-based và ML để tăng độ chính xác
CÔNG NGHỆ SỬ DỤNG
- Frontend: Streamlit (≥1.28)
- ML Model: Transformers (PhoBERT) (4.30+)
- NLP: Underthesea (6.0+)
- Database: SQLite3 (3.35+)
- Core Python (3.8+)
CÀI ĐẶT VÀ CHẠY ỨNG DỤNG
- Clone repository
git clone https://github.com/huongntk/sentiment.git
cd sentiment
- Tạo môi trường ảo (khuyến nghị)
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
- Cài đặt dependencies: pip install -r requirements.txt
- Chạy ứng dụng
streamlit run app.py
Ứng dụng sẽ mở tại: http://localhost:8501

CẤU TRÚC THƯ MỤC
sentimenT/
│
├── app.py                 # Giao diện Streamlit chính
├── __init__.py           # Khởi tạo package
│
├── engine.py             # Logic xử lý chính và quy tắc
├── preprocess.py         # Tiền xử lý văn bản tiếng Việt
├── pipeline.py           # Tải và quản lý mô hình ML
│
├── database/
│   └── sqlite_helper.py  # Quản lý SQLite database
│
├── requirements.txt      # Danh sách dependencies
├── README.md            
└── .gitignore           # Git ignore file
MÔ TẢ CÁC THÀNH PHẦN
- app.py - Giao diện người dùng
Giao diện web với Streamlit
Vùng nhập văn bản và hiển thị kết quả
Quản lý lịch sử phân loại
Xử lý tương tác người dùng
- engine.py - Bộ xử lý chính
Hàm classify_sentiment(): Phân loại cảm xúc chính
Áp dụng quy tắc bổ sung (từ khóa trung tính, ngưỡng điểm)
Ánh xạ nhãn từ mô hình sang định dạng chuẩn
- preprocess.py - Tiền xử lý văn bản
Chuẩn hóa Unicode và encoding
Loại bỏ ký tự đặc biệt, emoji
Chuẩn hóa từ viết tắt tiếng Việt
Tách từ với Underthesea
Giới hạn độ dài văn bản
- pipeline.py - Quản lý mô hình ML
Tải mô hình PhoBERT đã fine-tune
Cache mô hình với @functools.lru_cache
Tạo sentiment analysis pipeline
- database/sqlite_helper.py - Quản lý dữ liệu
Khởi tạo database SQLite
CRUD operations cho lịch sử phân loại
Truy vấn lịch sử gần nhất
HƯỚNG DẪN SỬ DỤNG
- Mở ứng dụng tại http://localhost:8501
- Nhập câu tiếng Việt cần phân tích vào ô văn bản
- Nhấn nút "Phân loại cảm xúc"
- Xem kết quả với:
    + TÍCH CỰC (màu xanh) - Cảm xúc tích cực
    + TRUNG LẬP (màu xanh dương) - Cảm xúc trung tính
    + TIÊU CỰC (màu đỏ) - Cảm xúc tiêu cực
- Xem độ tin cậy (% score) và câu gốc
- Xem lịch sử: 50 bản ghi gần nhất hiển thị dạng bảng
- Xóa lịch sử: Nhấn nút " Xóa lịch sử" và xác nhận
GHI NHẬN
- VinAI Research cho mô hình PhoBERT
- Hugging Face cho transformers library
- Streamlit cho framework web app
- Underthesea cho NLP tiếng Việt
