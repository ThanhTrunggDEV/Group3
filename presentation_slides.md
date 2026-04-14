---
marp: true
theme: default
class: lead
backgroundColor: #121212
color: #e0e0e0
---

# KỸ NGHỆ HỆ THỐNG X-AURUM
**Báo cáo Tiến độ Cung cấp Dịch vụ & Máy chủ (API & DevOps)**
**Nhóm 3:** Thành Trung - Văn Nguyễn - Xuân Hương - Quốc Đạt

---

<!-- Speaker: Thành Trung -->
## 1. KIẾN TRÚC API CUNG CẤP & ĐỊNH TUYẾN ⚙️

**1. ASP.NET Minimal API:**
- Hệ thống áp dụng cấu trúc Microservices tinh gọn trên nền Tảng .NET 10. Từ bỏ thiết kế Controller truyền thống, thiết lập Route Mapping trực tiếp.
- Phân luồng Cung cấp API (Providing APIs) 2 nhánh riêng biệt:
  - `POST /api/v1/predictions`: Interface cho phép Consumer truyền Payload JSON tuỳ chỉnh.
  - `GET /api/v1/predictions/realtime`: Interface chạy hoàn toàn ẩn danh, hệ thống tự động cung ứng data mà không cần Payload.

**2. Tiêu chuẩn Hóa Giao Tiếp:**
- Mọi Response từ API đều được bọc trong bộ `Data Wrapper` chuẩn RESTful (chứa cờ `success` và `data` objects) giúp các ứng dụng tiêu thụ (Consumer) parse JSON an toàn tuyệt đối.

---

<!-- Speaker: Văn Nguyễn -->
## 2. QUẢN TRỊ BỘ NHỚ LÕI & BẢO MẬT API 🛡️

**1. Tối ưu Hiệu năng RAM (PredictionEnginePool):**
- Điểm yếu lớn nhất khi Hosting API dạng Machine Learning là bị nghẽn ngã ba khi cấp phát Object (Memory Leak). Giới thiệu giải pháp **Object Pooling Thread-Safe**.
- API sử dụng `PredictionEnginePool` tạo sẵn không gian xử lý nội hàm trong RAM. Bất cứ Request HTTP nào bay vào đều tái sử dụng instance, xử lý luồng cực nhanh mà Server không bị Crash.

**2. Middleware Chống Chịu DDoS (Rate Limiting):**
- Can thiệp tầng Request Pipeline, cấu trúc thuật toán **Fixed Window (Token Bucket)**.
- Phân làn khắc nghiệt: Giới hạn IP chỉ 5 Request / 10 Giây. Chống Spam API và chặn họng (Reject) ngay lập tức bằng mã trạng thái `HTTP 429 Too Many Requests`.

---

<!-- Speaker: Xuân Hương -->
## 3. TÍCH HỢP HỆ THỐNG (CONSUMING 3RD-PARTY APIs) 🌐

**1. Sự kết hợp Thông Lượng Data đa nguồn:**
- Để đáp ứng nghiệp vụ Vàng thực tế, API Backend tiến hành bứt phá đóng thêm vai "Client" để bòn rút data của các hệ thống khác (Bài kiểm tra số 3). Điển hình:
  - Ngầm kết nối Sàn **Binance API** kéo giá nến PaxG (Gold Spot).
  - Ngầm kết nối **Open Exchange Rates API** bóc giá trị Đô-la sang Việt Nam Đồng.

**2. Cơ chế IHttpClientFactory + Async Socket:**
- Để phân giải song song nhiều API ngoại, mã nguồn xử lý bất đồng bộ kết hợp `IHttpClientFactory` chặn Exhaustion Socket và Dùng thuật toán `System.Text.Json` parse DOM tree lấy giá trị trực tiếp không cần map objects dườm rà.

---

<!-- Speaker: Quốc Đạt -->
## 4. DEVOPS CONTAINERIZATION & LIVE CASE STUDY 🐳

**1. Tự động hóa Triển Khai (CI/CD DevOps):**
- **Docker Multi-stage:** Chuyển hóa API thành Image. Giai đoạn Compile bằng SDK siêu nặng, sau đó trích xuất lõi ném sang Runtime Alpine (Chỉ vài MB).
- **GitHub Actions:** Auto-trigger kiểm thử và Release thẳng image lên trạm GHCR. Giúp bất kỳ Cloud Server nào cài Docker thao tác Start hệ thống chỉ bằng 1 dòng Lệnh gốc.

**2. System Demo - X-AURUM SWAGGER UI:**
- Mở Server truy cập trực tiếp vào giao diện OpenAPI (`/swagger`).
- Thực thi nhanh nhánh `GET /realtime` để chiêm ngưỡng luồng JSON từ API thứ 3 rót thẳng về hệ thống ra kết quả >124 Triệu VND trực quan! Test thử rào chắn Rate Limiting bằng cách Execute liên tiếp nhánh lệnh `POST` để trình diễn Lỗi 429 sống động ngay trên Console.

---
**XIN CẢM ƠN HỘI ĐỒNG XÉT DUYỆT!**
