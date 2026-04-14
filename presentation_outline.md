# BẢN PHÁC THẢO CHI TIẾT (OUTLINE) CHO BÀI KẾT THÚC MÔN

Dưới đây là kịch bản dàn ý được chia thành **12 Slides chi tiết (Mỗi người 3 Slides)**. Bố cục này dẫn dắt thầy cô theo **Vòng đời thực tế của kiến trúc hệ thống (System Lifecycle)**: Từ khâu lấy Dữ liệu Ngoại vi -> Xây dựng Cổng cung cấp -> Tối ưu Hệ thống phòng vệ -> Triển khai Đám mây.

---

## 👩‍💻 NGƯỜI SỐ 1: Xuân Hương (Tích hợp API Nguồn Ngoài - Consuming 3rd-Party APIs)
**Vai trò:** Kết nối sức mạnh cục bộ tới luồng tài chính của thế giới (Bài thi số 3). Đi từ gốc rễ: "Lấy nguyên liệu ở đâu?".
- **Slide 1: Mở rộng Không gian Tính Toán từ 3rd-Party:**
  - Bài toán: Để API không bị cô lập, Server tự chủ động đi thu thập 2 nguồn bên ngoài: (1) Sàn Binance, (2) Tổ chức Open Exchange Rates API.
- **Slide 2: Xử lý Bất đồng bộ (Async/Await) & JSON Parsing:**
  - Luồng xử lý đa luồng ngầm định `Task<IResult>` và Load DOM tree lấy Data siêu tốc độ để mix (trộn) với Data AI tính %VND.
- **Slide 3: Chiến lược Tích hợp Song Song (IHttpClientFactory):**
  - Chống tình trạng nghẽn cổ chai Socket do sử dụng lệnh tồi `new HttpClient()`, đảm bảo tính ổn định khi gọi API ngoài.

---

## 👨‍💻 NGƯỜI SỐ 2: Thành Trung (Khởi tạo Dịch Vụ API - API Provisioning)
**Vai trò:** Biến mớ "Nguyên liệu" ở Bước 1 thành một Dịch vụ mạng chuyên nghiệp.
- **Slide 4: Giới thiệu X-AURUM & ASP.NET Minimal API:** 
  - Khái quát cách bọc thuật toán bên trong 1 Web Service. Kiến trúc Minimal API tinh gọn (.NET 10) loại bỏ Controllers thừa thãi.
- **Slide 5: Thiết kế 2 luồng Endpoints cốt lõi:**
  - `POST /api/v1/predictions` cho các Client tự truyền dữ liệu và `GET /api/v1/predictions/realtime` tự kéo Data 3rd-party. Đi kèm chuẩn hóa đầu ra RESTful JSON.
- **Slide 6: Tự động hóa Tài liệu qua Swagger (OpenAPI):**
  - Trình bày tại sao chuẩn OpenAPI lại là xương sống của mọi API. Swagger UI tự động sinh Documentation mô tả giúp dễ tích hợp.

---

## 👨‍💻 NGƯỜI SỐ 3: Văn Nguyễn (Tối ưu Bộ nhớ & Lưới Lửa Bảo mật)
**Vai trò:** Kỹ sư hệ thống (System Engineer) - Bây giờ API đã có, làm sao bảo vệ và cho hàng ngàn người truy cập cùng lúc?
- **Slide 7: Bài toán Nút thắt RAM & Memory Leak:**
  - Sự nguy hiểm khi Host Machine Learning model làm Web API. Nhấn mạnh nguy cơ Crash Server nếu nạp file tĩnh 40MB mỗi giây.
- **Slide 8: Tuyệt kỹ PredictionEnginePool (Quản trị Thread-Safe):**
  - Giải pháp nạp bộ nhớ đúng 1 lần (Object Pooling). Khả năng tiếp nhận song song (Concurrent) hàng ngàn Request cùng lúc.
- **Slide 9: Tường lửa Tích hợp - Middleware Rate Limiting:**
  - Áp dụng cấu trúc Token Bucket (5 tín hiệu / 10 Giây). Bất kì phần mềm cố tình Flood Spam API sẽ bị chặn tại Kernel bằng HTTP 429.

---

## 👨‍💻 NGƯỜI SỐ 4: Quốc Đạt (DevOps & Test Triển Khai)
**Vai trò:** DevOps Kỹ nghệ vận hành, gói bộ giáp hoàn chỉnh thả lên Cloud và Thuyết minh bằng Live Demo.
- **Slide 10: Ảo Hoá Đám Mây (Docker Containerization):**
  - Cấu trúc Multi-stage Dockerfile: Gọt lõi .dll xuất ra Container siêu nhẹ vài chục MB sử dụng Alpine Linux.
- **Slide 11: Tự động hoá CI/CD & Mạng lưới Tên Miền Thực Tế:**
  - Github Actions -> Đẩy Image lên GHCR mượt mà. Kết nối Nginx Reverse Proxy Public Domain chính thức: **`nttspace.online`**.
- **Slide 12: Chạy Demo Phân Tích Thực tế (Sử Dụng Swagger API):**
  1. Demo `GET /realtime` trong Swagger -> Ra Response >120 Triệu VND tốc độ cao.
  2. Spammer Attack Demo: Bắn liên hoàn `POST` 7 lần trong Swagger để chứng minh rào chắn 429 xuất hiện.

---
