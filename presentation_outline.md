# BẢN PHÁC THẢO CHI TIẾT (OUTLINE) CHO BÀI KẾT THÚC MÔN

Dưới đây là kịch bản dàn ý được chia thành **12 Slides chi tiết (Mỗi người 3 Slides)**. Bố cục này dẫn dắt thầy cô từ: Tổng quan mục tiêu -> Cấu trúc thiết kế bên trong -> Quá trình liên kết với thế giới bên ngoài -> Đưa hệ thống lên môi trường thật.

---

## 👨‍💻 NGƯỜI SỐ 1: Thành Trung (Khởi tạo Dịch Vụ API - API Provisioning)
**Vai trò:** Giới thiệu cái nhìn tổng thể về ứng dụng và bộ khung định tuyến của Web Service.
- **Slide 1: Giới thiệu X-AURUM & Mục tiêu Bài Thi:** 
  - Bài toán: Không để AI nằm chết trong giao diện Console tĩnh, biến nó thành một Dịch Vụ Mạng (Web Service API) để bất kỳ ứng dụng mở rộng nào khác đều có thể kết nối vào hệ sinh thái.
- **Slide 2: Tự động hóa Tài liệu qua Swagger (OpenAPI):**
  - Một API chuyên nghiệp không thể thiếu bảng mô tả cho các tổ chức thứ 3 đọc và tích hợp. Thay vì viết tay, dùng chuẩn OpenAPI để tự động sinh "chỉ dẫn" (documentation).
  - Tích hợp giao diện Swagger UI chuyên biệt giúp kiểm thử ngay trên môi trường Web mà không cần phải cài công cụ trung gian (như Postman).
- **Slide 3: Thiết kế 2 luồng Endpoints cốt lõi (Giao tiếp API):**
  - Giao thức 1: Nhánh `POST /api/v1/predictions` cho các Client muốn truyền dữ liệu riêng.
  - Giao thức 2: Nhánh `GET /api/v1/predictions/realtime` hoàn toàn không phụ thuộc Client (Tự sống, tự kéo Data).
  - Chuẩn hóa đầu ra RESTful (Luôn bọc Response cấu trúc `success: true/false`, dễ dàng Parse JSON).

---

## 👨‍💻 NGƯỜI SỐ 2: Văn Nguyễn (Tối ưu Bộ nhớ & Lưới Lửa Bảo mật)
**Vai trò:** Kỹ sư hệ thống (System Engineer) giải quyết các bài toán về nghẽn RAM và bảo vệ máy chủ bị tấn công.
- **Slide 4: Bài toán Nút thắt Cổ Chai của Machine Learning làm REST API:**
  - Nhấn mạnh nguy cơ Crash Server / Memory Leak nặng nếu Cứ mỗi cú click lại Load 1 file tĩnh 40MB Model vật lý.
- **Slide 5: Tuyệt kỹ PredictionEnginePool (Quản trị Thread-Safe):**
  - Giải pháp nạp bộ nhớ 1 lần (Object Pooling). 
  - Khả năng tiếp nhận song song (Concurrent) cả ngàn Request gọi vào lõi Model giải phẫu ra kết quả đồng thời.
- **Slide 6: Tường lửa Tích hợp - Middleware Rate Limiting:**
  - Áp dụng cấu trúc Token Bucket giới hạn Fixed Window (Cấp phát đúng 5 tín hiệu / 10 Giây). Bất kì phần mềm cố tình Flood Request sẽ bị khước từ bằng rào chặn ở cấp hạt nhân: lỗi `HTTP 429 Too Many Requests`.

---

## 👩‍💻 NGƯỜI SỐ 3: Xuân Hương (Tích hợp API Nguồn Ngoài - 3rd-Party APIs)
**Vai trò:** Kết nối sức mạnh hệ thống cục bộ tới luồng tài chính của thế giới (Bài thi số 3).
- **Slide 7: Mở rộng Không gian Tính Toán từ 3rd-Party:**
  - Đóng vai Client bòn rút dữ liệu. Server tự chủ động đi thu thập 2 nguồn: (1) Sàn Tiền Ảo Toàn cầu Binance, (2) Tổ chức Open Exchange Rates API.
- **Slide 8: Chiến lược Tích hợp Song Song (IHttpClientFactory):**
  - Chống tình trạng tắc nghẽn Port do sử dụng lệnh tồi `new HttpClient()` bằng cách sử dụng Cơ chế Factory Lifecycle quản lý vòng đời bộ gọi.
- **Slide 9: Xử lý Bất đồng bộ (Async/Await) & JSON Parsing:**
  - Luồng xử lý đa luồng ngầm định `Task<IResult>`. 
  - Load DOM tree cấp siêu tốc độ và truy vấn Data Live ngay trong bộ nhớ để mix (trộn) với Data của AI -> Tính toán ra lượng %VND.

---

## 👨‍💻 NGƯỜI SỐ 4: Quốc Đạt (DevOps & Test Triển Khai)
**Vai trò:** DevOps Kỹ nghệ vận hành, gói gọn tất cả vào Hạ tầng mây (Cloud) và Thuyết minh bằng Live Demo.
- **Slide 10: Ảo Hoá Đám Mây (Docker Containerization):**
  - Cấu trúc Multi-stage Dockerfile: Gọt lõi .dll khỏi nền Build nặng nề của SDK, xuất ra Container gọn nhẹ vài MB sử dụng Alpine Linux.
- **Slide 11: Tự động hoá CI/CD & Mạng lưới Tên Miền Thực Tế:**
  - Github Actions: Tự động chạy chuỗi dây chuyền nén Docker khi dev Push Code -> Đẩy lên GHCR.
  - Phân giải Reverse Proxy bằng Nginx. Mang dự án rẽ hướng truy cập Public sống thật tại siêu Name: **`nttspace.online`**.
- **Slide 12: Chạy Demo Phân Tích Thực tế (Sử Dụng Swagger API):**
  1. Trình diễn bắn thủ công `GET /realtime` trong Swagger -> Nhận Response hơn 120 Triệu VND (Chung quy sự tham gia của Bot + 3rd API Binance + 3rd API Exchange).
  2. Spammer Attack: Bắn liên hoàn `POST` 7 lần trong Swagger để Console ói ra lỗi phòng thủ 429 Đỏ chót.

---
