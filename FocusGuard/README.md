# 🛡️ FocusGuard - Hệ Thống An Toàn Cho Lái Xe

## 📖 Giới Thiệu

**FocusGuard** là ứng dụng hỗ trợ an toàn cho lái xe, đặc biệt trong việc phát hiện buồn ngủ và mệt mỏi khi điều khiển phương tiện. Ứng dụng sử dụng trí tuệ nhân tạo để nhận diện trạng thái của người lái và đưa ra các gợi ý phù hợp.

## ✨ Tính Năng Chính

### 🎥 1. Giám Sát Thời Gian Thực
- Phát hiện buồn ngủ qua camera
- Nhận diện ngáp, chớp mắt liên tục
- Cảnh báo kịp thời khi phát hiện mệt mỏi

### 🗺️ 2. Bản Đồ Trạm Dừng Chân
- **MỚI**: Tìm kiếm trạm xăng, quán cà phê, nhà hàng gần vị trí
- Tích hợp OpenStreetMap API
- Hiển thị khoảng cách và chỉ đường
- Lọc theo loại cơ sở và bán kính

#### Cách sử dụng:
1. Nhấn nút **"🗺️ Trạm Dừng Chân"**
2. Nhập địa chỉ hiện tại của bạn
3. Chọn bán kính tìm kiếm (1-20 km)
4. Chọn loại cơ sở (Trạm xăng, Quán cà phê, Nhà hàng, Khách sạn)
5. Nhấn **"TÌM KIẾM"**
6. Chọn địa điểm và nhấn **"CHỈ ĐƯỜNG"** để mở Google Maps

### 🏋️ 3. Bài Tập Thể Dục
- Gợi ý các bài tập giãn cơ
- Phù hợp để thực hiện khi dừng xe nghỉ
- Giúp giảm mệt mỏi và tỉnh táo

### 🥗 4. Gợi Ý Dinh Dưỡng
- Tính toán nhu cầu calo cá nhân
- Đề xuất thực đơn phù hợp
- Phân tích chỉ số BMI, BMR, TEE

### 📊 5. Lịch Sử & Thống Kê
- Theo dõi lịch sử mệt mỏi
- Biểu đồ phân tích trực quan
- Báo cáo chi tiết

## 🚀 Cài Đặt

### Yêu cầu hệ thống:
- Python 3.8 trở lên
- Camera (cho chức năng phát hiện)
- Kết nối Internet (cho bản đồ)

### Bước 1: Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### Bước 2: Chạy ứng dụng
```bash
python Runner.py
```

## 📦 Cấu Trúc Thư Mục

```
FocusGuard/
│
├── Runner.py                 # File chính của ứng dụng
├── PhatHienMetMoi.py        # Module phát hiện mệt mỏi
├── rest_stops_api.py        # Module API tìm trạm dừng chân
├── requirements.txt         # Danh sách thư viện cần thiết
│
├── database/
│   ├── data.csv            # Dữ liệu thực phẩm
│   ├── fatigue_log.csv     # Lịch sử mệt mỏi
│   └── best.pt             # Model AI
│
├── excercise/              # Hình ảnh bài tập
├── images/                 # Hình ảnh giao diện
│
└── README.md              # File này
```

## 🎯 Hướng Dẫn Sử Dụng Chi Tiết

### Khi Lái Xe:

1. **Trước khi khởi hành:**
   - Mở ứng dụng FocusGuard
   - Nhấn **"BẬT MÁY ẢNH NHẬN DIỆN"**
   - Đặt thiết bị ở vị trí có thể nhìn thấy mặt bạn

2. **Trong khi lái:**
   - Ứng dụng sẽ tự động theo dõi
   - Nếu phát hiện buồn ngủ, sẽ có cảnh báo
   - Lưu lại lịch sử tự động

3. **Khi cảm thấy mệt:**
   - Dừng xe an toàn
   - Mở chức năng **"Trạm Dừng Chân"**
   - Tìm điểm nghỉ gần nhất
   - Thực hiện bài tập giãn cơ

### Mẹo An Toàn:

⚠️ **QUAN TRỌNG:**
- Không tương tác với ứng dụng khi đang lái xe
- Chỉ xem bản đồ khi đã dừng xe an toàn
- Nghỉ ngơi ít nhất 15 phút sau mỗi 2 giờ lái xe
- Uống cà phê hoặc nước tỉnh táo
- Nếu quá mệt, hãy ngủ 20-30 phút

## 🔧 Cấu Hình Nâng Cao

### Tích hợp API thực tế:

Ứng dụng sử dụng **OpenStreetMap** miễn phí. Nếu muốn tốc độ tốt hơn, bạn có thể:

1. Sử dụng Google Maps API (có phí)
2. Cài đặt server Overpass riêng
3. Sử dụng HERE Maps API

### Điều chỉnh độ nhạy phát hiện:

Chỉnh sửa trong file `PhatHienMetMoi.py`:
```python
# Thay đổi ngưỡng phát hiện
YAWN_THRESHOLD = 20  # Số khung hình ngáp
EYE_THRESHOLD = 30   # Số khung hình nhắm mắt
```

## 🐛 Xử Lý Lỗi Thường Gặp

### Lỗi: "Module rest_stops_api không khả dụng"
**Giải pháp:** Ứng dụng vẫn chạy được với dữ liệu mẫu. Để sử dụng API thực:
```bash
pip install requests
```

### Lỗi: Camera không hoạt động
**Giải pháp:**
- Kiểm tra quyền truy cập camera
- Đảm bảo không có ứng dụng khác đang sử dụng
- Thử khởi động lại máy tính

### Lỗi: Không tìm thấy địa điểm
**Giải pháp:**
- Kiểm tra kết nối Internet
- Thử nhập địa chỉ cụ thể hơn
- Tăng bán kính tìm kiếm

## 📱 Tính Năng Tương Lai

- [ ] Chế độ "Driving Mode" toàn màn hình
- [ ] Cảnh báo âm thanh mạnh mẽ
- [ ] Tích hợp GPS thời gian thực
- [ ] Phát hiện độ nghiêng đầu
- [ ] Đồng bộ với smartwatch
- [ ] Báo cáo hành trình chi tiết
- [ ] Chia sẻ vị trí khẩn cấp

## 🤝 Đóng Góp

Mọi đóng góp đều được hoan nghênh! Hãy:
1. Fork dự án
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push lên branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📄 Giấy Phép

Dự án này được phát triển cho mục đích an toàn giao thông.

## 👥 Tác Giả

**FocusGuard Team** - Phát triển vì an toàn giao thông

## 🙏 Lời Cảm Ơn

- OpenStreetMap cho dữ liệu bản đồ miễn phí
- ttkbootstrap cho giao diện đẹp
- Cộng đồng Python Việt Nam

---

**⚠️ LƯU Ý AN TOÀN:**
Ứng dụng này chỉ là công cụ hỗ trợ. Người lái xe vẫn có trách nhiệm đảm bảo an toàn khi tham gia giao thông. Không lái xe khi quá mệt mỏi!

🚗 **Lái Xe An Toàn - Về Nhà Bình An** 🏠
